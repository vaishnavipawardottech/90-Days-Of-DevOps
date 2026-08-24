# Day 24 – Advanced Git Notes

## Task 1: Git Merge

### What is a fast-forward merge?

A fast-forward merge happens when the target branch has not moved forward since the feature branch was created. Git can simply move the target branch pointer forward to the latest commit of the feature branch.

There is no separate merge commit.

### When does Git create a merge commit instead?

Git creates a merge commit when both branches have new commits and their histories have diverged. Git needs to combine the two lines of development.

### What is a merge conflict?

A merge conflict happens when Git cannot automatically combine changes from two branches, usually because the same part of a file was changed differently on both branches.

Git marks the conflicting section and we need to manually choose the correct changes before committing the merge.

---

## Task 2: Git Rebase

### What does rebase actually do to your commits?

Rebase moves the commits from one branch and reapplies them on top of another branch.

The commits are recreated with new commit IDs.

### How is the history different from a merge?

A merge keeps the original branch history and usually creates a merge commit.

A rebase creates a more linear history because the feature commits are placed on top of the latest target branch commits.

### Why should you never rebase commits that have been pushed and shared with others?

Rebase changes commit history and creates new commit IDs. If other people already have the old commits, rebasing can cause history conflicts and make collaboration difficult.

### When would you use rebase vs merge?

I would use rebase when I want to update my local feature branch with the latest changes from `main` and keep the history clean.

I would use merge when I want to preserve the existing branch history and safely combine changes without rewriting shared history.

---

## Task 3: Squash Commit vs Merge Commit

### What does squash merging do?

Squash merging combines all commits from a feature branch into one new commit on the target branch.

The individual feature branch commits are not added to the target branch history.

### When would you use squash merge vs regular merge?

I would use squash merge when a feature branch contains many small or temporary commits and I want one clean commit in `main`.

I would use a regular merge when I want to preserve the complete history of the feature branch.

### What is the trade-off of squashing?

Squashing creates a cleaner and simpler history, but it removes the individual commit history from the target branch.

---

## Task 4: Git Stash

### What is the difference between `git stash pop` and `git stash apply`?

`git stash pop` applies the stashed changes and removes that stash from the stash list.

`git stash apply` applies the stashed changes but keeps the stash in the stash list.

### When would you use stash in a real-world workflow?

I would use `git stash` when I have unfinished changes but need to temporarily switch branches to work on another task, such as an urgent bug fix.

After completing the other task, I can return to my original branch and restore the unfinished work.

---

## Task 5: Cherry Picking

### What does cherry-pick do?

`git cherry-pick` takes a specific commit from another branch and applies that commit to the current branch.

### When would you use cherry-pick in a real project?

I would use cherry-pick when I need one specific fix or change from another branch without merging the entire branch.

For example, a bug fix from a development branch may need to be applied to a production or release branch.

### What can go wrong with cherry-picking?

Cherry-picking can cause merge conflicts if the selected commit changes code that is different in the current branch.

It can also create duplicate changes or make the project history harder to understand if used unnecessarily.
