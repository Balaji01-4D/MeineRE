# File Operations

Meine provides powerful file operations through its regex-based command system. This guide covers all the available file operations and their advanced usage.

## Basic Operations

### Delete Files

```bash
# Delete a single file
del file.txt
rm file.txt

# Delete multiple files
del file1.txt, file2.txt
rm *.txt

# Delete with confirmation
del -i file.txt

# Force delete
del -f locked_file.txt
```

### Copy Files

```bash
# Copy a single file
copy source.txt to destination/
cp source.txt destination/

# Copy multiple files
copy file1.txt, file2.txt to backup/
cp *.txt backup/

# Copy with progress
copy -p large_file.iso to backup/

# Copy preserving attributes
copy -a config.json to settings/
```

### Move Files

```bash
# Move a single file
move old.txt to new/location/
mv old.txt new/location/

# Move multiple files
move *.pdf to documents/
mv file1.txt, file2.txt archive/

# Move with confirmation
move -i important.doc to backup/
```

### Rename Files

```bash
# Rename a single file
rename oldname.txt as newname.txt
ren document.txt as report.txt

# Rename with pattern
rename *.txt as *.md
ren "report (old).txt" as "report (new).txt"
```

## Advanced Operations

### Batch Operations

```bash
# Delete all .tmp files recursively
del -r **/*.tmp

# Copy all Python files to backup
copy **/*.py to backup/

# Move all images to photos directory
move **/*.{jpg,png,gif} to photos/
```

### Pattern Matching

Meine supports various pattern matching syntax:

```bash
# Wildcard matching
*.txt           # All .txt files
file?.txt       # file1.txt, fileA.txt, etc.
file[1-3].txt   # file1.txt, file2.txt, file3.txt

# Regular expressions
/^data.*\.csv$/  # Files starting with "data" and ending with .csv
/.*backup.*/     # Files containing "backup"
```

### File Attributes

```bash
# Show file attributes
attr file.txt

# Copy preserving all attributes
copy -a source.txt to dest/

# Change file permissions
chmod 644 file.txt
```

### Archive Operations

```bash
# Create archive
archive create archive.zip file1.txt file2.txt
zip new.zip *.txt

# Extract archive
extract archive.zip
unzip archive.zip

# List archive contents
list archive.zip
```

## Safety Features

### Confirmation Prompts

Add `-i` or `--interactive` to enable confirmation prompts:

```bash
del -i important.txt
move -i *.txt to backup/
copy -i config.json to /etc/
```

### Dry Run

Use `-n` or `--dry-run` to simulate operations:

```bash
del -n *.txt
move -n documents/ to archive/
```

### Backup

Create backups before operations:

```bash
del --backup file.txt
move --backup source/ to dest/
```

## Error Handling

### Common Error Messages

- `Permission denied`: Insufficient permissions
- `File not found`: File doesn't exist
- `Directory not empty`: Cannot delete non-empty directory
- `File exists`: Destination file already exists

### Error Recovery

```bash
# Force operation
del -f locked_file.txt

# Skip errors
copy --skip-errors source/ to dest/

# Create parent directories
move --parents file.txt to new/path/
```

## Best Practices

1. Use `--dry-run` for complex operations
2. Enable interactive mode (`-i`) for important files
3. Create backups for critical operations
4. Use pattern matching carefully
5. Check permissions before operations

## Next Steps

- Learn about [System Commands](/guide/system-commands)
- Explore [Terminal UI](/guide/terminal-ui) features
- Set up [Keyboard Shortcuts](/guide/shortcuts)
- Configure [Settings](/guide/configuration)
