# Day 22 – Git Basics Notes

## 1. What is the difference between `git add` and `git commit`?

`git add` moves the changes from the working directory to the staging area.

`git commit` saves the staged changes permanently in the Git repository with a commit message.

---

## 2. What does the staging area do? Why doesn't Git just commit directly?

The staging area allows us to choose which changes we want to include in the next commit.

This is useful when we have multiple changes but only want to commit some of them.

---

## 3. What information does `git log` show you?

`git log` shows the commit history of the repository.

It displays information such as:

* Commit ID
* Author
* Date
* Commit message

---

## 4. What is the `.git/` folder and what happens if you delete it?

The `.git/` folder contains the internal data and configuration required by Git to manage the repository.

If we delete the `.git/` folder, the project will no longer be a Git repository. The files will remain, but the Git commit history and repository information will be lost.

---

## 5. What is the difference between a working directory, staging area, and repository?

### Working Directory

The actual files where we make changes.

### Staging Area

The place where we prepare/select changes before committing them.

### Repository

The `.git/` directory where Git stores commits, history, and other repository information.

### Git Workflow

```text
Working Directory
       |
    git add
       ↓
Staging Area
       |
   git commit
       ↓
Repository
```
