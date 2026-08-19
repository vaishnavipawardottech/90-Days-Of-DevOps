# Day 16 – Shell Scripting Basics

## Task 1: Your First Script

### `hello.sh`

```bash
#!/bin/bash

echo "Hello, DevOps!"
```

### Run

```bash
chmod 774 hello.sh
./hello.sh
```

### Output

```text
Hello, DevOps!
```

### What happens if the shebang is removed?

```text
Without the shebang, the script does not explicitly specify which shell/interpreter should execute it.
When run directly with ./hello.sh, this can cause an interpreter-related error or unexpected behavior.
```

---

## Task 2: Variables

### `variables.sh`

```bash
#!/bin/bash

NAME="Vaishnavi"
ROLE="DevOps Engineer"

echo "Hello, I am $NAME and I am a $ROLE"
```

### Run

```bash
chmod 774 variables.sh
./variables.sh
```

### Output

```text
Hello, I am Vaishnavi and I am a DevOps Engineer
```

### Single Quotes vs Double Quotes

```bash
NAME="Vaishnavi"

echo 'Hello $NAME'
echo "Hello $NAME"
```

### Output

```text
Hello $NAME
Hello Vaishnavi
```

**Key difference:**

* Single quotes `' '` → variables are not expanded.
* Double quotes `" "` → variables are expanded.

---

## Task 3: User Input with `read`

### `greet.sh`

```bash
#!/bin/bash

read -p "Enter your name: " NAME
read -p "Enter your favourite tool: " TOOL

echo "Hello $NAME, your favourite tool is $TOOL"
```

### Run

```bash
chmod 774 greet.sh
./greet.sh
```

### Output

```text
Enter your name: Vaishnavi
Enter your favourite tool: Docker
Hello Vaishnavi, your favourite tool is Docker
```

---

## Task 4: If-Else Conditions

### `check_number.sh`

```bash
#!/bin/bash

read -p "Enter a number: " NUMBER

if [ "$NUMBER" -gt 0 ]; then
    echo "Positive"
elif [ "$NUMBER" -lt 0 ]; then
    echo "Negative"
else
    echo "Zero"
fi
```

### Output

```text
Enter a number: 10
Positive
```

---

### `file_check.sh`

```bash
#!/bin/bash

read -p "Enter filename: " FILE

if [ -f "$FILE" ]; then
    echo "File exists."
else
    echo "File does not exist."
fi
```

### Output

```text
Enter filename: devops.txt
File exists.
```

---

## Task 5: Combine It All

### `server_check.sh`

```bash
#!/bin/bash

SERVICE="nginx"

read -p "Do you want to check the status? (y/n): " CHOICE

if [ "$CHOICE" = "y" ]; then
    if systemctl is-active --quiet "$SERVICE"; then
        echo "$SERVICE is active."
    else
        echo "$SERVICE is not active."
    fi
elif [ "$CHOICE" = "n" ]; then
    echo "Skipped."
else
    echo "Invalid choice."
fi
```

### Run

```bash
chmod 774 server_check.sh
./server_check.sh
```

### Output – Service Active

```text
Do you want to check the status? (y/n): y
nginx is active.
```

### Output – Service Not Active

```text
Do you want to check the status? (y/n): y
nginx is not active.
```

### Output – Skipped

```text
Do you want to check the status? (y/n): n
Skipped.
```

---

# What I Learned

1. **Shebang** (`#!/bin/bash`) specifies that the script should be executed using Bash.
2. **Variables and user input** can be handled using variable assignment, `echo`, and `read`.
3. **Conditions** use `if`, `elif`, `else`, and tests such as `-f`, `-gt`, and `-lt` to make decisions in scripts.

# Useful Syntax

```bash
# Variable
NAME="Vaishnavi"

# Print
echo "$NAME"

# User input
read -p "Enter name: " NAME

# If-else
if [ condition ]; then
    # commands
elif [ condition ]; then
    # commands
else
    # commands
fi

# File exists
[ -f "$FILE" ]

# Make script executable
chmod 774 script.sh

# Run script
./script.sh
```
