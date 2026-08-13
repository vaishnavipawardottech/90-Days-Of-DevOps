# Day 07 – Linux File System Hierarchy & Scenario-Based Practice

## Objective

Understand the Linux file system hierarchy and practice troubleshooting common real-world scenarios using Linux commands.

---

# Part 1: Linux File System Hierarchy (30 minutes)

## Linux File System Hierarchy

| Directory | Description |
|---|---|
| `/` | The root directory and starting point of the Linux file system. All other directories and files exist under it. |
| `/home` | Contains the home directories of normal users and their personal files. |
| `/root` | The home directory of the root user. It is separate from `/home`. |
| `/etc` | Contains system-wide configuration files used by the operating system and installed services. |
| `/var/log` | Contains system and application log files. It is very important for troubleshooting and monitoring. |
| `/tmp` | Stores temporary files created by applications and users. |
| `/bin` | Contains essential command binaries required for basic system operations. On modern Linux systems, it may be a symbolic link to `/usr/bin`. |
| `/usr/bin` | Contains many user-level executable commands and utilities. |
| `/opt` | Used for optional or third-party software and applications. |

---

## `/` - Root Directory

**What it contains:**  
The root directory is the starting point of the Linux file system. All files and directories exist under `/`.

**Command:**

```bash
ls -l /
```

**I would use this when:** I need to understand the top-level structure of the Linux file system or locate important directories.

---

## `/home` - User Home Directories

**What it contains:**  
`/home` contains the home directories of normal users and their personal files.

**Commands:**

```bash
ls -l /home
ls -la ~
```

**I would use this when:** I need to access user files, personal configurations, or user-specific data.

---

## `/root` - Root User Home Directory

**What it contains:**  
`/root` is the home directory of the root user and is separate from `/home`.

**Command:**

```bash
sudo ls -la /root
```

**I would use this when:** I need to inspect files belonging to the root user while troubleshooting with elevated privileges.

---

## `/etc` - Configuration Files

**What it contains:**  
`/etc` contains system-wide configuration files used by Linux and installed services.

**Commands:**

```bash
ls -l /etc | head -20
cat /etc/hostname
cat /etc/os-release
```

**I would use this when:** I need to inspect or troubleshoot system and service configuration.

---

## `/var/log` - Log Files

**What it contains:**  
`/var/log` contains system and application log files. These logs are very useful for troubleshooting.

**Commands:**

```bash
ls -l /var/log
du -sh /var/log/* 2>/dev/null | sort -h | tail -5
```

**I would use this when:** I need to investigate system errors, application issues, or service failures using logs.

---

## `/tmp` - Temporary Files

**What it contains:**  
`/tmp` is used to store temporary files created by applications and users.

**Command:**

```bash
ls -la /tmp
```

**I would use this when:** I need to work with temporary files during scripts, applications, or troubleshooting.

---

## `/bin` - Essential Command Binaries

**What it contains:**  
`/bin` contains essential Linux command binaries. On modern Linux systems, it may be a symbolic link to `/usr/bin`.

**Command:**

```bash
ls -l /bin | head -20
```

**I would use this when:** I need to understand where essential Linux command binaries are located.

---

## `/usr/bin` - User Command Binaries

**What it contains:**  
`/usr/bin` contains many executable commands and utilities available to users.

**Command:**

```bash
ls -l /usr/bin | head -20
```

**I would use this when:** I need to locate or verify executable commands installed on the system.

---

## `/opt` - Optional Applications

**What it contains:**  
`/opt` is commonly used for optional or third-party applications.

**Command:**

```bash
ls -la /opt
```

**I would use this when:** I need to locate optional or third-party applications installed on the system.

---

## Hands-on Practice

### Find the Largest Log Files

```bash
du -sh /var/log/* 2>/dev/null | sort -h | tail -5
```

This finds and displays the five largest items under `/var/log`.

### Look at a Configuration File

```bash
cat /etc/hostname
```

This displays the hostname of the Linux machine.

### Check the Home Directory

```bash
ls -la ~
```

This displays all files, including hidden files, in my home directory.

---

# Part 2: Scenario-Based Practice (40 minutes)

**Important:** Focus on understanding the **troubleshooting flow**, not memorizing commands. Use the hints!

---

## SOLVED EXAMPLE: Understanding How to Approach Scenarios

**Example Scenario: Check if a Service is Running**

```text
Question: How do you check if the 'nginx' service is running?
```

**My Solution (Step by step):**

**Step 1:** Check service status

```bash
systemctl status nginx
```

**Why this command?** It shows whether the service is active, failed, or stopped.

**Step 2:** If the service is not found, list all services

```bash
systemctl list-units --type=service
```

**Why this command?** It helps identify what services exist and are currently loaded on the system.

