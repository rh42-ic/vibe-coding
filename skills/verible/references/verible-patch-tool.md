# verible-patch-tool

`verible-patch-tool` is a tool for managing patches and applying hunks selectively to SystemVerilog source files.

## Usage

```bash
verible-patch-tool command args...
```

## Available Commands

### help
Display help information for the tool or specific commands.

### changed-lines
Identifies changed lines in a patch file.

**Input:**
`patchfile` is a unified-diff file from `diff -u` or other version-controlled equivalents like `{p4,git,hg,cvs,svn} diff`. Use `-` to read from stdin.

**Output (stdout):**
Prints output in the following format per line:
```
filename [line-ranges]
```
where `line-ranges` (optional) is suitable for tools that accept a set of lines to operate on (e.g., `1-4,8,21-42`). `line-ranges` is omitted for files that are considered new in the patch file.

### apply-pick
Selectively applies patch hunks to files.

**Input:**
`patchfile` is a unified-diff file from `diff -u` or other version-controlled equivalents.

**Effect:**
Modifies patched files in-place, following user selections on which patch hunks to apply.
