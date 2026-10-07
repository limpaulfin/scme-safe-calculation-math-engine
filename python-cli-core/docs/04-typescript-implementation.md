# **Gợi ý thư viện cho TS/JS**

Lõi số học & parser

- mathjs — parser biểu thức, số lớn (BigNumber), ma trận, units tích hợp ổn.
- decimal.js — số thập phân chính xác cao (tốt hơn Number).
- fraction.js — phân số chính xác tuyệt đối cho phép tính hữu tỉ.
- interval-arithmetic — số học khoảng (bắt sai số/ổn định số).
- (tùy chọn) big-integer — số nguyên rất lớn.

Đại số ký hiệu (CAS, mức cơ bản)

- nerdamer — rút gọn, đạo hàm, giải một số phương trình ký hiệu; giới hạn nhưng nhẹ, chạy thuần JS.
    - Ngoài ra có algebra.js (rất cơ bản). Nếu cần CAS mạnh → cân nhắc dịch vụ phụ Python (SymPy) qua RPC (hybrid).
- 

Tuyến tính & tối ưu

- Tuyến tính: mathjs (ma trận), hoặc ml-matrix.
- LP/MILP: glpk.js (GLPK biên dịch Emscripten, khá vững), hoặc javascript-lp-solver (nhẹ, LP/MILP nhỏ).

Xác suất – thống kê

- simple-statistics — mô tả/ước lượng cơ bản.
- Phân phối: tự cài đặt hàm pdf/cdf/ppf phổ biến hoặc dùng jstat.

FFT / tín hiệu

- fft.js hoặc scijs/ndarray-fft.

Đơn vị

- Dùng luôn units của mathjs (quy đổi m ↔ ft, s, kg, N, J…), hoặc convert-units nếu muốn cực nhẹ.

# **Thiết kế endpoint (gợi ý)**

- calculate.eval — đánh giá biểu thức an toàn (mathjs + decimal/fraction + interval tùy chọn)
- calculate.units.convert — đổi đơn vị, kiểm tra thứ nguyên
- algebra.simplify, algebra.solve — dùng nerdamer
- matrix.solve, matrix.decompose — mathjs/ml-matrix
- numeric.root, numeric.integrate — tự triển khai Newton/bisection/Simpson hoặc dùng mathjs/lib nhỏ
- stats.describe, prob.dist — simple-statistics/jstat
- optimize.lp — glpk.js

Chính sách an toàn/độ tin cậy

- Chạy double-run: decimal.js và fraction.js so chéo (nếu áp dụng).
- Symbolic-first: cố gắng simplify trước khi evaluate.
- Interval guard: tính thêm khoảng sai số; nếu kết quả ra ngoài khoảng → gắn cờ.
- Giới hạn thời gian/tài nguyên mỗi call; log trace + versions + hash.

# **Skeleton MCP server (TypeScript, ESM)**

MCP SDK (chuẩn mới): @modelcontextprotocol/sdk

package.json

{

"name": "mcp-calculate",

"type": "module",

"private": true,

"scripts": {

"dev": "tsx src/server.ts",

"start": "node dist/server.js",

"build": "tsc -p tsconfig.json"

},

"dependencies": {

"@modelcontextprotocol/sdk": "^0.5.0",

"decimal.js": "^10.4.3",

"fraction.js": "^4.3.7",

"interval-arithmetic": "^1.2.0",

"mathjs": "^13.0.0",

"nerdamer": "^1.1.13",

"simple-statistics": "^7.10.3",

"glpk.js": "^4.65.0"

},

"devDependencies": {

"tsx": "^4.17.0",

"typescript": "^5.6.3"

}

}

tsconfig.json

{

"compilerOptions": {

"target": "ES2022",

"module": "ES2022",

"moduleResolution": "bundler",

"outDir": "dist",

"strict": true,

"skipLibCheck": true

},

"include": ["src"]

}

src/server.ts

import { Server, Tool } from "@modelcontextprotocol/sdk";

import { create, all, MathNumericType, MathJsStatic } from "mathjs";

import Decimal from "decimal.js";

