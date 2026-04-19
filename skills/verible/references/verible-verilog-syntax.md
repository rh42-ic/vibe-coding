# verible-verilog-syntax

`verible-verilog-syntax` parses SystemVerilog files and provides diagnostics, tokens, or the concrete syntax tree.

## Usage

```bash
verible-verilog-syntax [options] <file> [<file>...]
```

## Flags

### Output Selection

| Flag | Description | Default |
|------|-------------|---------|
| `--printrawtokens` | Print all lexed tokens, including filtered ones. | `false` |
| `--printtokens` | Print all lexed and filtered tokens. | `false` |
| `--printtree` | Print the concrete syntax tree. | `false` |
| `--export_json` | Output in JSON format for use by other tools. | `false` |
| `--verifytree` | Verify all tokens are parsed into the tree and print unmatched tokens. | `false` |

### Tool Behavior Options

| Flag | Description | Default |
|------|-------------|---------|
| `--error_limit` | Limit the number of syntax errors reported (0 for unlimited). | `0` |
| `--lang` | Select language variant: `auto` (SystemVerilog-2017 with auto-detection), `sv` (strict SystemVerilog-2017), `lib` (Verilog library map language). | `auto` |
| `--show_diagnostic_context` | Print the line where diagnostic was found with a position marker. | `false` |
| `--verilog_trace_parser` | Trace Verilog parser activity. | `false` |
