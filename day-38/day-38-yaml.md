# Day 38 – YAML Basics

## Goal

Understand YAML syntax and structure before working with CI/CD pipelines.

Today I practiced:

* Key-value pairs
* Lists
* Nested objects
* Multi-line strings
* YAML validation
* YAML indentation and syntax errors

---

## Task 1 – Key-Value Pairs

Created `person.yaml` to represent basic information using YAML key-value pairs.

```yaml
name: Vaishnavi Pawar
role: Software Engineer Intern
experience_years: 1
learning: true
```

### Key Points

* YAML uses `key: value` syntax.
* Boolean values can be written as `true` or `false`.
* YAML does not require quotes for simple strings.
* YAML uses indentation with spaces, not tabs.

---

## Task 2 – Lists

Added lists of DevOps tools and hobbies to `person.yaml`.

```yaml
name: Vaishnavi Pawar
role: Software Engineer Intern
experience_years: 1
learning: true

tools:
  - Docker
  - Git
  - GitHub Actions
  - Jenkins
  - Kubernetes

hobbies: [Coding, Learning, Music]
```

### Two Ways to Write Lists

**1. Block format**

```yaml
tools:
  - Docker
  - Git
  - Kubernetes
```

**2. Inline/flow format**

```yaml
hobbies: [Coding, Learning, Music]
```

Block format is generally easier to read when the list contains multiple items.

---

## Task 3 – Nested Objects

Created `server.yaml` using nested keys.

```yaml
server:
  name: dev-server
  ip: 192.168.1.10
  port: 8080

database:
  host: localhost
  name: tasktrack
  credentials:
    user: admin
    password: secret123
```

### Key Points

YAML represents hierarchy using indentation.

Here, `credentials` is nested inside `database`, and `user` and `password` are nested inside `credentials`.

### What Happens With Tabs?

YAML does not allow tabs for indentation.

Using a tab instead of spaces can cause a YAML parsing/validation error.

---

## Task 4 – Multi-line Strings

YAML provides two useful styles for multi-line strings.

### `|` Block Style

Preserves the line breaks.

```yaml
startup_script: |
  echo "Starting application"
  echo "Checking database"
  echo "Application started"
```

Use `|` when the exact line structure should be preserved, such as shell scripts or configuration blocks.

### `>` Fold Style

Folds multiple lines into a single line when parsed.

```yaml
startup_script: >
  This is a long message
  that is written across
  multiple lines.
```

Use `>` when the text is easier to read across multiple lines but should logically be treated as one line.

### Quick Difference

```text
|  → preserves newlines
>  → folds newlines into spaces
```

---

## Task 5 – Validate YAML

YAML files should be validated before using them in applications or CI/CD pipelines.

Used `yamllint` to check the YAML syntax.

```bash
yamllint person.yaml
yamllint server.yaml
```

If there are no syntax errors, the files pass YAML parsing/validation.

### Intentionally Broken Indentation

For example:

```yaml
server:
  name: dev-server
   ip: 192.168.1.10
```

The incorrect indentation causes a YAML syntax/indentation error.

After correcting the indentation:

```yaml
server:
  name: dev-server
  ip: 192.168.1.10
```

the file can be validated again.

---

## Task 6 – Spot the Difference

### Correct

```yaml
name: devops
tools:
  - docker
  - kubernetes
```

### Broken

```yaml
name: devops
tools:
- docker
  - kubernetes
```

The second block has inconsistent indentation.

`- docker` is not indented under `tools`, while `- kubernetes` is indented.

Correct version:

```yaml
name: devops
tools:
  - docker
  - kubernetes
```

### Key Lesson

YAML depends heavily on indentation. Incorrect indentation can change the structure or make the YAML invalid.

---

## What I Learned

### 1. Indentation Defines Structure

YAML uses spaces to represent hierarchy. Tabs should never be used for indentation.

### 2. YAML Supports Different Data Structures

YAML can represent key-value pairs, lists, nested objects, booleans, and multi-line strings in a simple readable format.

### 3. Validation Is Important

A small indentation or syntax mistake can break a YAML file. Using a validator such as `yamllint` helps identify these errors before using the file in automation or CI/CD pipelines.

---

## Files Created

```text
day-38/
├── day-38-yaml.md
├── person.yaml
└── server.yaml
```
