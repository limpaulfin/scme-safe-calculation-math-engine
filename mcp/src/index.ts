#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { execa } from "execa";
import { z } from "zod";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const CALC_SCRIPT = process.env.SCME_CALC_SCRIPT ?? resolve(dirname(fileURLToPath(import.meta.url)), "../../python-cli-core/calc.sh");

const CalculateSchema = z.object({
  operation: z.string().describe("Operation name: uuid|random|eval|base_convert|count|const_get|const_list|complex_eval|complex_to_polar|complex_from_polar|units_convert|units_quick|units_list|stats_describe|stats_regress|prob_dist|stat_test|solve_linear|solve_poly|differentiate|integrate|limit|combinatorics|number_theory|matrix_op|vector_op|batch"),
  params: z.record(z.string()).describe("Operation parameters as key-value pairs (all values as strings)"),
  operations: z.array(z.any()).optional().describe("For batch operation only: array of operations to execute"),
});

type CalculateParams = z.infer<typeof CalculateSchema>;

async function calculate(params: CalculateParams): Promise<string> {
  // Handle batch operation specially: operations is an array, not a string
  let finalParams = params.params;
  if (params.operation === 'batch' && params.operations) {
    finalParams = { operations: JSON.stringify(params.operations) };
  }

  const jsonInput = JSON.stringify({
    operation: params.operation,
    params: finalParams,
  });

  try {
    const { stdout } = await execa("bash", [CALC_SCRIPT, jsonInput], { timeout: 30000 });
    return stdout;
  } catch (error: any) {
    throw new Error(`Calculation failed: ${error.message}`);
  }
}

const server = new Server(
  { name: "mcp-safe-calculation", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "calculate",
      description: `Safe math calculator with 27 operations (CASIO fx-570ES PLUS parity).

🎯 RECOMMENDED: Use batch operation to execute multiple calculations trong 1 request
⚠️ CRITICAL: For batch, operations MUST be STRING (JSON.stringify), NOT direct array

Available operations (27 total):

🎯 BATCH PROCESSING (RECOMMENDED - LUÔN ƯU TIÊN SỬ DỤNG):
• batch - Execute multiple operations with labeled results
  Syntax: {"operation": "batch", "params": {"operations": "[...]"}}
  ✅ Correct: params.operations as STRING
  ❌ Wrong: operations as direct array

SINGLE OPERATIONS (chỉ khi thực sự cần 1 operation):
• uuid - UUID generator (full/tail modes)
• random - Random number generator (dec/hex/bin/oct)
• eval - Math expression evaluator with high precision
• base_convert - Number base conversion (dec/hex/oct/bin)
• count - Array counter with indexed mapping (solves AI counting errors)
• const_get - Get scientific constant by code/name
• const_list - List all 40+ CODATA 2022 constants
• complex_eval - Complex number arithmetic
• complex_to_polar - Rectangular to polar conversion
• complex_from_polar - Polar to rectangular conversion
• units_convert - General unit conversion
• units_quick - Quick unit conversion via preset codes
• units_list - List 14 preset unit conversions
• stats_describe - Descriptive statistics (mean/median/stdev/quantiles)
• stats_regress - Regression analysis (linear/log/exp/power)
• prob_dist - Probability distributions (normal/t/chi2/F/binomial/poisson)
• stat_test - Statistical hypothesis tests (t-test/chi2/ks)
• solve_linear - Linear system solver (Ax=b)
• solve_poly - Polynomial root finder
• differentiate - Symbolic differentiation
• integrate - Definite/indefinite integration
• limit - Limit calculation (including infinity)
• combinatorics - nCr, nPr, factorial
• number_theory - gcd, lcm, isprime, powmod
• matrix_op - Matrix operations (add/sub/mul/det/inv/rank/trace/transpose)
• vector_op - Vector operations (dot/cross/norm/angle)

📖 Full documentation: see README.md in the repository

Usage Examples:

🎯 BATCH OPERATION (RECOMMENDED):
{
  "operation": "batch",
  "params": {
    "operations": "[{\"name\":\"total\",\"operation\":\"eval\",\"params\":{\"expression\":\"100+200+300\"}},{\"name\":\"average\",\"operation\":\"eval\",\"params\":{\"expression\":\"(100+200+300)/3\"}},{\"name\":\"id\",\"operation\":\"uuid\",\"params\":{\"mode\":\"tail\"}}]"
  }
}

SINGLE OPERATION (chỉ khi cần 1 operation):
{
  "operation": "eval",
  "params": {
    "expression": "sqrt(16) + 2 * 3",
    "precision": "15"
  }
}

Returns JSON with status, operation, and data.`,
      inputSchema: {
        type: "object",
        properties: {
          operation: {
            type: "string",
            description: "Operation name (see list above)",
          },
          params: {
            type: "object",
            description: "For single operations: operation-specific parameters (all values as strings). Not used for batch operation.",
            additionalProperties: { type: "string" },
          },
          operations: {
            type: "array",
            description: "For batch operation only: array of operations to execute. Each item: {name: string, operation: string, params: {[key: string]: string}}",
            items: {
              type: "object",
              properties: {
                name: { type: "string", description: "Label for this operation" },
                operation: { type: "string", description: "Operation name" },
                params: {
                  type: "object",
                  description: "Operation parameters (all values as strings)",
                  additionalProperties: { type: "string" },
                },
              },
              required: ["name", "operation", "params"],
            },
          },
        },
        required: ["operation"],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "calculate") {
    const validatedParams = CalculateSchema.parse(request.params.arguments);
    const result = await calculate(validatedParams);
    return { content: [{ type: "text", text: result }] };
  }
  throw new Error(`Unknown tool: ${request.params.name}`);
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("mcp-safe-calculation server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
