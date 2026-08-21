# Shell Scripting Cheat Sheet

A simple and practical Bash Shell Scripting reference for DevOps and Linux practice.

---

# 1. Bash Basics

## Shebang

The shebang tells Linux which interpreter should be used to execute the script.

```bash
#!/bin/bash
```

Example:

```bash
#!/bin/bash

echo "Hello DevOps"
```

---

## Running a Bash Script

Create a script:

```bash
vim script.sh
```

Give execute permission:

```bash
chmod +x script.sh
```

Run it:

```bash
./script.sh
```

You can also run it directly using Bash:

```bash
bash script.sh
```

### Difference

```bash
./script.sh
```

Uses the interpreter specified by the shebang.

```bash
bash script.sh
```

Explicitly runs the script using Bash.

---

## Comments

Comments are ignored by Bash and are used to explain the code.

### Single-line comment

```bash
# This is a comment
echo "Hello"
```

### Inline comment

```bash
echo "Hello"  # Print greeting
```

---

# 2. Variables

Variables store values.

```bash
NAME="Vaishnavi"
AGE=22
```

Use a variable with `$`:

```bash
echo "$NAME"
echo "$AGE"
```

### Important

There should be **no spaces** around `=`.

Correct:

```bash
NAME="DevOps"
```

Wrong:

```bash
NAME = "DevOps"
```

---

## Quoting Variables

### Double quotes

Variables are expanded:

```bash
NAME="Vaishnavi"

echo "$NAME"
```

Output:

```text
Vaishnavi
```

### Single quotes

Variables are not expanded:

```bash
echo '$NAME'
```

Output:

```text
$NAME
```

### Best practice

Use double quotes when using variables:

```bash
echo "$NAME"
```

This also helps when the value contains spaces.

---

# 3. Reading User Input

Use `read` to accept input from the user.

```bash
echo "Enter your name:"
read NAME

echo "Hello $NAME"
```

Short form:

```bash
read -p "Enter your name: " NAME
echo "Hello $NAME"
```

---

# 4. Command-Line Arguments

Arguments are values passed to a script when running it.

Example:

```bash
./script.sh hello devops
```

| Variable | Meaning                         |
| -------- | ------------------------------- |
| `$0`     | Script name                     |
| `$1`     | First argument                  |
| `$2`     | Second argument                 |
| `$#`     | Number of arguments             |
| `$@`     | All arguments                   |
| `$?`     | Exit status of previous command |

Example:

```bash
#!/bin/bash

echo "Script: $0"
echo "First argument: $1"
echo "Second argument: $2"
echo "Number of arguments: $#"
echo "All arguments: $@"
```

Run:

```bash
./script.sh Linux DevOps
```

---

# 5. Operators and Conditionals

## String Comparisons

| Operator | Meaning             |
| -------- | ------------------- |
| `=`      | Equal               |
| `!=`     | Not equal           |
| `-z`     | String is empty     |
| `-n`     | String is not empty |

Example:

```bash
NAME="DevOps"

if [ "$NAME" = "DevOps" ]; then
    echo "Correct"
fi
```

Check if a string is empty:

```bash
if [ -z "$NAME" ]; then
    echo "Name is empty"
fi
```

---

# 6. Integer Comparisons

| Operator | Meaning               |
| -------- | --------------------- |
| `-eq`    | Equal                 |
| `-ne`    | Not equal             |
| `-lt`    | Less than             |
| `-gt`    | Greater than          |
| `-le`    | Less than or equal    |
| `-ge`    | Greater than or equal |

Example:

```bash
AGE=22

if [ "$AGE" -ge 18 ]; then
    echo "Adult"
fi
```

---

# 7. File Test Operators

| Operator | Meaning                      |
| -------- | ---------------------------- |
| `-f`     | Regular file exists          |
| `-d`     | Directory exists             |
| `-e`     | File or directory exists     |
| `-r`     | File is readable             |
| `-w`     | File is writable             |
| `-x`     | File is executable           |
| `-s`     | File exists and is not empty |