import Fraction from "fraction.js";

import * as IA from "interval-arithmetic";

import nerdamer from "nerdamer";

import "nerdamer/Solve";

import "nerdamer/Calculus";

import "nerdamer/Algebra";

import ss from "simple-statistics";

// @ts-ignore

import GLPK from "glpk.js";

const math = create(all, {

number: "BigNumber",

precision: 64,

predictable: true

}) as MathJsStatic;

type EvalSettings = {

mode?: "decimal" | "fraction" | "auto";

precision?: number;          // cho decimal

returnInterval?: boolean;    // trả thêm khoảng sai số

timeoutMs?: number;

};

function safeEvalExpression(expr: string, settings: EvalSettings) {

// 1) thử symbolic simplify nhẹ để giảm sai số

let simplified = expr;

try { simplified = nerdamer(expr).toString(); } catch { /* giữ nguyên */ }

// 2) chọn engine

const mode = settings.mode ?? "auto";

const start = Date.now();

const checkTimeout = () => {

if (settings.timeoutMs && Date.now() - start > settings.timeoutMs)

throw new Error("timeout");

};

// 3) Fraction (ưu tiên phép tính hữu tỉ)

const tryFraction = () => {

// parse tokens bằng mathjs rồi thay số -> Fraction khi có thể

const n = math.evaluate(simplified); // BigNumber/Unit/…

// Nếu là số hữu tỉ đơn, convert:

if (typeof n === "number") return new Fraction(n).toFraction(true);

if (Decimal.isDecimal(n as any)) {

const dec = n as unknown as Decimal;

return new Fraction(dec.toString()).toFraction(true);

}

return math.evaluate(simplified).toString(); // fallback

};

// 4) Decimal

const tryDecimal = () => {

if (settings.precision) Decimal.set({ precision: settings.precision });

// mathjs BigNumber → string → Decimal để đảm bảo kiểm soát

const val = math.evaluate(simplified) as MathNumericType;

const s = math.format(val, { notation: "auto", precision: settings.precision ?? 34 });

return new Decimal(s).toString();

};

// 5) Interval (đơn giản: dùng eval interval-arithmetic cho số học cơ bản)

const tryInterval = () => {

try {

// interval-arithmetic không hiểu mọi hàm, nên chỉ bật khi expr cơ bản

const out = IA.eval(simplified);

if (IA.isInterval(out)) {

return { lo: out.lo, hi: out.hi };

}

} catch { /* ignore */ }

return null;

};

checkTimeout();

let result: any;

if (mode === "fraction") result = tryFraction();

else if (mode === "decimal") result = tryDecimal();

else {

// auto: thử fraction trước, nếu hỏng thì decimal

try { result = tryFraction(); }

catch { result = tryDecimal(); }

}

let interval = null as null | { lo: number; hi: number };

if (settings.returnInterval) {

checkTimeout();

interval = tryInterval();

}

return { expr, simplified, mode: mode, result, interval };

}

/** ---------- Tools ---------- **/

const evalTool: Tool = {

name: "calculate.eval",

description: "Đánh giá biểu thức toán học an toàn (decimal/fraction/interval).",

inputSchema: {

type: "object",

properties: {

expression: { type: "string" },

settings: {

type: "object",

properties: {

mode: { enum: ["decimal", "fraction", "auto"] },

precision: { type: "number" },

returnInterval: { type: "boolean" },

timeoutMs: { type: "number" }

}

}

},

required: ["expression"]

},

handler: async (input) => {

const { expression, settings = {} } = input as { expression: string; settings?: any };

const out = safeEvalExpression(expression, settings);

return { ok: true, ...out };

}

};

const unitsConvertTool: Tool = {

name: "calculate.units.convert",

description: "Chuyển đổi đơn vị, kiểm tra thứ nguyên bằng mathjs.",

inputSchema: {

type: "object",

properties: {

value: { type: "string", description: "VD: '9.81 m/s^2'" },

to: { type: "string", description: "VD: 'ft/s^2'" }

},

required: ["value", "to"]

},

handler: async (input) => {

const { value, to } = input as { value: string; to: string };

const v = math.evaluate(value); // Unit hoặc BigNumber

if (!math.isUnit(v)) throw new Error("Giá trị không phải Unit hợp lệ.");

const converted = v.to(to);

return { ok: true, result: converted.toString() };

}

};

