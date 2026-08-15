# Day 10 – File Permissions & File Operations Challenge

## Objective

The goal of this challenge was to practice basic Linux file operations and understand how file and directory permissions work using `chmod`.

## Files Created

The following files and directory were created:

* `devops.txt` – Empty file created using `touch`
* `notes.txt` – Text file created using `cat`
* `script.sh` – Shell script created using `vim`
* `project/` – Directory created for permission practice


## Permission Changes

### `script.sh`

Initially, the script did not have execute permission.

```bash
chmod +x script.sh
```

After changing the permission, the script was executed using:

```bash
./script.sh
```

Output:

```text
Hello DevOps
```

### `devops.txt`

Write permission was removed from the file:

```bash
chmod -w devops.txt
```

The file became read-only.

Attempting to write to it resulted in:

```text
Permission denied
```

### `notes.txt`

The file was changed to permission `640`:

```bash
chmod 640 notes.txt
```

Permission breakdown:

```text
Owner  = rw- = 6
Group  = r-- = 4
Others = --- = 0
```

Therefore:

```text
640
```

### `project/`

The directory was created with permission `755`:

```bash
mkdir project
chmod 755 project
```

Permission breakdown:

```text
Owner  = rwx = 7
Group  = r-x = 5
Others = r-x = 5
```

Therefore:

```text
755
```

## Permission Testing

### Testing Read-Only File

Command:

```bash
echo "Testing permissions" > devops.txt
```

Result:

```text
Permission denied
```

This happened because write permission was removed from `devops.txt`.

### Testing Execute Permission

Execute permission was removed from `script.sh`:

```bash
chmod -x script.sh
```

Running the script:

```bash
./script.sh
```

resulted in:

```text
Permission denied
```

Execute permission was then restored:

```bash
chmod +x script.sh
```

## Final Permissions

The final permissions were verified using:

```bash
ls -l
```

Expected permission settings:

| File/Directory | Permission | Meaning                                                         |
| -------------- | ---------- | --------------------------------------------------------------- |
| `devops.txt`   | `444`      | Read-only for owner, group and others                           |
| `notes.txt`    | `640`      | Owner can read/write, group can read                            |
| `script.sh`    | `755`      | Owner can read/write/execute, group and others can read/execute |
| `project/`     | `755`      | Owner has full access, group and others can read/execute        |

## Commands Used

### File Creation

```bash
touch devops.txt

cat > notes.txt

vim script.sh
```

### File Reading

```bash
cat notes.txt

vim -R script.sh

head -n 5 /etc/passwd

tail -n 5 /etc/passwd
```

### Permission Verification

```bash
ls -l

ls -l devops.txt notes.txt script.sh
```

### Modify File Permissions

```bash
chmod +x script.sh

./script.sh

chmod -w devops.txt

chmod 640 notes.txt
```

### Directory Permissions

```bash
mkdir project

chmod 755 project

ls -ld project
```

### Permission Testing

```bash
echo "Testing permissions" > devops.txt

chmod -x script.sh

./script.sh

chmod +x script.sh
```

### Final Verification

```bash
ls -l

ls -ld project
```

## What I Learned

1. Linux uses `r`, `w`, and `x` permissions to control access to files and directories.
2. `chmod` can be used to add, remove, or set specific permissions using symbolic or numeric notation.
3. Execute permission is required to run a script, while write permission is required to modify a file.


Day 10 successfully completed: **File Permissions & File Operations Challenge**.
