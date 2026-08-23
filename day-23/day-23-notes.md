# Day 23 – Git Branching & GitHub Notes

## Task 1: Understanding Branches

### 1. What is a branch in Git?

A branch is a separate line of development in a Git repository. It allows us to work on changes without affecting other branches.

### 2. Why do we use branches instead of committing everything to `main`?

Branches allow us to work on new features, fixes, and experiments separately. This keeps the `main` branch stable.

### 3. What is `HEAD` in Git?

`HEAD` is a pointer that tells Git which branch or commit we are currently working on.

### 4. What happens to your files when you switch branches?

Git updates the files in the working directory to match the selected branch. Changes that exist only on one branch may appear or disappear when switching branches.

---

## Task 3: Push to GitHub

### What is the difference between `origin` and `upstream`?

`origin` is usually the name given to the remote repository that we cloned or connected our local repository to.

`upstream` usually refers to the original repository from which a fork was created.

---

## Task 4: Pull from GitHub

### What is the difference between `git fetch` and `git pull`?

`git fetch` downloads the latest changes from the remote repository but does not apply them to the current branch.

`git pull` downloads the changes and also integrates them into the current branch.

---

## Task 5: Clone vs Fork

### What is the difference between clone and fork?

**Clone** copies a repository from GitHub to our local machine.

**Fork** creates our own copy of another user's repository on GitHub.

### When would you clone vs fork?

We clone a repository when we want to work with an existing repository locally.

We fork a repository when we want our own GitHub copy, usually to make changes without directly modifying the original repository.

### After forking, how do you keep your fork in sync with the original repo?

We can add the original repository as an `upstream` remote and fetch changes from it.

Example:

```bash
git remote add upstream <original-repository-url>
git fetch upstream
git merge upstream/main
```
