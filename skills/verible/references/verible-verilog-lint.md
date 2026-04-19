# verible-verilog-lint

`verible-verilog-lint` is a linter for SystemVerilog that identifies style violations and potential bugs.

## Usage

```bash
verible-verilog-lint [options] <file> [<file>...]
```

## Flags

### Linter Rule Selection

| Flag | Description | Default |
|------|-------------|---------|
| `--rules` | Comma-separated lint rules to enable. Use `+` prefix to enable, `-` to disable. Configuration follows `=`. | (empty) |
| `--rules_config` | Path to a lint rules configuration file. Disables `--rules_config_search` if set. | `""` |
| `--rules_config_search` | Search upward for `.rules.verible_lint` config file from the file location. | `false` |
| `--ruleset` | Base set of rules to use: `default`, `all`, or `none`. | `default` |
| `--waiver_files` | Comma-separated paths to waiver configuration files. | `""` |

### Autofix and Output Options

| Flag | Description | Default |
|------|-------------|---------|
| `--autofix` | Autofix mode: `no`, `patch-interactive`, `patch`, `inplace-interactive`, `inplace`, `generate-waiver`. | `no` |
| `--autofix_output_file` | File to write patches or waivers when using specific `--autofix` modes. | `""` |
| `--generate_markdown` | Print description of every rule formatted as Markdown and exit. | `false` |
| `--help_rules` | Print description of one or all rules and exit (e.g., `all` or `<rule-name>`). | `""` |
| `--print_rules_file` | Print current set of lint rules in configuration format and exit. | `false` |
| `--show_diagnostic_context` | Print the line where diagnostic was found with a position marker. | `false` |

### Tool Behavior Options

| Flag | Description | Default |
|------|-------------|---------|
| `--check_syntax` | Check for lexical and syntax errors if true. | `true` |
| `--lint_fatal` | Exit with non-zero status if violations are found. | `true` |
| `--parse_fatal` | Exit with non-zero status if syntax errors are found. | `true` |
| `--verilog_trace_parser` | Trace Verilog parser activity. | `false` |
