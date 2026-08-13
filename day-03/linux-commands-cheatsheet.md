# Day 03 – Linux Commands Cheat Sheet

## 1. Process Management

| Command        | Usage                                                        |
| -------------- | ------------------------------------------------------------ |
| `ps`           | View currently running processes.                            |
| `top`          | Monitor running processes and CPU/memory usage in real time. |
| `htop`         | Interactive view of running processes and system resources.  |
| `kill <PID>`   | Stop a process using its Process ID.                         |
| `pkill <name>` | Stop processes using their name.                             |
| `pgrep <name>` | Find the PID of a process by its name.                       |
| `jobs`         | View processes running in the current terminal.              |
| `bg`           | Resume a stopped process in the background.                  |
| `fg`           | Bring a background process to the foreground.                |

---

## 2. File System

| Command                     | Usage                                                              |
| --------------------------- | ------------------------------------------------------------------ |
| `pwd`                       | Show the current working directory.                                |
| `ls`                        | List files and directories.                                        |
| `ls -la`                    | List all files, including hidden files, with detailed information. |
| `cd <directory>`            | Move to another directory.                                         |
| `mkdir <name>`              | Create a new directory.                                            |
| `touch <file>`              | Create a new empty file.                                           |
| `cp <source> <destination>` | Copy files or directories.                                         |
| `mv <source> <destination>` | Move or rename files and directories.                              |
| `rm <file>`                 | Remove a file.                                                     |
| `rm -rf <directory>`        | Remove a directory and its contents.                               |
| `cat <file>`                | Display the contents of a file.                                    |
| `head <file>`               | Display the first lines of a file.                                 |
| `tail <file>`               | Display the last lines of a file.                                  |
| `grep <text> <file>`        | Search for specific text inside a file.                            |
| `find <path> -name <name>`  | Search for files or directories by name.                           |
| `df -h`                     | Check disk space usage in a readable format.                       |
| `du -sh <directory>`        | Check the size of a directory.                                     |

---

## 3. Networking Troubleshooting

| Command        | Usage                                              |
| -------------- | -------------------------------------------------- |
| `ping <host>`  | Check whether a host is reachable.                 |
| `ip addr`      | Display network interfaces and IP addresses.       |
| `curl <URL>`   | Send requests to a URL and test HTTP connectivity. |
| `dig <domain>` | Look up DNS information for a domain.              |
| `ss`           | Display network connections and listening ports.   |

---

## 4. Service and Log Commands

| Command                       | Usage                          |
| ----------------------------- | ------------------------------ |
| `systemctl status <service>`  | Check the status of a service. |
| `systemctl restart <service>` | Restart a service.             |
| `systemctl stop <service>`    | Stop a running service.        |
| `systemctl start <service>`   | Start a service.               |

---

## Quick Troubleshooting Examples

### Check running processes

```bash
ps
top
```

### Check disk and memory

```bash
df -h
free -h
```

### Check network connectivity

```bash
ping google.com
ip addr
curl https://example.com
```

### Check a service

```bash
systemctl status <service>
```

### Find something in a file

```bash
grep "error" application.log
```

---

### #90DaysOfDevOps