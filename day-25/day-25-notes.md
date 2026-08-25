# Day 25 – Git Reset vs Revert & Branching Strategies

## Overview

Today I learned how to safely undo mistakes in Git using `git reset` and `git revert`.

I also explored common branching strategies used by software development teams:

* GitFlow
* GitHub Flow
* Trunk-Based Development

The main goal of this task was to understand the difference between rewriting Git history and safely creating a new commit that reverses previous changes.

---

# Task 1 – Git Reset

## Objective

Understand the difference between:

```bash
git reset --soft
git reset --mixed
git reset --hard
```

I created three commits:

```text
Commit A
   ↓
Commit B
   ↓
Commit C
```

---

## 1. git reset --soft

Command used:

```bash
git reset --soft HEAD~1
```

### Observation

`--soft` moves the current branch back by one commit.

The changes from the removed commit are:

* Kept in the working directory
* Kept in the staging area
* Ready to be committed again

I verified this using:

```bash
git status
```

and:

```bash
git diff --cached
```

### Example

Before reset:

```text
A → B → C
```

After:

```text
A → B
```

But the changes from C are still staged.

### When to use

Use `--soft` when I want to remove a commit but keep all its changes staged.

For example, if I made a commit too early and want to modify the commit or create a new commit.

---

## 2. git reset --mixed

Command used:

```bash
git reset --mixed HEAD~1
```

### Observation

`--mixed` also moves the branch back by one commit.

The changes from the removed commit are:

* Kept in the working directory
* Removed from the staging area

I verified this using:

```bash
git status
```

and:

```bash
git diff
```

### Example

Before:

```text
A → B → C
```

After:

```text
A → B
```

The changes from C remain as unstaged changes.

### When to use

Use `--mixed` when I want to undo a commit but keep the changes so I can edit, review, or selectively stage them again.

`--mixed` is also the default behavior of:

```bash
git reset HEAD~1
```

---

## 3. git reset --hard

Command used:

```bash
git reset --hard HEAD~1
```

### Observation

`--hard` moves the branch back and also updates the working directory.

The changes from the removed commit are discarded from the working tree.

### Example

Before:

```text
A → B → C
```

After:

```text
A → B
```

The changes introduced by C are removed from the working directory.

### When to use

Use `--hard` only when I am sure that I do not need the changes being removed.

It can be dangerous because uncommitted changes can be lost.

If something goes wrong, `git reflog` can often help recover previous commit positions.

---

## Difference Between --soft, --mixed and --hard

| Reset Type | Commit History | Staging Area        | Working Directory |
| ---------- | -------------- | ------------------- | ----------------- |
| `--soft`   | Moved back     | Changes kept staged | Changes kept      |
| `--mixed`  | Moved back     | Changes unstaged    | Changes kept      |
| `--hard`   | Moved back     | Changes removed     | Changes removed   |

---

## Which reset is destructive?

`git reset --hard` is the most destructive because it can remove changes from the working directory.

However, `git reset` in general changes the branch history, so it should be used carefully, especially on shared branches.

---

## Should I use git reset on already pushed commits?

Generally, I should avoid using `git reset` on commits that have already been pushed to a shared remote branch.

Reset changes the branch history.

For example:

```text
Remote:

A → B → C
```

After resetting locally:

```text
A → B
```

If I force-push this change, the shared history can be rewritten and other developers may be affected.

For shared or public branches, `git revert` is usually safer.

---

# Task 2 – Git Revert

## Objective

Understand how `git revert` can undo an existing commit without deleting it from Git history.

I created three commits:

```text
Commit X
   ↓
Commit Y
   ↓
Commit Z
```

Then I reverted Commit Y.

Command used:

```bash
git revert <commit-Y-hash>
```

---

## Observation

After reverting Commit Y, Git created a new commit.

The history became:

```text
X → Y → Z → Revert Y
```

Commit Y is still present in the history.

The new revert commit contains changes that reverse the changes introduced by Y.

I checked the history using:

```bash
git log --oneline
```

---

## Is Commit Y still in history?

Yes.

`git revert` does not remove the original commit.

Instead, it creates another commit that undoes the changes.

---

# Git Revert vs Git Reset

## git reset

`git reset` moves the current branch pointer to another commit.

Example:

```text
Before:

A → B → C

After reset:

A → B
```

Commit C is no longer part of the current branch history.

---

## git revert

`git revert` creates a new commit that reverses an earlier commit.

Example:

```text
Before:

A → B → C

After revert:

A → B → C → R
```

`R` is the new revert commit.

---

## Why is revert safer for shared branches?

A shared branch may be used by many developers.

Using reset and force-pushing can rewrite the branch history and cause problems for other developers.

Revert does not rewrite the existing history.

Instead, it adds a new commit.

Therefore:

```text
Shared branch
     ↓
Use git revert
     ↓
Existing history remains
     ↓
New commit reverses the change
```

This makes revert safer for branches such as `main`.

---

## When should I use reset vs revert?

### Use reset when:

* I am working on my local branch.
* The commits have not been pushed.
* I want to clean up local commit history.
* I want to remove or modify recent local commits.

### Use revert when:

* The commit has already been pushed.
* The branch is shared with other developers.
* I want to safely undo a change.
* I want to preserve the existing Git history.

---

# Task 3 – Reset vs Revert Summary

