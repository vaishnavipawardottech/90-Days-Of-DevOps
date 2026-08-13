# Day 06 – Linux Fundamentals: Read and Write Text Files

## Objective

Practice creating, writing, appending, and reading text files using basic Linux commands.

## Commands and Description

| Command | Description                                                                       |
| ------- | --------------------------------------------------------------------------------- |
| `touch` | Creates a new empty file.                                                         |
| `echo`  | Prints text to the terminal or sends text to another command or file.             |
| `>`     | Writes output to a file and overwrites existing content.                          |
| `>>`    | Appends output to the end of an existing file without overwriting it.             |
| `cat`   | Displays the complete contents of a file.                                         |
| `head`  | Displays the beginning of a file.                                                 |
| `tail`  | Displays the end of a file.                                                       |
| `tee`   | Displays output on the terminal and writes it to a file.                          |
| `-a`    | Appends the output instead of overwriting the file when used with `tee`.          |
| `-n`    | Specifies the number of lines to display with commands such as `head` and `tail`. |

## Commands Practiced

### 1. Create a File

**Command:**

```bash
touch notes.txt
```

**Description:** Creates an empty file named `notes.txt`.

---

### 2. Write Text to a File

**Command:**

```bash
echo "Linux is the foundation of DevOps." > notes.txt
```

**Description:** Writes text to `notes.txt`. The `>` operator overwrites the existing content of the file.

---

### 3. Append Text to a File

**Command:**

```bash
echo "File handling is important for automation." >> notes.txt
```

**Description:** Adds a new line to the end of `notes.txt` without removing the existing content. The `>>` operator is used for appending.

---

### 4. Use `tee` to Write and Display

**Command:**

```bash
echo "Logs and configuration files are commonly text files." | tee -a notes.txt
```

**Description:** Displays the text on the terminal and appends it to `notes.txt`. The `-a` option prevents existing content from being overwritten.

---

### 5. Read the Complete File

**Command:**

```bash
cat notes.txt
```

**Description:** Displays the complete contents of `notes.txt`.

---

### 6. Read the First Two Lines

**Command:**

```bash
head -n 2 notes.txt
```

**Description:** Displays the first two lines of `notes.txt`. The `-n 2` option specifies that two lines should be displayed.

---

### 7. Read the Last Two Lines

**Command:**

```bash
tail -n 2 notes.txt
```

**Description:** Displays the last two lines of `notes.txt`. The `-n 2` option specifies that two lines should be displayed.

## Why It Matters in DevOps

* **Log Management:** DevOps engineers frequently read application and system logs stored as text files.
* **Configuration Management:** Linux configuration files are commonly text-based and need to be read or modified.
* **Automation:** Shell scripts often create, update, and read files as part of automated tasks.
* **Troubleshooting:** Commands such as `cat`, `head`, and `tail` help quickly inspect files and logs.
* **CI/CD and Deployment:** Build and deployment processes often read or write configuration, environment, and log files.