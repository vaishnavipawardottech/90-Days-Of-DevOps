# Day 07 – Linux File System Hierarchy & Scenario-Based Practice

## Objective

Understand the Linux file system hierarchy and practice troubleshooting common real-world scenarios using Linux commands.

---

# Part 1: Linux File System Hierarchy

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


---

# Scenario 1: Service Not Starting

```text
Question: A web application service called 'myapp' failed to start after a server reboot.
What commands would you run to diagnose the issue?
```

**My Solution (Step by step):**

**Step 1:** Check the current status of the service

```bash
systemctl status myapp
```

**Why this command?** It shows whether `myapp` is running, stopped, or failed and may provide an initial error message.

**Step 2:** Check the recent logs of the service

```bash
journalctl -u myapp -n 50
```

**Why this command?** It displays the latest 50 log entries for `myapp`, which can help identify why the service failed to start.

**Step 3:** Check logs from the current boot

```bash
journalctl -u myapp -b
```

**Why this command?** It shows the `myapp` service logs from the current boot, which is useful when the problem occurred after a server restart.

**Step 4:** Check whether the service is enabled on boot

```bash
systemctl is-enabled myapp
```

**Why this command?** It verifies whether `myapp` is configured to start automatically when the server boots.

**Step 5:** Check the service configuration

```bash
systemctl cat myapp
```

**Why this command?** It displays the systemd unit configuration for `myapp`, including the command used to start the application and other service settings.

**Step 6:** Try starting the service manually

```bash
sudo systemctl start myapp
```

**Why this command?** It attempts to start `myapp` and helps determine whether the service can start successfully.

**Step 7:** Verify the service status again

```bash
systemctl status myapp
```

**Why this command?** It confirms whether the service started successfully or is still failing.

**Step 8:** Enable the service if it is not enabled

```bash
sudo systemctl enable myapp
```

**Why this command?** It configures `myapp` to start automatically during future system boots.

**What I learned:** When a service fails after a reboot, I should first check its status, inspect its logs, verify its configuration and boot settings, attempt to start it, and finally verify the result.

---

# Scenario 2: High CPU Usage

```text
Question: Your manager reports that the application server is slow.
You SSH into the server. What commands would you run to identify
which process is using high CPU?
```

**My Solution (Step by step):**

**Step 1:** Check CPU and process usage in real time

```bash
top
```

**Why this command?** It provides a real-time view of system resource usage and running processes, allowing me to identify processes consuming high CPU.

Press `q` to exit.

**Step 2:** List processes sorted by CPU usage

```bash
ps aux --sort=-%cpu | head -10
```

**Why this command?** It sorts processes by CPU utilization and displays the processes consuming the most CPU.

**Step 3:** Identify the PID of the high-CPU process

```bash
ps aux --sort=-%cpu | head -10
```

**Why this command?** The `PID` column identifies the process consuming high CPU, which can then be investigated further.

**Step 4:** Get detailed information about the process

```bash
ps -p <PID> -f
```

**Why this command?** It displays detailed information about the process associated with the identified PID.

Replace `<PID>` with the actual process ID.

**Step 5:** Identify the executable associated with the process

```bash
readlink -f /proc/<PID>/exe
```

**Why this command?** It identifies the executable associated with the process and helps determine which application or service is responsible for the high CPU usage.

Replace `<PID>` with the actual process ID.

**Step 6:** Monitor the specific process

```bash
top -p <PID>
```

**Why this command?** It allows me to monitor the CPU and memory usage of the specific process in real time.

Replace `<PID>` with the actual process ID.

**What I learned:** When an application server is slow, I should first check overall CPU usage, identify the process consuming the most CPU, find its PID, and investigate that specific process further.

---

# Scenario 3: Finding Service Logs

```text
Question: A developer asks: "Where are the logs for the 'docker' service?"
The service is managed by systemd.
What commands would you use?
```

**My Solution (Step by step):**

**Step 1:** Check the status of the Docker service

```bash
systemctl status docker
```

**Why this command?** It confirms whether the Docker service exists and shows its current status along with recent log information.

**Step 2:** View the last 50 lines of Docker logs

```bash
journalctl -u docker -n 50
```

**Why this command?** It displays the most recent 50 log entries generated by the Docker service.

**Step 3:** View Docker logs from the current boot

```bash
journalctl -u docker -b
```

**Why this command?** It displays Docker service logs generated during the current system boot, which is useful when investigating startup or reboot-related issues.

**Step 4:** View Docker logs from a specific time period

```bash
journalctl -u docker --since "1 hour ago"
```

**Why this command?** It limits the output to recent logs and makes it easier to investigate an issue that occurred within a specific time period.

**Step 5:** Follow Docker logs in real time

```bash
journalctl -u docker -f
```

**Why this command?** The `-f` option continuously displays new log entries as they are generated, allowing me to monitor the service in real time.

Press `Ctrl + C` to stop following the logs.

**Step 6:** View Docker error messages

```bash
journalctl -u docker -p err
```

**Why this command?** It filters the Docker service logs to show error-level and more severe messages, making it easier to identify failures.

**What I learned:** For a systemd-managed service, `journalctl -u <service-name>` is the main command for viewing its logs. Options such as `-n`, `-b`, `--since`, `-f`, and `-p` can be used to narrow down and monitor the logs.

---

# Scenario 4: File Permissions Issue

```text
Question: A script at /home/user/backup.sh is not executing.
When you run it: ./backup.sh
You get: "Permission denied"

What commands would you use to fix this?
```

**My Solution (Step by step):**

**Step 1:** Check the current permissions of the script

```bash
ls -l /home/user/backup.sh
```

**Why this command?** It displays the file permissions, owner, and group. I need to check whether the file has the `x` execute permission.

For example:

```text
-rw-r--r-- 1 user user 120 Aug 13 10:00 backup.sh
```

Here, there is no `x` permission, so the script cannot be executed directly.

**Step 2:** Add execute permission

```bash
chmod +x /home/user/backup.sh
```

**Why this command?** It adds execute permission to the script so that it can be run as an executable file.

**Step 3:** Verify the updated permissions

```bash
ls -l /home/user/backup.sh
```

**Why this command?** It confirms that the execute permission has been added.

For example:

```text
-rwxr-xr-x 1 user user 120 Aug 13 10:00 backup.sh
```

The `x` indicates that the file is now executable.

**Step 4:** Run the script

```bash
/home/user/backup.sh
```

**Why this command?** It verifies that the permission issue has been resolved and the script can now execute.

**Step 5:** Run the script from its directory

```bash
cd /home/user
./backup.sh
```

**Why this command?** `./backup.sh` explicitly tells Linux to execute the `backup.sh` file from the current directory.

**What I learned:** When a script returns `Permission denied`, I should check its permissions using `ls -l`, verify whether the execute permission is missing, add it using `chmod +x`, verify the change, and then run the script again.

---

# Troubleshooting Flow

The main troubleshooting approach I learned from these scenarios is:

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

- **Service Troubleshooting:** `systemctl` and `journalctl` help diagnose services that fail to start or stop unexpectedly.
- **Log Analysis:** Service logs provide important information about errors and failures during production incidents.
- **Performance Troubleshooting:** Commands such as `top` and `ps` help identify processes consuming excessive CPU resources.
- **Permission Management:** Understanding Linux permissions helps resolve script execution and deployment problems.
- **Structured Troubleshooting:** Following a consistent flow of checking, investigating, fixing, and verifying helps reduce troubleshooting time during incidents.
- **Production Support:** These commands and troubleshooting patterns are useful when investigating real application and server issues.