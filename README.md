# Safe Calculation Math Engine (SCME)

A Model Context Protocol (MCP) server that lets an AI assistant delegate exact
mathematical computation to verified Python libraries (SymPy, SciPy, NumPy)
instead of guessing the result. It exposes a single `calculate` tool with 27
operations (arithmetic, statistics and regression, calculus, linear algebra,
number theory, units, complex numbers, batch processing and more).

This repository is a snapshot of **release v1.1.0, the version evaluated in the
master's thesis "Safe Calculation Math Engine" (Ho Chi Minh University of
Banking)**. It is published so that the evaluated artifact can be inspected and
re-run independently.

## Layout

- `python-cli-core/`: the computation core and the `calc.sh` command-line wrapper.
- `mcp/`: the TypeScript MCP server that forwards requests to the CLI.
- `docs/`, `CHANGELOG.md`, `HOW-TO-USE-MCP.md`: documentation and the v1.1.0 change record.

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install sympy scipy numpy
./python-cli-core/calc.sh '{"operation": "eval", "params": {"expression": "2 + 3 * 4"}}'
```

`calc.sh` uses the virtual environment at `.venv` next to the `python-cli-core`
folder when it exists (override with `SCME_VENV`), otherwise the `python3` on
your `PATH`.

To run the MCP server, build it with `npm install && npm run build` inside
`mcp/`, then register `mcp/dist/index.js` with your MCP client (see
`mcp/mcp-config-sample.json`, where `<SCME_DIR>` is the folder of this
checkout). The server finds `calc.sh` relative to itself; set
`SCME_CALC_SCRIPT` to use another location.

## Known limitations of this snapshot

- Results are returned as double-precision numbers (expression evaluation also
  returns a symbolic form), so exactness beyond double precision is not provided
  for every operation.
- Each call starts a fresh process (stateless design), which costs latency.
- Some older documentation files under `docs/` describe the author's own
  development setup and use placeholders such as `<SCME_DIR>` and `<VENV>`.
- This is research software released without warranty. It was evaluated on a
  54-case suite constructed for the thesis and on external benchmarks described
  in the thesis; do not treat it as a verified numerical library.
- Later development versions (more operations, an optional visualizer layer)
  are not part of this snapshot.

## License

MIT, see `LICENSE`.
