# Day 20 – Bash Scripting Challenge: Log Analyzer and Report Generator

## Task

The goal of this task is to create a Bash script that analyzes a log file and generates a daily summary report.

The script will:

* Accept a log file as an argument
* Validate the input file
* Count errors
* Find critical events with line numbers
* Find the top 5 most common error messages
* Generate a summary report
* Optionally archive the processed log file

---

# 1. Create the Working Directory

```bash
mkdir day-20
cd day-20
```

Create the required files:

```bash
touch log_analyzer.sh
touch sample_log.log
```

Give execute permission to the script:

```bash
chmod +x log_analyzer.sh
```

---

# 2. Create Sample Log File

Create sample log entries:

```bash
vim sample_log.log
```

Add the following content:

```text
2026-08-21 09:00:01 INFO Server started successfully
2026-08-21 09:01:12 INFO User login successful
2026-08-21 09:02:15 ERROR Connection timed out
2026-08-21 09:03:20 INFO Processing request
2026-08-21 09:04:10 ERROR File not found
2026-08-21 09:05:33 WARNING High memory usage
2026-08-21 09:06:45 ERROR Connection timed out
2026-08-21 09:07:12 CRITICAL Disk space below threshold
2026-08-21 09:08:01 INFO Backup started
2026-08-21 09:09:22 ERROR Permission denied
2026-08-21 09:10:15 ERROR Connection timed out
2026-08-21 09:11:30 INFO Backup completed
2026-08-21 09:12:45 ERROR File not found
2026-08-21 09:13:20 CRITICAL Database connection lost
2026-08-21 09:14:11 ERROR Permission denied
2026-08-21 09:15:00 INFO Server health check completed
2026-08-21 09:16:23 ERROR Connection timed out
2026-08-21 09:17:40 ERROR File not found
2026-08-21 09:18:55 WARNING CPU usage high
2026-08-21 09:19:10 ERROR Connection timed out
```

Check the file:

```bash
cat sample_log.log
```

---

# 3. Create the Bash Script

Open the script:

```bash
vim log_analyzer.sh
```

Add the following code:

```bash
#!/bin/bash

# Check if log file argument is provided
if [ $# -eq 0 ]; then
    echo "Error: Please provide a log file."
    echo "Usage: $0 <log_file>"
    exit 1
fi

LOG_FILE=$1

# Check if file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "Error: File '$LOG_FILE' does not exist."
    exit 1
fi

# Get current date
DATE=$(date +%Y-%m-%d)

# Report file name
REPORT="log_report_$DATE.txt"

# Count total lines
TOTAL_LINES=$(wc -l < "$LOG_FILE")

# Count ERROR and Failed lines
ERROR_COUNT=$(grep -Ei "ERROR|Failed" "$LOG_FILE" | wc -l)

echo "===== Log Analyzer ====="
echo "Log File: $LOG_FILE"
echo "Total Lines: $TOTAL_LINES"
echo "Total Errors: $ERROR_COUNT"

# Display critical events
echo ""
echo "--- Critical Events ---"

CRITICAL_EVENTS=$(grep -n "CRITICAL" "$LOG_FILE")

if [ -n "$CRITICAL_EVENTS" ]; then
    echo "$CRITICAL_EVENTS"
else
    echo "No critical events found."
fi

# Find top 5 error messages
echo ""
echo "--- Top 5 Error Messages ---"

TOP_ERRORS=$(grep "ERROR" "$LOG_FILE" | \
    sed -E 's/.*ERROR //' | \
    sort | \
    uniq -c | \
    sort -rn | \
    head -5)

echo "$TOP_ERRORS"

# Generate report
{
    echo "========================================"
    echo "         DAILY LOG ANALYSIS REPORT"
    echo "========================================"
    echo ""
    echo "Date of Analysis: $DATE"
    echo "Log File: $LOG_FILE"
    echo "Total Lines Processed: $TOTAL_LINES"
    echo "Total Error Count: $ERROR_COUNT"
    echo ""

    echo "--- Top 5 Error Messages ---"
    echo "$TOP_ERRORS"
    echo ""

    echo "--- Critical Events ---"
    
    if [ -n "$CRITICAL_EVENTS" ]; then
        echo "$CRITICAL_EVENTS"
    else
        echo "No critical events found."
    fi

    echo ""
    echo "========================================"
    echo "Report generated successfully."
    echo "========================================"
} > "$REPORT"

echo ""
echo "Report generated: $REPORT"
```

Save the file and exit Vim.

---

# 4. Understand the Script

## Step 1 – Check Command-Line Argument

```bash
if [ $# -eq 0 ]; then
```

`$#` gives the number of command-line arguments.

For example:

```bash
./log_analyzer.sh sample_log.log
```

Here:

```text
$# = 1
```

If no file is provided, the script displays an error and exits.

---

## Step 2 – Store the Log File

```bash
LOG_FILE=$1
```

`$1` represents the first command-line argument.

So:

```bash
./log_analyzer.sh sample_log.log
```

means:

```text
$1 = sample_log.log
```

---

## Step 3 – Check Whether File Exists

```bash
if [ ! -f "$LOG_FILE" ]; then
```

The `-f` condition checks whether the given path is a regular file.

If the file does not exist, the script exits.

---

# 5. Count Total Lines

```bash
TOTAL_LINES=$(wc -l < "$LOG_FILE")
```

`wc -l` counts the number of lines.

Example:

```bash
wc -l sample_log.log
```

The result is used to store the total number of processed lines.

---

# 6. Count Errors

```bash
ERROR_COUNT=$(grep -Ei "ERROR|Failed" "$LOG_FILE" | wc -l)
```

Here:

