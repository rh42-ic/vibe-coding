# verible-verilog-obfuscate

`verible-verilog-obfuscate` mangles Verilog code by changing identifiers while preserving whitespaces and identifier lengths.

## Usage

```bash
verible-verilog-obfuscate [options] < original > output
```
Output is written to stdout.

## Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--decode` | Apply translation dictionary in reverse to de-obfuscate (requires `--load_map`). | `false` |
| `--load_map` | Pre-load an existing translation dictionary (from `--save_map`). | `""` |
| `--save_map` | Save the translation dictionary for future reuse. | `""` |
| `--preserve_builtin_functions` | Preserve built-in function names like `sin()`, `ceil()`. | `true` |
| `--preserve_interface` | Preserve module, port, and parameter names. | `false` |
| `--verilog_trace_parser` | Trace Verilog parser activity. | `false` |
