# Day 27 – GitHub Profile Makeover: Build Your Developer Identity

## Overview

Today I focused on improving my GitHub profile and organizing my repositories to make my GitHub presence more professional and useful as a developer portfolio.

The goal was to make my profile easier for recruiters and other developers to understand by clearly showing:

* Who I am
* What technologies I work with
* What I am currently learning
* My important projects
* My DevOps learning journey
* My best repositories

---

# Task 1 – Audit My Current GitHub Profile

## Profile

GitHub Profile:

```text
https://github.com/vaishnavipawardottech
```

I reviewed my profile as if I were a recruiter or someone seeing my GitHub for the first time.

### Before the makeover

I checked the following:

* Profile picture
* Name
* Bio
* Profile README
* Pinned repositories
* Repository descriptions
* Repository READMEs
* Repository organization
* Public repositories
* Possible exposed secrets

### Observations

My profile already had:

* A profile picture
* A profile README
* Multiple repositories
* Pinned repositories
* Projects related to software development
* My 90 Days of DevOps repository

However, the profile README was very short and did not clearly communicate my current focus.

The previous README mainly described me as a Software Engineering Intern and mentioned TypeScript, React, Node.js and AI.

Since I am now focusing on software engineering as well as DevOps and cloud technologies, I decided to update the profile README to better represent my current skills and learning journey.

---

# Task 2 – Create / Update Profile README

GitHub profile README repository:

```text
vaishnavipawardottech/vaishnavipawardottech
```

I updated the profile README to include:

* Short introduction
* Current learning focus
* Technical skills
* 90 Days of DevOps journey
* Important repositories
* LinkedIn/contact information

---

# Task 3 – Organize My Repositories

I reviewed my existing GitHub repositories and categorized them based on their purpose.

The main categories I focused on were:

```text
90 Days of DevOps
Shell Scripts
Python Scripts
DevOps Notes
Software Development Projects
```

---

## 90 Days of DevOps

Repository:

```text
90-Days-Of-DevOps
```

Purpose:

This repository contains my hands-on learning journey through the 90 Days of DevOps challenge.

Topics include:

* Linux
* Networking
* AWS
* Git
* GitHub
* Shell Scripting
* Git branching
* Git reset and revert
* GitHub CLI
* CI/CD
* Docker
* Other DevOps concepts

The repository is organized by day:

```text
2026/
├── day-01/
├── day-02/
├── day-03/
├── ...
├── day-25/
├── day-26/
└── day-27/
```

I continue adding my daily notes, commands, and practical work to this repository.

---

## Shell Scripts

I organized my shell scripting work from the DevOps learning journey.

Important topics include:

* Shell scripting basics
* Variables
* Conditions
* Loops
* Functions
* Error handling
* Log rotation
* Backup automation
* Log analysis
* Cron jobs

Examples of scripts practiced include:

```text
hello.sh
for_loop.sh
count.sh
countdown.sh
log_rotation.sh
log_analyzer.sh
```

The goal is to maintain reusable shell scripting examples separately from the daily learning notes.

---

## Python Scripts

I identified my Python practice and project work that can be organized into a dedicated repository.

The purpose of this repository is to maintain:

* Python practice scripts
* Automation scripts
* Small projects
* Programming exercises

This makes the Python work easier to find instead of keeping unrelated scripts mixed with other repositories.

---

## DevOps Notes

I organized my DevOps learning notes and command references into topic-based sections.

The planned structure is:

```text
devops-notes/
│
├── README.md
│
├── linux/
├── networking/
├── git/
├── shell-scripting/
└── aws/
```

Important reference files include:

```text
git-commands.md
shell-scripting-cheatsheet.md
linux-notes.md
networking-notes.md
aws-notes.md
```

This repository can be used as a personal DevOps reference while continuing the 90 Days of DevOps journey.

---

# Repository README Checklist

For my important repositories, I checked the following:

