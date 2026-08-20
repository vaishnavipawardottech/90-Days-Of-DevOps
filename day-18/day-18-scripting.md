# Day 18 – Shell Scripting: Functions & Intermediate Concepts

## Task 1: Basic Functions

### `functions.sh`

```bash
#!/bin/bash

greet() {
    local name="$1"
    echo "Hello, $name!"
}

add() {
    local num1="$1"
    local num2="$2"
    local sum=$((num1 + num2))
    echo "Sum: $sum"
}

greet "Vaishnavi"
add 10 20
```

### Output

```text
Hello, Vaishnavi!
Sum: 30
```

---

## Task 2: Functions with Return Values

### `disk_check.sh`

```bash
#!/bin/bash

check_disk() {
    echo "Disk Usage:"
    df -h /
}

check_memory() {
    echo "Memory Usage:"
    free -h
}

echo "===== System Resource Check ====="

check_disk

echo

check_memory
```

### Output

```text
===== System Resource Check =====

Disk Usage:
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        20G  8.0G   12G  40% /

Memory Usage:
               total        used        free      shared  buff/cache   available
Mem:            1.9Gi       500Mi       700Mi       5.0Mi       700Mi       1.3Gi
Swap:              0B          0B          0B
```

> Note: Disk and memory values will vary depending on the EC2 instance.

---

## Task 3: Strict Mode — `set -euo pipefail`

### `strict_demo.sh`

```bash
#!/bin/bash

set -euo pipefail

echo "Script started."

echo "Testing successful command..."
echo "Hello World" | grep "Hello"

echo "Testing failed command..."
false

echo "This line will not execute."
```

### Output

```text
Script started.
Testing successful command...
Hello World
Testing failed command...
```

The script stops when `false` returns a non-zero exit status because of `set -e`.

---

### Testing `set -u`

```bash
#!/bin/bash

set -u

echo "Starting script..."
echo "Value: $UNDEFINED_VARIABLE"
echo "This line will not execute."
```

### Output

```text
Starting script...
./strict_demo.sh: line 4: UNDEFINED_VARIABLE: unbound variable
```

---

### Testing `set -o pipefail`

```bash
#!/bin/bash

set -o pipefail

false | echo "Pipeline command"

echo "Exit status: $?"
```

### Output

```text
Pipeline command
Exit status: 1
```

---

### Strict Mode Summary

```text
set -e          → Exit immediately when a command fails.
set -u          → Treat undefined variables as errors.
set -o pipefail → Make a pipeline fail if any command in the pipeline fails.
```

---

## Task 4: Local Variables

### `local_demo.sh`

```bash
#!/bin/bash

regular_variable() {
    regular_var="I am a regular variable"
    echo "Inside function: $regular_var"
}

local_variable() {
    local local_var="I am a local variable"
    echo "Inside function: $local_var"
}

echo "===== Regular Variable ====="

regular_variable
echo "Outside function: $regular_var"

echo

echo "===== Local Variable ====="

local_variable

if [ -z "${local_var+x}" ]; then
    echo "Outside function: local_var is not available"
else
    echo "Outside function: $local_var"
fi
```

### Output

```text
===== Regular Variable =====
Inside function: I am a regular variable
Outside function: I am a regular variable

===== Local Variable =====
Inside function: I am a local variable
Outside function: local_var is not available
```

---

## Task 5: Build a Script — System Info Reporter

### `system_info.sh`

```bash
#!/bin/bash

set -euo pipefail

print_header() {
    echo
    echo "========================================"
    echo "$1"
    echo "========================================"
}

hostname_os_info() {
    echo "Hostname: $(hostname)"
    echo "OS: $(. /etc/os-release && echo "$PRETTY_NAME")"
    echo "Kernel: $(uname -r)"
}

show_uptime() {
    uptime
}

disk_usage() {
    echo "Top 5 Files/Directories by Size:"
    sudo du -ah / 2>/dev/null | sort -rh | head -n 5
}

memory_usage() {
    free -h
}

top_cpu_processes() {
    ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -n 6
}

main() {
    print_header "HOSTNAME & OS INFORMATION"
    hostname_os_info

    print_header "UPTIME"
    show_uptime

    print_header "TOP 5 DISK USAGE"
    disk_usage

    print_header "MEMORY USAGE"
    memory_usage

    print_header "TOP 5 CPU-CONSUMING PROCESSES"
    top_cpu_processes
}

main
```

### Output

```text
========================================
HOSTNAME & OS INFORMATION
========================================
Hostname: AI-Powered-Devops-vaishnavi
OS: Ubuntu 26.04 LTS
Kernel: 6.x.x-xx-generic

========================================
UPTIME
========================================
12:15:32 up 2 days, 4:21, 1 user, load average: 0.05, 0.03, 0.01

========================================
TOP 5 DISK USAGE
========================================
Top 5 Files/Directories by Size:
4.2G    /
1.8G    /usr
1.1G    /var
850M    /usr/lib
600M    /var/lib

========================================
MEMORY USAGE
========================================
               total        used        free      shared  buff/cache   available
Mem:            1.9Gi       500Mi       700Mi       5.0Mi       700Mi       1.3Gi
Swap:              0B          0B          0B

========================================
TOP 5 CPU-CONSUMING PROCESSES
========================================
    PID COMMAND         %CPU %MEM
   1234 docker          5.2  2.1
    987 nginx           1.4  0.8
    456 systemd         0.5  0.4
    789 sshd            0.2  0.3
    321 bash            0.1  0.2
```

> Note: Hostname, OS version, uptime, disk usage, memory usage, and running processes will vary depending on the EC2 instance.

---

# What I Learned

1. **Functions** make Bash scripts cleaner, reusable, and easier to maintain by grouping related commands together.

2. **Strict mode** using `set -euo pipefail` helps make scripts safer by detecting command failures, undefined variables, and pipeline failures.

3. **Local variables** prevent variables inside functions from unintentionally affecting other parts of the script.

---

# Useful Syntax

```bash
# Define a function
function_name() {
    echo "Hello"
}

# Function with arguments
greet() {
    local name="$1"
    echo "Hello, $name!"
}

greet "Vaishnavi"

# Local variable
my_function() {
    local MY_VAR="value"
    echo "$MY_VAR"
}

# Strict mode
set -euo pipefail

# Return success
return 0

# Return failure
return 1

# Get exit code of last command
echo $?

# Check command result
command && echo "Success"
command || echo "Failed"

# Main function
main() {
    # commands
}

main
```

# Day 18 Summary

Today I practiced writing cleaner and more reusable Bash scripts using **functions, local variables, return values, and strict mode**.

I also built a **System Info Reporter** that collects hostname, OS, uptime, disk usage, memory usage, and top CPU-consuming processes using reusable functions.
