# Day 12 – Revision: Days 01–11

## 1. Linux Basics

### Linux Architecture

```text
Applications
     ↓
Shell
     ↓
Kernel
     ↓
Hardware
```

### Boot Process

```text
BIOS/UEFI
   ↓
Bootloader
   ↓
Kernel
   ↓
systemd
   ↓
Services
   ↓
Login
```

---

## 2. Important Linux Commands

### File & Directory

```bash
ls -la
pwd
cd
mkdir
touch
cp
mv
rm
cat
head
tail
```

### System & Processes

```bash
ps
ps aux
top
free -h
df -h
du -sh
uname -a
```

### Services & Logs

```bash
systemctl status <service>
systemctl start <service>
systemctl stop <service>
systemctl restart <service>

journalctl -u <service>
```

### Networking

```bash
ping google.com
ip addr
ss -tuln
```

---

## 3. File Operations

### Create & Write

```bash
touch file.txt
echo "Hello" > file.txt
echo "New line" >> file.txt
cat file.txt
```

* `>` → overwrite
* `>>` → append

### Read

```bash
cat file.txt
head -n 5 file.txt
tail -n 5 file.txt
```

---

## 4. File Permissions

### Permission Format

```text
rwxrwxrwx
 │   │   │
 │   │   └── Others
 │   └────── Group
 └────────── Owner
```

```text
r = 4
w = 2
x = 1
```

### chmod

```bash
chmod +x script.sh
chmod -x script.sh
chmod -w file.txt
chmod 640 file.txt
chmod 755 directory/
```

---

## 5. File Ownership

### Check Ownership

```bash
ls -l filename
```

Format:

```text
-rw-r--r-- 1 owner group size date filename
```

### Change Owner

```bash
sudo chown user file.txt
```

### Change Group

```bash
sudo chgrp group file.txt
```

### Change Owner + Group

```bash
sudo chown user:group file.txt
```

### Recursive Ownership

```bash
sudo chown -R user:group directory/
```

---

## 6. Users & Groups

### User Commands

```bash
sudo useradd -m username
sudo passwd username
id username
```

### Group Commands

```bash
sudo groupadd groupname
getent group groupname
```

### Add User to Group

```bash
sudo usermod -aG groupname username
```

---

## 7. DevOps Concepts Covered

* Linux architecture
* Linux file system
* Files and directories
* Processes
* Services and `systemd`
* Logs using `journalctl`
* File operations
* File permissions
* Users and groups
* File ownership
* `chmod`
* `chown`
* `chgrp`
* Basic networking
* Linux troubleshooting
* AWS EC2
* SSH
* Nginx
* Docker
* Basic web deployment

---

## 8. Quick Troubleshooting Flow

When something is not working:

```bash
# Check system
uname -a
free -h
df -h

# Check process
ps aux
top

# Check service
systemctl status <service>

# Check logs
journalctl -u <service>

# Check permissions
ls -l

# Check ownership
ls -l filename

# Check network
ping google.com
ss -tuln
```

---

## 9. Mini Self-Check

### 1. Which commands save me the most time?

* `ls -l` → check files, permissions and ownership
* `systemctl status` → check service health
* `journalctl` → troubleshoot service errors

### 2. How do I check if a service is healthy?

```bash
systemctl status <service>
journalctl -u <service>
ps aux | grep <service>
```

### 3. How do I safely change ownership and permissions?

First check the current state:

```bash
ls -l file.txt
```

Then make the required change:

```bash
sudo chown user:group file.txt
chmod 640 file.txt
```

Verify again:

```bash
ls -l file.txt
```

### 4. What should I focus on next?

* Strengthen Linux commands
* Practice troubleshooting
* Improve Git and networking skills
* Continue with AWS and DevOps tools

---


Day 12 completed: **Revision of Days 01–11**.