Examples:

### Check file

```bash
if [ -f "app.log" ]; then
    echo "File exists"
fi
```

### Check directory

```bash
if [ -d "backup" ]; then
    echo "Directory exists"
fi
```

### Check executable

```bash
if [ -x "script.sh" ]; then
    echo "Script is executable"
fi
```

---

# 8. if, elif and else

Basic syntax:

```bash
if [ condition ]; then
    commands
elif [ condition ]; then
    commands
else
    commands
fi
```

Example:

```bash
AGE=20

if [ "$AGE" -ge 18 ]; then
    echo "Adult"
else
    echo "Minor"
fi
```

Example with `elif`:

```bash
MARKS=75

if [ "$MARKS" -ge 90 ]; then
    echo "Excellent"
elif [ "$MARKS" -ge 60 ]; then
    echo "Good"
else
    echo "Needs improvement"
fi
```

---

# 9. Logical Operators

## AND – `&&`

Run the second command only if the first succeeds.

```bash
mkdir backup && echo "Backup directory created"
```

---

## OR – `||`

Run the second command if the first command fails.

```bash
[ -f app.log ] || echo "File not found"
```

---

## NOT – `!`

Negates a condition.

```bash
if [ ! -f app.log ]; then
    echo "File does not exist"
fi
```

---

# 10. case Statement

`case` is useful when checking multiple possible values.

Syntax:

```bash
case "$variable" in
    value1)
        commands
        ;;
    value2)
        commands
        ;;
    *)
        default commands
        ;;
esac
```

Example:

```bash
read -p "Enter environment: " ENV

case "$ENV" in
    dev)
        echo "Development environment"
        ;;
    test)
        echo "Testing environment"
        ;;
    prod)
        echo "Production environment"
        ;;
    *)
        echo "Unknown environment"
        ;;
esac
```

---

# 11. for Loop

## List-based for loop

```bash
for name in Alice Bob Charlie
do
    echo "Hello $name"
done
```

Short form:

```bash
for name in Alice Bob Charlie; do
    echo "$name"
done
```

---

## C-style for loop

```bash
for ((i=1; i<=5; i++))
do
    echo "$i"
done
```

Output:

```text
1
2
3
4
5
```

---

# 12. while Loop

A `while` loop runs while the condition is true.

```bash
COUNT=1

while [ "$COUNT" -le 5 ]
do
    echo "$COUNT"
    COUNT=$((COUNT + 1))
done
```

---

# 13. until Loop

An `until` loop runs until the condition becomes true.

```bash
COUNT=1

until [ "$COUNT" -gt 5 ]
do
    echo "$COUNT"
    COUNT=$((COUNT + 1))
done
```

---

# 14. break and continue

## break

Stops the loop completely.

```bash
for i in 1 2 3 4 5
do
    if [ "$i" -eq 3 ]; then
        break
    fi

    echo "$i"
done
```

Output:

```text
1
2
```

---

## continue

Skips the current iteration.

```bash
for i in 1 2 3 4 5
do
    if [ "$i" -eq 3 ]; then
        continue
    fi

    echo "$i"
done
```

Output:

```text
1
2
4
5
```

---

# 15. Loop Over Files

To process all `.log` files:

```bash
for file in *.log
do
    echo "Processing $file"
done
```

This is useful when automating log processing.

---

# 16. Loop Over Command Output

Using `while read`:

```bash
cat users.txt | while read line
do
    echo "$line"
done
```

A common pattern is:

```bash
while read line
do
    echo "$line"
done < users.txt
```

---

# 17. Functions

Functions help organize reusable code.

## Define a Function

```bash
greet() {
    echo "Hello DevOps"
}
```

## Call a Function

```bash
greet
```

Complete example:

