# verible-verilog-ls

`verible-verilog-ls` is a Language Server Protocol (LSP) implementation for SystemVerilog.

## Usage

```bash
verible-verilog-ls [options]
```

## Flags

### Project Management

| Flag | Description | Default |
|------|-------------|---------|
| `--file_list_path` | Path to the Verible FileList for the project. | `verible.filelist` |

### LSP Behavior

| Flag | Description | Default |
|------|-------------|---------|
| `--lsp_enable_hover` | Enable experimental hover mode. | `false` |
| `--push_diagnostic_notifications` | Send diagnostics as notifications. | `true` |
| `--variables_in_outline` | Include variables in the symbol outline. | `true` |

### Formatting Options (LSP Formatting)

| Flag | Description | Default |
|------|-------------|---------|
| `--column_limit` | Target line length limit. | `100` |
| `--indentation_spaces` | Spaces per indentation level. | `2` |
| `--line_terminator` | Output line terminator (`auto`, `CR`, `CRLF`). | `auto` |
| `--wrap_spaces` | Spaces per wrap level. | `4` |
| (Many other formatting flags from `verible-verilog-format` are also supported) | | |

### Linter Options (LSP Linting)

| Flag | Description | Default |
|------|-------------|---------|
| `--rules` | Enabled lint rules. | (empty) |
| `--ruleset` | Base ruleset: `default`, `all`, `none`. | `default` |
| `--rules_config` | Path to lint configuration file. | `""` |
| `--rules_config_search` | Search upward for configuration file. | `false` |

### Parser Options

| Flag | Description | Default |
|------|-------------|---------|
| `--verilog_trace_parser` | Trace Verilog parser activity. | `false` |
