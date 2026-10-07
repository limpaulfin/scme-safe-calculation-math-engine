#!/bin/bash
# Test count operation - Standalone testing
# Date: 2025-10-18

CLI_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/python-cli-core/calc.sh"

echo "================================"
echo "TEST COUNT OPERATION - STANDALONE"
echo "================================"
echo ""

# Test 1: Count simple array
echo "Test 1: Count simple array"
$CLI_PATH '{"operation": "count", "params": {"data": "[\"item1\", \"item2\", \"item3\"]", "type": "items"}}'
echo ""

# Test 2: Count array from example (downgrade positions)
echo "Test 2: Count downgrade positions (13 items)"
$CLI_PATH '{"operation": "count", "params": {"data": "[\"pos1\", \"pos2\", \"pos3\", \"pos4\", \"pos5\", \"pos6\", \"pos7\", \"pos8\", \"pos9\", \"pos10\", \"pos11\", \"pos12\", \"pos13\"]", "type": "items"}}'
echo ""

# Test 3: Count simple 5 items
echo "Test 3: Count 5 files"
$CLI_PATH '{"operation": "count", "params": {"data": "[\"file1\", \"file2\", \"file3\", \"file4\", \"file5\"]", "type": "items"}}'
echo ""

# Test 4: Empty array
echo "Test 4: Empty array"
$CLI_PATH '{"operation": "count", "params": {"data": "[]", "type": "items"}}'
echo ""

# Test 5: Single item
echo "Test 5: Single item array"
$CLI_PATH '{"operation": "count", "params": {"data": "[\"only_one\"]", "type": "items"}}'
echo ""

echo "================================"
echo "ALL TESTS COMPLETED"
echo "================================"