```bash
#!/bin/bash

greet() {
    echo "Hello DevOps"
}

greet
```

---

# 18. Function Arguments

Function arguments work like script arguments.

```bash
greet() {
    echo "Hello $1"
}

greet "Vaishnavi"
```

Output:

```text
Hello Vaishnavi
```

Example with two arguments:

```bash
add() {
    echo "$1 + $2"
}

add 10 20
```

---

# 19. return vs echo

## echo

Use `echo` when you want to output a value.

```bash
get_name() {
    echo "Vaishnavi"
}

NAME=$(get_name)

echo "$NAME"
```

---

## return

`return` is used to return an exit status from a function.

```bash
check_file() {
    if [ -f "$1" ]; then
        return 0
    else
        return 1
    fi
}
```

Check the result:

```bash
check_file "app.log"

if [ $? -eq 0 ]; then
    echo "File exists"
else
    echo "File does not exist"
fi
```

---

# 20. Local Variables

Use `local` inside functions when the variable should only belong to that function.

```bash
greet() {
    local NAME="Vaishnavi"
    echo "Hello $NAME"
}

greet
```

---

# 21. Text Processing Commands

These commands are very important for DevOps and log analysis.

---

## grep

Search for text or patterns.

```bash
grep "ERROR" app.log
```

### Useful options

| Option | Purpose                      |
| ------ | ---------------------------- |
| `-i`   | Ignore case                  |
| `-r`   | Search recursively           |
| `-c`   | Count matches                |
| `-n`   | Show line number             |
| `-v`   | Invert match                 |
| `-E`   | Extended regular expressions |

Examples:

```bash
grep -i "error" app.log
```

```bash
grep -n "ERROR" app.log
```

```bash
grep -c "ERROR" app.log
```

```bash
grep -v "INFO" app.log
```

---

# 22. awk

`awk` is useful for processing columns and structured text.

Example:

```bash
awk '{print $1}' file.txt
```

Print the first column.

Print multiple columns:

```bash
awk '{print $1, $3}' file.txt
```

### Field separator

For `/etc/passwd`, fields are separated by `:`.

```bash
awk -F: '{print $1}' /etc/passwd
```

### Pattern

```bash
awk '$3 > 80 {print $1}' data.txt
```

### BEGIN and END

```bash
awk 'BEGIN {print "Start"} {print $1} END {print "Done"}' file.txt
```

---

# 23. sed

`sed` is useful for modifying and filtering text.

### Replace text

```bash
sed 's/old/new/g' file.txt
```

### Delete lines

Delete line 2:

```bash
sed '2d' file.txt
```

### In-place edit

```bash
sed -i 's/foo/bar/g' config.txt
```

---

# 24. cut

`cut` extracts parts of lines.

Extract first field separated by `:`:

```bash
cut -d: -f1 /etc/passwd
```

Extract characters:

```bash
cut -c1-5 file.txt
```

---

# 25. sort

Sort lines.

### Alphabetical

```bash
sort names.txt
```

### Numerical

```bash
sort -n numbers.txt
```

### Reverse

```bash
sort -r names.txt
```

### Remove duplicates

```bash
sort -u names.txt
```

---

# 26. uniq

`uniq` removes repeated adjacent lines.

```bash
uniq names.txt
```

Count occurrences:

```bash
uniq -c names.txt
```

Common combination:

```bash
sort names.txt | uniq -c
```

---

# 27. tr

`tr` translates or deletes characters.

Convert lowercase to uppercase:

```bash
echo "hello" | tr 'a-z' 'A-Z'
```

Output:

```text
HELLO
```

Delete spaces:

```bash
echo "Dev Ops" | tr -d ' '
```

Output:

```text
DevOps
```

---

# 28. wc

`wc` counts lines, words and characters.

### Count lines

```bash
wc -l file.txt
```

### Count words

```bash
wc -w file.txt
```

### Count characters

```bash
wc -m file.txt
```

