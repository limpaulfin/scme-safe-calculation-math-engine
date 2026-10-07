# **1) Nhóm CORE (bắt buộc, nhỏ gọn, cực tin cậy)**

- Arithmetic chính xác: số nguyên lớn (BigInt), Decimal bội chính xác (không trôi số), Fraction/Rational cho phép tính đúng tuyệt đối.
- Parser biểu thức an toàn: hỗ trợ () ^ * / + -, hàm chuẩn (sqrt, log, sin…), biến, hằng; không eval code.
- Đơn vị & kiểm tra thứ nguyên (Units/Dimensional analysis): gắn đơn vị, tự động quy đổi (m, s, kg, J, N, °C↔K…), chặn phép cộng sai đơn vị.
- Interval arithmetic: cho mỗi kết quả số thực, xuất thêm khoảng sai số để chống tích lũy lỗi.
- Bộ quy tắc ràng buộc/kiểm lỗi: kiểm tra số chia cho 0, miền xác định (log âm, sqrt âm…), cảnh báo tràn số, giới hạn thời gian.

Gợi ý tool endpoints (MCP):

- calculate.eval → tính biểu thức (Decimal/Fraction)
- calculate.units.convert → đổi đơn vị + kiểm tra thứ nguyên
- calculate.interval.eval → đánh giá kèm khoảng sai số

# **2) Nhóm ALGEBRA & CALCULUS (chuẩn cho bài toán “có bước làm”)**

- Đại số ký hiệu (CAS): rút gọn, khai triển, phân tích thừa số, giải phương trình (1/đa ẩn), hệ tuyến tính.
- Ma trận & tuyến tính: nghịch đảo, định thức, phân rã (LU/QR/SVD), chuẩn, hạng, giải Ax=b.
- Giải tích: đạo hàm, tích phân (bất định/xác định), giải ODE đơn giản, chuỗi Taylor.
- Tối ưu cơ bản: LP/QP nhỏ (ràng buộc tuyến tính), MILP quy mô vừa (nếu cần VRP/ILP).
- Số học chuẩn: tìm nghiệm số (root finding), tích phân số, nội suy, xấp xỉ.

Endpoints:

- algebra.simplify, algebra.solve, matrix.solve, matrix.decompose,
- calculus.diff, calculus.integrate, calculus.series, ode.solve,
- numeric.root, numeric.integrate,
- optimize.lp, optimize.milp (nếu cần).

# **3) Nhóm XÁC SUẤT – THỐNG KÊ & CHUYÊN BIỆT**

- Phân phối (Normal, t, χ², Binomial, Poisson…): pdf/cdf/ppf, lấy mẫu, ước lượng.
- Thống kê mô tả & kiểm định: mean/var/CI, t-test, χ², ANOVA cơ bản.
- Tổ hợp: nCr, số Catalan, hoán vị có ràng buộc…
- Tín hiệu/FFT (nếu bạn hay xử lý chuỗi): FFT/IFFT, lọc cơ bản.
- Tài chính (tùy chọn): lãi suất hiệu dụng, NPV/IRR, annuity, day-count conventions (30/360, ACT/365…), chuyển đổi lịch tài chính.

Endpoints:

- prob.dist (pdf/cdf/ppf), stats.describe, stats.test, combinatorics.nCr,
- signal.fft, signal.ifft,
- finance.rate, finance.cashflow, finance.daycount.

# **4) Chiến lược**

# **bảo đảm đúng**

# **(anti-hallucination cho LLM)**

- Dual-engine check: tính bằng Fraction/Decimal song song ⇒ lệch thì gắn cờ.
- Symbolic → Numeric: với bài biểu thức, rút gọn ký hiệu trước, rồi mới tính số.
- Interval sanity: kết quả số phải nằm trong khoảng đã tính; nếu không ⇒ lỗi.
- Property checks: bất đẳng thức, miền xác định, đơn vị hợp lệ.
- Deterministic log: lưu chuỗi bước, phiên bản lib, seed, hash input/output (phù hợp style reproducibility của bạn).

# **5) Gợi ý thư viện (tùy runtime)**

Python (khuyến nghị để chuẩn xác & giàu tính năng):

- Arithmetic/Exact: fractions, decimal, fractions.Fraction, mpmath
- CAS: sympy
- Units: pint
- LA: numpy (số), sympy.Matrix (chính xác)
- Optimization: pulp/ortools
- Stats: scipy.stats (nếu cần), hoặc tự cài đặt subset
- Signal: numpy.fft

Node.js (nếu muốn JS):

- mathjs (parser + bigNumber), decimal.js, fraction.js, nerdamer (CAS nhẹ), convert-units (đơn vị cơ bản).
(Python vẫn mạnh hơn cho CAS/tối ưu.)

# **6) Thiết kế API / Schema (gợi ý)**

Request (chung):

{

"op": "algebra.solve",

"input": {

"equation": "x^2 - 5x + 6 = 0",

"vars": ["x"]

},

"settings": {

"mode": "exact|decimal",

"precision": 50,

"units": false,

"interval": false,

"timeout_ms": 1500

}

}

Response:

{

"ok": true,

"result": {"x": ["2", "3"]},

"trace": [

"factor(x^2-5x+6) = (x-2)(x-3)",

"solutions = 2,3"

],

"checks": {

"dual_engine_agree": true,

"units_ok": true,

"domain_ok": true

},

"meta": {

"hash_in": "…",

"hash_out": "…",

"elapsed_ms": 42,

"lib_versions": {"sympy": "1.13.2"}

}

}

# **7) Hành vi mặc định & UX với LLM**

- Mặc định exact cho số nguyên/phân số; decimal khi có hàm siêu việt (sin, exp, log) với precision cao.
- Luôn trả “trace” ngắn gọn (các bước chính) để LLM có thể trình bày lời giải.
- Cảnh báo rõ ràng (ví dụ “units_mismatch”, “interval_violation”, “timeout”) kèm đề xuất: giảm độ phức tạp, tăng precision, đổi mode.
- Idempotent: cùng input → cùng output + hash.

# **8) Một số “preset” hữu ích**

- profile.strict: exact + interval + dual-engine + timeouts ngắn (dùng cho chấm/kiểm).
- profile.fast: decimal + precision 34 (quad-decimal) cho tốc độ.
- profile.symbolic_first: luôn simplify trước khi eval.

# **9) Ví dụ các lệnh điển hình**

- calculate.eval: "2/3 + 4/9" → trả Fraction, Decimal, Interval.
- algebra.solve: "2x+3=7"; hệ tuyến tính; đa thức bậc cao (có cảnh báo Galois khi cần dạng đóng).
- calculus.integrate: "∫ (sin x)/x dx, 0→∞" → cảnh báo “không có nguyên hàm sơ cấp”, chuyển sang tích phân số với sai số kèm theo.
- units.convert: "9.81 m/s^2 → ft/s^2"
- optimize.lp: min c^T x s.t. Ax≤b, x≥0 → trả nghiệm, chứng chỉ dual (nếu có).

Nếu bạn muốn, mình có thể phác sẵn skeleton MCP server (Python) với:

- router các endpoints ở trên,
- adapter SymPy/Pint/NumPy/OR-Tools,
- lớp kiểm lỗi (dual-engine, interval),
- logger sinh trace + hash,
- kèm 10 bài test mẫu (unit & property-based).
Bạn chỉ việc docker compose up là chạy được.

---

Here’s a survey of recent arXiv / preprint research (2023-2025) exploring why LLMs often make mistakes in calculation / mathematical reasoning, along with key causes and open challenges. If you like, I can also send you a curated list of future-directions papers.