* [x] Clear repository name
* [x] One-line repository description
* [x] README.md
* [x] Relevant `.gitignore`
* [x] Clear folder structure
* [x] No unnecessary files
* [x] No exposed credentials or secrets

A good README should make it possible for someone visiting the repository to quickly understand:

```text
What is this project?
        ↓
What technologies were used?
        ↓
What does it do?
        ↓
How can it be run?
```

---

# Task 4 – Pin My Best Repositories

GitHub allows up to six repositories or gists to be pinned to the profile.

I reviewed my repositories and selected repositories that best represent my skills and current learning.

My pinned repositories focus on:

1. Strong software development projects
2. Full-stack development
3. Backend / AI-related work
4. 90 Days of DevOps
5. DevOps / Shell scripting work
6. Another strong project

The goal of the pinned section is to show my best work instead of simply showing random or old repositories.

---

# Task 5 – Clean Up My GitHub

I reviewed my repositories for:

* Empty repositories
* Old practice repositories
* Duplicate repositories
* Unclear repository names
* Repositories without descriptions
* Repositories without proper README files
* Unnecessary forks

For repositories that were no longer useful, I considered archiving or removing them.

For important repositories, I improved the repository description and README.

---

## Secret and Security Check

I also checked my repositories for accidentally exposed sensitive information.

Things I looked for included:

```text
.env
.env.local
API_KEY
SECRET_KEY
PASSWORD
TOKEN
ACCESS_KEY
PRIVATE_KEY
```

I also checked whether `.gitignore` files were configured correctly.

Example:

```gitignore
.env
.env.*
!.env.example

node_modules/
dist/
build/

*.log

__pycache__/
*.pyc

.venv/
venv/
```

Sensitive information such as passwords, API keys, access tokens, and private keys should never be committed to a public repository.

---

# Task 6 – Before and After

## Before Screenshot

The screenshot below shows my GitHub profile before starting the Day 27 makeover.

![GitHub Profile Before](./before-profile.png)

---

## After Screenshot

The screenshot below shows my GitHub profile after completing the makeover.

![GitHub Profile After](./after-profile.png)

---

# Three Main Improvements

## 1. Improved Profile README

### Before

The profile README was very short and mainly mentioned my internship and a few technologies.

### After

The README now explains:

* Who I am
* My development background
* My technical skills
* My current DevOps learning journey
* My important work
* How to connect with me

### Why?

A recruiter should be able to understand my technical background and current focus quickly by looking at my profile.

---

## 2. Organized and Improved Repositories

I reviewed my repositories and focused on:

* Clear names
* Useful descriptions
* Proper README files
* Logical folder structures
* Better organization of DevOps learning work

### Why?

A repository should be understandable without requiring someone to inspect every file.

---

## 3. Improved Pinned Repositories

I selected repositories that better represent my strongest technical work and current learning.

### Why?

The pinned repositories are one of the first sections someone sees when visiting my GitHub profile.

They should represent my best work rather than random or outdated repositories.

---


# Key Learnings

1. A GitHub profile can act as an additional developer portfolio.
2. A profile README should quickly communicate who I am and what I work on.
3. Pinned repositories should represent my strongest work.
4. Repository descriptions and READMEs are important for making projects understandable.
5. Repository names should be clear and descriptive.
6. Organizing repositories by purpose makes a GitHub profile easier to navigate.
7. `.gitignore` is important for preventing accidental commits of sensitive or unnecessary files.
8. API keys, passwords, tokens, and other secrets should never be exposed in public repositories.
9. A clean profile is more useful than a profile overloaded with badges and widgets.
10. My GitHub profile should evolve as my skills and career direction change.

---

GitHub Profile:

```text
https://github.com/vaishnavipawardottech
```

This profile makeover helped me understand that GitHub is not only a place to store code. It can also be used to showcase my skills, projects, learning journey, and developer identity.
