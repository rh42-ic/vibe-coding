# Verible Formatting Flags Reference

This document provides a comprehensive list of formatting flags for `verible-verilog-format`.

| Flag Name | Description | Default Value | Possible Values |
|-----------|-------------|---------------|-----------------|
| `--column_limit` | Target line length limit to stay under when formatting. | 100 | |
| `--indentation_spaces` | Each indentation level adds this many spaces. | 2 | |
| `--line_break_penalty` | Penalty added to solution for each introduced line break. | 2 | |
| `--line_terminator` | Line terminator. The 'auto' option chooses the output depending on the observed input. The explicit choice CR or CRLF fixes the output line terminator. | `auto` | `auto`, `CR`, `CRLF` |
| `--over_column_limit_penalty` | For penalty minimization, this represents the baseline penalty value of exceeding the column limit. Additional penalty of 1 is incurred for each character over this limit. | 100 | |
| `--wrap_spaces` | Each wrap level adds this many spaces. This applies when the first element after an open-group section is wrapped. Otherwise, the indentation level is set to the column position of the open-group operator. | 4 | |
| `--assignment_statement_alignment` | Format various assignments. | `infer` | `align`, `flush-left`, `preserve`, `infer` |
| `--case_items_alignment` | Format case items. | `infer` | `align`, `flush-left`, `preserve`, `infer` |
| `--class_member_variable_alignment` | Format class member variables. | `infer` | `align`, `flush-left`, `preserve`, `infer` |
| `--compact_indexing_and_selections` | Use compact binary expressions inside indexing / bit selection operators. | `true` | `true`, `false` |
| `--distribution_items_alignment` | Aligh distribution items. | `infer` | `align`, `flush-left`, `preserve`, `infer` |
| `--enum_assignment_statement_alignment` | Format assignments with enums. | `infer` | `align`, `flush-left`, `preserve`, `infer` |
| `--expand_coverpoints` | If true, always expand coverpoints. | `false` | `true`, `false` |
| `--formal_parameters_alignment` | Format formal parameters. | `infer` | `align`, `flush-left`, `preserve`, `infer` |
| `--formal_parameters_indentation` | Indent formal parameters. | `wrap` | `indent`, `wrap` |
| `--module_net_variable_alignment` | Format net/variable declarations. | `infer` | `align`, `flush-left`, `preserve`, `infer` |
| `--named_parameter_alignment` | Format named actual parameters. | `infer` | `align`, `flush-left`, `preserve`, `infer` |
| `--named_parameter_indentation` | Indent named parameter assignments. | `wrap` | `indent`, `wrap` |
| `--named_port_alignment` | Format named port connections. | `infer` | `align`, `flush-left`, `preserve`, `infer` |
| `--named_port_indentation` | Indent named port connections. | `wrap` | `indent`, `wrap` |
| `--port_declarations_alignment` | Format port declarations. | `infer` | `align`, `flush-left`, `preserve`, `infer` |
| `--port_declarations_indentation` | Indent port declarations. | `wrap` | `indent`, `wrap` |
| `--port_declarations_right_align_packed_dimensions` | If true, packed dimensions in contexts with enabled alignment are aligned to the right. | `false` | `true`, `false` |
| `--port_declarations_right_align_unpacked_dimensions` | If true, unpacked dimensions in contexts with enabled alignment are aligned to the right. | `false` | `true`, `false` |
| `--struct_union_members_alignment` | Format struct/union members. | `infer` | `align`, `flush-left`, `preserve`, `infer` |
| `--try_wrap_long_lines` | If true, let the formatter attempt to optimize line wrapping decisions where wrapping is needed, else leave them unformatted. This is a short-term measure to reduce risk-of-harm. | `false` | `true`, `false` |
| `--wrap_end_else_clauses` | Split end and else keywords into separate lines. | `false` | `true`, `false` |
| `--verilog_trace_parser` | Trace verilog parser. | `false` | `true`, `false` |
| `--failsafe_success` | If true, always exit with 0 status, even if there were input errors or internal errors. In all error conditions, the original text is always preserved. This is useful in deploying services where fail-safe behaviors should be considered a success. | `true` | `true`, `false` |
| `--inplace` | If true, overwrite the input file on successful conditions. | `false` | `true`, `false` |
| `--lines` | Specific lines to format, 1-based, comma-separated, inclusive N-M ranges, N is short for N-N. By default, left unspecified, all lines are enabled for formatting. (repeatable, cumulative). | | |
| `--max_search_states` | Limits the number of search states explored during line wrap optimization. | 100000 | |
| `--show_equally_optimal_wrappings` | If true, print when multiple optimal solutions are found (stderr), but continue to operate normally. | `false` | `true`, `false` |
| `--show_inter_token_info` | If true, along with show_token_partition_tree, include inter-token information such as spacing and break penalties. | `false` | `true`, `false` |
| `--show_largest_token_partitions` | If > 0, print token partitioning and then exit without formatting output. | 0 | |
| `--show_token_partition_tree` | If true, print diagnostics after token partitioning and then exit without formatting output. | `false` | `true`, `false` |
| `--stdin_name` | When using '-' to read from stdin, this gives an alternate name for diagnostic purposes. Otherwise this is ignored. | `<stdin>` | |
| `--verbose` | Be more verbose. | `false` | `true`, `false` |
| `--verify` | If true, only checks if formatting would be done. Return code 0 means no files would change. Return code 1 means some files would be reformatted. | `false` | `true`, `false` |
| `--verify_convergence` | If true, and not incrementally formatting with --lines, verify that re-formatting the formatted output yields no further changes, i.e. formatting is convergent. | `true` | `true`, `false` |
