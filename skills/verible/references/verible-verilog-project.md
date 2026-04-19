# verible-verilog-project

`verible-verilog-project` provides project-level analysis for SystemVerilog codebases, including symbol tables and dependency analysis.

## Usage

```bash
verible-verilog-project command args...
```

## Available Commands

### help
Display help information for the tool or specific commands.

### symbol-table-defs
Prints a human-readable unified symbol table representation of all files in the project. Does not resolve symbols.

### symbol-table-refs
Prints a human-readable representation of symbol table references after attempting to resolve symbols.

### file-deps
Prints human-readable representation of inter-file dependencies (e.g., `"file1.sv" depends on "file2.sv" for symbols { X, Y, Z... }`).

## Flags (Project Options)

| Flag | Description | Default |
|------|-------------|---------|
| `--file_list_path` | Path to the file list containing SystemVerilog source files. Files should be ordered by dependencies. | `""` |
| `--file_list_root` | Absolute location prepended to files in the file list. | `.` |
| `--include_dir_paths` | Comma-separated directory paths for include file searching. Order matters. | (empty) |
| `--verilog_trace_parser` | Trace Verilog parser activity. | `false` |
