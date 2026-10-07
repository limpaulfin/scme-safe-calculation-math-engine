#!/usr/bin/env bash
# Autodebug Script - Run tool and analyze debug log
# Usage: ./autodebug.sh <command> [args...]
#
# Example:
#   ./autodebug.sh uuid --tail --count 5

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/logs/debug.log"

echo "🔍 Autodebug Mode - Safe Calculation Math Engine"
echo "=================================================="
echo ""

# Clear old log
> "$LOG_FILE"
echo "✓ Cleared debug log"

# Run command
echo "▶ Running: ./calc.sh $@"
echo ""
./calc.sh "$@"
EXIT_CODE=$?

echo ""
echo "=================================================="
echo "📊 Debug Log Analysis"
echo "=================================================="
echo ""

# Show last 50 lines of debug log
echo "📝 Last 50 lines from debug.log:"
echo "--------------------------------------------------"
tail -50 "$LOG_FILE"
echo "--------------------------------------------------"
echo ""

# Check for errors
ERROR_COUNT=$(grep -c "\[ERROR\]" "$LOG_FILE" || true)
WARNING_COUNT=$(grep -c "\[WARNING\]" "$LOG_FILE" || true)

echo "📈 Summary:"
echo "  - Exit code: $EXIT_CODE"
echo "  - Errors: $ERROR_COUNT"
echo "  - Warnings: $WARNING_COUNT"
echo ""

if [ $ERROR_COUNT -gt 0 ]; then
    echo "❌ Errors found in log:"
    grep "\[ERROR\]" "$LOG_FILE" || true
    echo ""
fi

if [ $WARNING_COUNT -gt 0 ]; then
    echo "⚠️  Warnings found in log:"
    grep "\[WARNING\]" "$LOG_FILE" || true
    echo ""
fi

# Performance analysis
PERF_LINES=$(grep "PERF" "$LOG_FILE" || true)
if [ -n "$PERF_LINES" ]; then
    echo "⚡ Performance:"
    echo "$PERF_LINES"
    echo ""
fi

if [ $EXIT_CODE -eq 0 ] && [ $ERROR_COUNT -eq 0 ]; then
    echo "✅ All checks passed!"
else
    echo "❌ Issues detected - check log above"
fi

echo ""
echo "💡 Full log: $LOG_FILE"
echo "=================================================="

exit $EXIT_CODE