|                                             | `git reset`                               | `git revert`                                         |
| ------------------------------------------- | ----------------------------------------- | ---------------------------------------------------- |
| What it does                                | Moves branch pointer to an earlier commit | Creates a new commit that undoes another commit      |
| Removes commit from current branch history? | Yes, depending on reset target            | No                                                   |
| Creates a new commit?                       | No                                        | Yes                                                  |
| Rewrites history?                           | Yes                                       | No                                                   |
| Safe for shared/pushed branches?            | Usually no                                | Yes                                                  |
| Best use                                    | Local/unpublished commits                 | Shared/pushed commits                                |
| Main risk                                   | Can rewrite history or lose changes       | Usually safer, but conflicts may need to be resolved |

---

# Task 4 – Branching Strategies

## 1. GitFlow

GitFlow uses several types of branches for different stages of development.

Main branches:

* `main`
* `develop`

Supporting branches:

* `feature/*`
* `release/*`
* `hotfix/*`

### Flow

```text
                         feature/login
                              │
                              ↓
main ─────────────── develop ──────────────
                       │
                       │
                       ↓
                  release/1.0
                       │
                       ↓
                     main

hotfix/critical-bug
        │
        ↓
      main
```

### How it works

Developers create feature branches from `develop`.

After completing features, they merge them back into `develop`.

When the project is ready for a release, a release branch is created.

Critical production problems can be fixed using a hotfix branch.

### Where it is used

GitFlow can be useful for projects that have:

* Scheduled releases
* Multiple release versions
* Formal release processes
* Long development cycles

### Advantages

* Clear separation between development and production.
* Good support for scheduled releases.
* Release and hotfix branches provide structure.
* Useful for teams managing multiple versions.

### Disadvantages

* More branches to manage.
* More complex than simpler workflows.
* Can create merge complexity.
* May slow down continuous delivery.

---

# 2. GitHub Flow

GitHub Flow is a simpler branching model.

It mainly uses:

```text
main
feature branch
```

### Flow

```text
main
  │
  ├──── feature/login
  │           │
  │           ↓
  │      Pull Request
  │           │
  │           ↓
  └───────── main
```

### How it works

1. Start from `main`.
2. Create a short-lived feature branch.
3. Make changes and commit them.
4. Push the branch.
5. Create a Pull Request.
6. Review and test the changes.
7. Merge into `main`.
8. Deploy if appropriate.

### Where it is used

GitHub Flow is useful for:

* Web applications
* Continuous delivery
* Small and medium teams
* Projects that deploy frequently

### Advantages

* Simple to understand.
* Fewer branches.
* Easy Pull Request workflow.
* Works well with continuous deployment.
* Less branch management overhead.

### Disadvantages

* Less suitable for complex scheduled release processes.
* Requires good CI/CD and code review practices.
* Long-running features can still create integration problems.

---

# 3. Trunk-Based Development

In Trunk-Based Development, developers integrate changes into the main branch frequently.

The main branch is often called the trunk.

Feature branches, if used, are very short-lived.

### Flow

```text
                 short-lived branch
                       │
                       ↓
main ────●────●───────●────●────●────
                       ↑
                    merge
```

Developers may also commit directly to `main` when the team's process allows it.

### How it works

* Keep branches short-lived.
* Integrate changes frequently.
* Keep `main` in a working state.
* Use automated tests and CI.
* Use feature flags when incomplete features need to be merged safely.

### Where it is used

Trunk-Based Development is commonly associated with:

* Continuous Integration
* Continuous Delivery
* Fast-moving engineering teams
* Large teams with strong automation

### Advantages

* Very frequent integration.
* Reduces long-running branch conflicts.
* Encourages continuous integration.
* Supports fast delivery.
* Keeps the number of active branches low.

### Disadvantages

* Requires strong CI/CD.
* Requires good automated testing.
* Developers need discipline.
* Incomplete features may require feature flags.

---

# Branching Strategy Comparison

| Strategy    | Main Idea                                      | Complexity | Best For                   |
| ----------- | ---------------------------------------------- | ---------- | -------------------------- |
| GitFlow     | Multiple branches for development and releases | High       | Scheduled releases         |
| GitHub Flow | Main + short-lived feature branches            | Low        | Continuous delivery        |
| Trunk-Based | Frequent integration into main                 | Low        | Fast development and CI/CD |

---

# Which strategy would I use for a startup shipping fast?

I would choose **GitHub Flow** or **Trunk-Based Development**.

For a small startup, GitHub Flow is easy to understand and provides a clean Pull Request workflow.

If the team has mature CI/CD and automated testing, Trunk-Based Development can be even faster.

My choice:

```text
Startup
   ↓
GitHub Flow
   ↓
Short-lived feature branches
   ↓
Pull Request
   ↓
Review + CI
   ↓
main
```

---

# Which strategy would I use for a large team with scheduled releases?

I would choose **GitFlow** when the team has scheduled releases and needs separate development, release, and hotfix workflows.

Example:

```text
feature
   ↓
develop
   ↓
release
   ↓
main
```

This gives the release process a clear structure.

---

# Open-Source Project Branching Strategy

For this task, I checked an open-source project on GitHub.

For example, the Kubernetes project uses a development workflow centered around its `main` branch with release branches maintained for released versions.

This demonstrates that large open-source projects may use a combination of trunk-style development and release branches rather than following GitFlow exactly.

The important point is that real projects often adapt their branching model according to their release and development requirements.

---
