# verible-verilog-preprocessor

`verible-verilog-preprocessor` provides tools for preprocessing SystemVerilog files, including macro expansion and comment removal.

## Usage

```bash
verible-verilog-preprocessor command args...
```

## Available Commands

### help
Display help information for the tool or specific commands.

### preprocess
Expands macros and interprets compiler directives.

**Input:**
`preprocess [define-include-flags] file [file...]`
Accepts one or more files. Each file is preprocessed independently. `+define+` and `+include+` flags are supported.

**Output (stdout):**
Concatenated preprocessed content.

### strip-comments
Removes comments from source files.

**Input:**
`strip-comments file [replacement-char]`
`replacement-char` (optional) is used to replace comment contents. Defaults to space. Use empty string `""` for deletion. Newlines are preserved.

**Output (stdout):**
Original file content with comments removed.

### generate-variants
Generates possible variants based on conditional directives.

**Input:**
`generate-variants file [-limit_variants number]`
`limit_variants` (optional) limits the number of variants printed (default 20).

**Output (stdout):**
Every possible variant of `` `ifdef `` blocks.

## Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--limit_variants` | Maximum number of variants printed by `generate-variants`. | `20` |
| `--verilog_trace_parser` | Trace Verilog parser activity. | `false` |