const simplifyTool: Tool = {

name: "algebra.simplify",

description: "Rút gọn biểu thức bằng nerdamer.",

inputSchema: {

type: "object",

properties: { expression: { type: "string" } },

required: ["expression"]

},

handler: async (input) => {

const { expression } = input as { expression: string };

const simp = nerdamer(expression).simplify().toString();

return { ok: true, result: simp };

}

};

const solveTool: Tool = {

name: "algebra.solve",

description: "Giải phương trình (một số lớp) bằng nerdamer. Ví dụ: 'x^2-5x+6=0'.",

inputSchema: {

type: "object",

properties: {

equation: { type: "string" },

variable: { type: "string", default: "x" }

},

required: ["equation"]

},

handler: async (input) => {

const { equation, variable = "x" } = input as { equation: string; variable?: string };

const sol = nerdamer.solveEquations([equation], [variable] as any);

// nerdamer trả dạng mảng cặp [var, value]

return { ok: true, result: sol };

}

};

const statsDescribeTool: Tool = {

name: "stats.describe",

description: "Thống kê mô tả: count, mean, variance, std, min, max, quantiles.",

inputSchema: {

type: "object",

properties: {

data: {

type: "array",

items: { type: "number" }

}

},

required: ["data"]

},

handler: async (input) => {

const { data } = input as { data: number[] };

if (!Array.isArray(data) || data.length === 0) throw new Error("data rỗng");

data.sort((a, b) => a - b);

const mean = ss.mean(data);

const variance = ss.variance(data);

const std = Math.sqrt(variance);

const q25 = ss.quantileSorted(data, 0.25);

const q50 = ss.quantileSorted(data, 0.5);

const q75 = ss.quantileSorted(data, 0.75);

return {

ok: true,

result: {

count: data.length,

mean, variance, std,

min: data[0],

max: data[data.length - 1],

q25, median: q50, q75

}

};

}

};

async function main() {

const server = new Server({

name: "mcp-calculate",

version: "0.1.0"

});

server.tool(evalTool);

server.tool(unitsConvertTool);

server.tool(simplifyTool);

server.tool(solveTool);

server.tool(statsDescribeTool);

// TODO: add matrix.solve, numeric.root, optimize.lp (GLPK), etc.

await server.start();

// Tùy MCP host, có thể cần in ra info hoặc bind stdio/socket tùy môi trường.

console.log("MCP calculate server ready.");

}

main().catch((e) => {

console.error(e);

process.exit(1);

});

# **Cách mở rộng nhanh**

- matrix.solve: nhận A (2D) và b (1D), dùng math.lusolve/math.inv.
- numeric.root: triển khai bisection (ổn định) + Newton (nhanh) với guard miền.
- optimize.lp: gọi glpk.js (nhập A, b, c, sense) → trả nghiệm + chứng chỉ.
- prob.dist: gói jstat làm pdf/cdf/ppf cho Normal/Binomial/Poisson…

# **Lời khuyên kiến trúc**

- Profiles: strict (fraction + interval + timeout ngắn) / fast (decimal 34-64) / symbolic_first.
- Trace & reproducibility: luôn trả trace, lib_versions, elapsed_ms, hash_in/out.
- Hybrid tuỳ chọn: nếu cần CAS mạnh (factor đa thức bậc cao, tích phân khó), thêm adapter RPC sang một microservice SymPy, nhưng vẫn giữ API MCP thống nhất.

Nếu bạn muốn, mình có thể thêm ngay các tool còn thiếu (matrix.solve, numeric.root, optimize.lp) vào skeleton trên để bạn chạy thử.

---

Python 

Mcp 

Quá hay. Nếu bạn muốn làm một MCP server “calculate” để LLM gọi mỗi khi cần tính đúng–chắc–nhanh, mình đề xuất cấu trúc theo tầng + bộ công cụ như sau:

