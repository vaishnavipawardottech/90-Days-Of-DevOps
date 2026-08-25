# Day 26 – GitHub CLI: Manage GitHub from Your Terminal

## Overview

Today I learned about the **GitHub CLI (`gh`)**, which allows me to manage GitHub repositories, issues, pull requests, workflows, releases, and other GitHub features directly from the terminal.

Instead of switching between the terminal and GitHub's web interface, I can perform many GitHub operations using `gh` commands.

---

# Task 1 – Install and Authenticate

## Installation

I checked whether GitHub CLI was installed:

```bash
gh --version
```

If it was not installed, I installed it using:

```bash
sudo apt update
sudo apt install gh -y
```

Then verified the installation:

```bash
gh --version
```

---

## Authentication

I authenticated with GitHub using:

```bash
gh auth login
```

I selected:

* GitHub.com
* HTTPS for Git operations
* Login with a web browser

After authentication, I verified the active account using:

```bash
gh auth status
```

I also tested the GitHub API using:

```bash
gh api user
```

---

## What authentication methods does `gh` support?

GitHub CLI supports several authentication approaches.

The interactive:

```bash
gh auth login
```

command can authenticate through a web browser or other supported methods depending on the environment.

GitHub CLI can also use authentication tokens through environment variables such as:

```bash
GH_TOKEN
```

For automation and CI/CD environments, using a token through an environment variable is useful because an interactive browser login is not possible.

### Important

Authentication credentials should never be committed to a Git repository or written directly into scripts.

---

# Task 2 – Working with Repositories

## Create a repository from the terminal

I created a temporary public repository using:

```bash
gh repo create day-26-gh-cli-test --public --add-readme --clone
```

This command created a public GitHub repository, added a README file, and cloned it locally.

---

## Clone a repository using GitHub CLI

Instead of:

```bash
git clone <repository-url>
```

I can use:

```bash
gh repo clone OWNER/REPOSITORY
```

Example:

```bash
gh repo clone vaishnavipawardottech/90DaysOfDevOps
```

---

## View repository details

I used:

```bash
gh repo view
```

For a specific repository:

```bash
gh repo view OWNER/REPOSITORY
```

I can also request structured information:

```bash
gh repo view --json name,description,isPrivate,url
```

---

## List repositories

I used:

```bash
gh repo list
```

I can also limit the number of repositories displayed:

```bash
gh repo list --limit 20
```

---

## Open a repository in the browser

I used:

```bash
gh repo view --web
```

This opens the repository directly in the browser.

---

## Delete a test repository

I verified the test repository before deleting it:

```bash
gh repo view OWNER/day-26-gh-cli-test
```

Then deleted it:

```bash
gh repo delete OWNER/day-26-gh-cli-test
```

The delete operation must be performed carefully because deleting a repository is destructive.

---

# Task 3 – Issues

## Create an issue

I created an issue using:

```bash
gh issue create \
  --title "Test issue using GitHub CLI" \
  --body "This issue was created from the terminal using GitHub CLI." \
  --label "documentation"
```

The exact label depends on the labels available in the repository.

I can check available labels using:

```bash
gh label list
```

---

## List open issues

```bash
gh issue list
```

or:

```bash
gh issue list --state open
```

---

## View a specific issue

```bash
gh issue view <issue-number>
```

I can also open the issue in the browser:

```bash
gh issue view <issue-number> --web
```

---

## Close an issue

```bash
gh issue close <issue-number>
```

I can then verify the issue status using:

```bash
gh issue list --state all
```

---

## How can `gh issue` be used in automation?

`gh issue` can be useful in automation and monitoring scripts.

For example, if a deployment fails, a script could automatically create an issue:

```bash
gh issue create \
  --title "Deployment failed" \
  --body "The production deployment failed. Please investigate." \
  --label "bug"
```

This can connect monitoring or CI/CD systems with GitHub issue tracking.

---

# Task 4 – Pull Requests

## Create a branch

I created a new branch using:

```bash
git switch -c day-26-gh-cli-pr
```

---

## Make a change

I created a small file:

```bash
echo "GitHub CLI practice" >> day-26-cli.txt
```

Then checked the changes:

```bash
git status
```

---

## Commit the change

```bash
git add day-26-cli.txt
git commit -m "Add GitHub CLI practice"
```

---

## Push the branch

```bash
git push -u origin day-26-gh-cli-pr
```

---

## Create a Pull Request using `gh`

I created the Pull Request directly from the terminal:

```bash
gh pr create --fill
```

I could also provide the details manually:

```bash
gh pr create \
  --base main \
  --head day-26-gh-cli-pr \
  --title "Day 26 GitHub CLI Practice" \
  --body "Practiced creating and managing a pull request using GitHub CLI."
```

