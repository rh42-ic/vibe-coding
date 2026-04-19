# verible-verilog-diff

`verible-verilog-diff` compares two SystemVerilog files and identifies differences based on the selected mode.

## Usage

```bash
verible-verilog-diff [options] file1 file2
```
Use `-` as a file name to read from stdin.

## Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--mode` | Defines difference functions: `format` (ignore whitespaces, compare token texts; useful for verifying formatter output), `obfuscate` (preserve whitespaces, compare token texts' lengths only; useful for verifying obfuscator output). | `format` |
