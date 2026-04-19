# verible-verilog-kythe-extractor

`verible-verilog-kythe-extractor` extracts Kythe indexing facts from SystemVerilog source files.

## Usage

```bash
verible-verilog-kythe-extractor [options] --file_list_path FILE
```

**Input:**
A file list path which contains SystemVerilog top-level translation unit files (one per line, relative to the file list location). Files should be ordered by definition dependencies.

**Output:**
Produces indexing facts for Kythe (http://kythe.io).

## Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--file_list_path` | Path to the file list containing SystemVerilog source files. | `""` |
| `--file_list_root` | Absolute location prepended to files in the file list. | `.` |
| `--include_dir_paths` | Comma-separated directory paths for include file searching. Order matters. | (empty) |
| `--print_kythe_facts` | Format for outputting Kythe facts: `json`, `json_debug`, `proto`, or `none`. | `json` |
| `--printextraction` | Print the extracted general indexing facts tree from the middle layer. | `false` |
| `--verilog_project_name` | Verilog project name to use as Kythe corpus (optional). | `""` |
| `--verilog_trace_parser` | Trace Verilog parser activity. | `false` |