**Step 3:** Check if the service is enabled on boot

```bash
systemctl is-enabled nginx
```

**Why this command?** It tells whether nginx is configured to start automatically after a reboot.

**What I learned:** Always check the service status first, then investigate based on what you see.

---

# Now Try These Scenarios Yourself

---

## Scenario 1: Service Not Starting

```text
Question: A web application service called 'myapp' failed to start after a server reboot.
What commands would you run to diagnose the issue?

For practice, I used the 'nginx' service because it is a real
systemd-managed service that can be started, stopped, and investigated.
```

**Hint:**

- First check: Is the service running or failed?
- Then check: What do the logs say?
- Finally check: Is it enabled to start on boot?

**Commands to explore:**

```bash
systemctl status nginx
journalctl -u nginx -n 50
systemctl is-enabled nginx
sudo systemctl start nginx
```

**My Solution (Step by step):**

**Step 1:** Check whether nginx is installed

```bash
nginx -v
```

**Why this command?** It confirms whether nginx is installed on the system.

If nginx is not installed:

```bash
sudo apt update
sudo apt install nginx
```

**Step 2:** Check the service status

```bash
systemctl status nginx
```

**Why this command?** It shows whether nginx is running, stopped, or failed and can provide initial error information.

**Step 3:** Check the service logs

```bash
journalctl -u nginx -n 50
```

**Why this command?** It displays the latest 50 log entries for nginx and helps identify the reason for a service failure.

**Step 4:** Check whether nginx is enabled on boot

```bash
systemctl is-enabled nginx
```

**Why this command?** It tells whether nginx is configured to start automatically when the system boots.

**Step 5:** Start nginx if it is stopped

```bash
sudo systemctl start nginx
```

**Why this command?** It starts the nginx service if it is currently stopped.

**Step 6:** Verify the service status

```bash
systemctl status nginx
```

**Why this command?** It confirms whether nginx started successfully after applying the fix.

**What I learned:** For a service problem, I should first check the status, then inspect the logs, check whether it is enabled on boot, start the service if required, and finally verify the result.

---

## Scenario 2: High CPU Usage

```text
Question: Your manager reports that the application server is slow.
You SSH into the server. What commands would you run to identify
which process is using high CPU?
```

**Hint:**

- Use a command that shows **live** CPU usage.
- Look for processes sorted by CPU percentage.
- Note the PID (Process ID) of the top process.

**Commands to explore:**

```bash
top
ps aux --sort=-%cpu | head -10
```

**My Solution (Step by step):**

**Step 1:** Monitor CPU usage in real time

```bash
top
```

**Why this command?** `top` provides a live view of running processes and their CPU and memory usage.

Press `q` to exit.

**Step 2:** List processes sorted by CPU usage

```bash
ps aux --sort=-%cpu | head -10
```

**Why this command?** It sorts running processes by CPU usage and displays the processes consuming the most CPU.

**Step 3:** Identify the process ID

Look at the `PID` and `%CPU` columns.

Example:

```text
USER       PID   %CPU   %MEM   COMMAND
ubuntu   12345   98.5    0.1   example-process
```

**Why this command?** The PID identifies the specific process that is consuming high CPU.

**Step 4:** Get detailed information about the process

```bash
ps -p <PID> -f
```

**Why this command?** It provides detailed information about the process identified by its PID.

Replace `<PID>` with the actual process ID.

**Step 5:** Create CPU load for practice

Open another terminal and run:

```bash
yes > /dev/null
```

Then, in the first terminal, run:

```bash
ps aux --sort=-%cpu | head -10
```

**Why this command?** It allows me to see the `yes` process consuming CPU and practice identifying a high CPU process.

Find the PID of the `yes` process.

Go back to the terminal running `yes` and press:

```text
Ctrl + C
```

**What I learned:** When a server is slow, I should check CPU usage, identify the process consuming the most CPU, note its PID, and investigate that process further.

---

## Scenario 3: Finding Service Logs

```text
Question: A developer asks: "Where are the logs for the 'docker' service?"
The service is managed by systemd. What commands would you use?

For practice, I used the 'nginx' service because it is available
as a systemd-managed service on my Linux machine.
```

**Hint:**

- systemd services → logs are in journald.
- Command pattern: `journalctl -u <service-name>`.
- Use `-n` to limit the number of lines.
- Use `-f` to follow logs in real time.

**Commands to explore:**

```bash
systemctl status nginx
journalctl -u nginx -n 50
journalctl -u nginx -f
```

**My Solution (Step by step):**

**Step 1:** Check the service status

```bash
systemctl status nginx
```

**Why this command?** It confirms that the service exists and shows its current state.

**Step 2:** View the last 50 lines of logs

```bash
journalctl -u nginx -n 50
```