* `grep` searches for matching text
* `-E` allows multiple patterns
* `-i` makes the search case-insensitive
* `ERROR|Failed` searches for either `ERROR` or `Failed`
* `wc -l` counts matching lines

Example:

```bash
grep -Ei "ERROR|Failed" sample_log.log
```

---

# 7. Find Critical Events

```bash
grep -n "CRITICAL" "$LOG_FILE"
```

The `-n` option displays the line number along with the matching line.

Example:

```text
8:2026-08-21 09:07:12 CRITICAL Disk space below threshold
14:2026-08-21 09:13:20 CRITICAL Database connection lost
```

The script stores this output in:

```bash
CRITICAL_EVENTS
```

---

# 8. Find Top 5 Error Messages

The script uses:

```bash
grep "ERROR" "$LOG_FILE" | \
    sed -E 's/.*ERROR //' | \
    sort | \
    uniq -c | \
    sort -rn | \
    head -5
```

The commands work together:

### `grep`

Finds lines containing `ERROR`.

### `sed`

Removes everything before `ERROR`.

For example:

```text
2026-08-21 09:02:15 ERROR Connection timed out
```

becomes:

```text
Connection timed out
```

### `sort`

Sorts identical messages together.

### `uniq -c`

Counts repeated messages.

### `sort -rn`

Sorts the counts from highest to lowest.

### `head -5`

Displays only the top 5 messages.

---

# 9. Generate the Report

The report name is created using:

```bash
DATE=$(date +%Y-%m-%d)
REPORT="log_report_$DATE.txt"
```

For example:

```text
log_report_2026-08-21.txt
```

The report is generated using:

```bash
{
    ...
} > "$REPORT"
```

The output inside the braces is redirected into the report file.

---

# 10. Run the Script

First check the files:

```bash
ls
```

Expected:

```text
log_analyzer.sh
sample_log.log
```

Run the script:

```bash
./log_analyzer.sh sample_log.log
```

---

# 11. Expected Console Output

```text
===== Log Analyzer =====
Log File: sample_log.log
Total Lines: 20
Total Errors: 10

--- Critical Events ---
8:2026-08-21 09:07:12 CRITICAL Disk space below threshold
14:2026-08-21 09:13:20 CRITICAL Database connection lost

--- Top 5 Error Messages ---
4 Connection timed out
3 File not found
2 Permission denied

Report generated: log_report_2026-08-21.txt
```

The exact error counts depend on the contents of the log file.

---

# 12. Check Generated Report

List the files:

```bash
ls
```

Expected:

```text
log_analyzer.sh
log_report_2026-08-21.txt
sample_log.log
```

Read the report:

```bash
cat log_report_2026-08-21.txt
```

Expected structure:

```text
========================================
         DAILY LOG ANALYSIS REPORT
========================================

Date of Analysis: 2026-08-21
Log File: sample_log.log
Total Lines Processed: 20
Total Error Count: 10

--- Top 5 Error Messages ---
4 Connection timed out
3 File not found
2 Permission denied

--- Critical Events ---
8:2026-08-21 09:07:12 CRITICAL Disk space below threshold
14:2026-08-21 09:13:20 CRITICAL Database connection lost

========================================
Report generated successfully.
========================================
```

---

# 13. Test Input Validation

## Test 1 – No Argument

Run:

```bash
./log_analyzer.sh
```

Expected:

```text
Error: Please provide a log file.
Usage: ./log_analyzer.sh <log_file>
```

---

## Test 2 – File Does Not Exist

Run:

```bash
./log_analyzer.sh missing.log
```

Expected:

```text
Error: File 'missing.log' does not exist.
```

---

# 14. Optional Task – Archive Processed Logs

After confirming that the analysis works correctly, the script can be extended to archive the processed log.

Add the following at the end of the script:

```bash
mkdir -p archive

mv "$LOG_FILE" archive/

echo "Log file moved to archive/"
```

`mkdir -p` creates the directory only if it does not already exist.

After running the script:

```bash
ls
```

You will see:

```text
archive
log_analyzer.sh
log_report_2026-08-21.txt
```

Check the archive:

```bash
ls archive
```

The processed log file will be inside it.

> **Note:** During initial testing, it is better to keep the archive section commented out so that you can run the script multiple times against the same sample log.

---

# 15. Commands and Tools Used

| Command    | Purpose                               |
| ---------- | ------------------------------------- |
| `grep`     | Search for ERROR, Failed and CRITICAL |
| `wc -l`    | Count lines                           |
| `sed`      | Remove unwanted parts of log messages |
| `sort`     | Sort error messages                   |
| `uniq -c`  | Count repeated messages               |
| `head -5`  | Display top 5 results                 |
| `date`     | Generate report date                  |
| `mkdir -p` | Create archive directory              |
| `mv`       | Move processed log                    |
| `cat`      | Display files                         |
| `chmod`    | Give execute permission               |

---

# 16. What I Learned

### 1. Command-Line Arguments

I learned how Bash scripts can accept input using:

```bash
$1
```

and check the number of arguments using:

```bash
$#
```

### 2. Combining Linux Commands

I learned how commands can be combined using pipes:

```bash
grep | sed | sort | uniq | head
```

This makes it possible to process large amounts of log data using simple Linux commands.

### 3. Automating Log Analysis

I learned how Bash scripting can automate repetitive system administration tasks such as:

* Searching logs
* Counting errors
* Finding critical events
* Generating reports
* Archiving processed files

---

# 17. Final Files

After completing the task, the Day 20 directory contains:

```text
day-20/
├── log_analyzer.sh
├── sample_log.log
└── log_report_2026-08-21.txt
```

If the optional archive task is completed:

```text
day-20/
├── archive/
│   └── sample_log.log
├── log_analyzer.sh
└── log_report_2026-08-21.txt
```

---

