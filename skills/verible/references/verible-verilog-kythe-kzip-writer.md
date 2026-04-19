# verible-verilog-kythe-kzip-writer

`verible-verilog-kythe-kzip-writer` produces Kythe KZip files from SystemVerilog source files.

## Usage

```bash
verible-verilog-kythe-kzip-writer [options] --filelist_path FILE
```

**Input:**
A file list path which contains SystemVerilog top-level translation unit files (one per line, relative to the file list location). Files should be ordered by definition dependencies.

**Output:**
Produces Kythe KZip (https://kythe.io/docs/kythe-kzip.html).

## Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--filelist_path` | Path to the file list containing SystemVerilog source files. | `""` |
| `--output_path` | Path where the kzip file will be written. | `""` |
| `--corpus` | Corpus name (e.g., the project) to which the code belongs. | `""` |
| `--code_revision` | Version control revision for the code. | `""` |