---

# 29. head and tail

## head

Display the first lines.

```bash
head file.txt
```

First 5 lines:

```bash
head -5 file.txt
```

---

## tail

Display the last lines.

```bash
tail file.txt
```

Last 5 lines:

```bash
tail -5 file.txt
```

Follow a log in real time:

```bash
tail -f app.log
```

---

# 30. Useful Pipes

The pipe `|` sends the output of one command to another command.

Example:

```bash
cat app.log | grep "ERROR"
```

Multiple commands:

```bash
grep "ERROR" app.log | sort | uniq -c | sort -rn
```

This is especially useful for log analysis.

---

# 31. Useful One-Liners

## 1. Find files older than 7 days

```bash
find . -type f -mtime +7
```

Delete them:

```bash
find . -type f -mtime +7 -delete
```

---

## 2. Count lines in all `.log` files

```bash
wc -l *.log
```

---

## 3. Replace a string in multiple files

```bash
sed -i 's/old/new/g' *.txt
```

---

## 4. Check if a service is running

```bash
systemctl is-active nginx
```

Or:

```bash
systemctl status nginx
```

---

## 5. Check disk usage

```bash
df -h
```

Check if root disk usage is above 80%:

```bash
df -h / | awk 'NR==2 {print $5}'
```

---

## 6. Monitor logs for errors

```bash
tail -f app.log | grep "ERROR"
```

---

## 7. Count ERROR messages

```bash
grep -c "ERROR" app.log
```

---

## 8. Find the top error messages

```bash
grep "ERROR" app.log | sed -E 's/.*ERROR //' | sort | uniq -c | sort -rn | head -5
```

---

# 32. Exit Codes

Every command returns an exit status.

```bash
echo $?
```

Usually:

```text
0 = Success
Non-zero = Failure
```

Example:

```bash
ls /tmp
echo $?
```

---

## exit 0

Exit successfully:

```bash
exit 0
```

## exit 1

Exit with an error:

```bash
exit 1
```

Example:

```bash
if [ ! -f "$1" ]; then
    echo "File not found"
    exit 1
fi
```

---

# 33. set -e

`set -e` makes the script stop when a command fails.

```bash
#!/bin/bash

set -e

mkdir test
cat missing.txt

echo "This will not run if cat fails"
```

Useful for catching unexpected errors.

---

# 34. set -u

`set -u` treats unset variables as errors.

```bash
#!/bin/bash

set -u

echo "$NAME"
```

If `NAME` was never defined, Bash reports an error.

---

# 35. set -o pipefail

Normally, a pipeline may hide an earlier command's failure.

```bash
set -o pipefail
```

This makes the pipeline return a failure if one of its commands fails.

Example:

```bash
set -o pipefail

cat missing.txt | grep "ERROR"
```

---

# 36. set -x

`set -x` prints commands as Bash executes them.

Useful for debugging.

```bash
#!/bin/bash

set -x

NAME="DevOps"
echo "$NAME"
```

Turn it off:

```bash
set +x
```

---

# 37. trap

`trap` can execute commands when a script exits.

Example:

```bash
cleanup() {
    echo "Cleaning up..."
}

trap cleanup EXIT
```

Now `cleanup` runs when the script exits.

Useful for removing temporary files.

Example:

```bash
#!/bin/bash

TEMP_FILE="temp.txt"

cleanup() {
    rm -f "$TEMP_FILE"
    echo "Temporary file removed"
}

trap cleanup EXIT

touch "$TEMP_FILE"

echo "Working..."
```

---

## Key Takeaways

1. **Bash scripting helps automate repetitive Linux and DevOps tasks.**
2. **Commands like `grep`, `awk`, `sed`, `sort`, and `uniq` are very useful for processing logs and text.**
3. **Conditions, loops, functions, and error handling make scripts more useful and reliable.**
4. **Simple scripts are often enough to automate real system administration tasks.**
