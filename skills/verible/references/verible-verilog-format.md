# verible-verilog-format

`verible-verilog-format` is a SystemVerilog source code formatter that ensures a consistent code style across files.

## Usage

```bash
verible-verilog-format [options] <file> [<file...>]
```
To pipe from stdin, use `-` as `<file>`.

## Flags

### Formatting Style Options

| Flag | Description | Default |
|------|-------------|---------|
| `--column_limit` | Target line length limit to stay under when formatting. | `100` |
| `--indentation_spaces` | Number of spaces per indentation level. | `2` |
| `--line_break_penalty` | Penalty for each introduced line break during formatting optimization. | `2` |
| `--line_terminator` | Output line terminator (`auto`, `CR`, `CRLF`). `auto` detects input terminator. | `auto` |
| `--over_column_limit_penalty` | Baseline penalty for exceeding the column limit. | `100` |
| `--wrap_spaces` | Number of spaces per wrap level. | `4` |

### SystemVerilog Specific Style Options

| Flag | Description | Default |
|------|-------------|---------|
| `--assignment_statement_alignment` | Alignment for assignments (`align`, `flush-left`, `preserve`, `infer`). | `infer` |
| `--case_items_alignment` | Alignment for case items (`align`, `flush-left`, `preserve`, `infer`). | `infer` |
| `--class_member_variable_alignment` | Alignment for class member variables (`align`, `flush-left`, `preserve`, `infer`). | `infer` |
| `--compact_indexing_and_selections` | Use compact binary expressions inside indexing / bit selection operators. | `true` |
| `--distribution_items_alignment` | Alignment for distribution items (`align`, `flush-left`, `preserve`, `infer`). | `infer` |
| `--enum_assignment_statement_alignment` | Alignment for enum assignments (`align`, `flush-left`, `preserve`, `infer`). | `infer` |
| `--expand_coverpoints` | Always expand coverpoints if true. | `false` |
| `--formal_parameters_alignment` | Alignment for formal parameters (`align`, `flush-left`, `preserve`, `infer`). | `infer` |
| `--formal_parameters_indentation` | Indentation for formal parameters (`indent`, `wrap`). | `wrap` |
| `--module_net_variable_alignment` | Alignment for net/variable declarations (`align`, `flush-left`, `preserve`, `infer`). | `infer` |
| `--named_parameter_alignment` | Alignment for named actual parameters (`align`, `flush-left`, `preserve`, `infer`). | `infer` |
| `--named_parameter_indentation` | Indentation for named parameter assignments (`indent`, `wrap`). | `wrap` |
| `--named_port_alignment` | Alignment for named port connections (`align`, `flush-left`, `preserve`, `infer`). | `infer` |
| `--named_port_indentation` | Indentation for named port connections (`indent`, `wrap`). | `wrap` |
| `--port_declarations_alignment` | Alignment for port declarations (`align`, `flush-left`, `preserve`, `infer`). | `infer` |
| `--port_declarations_indentation` | Indentation for port declarations (`indent`, `wrap`). | `wrap` |
| `--port_declarations_right_align_packed_dimensions` | Align packed dimensions to the right when alignment is enabled. | `false` |
| `--port_declarations_right_align_unpacked_dimensions` | Align unpacked dimensions to the right when alignment is enabled. | `false` |
| `--struct_union_members_alignment` | Alignment for struct/union members (`align`, `flush-left`, `preserve`, `infer`). | `infer` |
| `--try_wrap_long_lines` | Attempt to optimize line wrapping decisions if true, else leave unformatted. | `false` |
| `--wrap_end_else_clauses` | Split `end` and `else` keywords into separate lines. | `false` |

### Tool Behavior Options

| Flag | Description | Default |
|------|-------------|---------|
| `--failsafe_success` | Exit with 0 status even if errors occur, preserving original text. | `true` |
| `--inplace` | Overwrite input files on successful formatting. | `false` |
| `--lines` | Specific line ranges to format (1-based, inclusive N-M, comma-separated). | (all lines) |
| `--max_search_states` | Limit search states explored during line wrap optimization. | `100000` |
| `--stdin_name` | Alternate name for stdin for diagnostic purposes. | `<stdin>` |
| `--verify` | Check if formatting would be done without modifying files. Returns 1 if changes needed. | `false` |
| `--verify_convergence` | Verify that re-formatting output results in no further changes. | `true` |
| `--verbose` | Increase output verbosity. | `false` |

### Parser Options

| Flag | Description | Default |
|------|-------------|---------|
| `--verilog_trace_parser` | Trace Verilog parser activity. | `false` |
