# File Operations

Meine provides powerful file operations through its regex-based command system. This guide covers all the available file operations and their advanced usage.


## Basic Operations

### Delete Files

```bash
# Delete a single file
del file.txt
rm file.txt

# Delete multiple files
del file1.txt,file2.txt
```
::: warning
**Risk:**
Deleting system files using `meine` is **not reversible**. Proceed with caution.
:::

::: tip
**Alternative Commands for `delete`:**
You can also use `rm`, `delete`, `del`, or `d`.
:::


### Copy Files

```bash
# Copy a single file
copy source.txt to destination/
cp source.txt destination/

# Copy multiple files
copy file1.txt,file2.txt to backup/
```
::: tip
**Alternative Commands for `copy`:**
You can also use `cp` or `c` as alternatives to `copy`.
:::

### Move Files

```bash
# Move a single file
move old.txt to new/location/
mv old.txt to new/location/

# Move multiple files
mv file1.txt,file2.txt to archive/
```
::: tip
**Alternative Commands for `move`:**
You can also use `mv` or `m` as alternatives to `move`.
:::


### Rename Files

```bash
# Rename a single file
rename oldname.txt as newname.txt
rn document.txt to report.txt

# Rename multiple files
rn old1.txt,old2.py as new1.txt,new2.py
rename old1.txt as new1
```
::: tip
**Alternative Command for `rename`:**
You can also use `rn`.

You can rename files with or without including the file extension in the `new name`.
:::



### Others

```bash
# show the file content in the output console
show file1.txt

#clear the file content
clr file1.txt

```
::: warning
**Binary Files Not Supported:**
The show commands do not support binary files.
:::

::: tip
**Quick Access:**
You can use the text area to view by clicking them directly in the directory tree.
:::

::: info
**Upcoming Feature:**
File editing will be available in future updates.
:::


## Additional Instructions

- Always use **single quotes** for filenames that contain spaces.

    **Example:** `move 'high school' to documents`

- Do **not** change the directory while a process is running.
  This may cause errors—whether you're using the `cd` command or navigating through the directory tree.

- When handling multiple files, if an error occurs partway through, the operations are performed up to the error point.

    For example, if you move `files A, B, and C` to `folder D` and **file B is not found**, file A will be moved `successfully without any notification`.
::: info
**Upcoming Feature:**
These limitations will be addressed in future updates.
:::