**Why this command?** It displays the latest 50 log entries generated by the nginx service.

**Step 3:** View logs from the last hour

```bash
journalctl -u nginx --since "1 hour ago"
```

**Why this command?** It helps narrow down logs to a specific time period, which is useful when investigating when an issue occurred.

**Step 4:** Follow logs in real time

```bash
journalctl -u nginx -f
```

**Why this command?** The `-f` option continuously displays new log entries as they are generated, similar to `tail -f`.

Press `Ctrl + C` to stop following the logs.

**What I learned:** For systemd-managed services, `journalctl -u <service>` is useful for finding service-specific logs. I can use `-n` for recent entries and `-f` to monitor logs in real time.

---

## Scenario 4: File Permissions Issue

```text
Question: A script at /home/user/backup.sh is not executing.
When you run it: ./backup.sh
You get: "Permission denied"

What commands would you use to fix this?

For practice, I created a backup.sh script in my home directory.
```

**Hint:**

- First: Check what permissions the file has.
- Understand: Files need `x` (execute) permission to run.
- Fix: Add execute permission with `chmod`.

**My Solution (Step by step):**

**Step 1:** Create a practice directory

```bash
mkdir -p ~/permission-practice
cd ~/permission-practice
```

**Why this command?** It creates a separate directory for practicing file permissions without modifying important system files.

**Step 2:** Create the script

```bash
echo '#!/bin/bash' > backup.sh
echo 'echo "Backup completed successfully."' >> backup.sh
```

**Why this command?** It creates a simple shell script that can be used to practice execute permissions.

**Step 3:** Check the current permissions

```bash
ls -l backup.sh
```

Example:

```text
-rw-r--r-- backup.sh
```

**Why this command?** It allows me to check whether the file has execute permission. The `x` permission is missing in this example.

**Step 4:** Try to execute the script

```bash
./backup.sh
```

Expected result:

```text
Permission denied
```

**Why this command?** It reproduces the permission problem from the scenario.

**Step 5:** Add execute permission

```bash
chmod +x backup.sh
```

**Why this command?** It adds execute permission to the script so it can be executed.

**Step 6:** Verify the permission

```bash
ls -l backup.sh
```

Example:

```text
-rwxr-xr-x backup.sh
```

**Why this command?** It confirms that the `x` execute permission has been added.

**Step 7:** Run the script again

```bash
./backup.sh
```

Expected output:

```text
Backup completed successfully.
```

**Why this command?** It verifies that the permission issue has been resolved and the script can now execute.

**What I learned:** When I get a `Permission denied` error while running a script, I should first check the file permissions with `ls -l`, add execute permission using `chmod +x` if required, verify the permission, and then run the script again.

---

# Troubleshooting Flow

The main troubleshooting approach I learned today is:

```text
Identify the problem
        ↓
Check the current state
        ↓
Collect information and logs
        ↓
Identify the cause
        ↓
Apply the fix
        ↓
Verify the result
```

---

# Why This Matters in DevOps

- **File System Understanding:** Knowing where configurations, logs, binaries, user files, and temporary files are stored makes Linux troubleshooting faster.
- **Log Troubleshooting:** `/var/log` and `journalctl` are important sources of information when diagnosing application and service failures.
- **Service Management:** `systemctl` helps DevOps engineers check, start, stop, and troubleshoot services.
- **Performance Troubleshooting:** `top` and `ps` help identify processes consuming excessive CPU resources.
- **Permission Troubleshooting:** Understanding Linux permissions and `chmod` helps resolve common script and deployment issues.
- **Production Incidents:** These troubleshooting patterns are useful when investigating service failures, performance problems, log issues, and deployment errors.
- **Automation:** Understanding Linux paths and permissions helps when writing reliable shell scripts and deployment automation.

---

# Summary

Today I learned the Linux file system hierarchy and practiced working with important directories such as `/etc`, `/var/log`, `/home`, `/tmp`, `/usr/bin`, and `/opt`.

I also practiced troubleshooting service failures, identifying high CPU processes, finding systemd service logs, and fixing file permission issues.

The most important concept I learned is to follow a structured troubleshooting process instead of randomly trying commands.

```text
Identify → Investigate → Fix → Verify
```

---

## Submission

1. Navigate to the `day-07/` folder in the repository.
2. Add the `day-07-linux-fs-and-scenarios.md` file.
3. Commit the changes.
4. Push the changes to GitHub.

## Learn in Public

Share your Day 07 progress on LinkedIn:

- Post 2–3 lines about what you learned about the Linux file system.
- Share one troubleshooting scenario you found challenging and how you solved it.
- Optionally share a screenshot of your notes or terminal practice.

Use hashtags:

```text
#90DaysOfDevOps
#DevOpsKaJosh
#TrainWithShubham
```