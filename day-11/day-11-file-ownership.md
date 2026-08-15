# Day 11 – File Ownership Challenge

## Objective

The goal of this challenge was to understand Linux file and directory ownership and practice changing ownership using `chown` and `chgrp`.

## Files & Directories Created

The following files, directories, users, and groups were used during the challenge:

### Files

* `devops-file.txt`
* `team-notes.txt`
* `project-config.yaml`
* `heist-project/vault/gold.txt`
* `heist-project/plans/strategy.conf`
* `bank-heist/access-codes.txt`
* `bank-heist/blueprints.pdf`
* `bank-heist/escape-plan.txt`

### Directories

* `app-logs/`
* `heist-project/`
* `heist-project/vault/`
* `heist-project/plans/`
* `bank-heist/`

### Users

* `tokyo`
* `berlin`
* `nairobi`
* `professor`

### Groups

* `heist-team`
* `planners`
* `vault-team`
* `tech-team`

## Understanding Ownership

Linux files have an owner and a group.

The output of `ls -l` follows this general format:

```text
-rw-r--r-- 1 owner group size date filename
```

For example:

```text
-rw-r--r-- 1 ubuntu ubuntu 0 Aug 15 12:00 file.txt
```

Here:

* `ubuntu` is the file owner.
* `ubuntu` is the group.
* The owner is the user who owns the file.
* The group represents users who can be given shared access to the file.

## Ownership Changes

### `devops-file.txt`

Initial ownership:

```text
ubuntu:ubuntu
```

Owner changed to `tokyo`:

```bash
sudo chown tokyo devops-file.txt
```

Owner then changed to `berlin`:

```bash
sudo chown berlin devops-file.txt
```

Final ownership:

```text
berlin:ubuntu
```

### `team-notes.txt`

Initial ownership:

```text
ubuntu:ubuntu
```

Group changed to `heist-team`:

```bash
sudo chgrp heist-team team-notes.txt
```

Final ownership:

```text
ubuntu:heist-team
```

### `project-config.yaml`

Owner and group were changed together:

```bash
sudo chown professor:heist-team project-config.yaml
```

Final ownership:

```text
professor:heist-team
```

### `app-logs/`

Owner and group were changed together:

```bash
sudo chown berlin:heist-team app-logs
```

Final ownership:

```text
berlin:heist-team
```

## Recursive Ownership

The following directory structure was created:

```text
heist-project/
├── plans/
│   └── strategy.conf
└── vault/
    └── gold.txt
```

The entire directory structure was assigned to `professor` and the `planners` group using:

```bash
sudo chown -R professor:planners heist-project/
```

The `-R` option applies the ownership change recursively to the directory, its subdirectories, and files.

Final ownership:

```text
heist-project/              → professor:planners
heist-project/plans/        → professor:planners
heist-project/plans/strategy.conf → professor:planners
heist-project/vault/        → professor:planners
heist-project/vault/gold.txt → professor:planners
```


## Commands Used

### Directory Setup

```bash
mkdir -p ~/devops-day11
cd ~/devops-day11
```

### User Management

```bash
id tokyo
id berlin
id nairobi
id professor

sudo useradd -m tokyo
sudo useradd -m berlin
sudo useradd -m nairobi
sudo useradd -m professor
```

### Ownership Verification

```bash
cd ~
ls -l

cd ~/devops-day11
ls -ld .
```

### Basic `chown` Operations

```bash
touch devops-file.txt

ls -l devops-file.txt

sudo chown tokyo devops-file.txt

ls -l devops-file.txt

sudo chown berlin devops-file.txt

ls -l devops-file.txt
```

### Basic `chgrp` Operations

```bash
touch team-notes.txt

ls -l team-notes.txt

sudo groupadd heist-team

getent group heist-team

sudo chgrp heist-team team-notes.txt

ls -l team-notes.txt
```

### Combined Owner and Group Changes

```bash
touch project-config.yaml

ls -l project-config.yaml

sudo chown professor:heist-team project-config.yaml

ls -l project-config.yaml

mkdir app-logs

ls -ld app-logs

sudo chown berlin:heist-team app-logs

ls -ld app-logs
```

### Recursive Ownership

```bash
mkdir -p heist-project/vault
mkdir -p heist-project/plans

touch heist-project/vault/gold.txt
touch heist-project/plans/strategy.conf

ls -lR heist-project/

sudo groupadd planners

getent group planners

sudo chown -R professor:planners heist-project/

ls -lR heist-project/
```

### Practice Challenge

```bash
id tokyo
id berlin
id nairobi

sudo groupadd vault-team
sudo groupadd tech-team

getent group vault-team
getent group tech-team

mkdir bank-heist

touch bank-heist/access-codes.txt
touch bank-heist/blueprints.pdf
touch bank-heist/escape-plan.txt

sudo chown tokyo:vault-team bank-heist/access-codes.txt
sudo chown berlin:tech-team bank-heist/blueprints.pdf
sudo chown nairobi:vault-team bank-heist/escape-plan.txt

ls -l bank-heist/
```

### Final Verification

```bash
ls -l
ls -l bank-heist/
ls -lR heist-project/
```

## What I Learned

1. Linux files and directories have both an owner and a group, which control how access is managed.
2. `chown` changes the owner, while `chgrp` changes the group of a file or directory.
3. The `-R` option with `chown` allows ownership changes to be applied recursively to directories, subdirectories, and files.

## Why File Ownership Matters in DevOps

File ownership is important in real DevOps environments for:

* Application deployments
* Shared team directories
* Container file permissions
* CI/CD pipeline artifacts
* Log file management


Day 11 successfully completed: **File Ownership Challenge (chown & chgrp)**.