---

## List open Pull Requests

```bash
gh pr list
```

---

## View a Pull Request

```bash
gh pr view <pr-number>
```

I can open it in the browser using:

```bash
gh pr view <pr-number> --web
```

---

## Check Pull Request status

I used:

```bash
gh pr checks <pr-number>
```

This shows the status of CI checks associated with the Pull Request.

I can also request structured information:

```bash
gh pr view <pr-number> \
  --json title,state,author,reviewRequests,statusCheckRollup
```

---

## Review someone else's Pull Request

I can first list Pull Requests:

```bash
gh pr list
```

Then view a specific PR:

```bash
gh pr view <pr-number>
```

View the changes:

```bash
gh pr diff <pr-number>
```

Check CI status:

```bash
gh pr checks <pr-number>
```

I can also checkout the PR locally:

```bash
gh pr checkout <pr-number>
```

This allows me to inspect and test someone else's changes locally.

---

## Merge methods supported by `gh pr merge`

`gh pr merge` supports three common merge methods:

### Merge commit

```bash
gh pr merge <pr-number> --merge
```

### Squash merge

```bash
gh pr merge <pr-number> --squash
```

### Rebase merge

```bash
gh pr merge <pr-number> --rebase
```

### Summary

| Method     | Description                          |
| ---------- | ------------------------------------ |
| `--merge`  | Creates a merge commit               |
| `--squash` | Combines PR commits into one commit  |
| `--rebase` | Replays commits onto the base branch |

---

## Merge the Pull Request

After reviewing the PR and checking the CI status, I can merge it using:

```bash
gh pr merge <pr-number>
```

Or explicitly choose a method:

```bash
gh pr merge <pr-number> --squash
```

---

# Task 5 – GitHub Actions & Workflows

## List workflows

I can list workflows in a repository using:

```bash
gh workflow list --repo OWNER/REPOSITORY
```

---

## List workflow runs

```bash
gh run list --repo OWNER/REPOSITORY
```

I can limit the number of results:

```bash
gh run list --repo OWNER/REPOSITORY --limit 10
```

---

## View a workflow run

First I get the run ID using:

```bash
gh run list --repo OWNER/REPOSITORY
```

Then:

```bash
gh run view <run-id> --repo OWNER/REPOSITORY
```

---

## Watch a workflow run

For a workflow that is currently running:

```bash
gh run watch <run-id> --repo OWNER/REPOSITORY
```

---

## How can `gh run` and `gh workflow` help in CI/CD?

GitHub CLI can help DevOps engineers manage CI/CD pipelines directly from the terminal.

For example:

```text
Code Push
    ↓
GitHub Actions
    ↓
Build
    ↓
Test
    ↓
Deploy
    ↓
gh run
    ↓
Check workflow status
```

`gh run` can be used to:

* List recent workflow runs.
* Check whether a workflow succeeded or failed.
* Inspect a particular workflow run.
* Watch a running workflow.

`gh workflow` can be used to:

* List workflows.
* View workflow information.
* Run workflows manually.
* Manage workflow-related operations.

This can be useful in scripts, deployment processes, and CI/CD automation.

---

# Task 6 – Useful `gh` Tricks

## 1. gh api

`gh api` allows me to make requests to the GitHub API directly from the terminal.

Check the authenticated user:

```bash
gh api user
```

Get repository information:

```bash
gh api repos/OWNER/REPOSITORY
```

Use `--jq` to extract selected information:

```bash
gh api repos/OWNER/REPOSITORY \
  --jq '.name, .visibility, .default_branch'
```

This is useful for automation because scripts can interact directly with GitHub's API.

---

# 2. gh gist

Create a Gist:

```bash
echo "GitHub CLI practice" > gist-demo.txt
gh gist create gist-demo.txt --public
```

List Gists:

```bash
gh gist list
```

View a Gist:

```bash
gh gist view <gist-id>
```

Gists are useful for sharing small pieces of code, commands, or notes.

---

# 3. gh release

List releases:

```bash
gh release list
```

View a release:

```bash
gh release view
```

Create a release:

```bash
gh release create v1.0.0 --generate-notes
```

Releases can be used to publish versions of a project.

---

# 4. gh alias

List aliases:

```bash
gh alias list
```

Create an alias:

```bash
gh alias set pv 'pr view'
```

Now I can use:

```bash
gh pv
```

instead of:

```bash
gh pr view
```

Aliases are useful for commands that I use frequently.

---

# 5. gh search repos

Search GitHub repositories:

```bash
gh search repos "devops"
```

Limit the results:

```bash
gh search repos "devops" --limit 10
```

This allows me to search GitHub repositories without opening the website.

---

This makes GitHub CLI a useful tool for DevOps workflows and CI/CD automation.
