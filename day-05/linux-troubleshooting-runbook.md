# Day 05 – Linux Troubleshooting Runbook

## 1. Target Service

**Target Service:** `cron`

The `cron` service was selected as the target service for this troubleshooting drill.

---

## 2. Environment Basics

### 2.1 Check Kernel and System Information

**Command:**

```bash
uname -a
```

**Description:**
Shows information about the Linux kernel and system architecture.

**Output:**

```text
Linux ip-172-31-29-70 7.0.0-1006-aws #6-Ubuntu SMP PREEMPT Tue May 26 12:04:34 UTC 2026 x86_64 GNU/Linux
```

**Observation:**
The system is running Ubuntu Linux with kernel version 7.0.0 on a 64-bit AWS machine.

---

### 2.2 Check Linux Distribution

**Command:**

```bash
cat /etc/os-release
```

**Description:**
Shows information about the Linux distribution and version.

**Output:**

```text
PRETTY_NAME="Ubuntu 26.04 LTS"
NAME="Ubuntu"
VERSION_ID="26.04"
VERSION="26.04 LTS (Resolute Raccoon)"
VERSION_CODENAME=resolute
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=resolute
LOGO=ubuntu-logo

```

**Observation:**
The system is running Ubuntu 26.04 LTS

---

## 3. Filesystem Sanity

### 3.1 Create a Temporary Directory

**Command:**

```bash
mkdir /tmp/runbook-demo
```

**Description:**
Creates a temporary directory for testing filesystem operations.

**Output:**

```text
no output
```

**Observation:**
The temporary directory was created successfully.

---

### 3.2 Copy and Check a File

**Command:**

```bash
cp /etc/hosts /tmp/runbook-demo/hosts-copy && ls -l /tmp/runbook-demo
```

**Description:**
Copies `/etc/hosts` to the temporary directory and verifies the copied file.

**Output:**

```text
-rw-r--r-- 1 ubuntu ubuntu 221 Aug 12 09:49 host-copy
```

**Observation:**
The file was copied successfully and is present in the temporary directory.

---

## 4. CPU and Memory

### 4.1 Check Cron Process CPU and Memory Usage

**Command:**

```bash
pgrep -a cron
```

Then:

```bash
ps -o pid,pcpu,pmem,comm -p <CRON_PID>
```

**Description:**
Checks the CPU and memory usage of the cron process.

**Output:**

```text
    PID %CPU %MEM COMMAND
    587  0.0  0.3 cron
```

**Observation:**
The cron process is using 0.0% CPU and 0.3% memory, indicating very low resource usage.

---

### 4.2 Check Memory Usage

**Command:**

```bash
free -h
```

**Description:**
Shows the system's total, used, free, and available memory.

**Output:**

```text
               total        used        free      shared  buff/cache   available
Mem:           908Mi       309Mi       420Mi       2.7Mi       287Mi       599Mi
Swap:             0B          0B          0B

```

**Observation:**
The system has 599 MiB of available memory, with 309 MiB currently used, indicating sufficient available memory and no obvious memory pressure.

---

## 5. Disk and I/O

### 5.1 Check Disk Usage

**Command:**

```bash
df -h
```

**Description:**
Shows disk space usage for the mounted filesystems.

**Output:**

```text
Filesystem       Size  Used Avail Use% Mounted on
/dev/root        6.7G  2.1G  4.6G  32% /
tmpfs            455M     0  455M   0% /dev/shm
tmpfs            182M  912K  181M   1% /run
efivarfs         128K  3.3K  120K   3% /sys/firmware/efi/efivars
tmpfs            455M  4.0K  455M   1% /tmp
none             1.0M     0  1.0M   0% /run/credentials/systemd-journald.service
none             1.0M     0  1.0M   0% /run/credentials/systemd-resolved.service
/dev/nvme0n1p13  989M   96M  827M  11% /boot
/dev/nvme0n1p15  105M  6.3M   99M   7% /boot/efi
none             1.0M     0  1.0M   0% /run/credentials/systemd-networkd.service
none             1.0M     0  1.0M   0% /run/credentials/getty@tty1.service
none             1.0M     0  1.0M   0% /run/credentials/serial-getty@ttyS0.service
tmpfs             91M  8.0K   91M   1% /run/user/1000

```

**Observation:**
The root filesystem is 32% used with 4.6 GB available, so there is sufficient disk space and no immediate disk-space issue.

---

### 5.2 Check Log Directory Size

**Command:**

```bash
sudo du -sh /var/log
```

**Description:**
Shows the total size of the `/var/log` directory.

**Output:**

```text
18M     /var/log
```

**Observation:**
The /var/log directory is using 18 MB of disk space, which is relatively low and does not indicate a disk-space concern.

---

## 6. Network

### 6.1 Check Listening Ports

**Command:**

```bash
ss -tulpn
```

**Description:**
Shows listening network ports and the processes using them.

**Output:**

```text
Netid                State                 Recv-Q                Send-Q                                   Local Address:Port                               Peer Address:Port               Process
udp                  UNCONN                0                     0                                           127.0.0.54:53                                      0.0.0.0:*
udp                  UNCONN                0                     0                                        127.0.0.53%lo:53                                      0.0.0.0:*
udp                  UNCONN                0                     0                                    172.31.29.70%ens5:68                                      0.0.0.0:*
udp                  UNCONN                0                     0                                            127.0.0.1:323                                     0.0.0.0:*
udp                  UNCONN                0                     0                                                [::1]:323                                        [::]:*
tcp                  LISTEN                0                     4096                                        127.0.0.54:53                                      0.0.0.0:*
tcp                  LISTEN                0                     4096                                           0.0.0.0:22                                      0.0.0.0:*
tcp                  LISTEN                0                     4096                                     127.0.0.53%lo:53                                      0.0.0.0:*
tcp                  LISTEN                0                     4096                                              [::]:22                                         [::]:*

```

**Observation:**
The system has SSH listening on port 22 and DNS services listening on port 53. No unusual listening ports were observed.

---

### 6.2 Check Network Connectivity

**Command:**

```bash
ping -c 4 google.com
```

**Description:**
Checks whether the system can reach Google and shows packet loss and response time.

**Output:**

```text
PING google.com (192.178.155.138) 56(84) bytes of data.
64 bytes from yuiadrs-in-f138.1e100.net (192.178.155.138): icmp_seq=1 ttl=106 time=1.29 ms
64 bytes from yuiadrs-in-f138.1e100.net (192.178.155.138): icmp_seq=2 ttl=106 time=1.29 ms
64 bytes from yuiadrs-in-f138.1e100.net (192.178.155.138): icmp_seq=3 ttl=106 time=1.32 ms
64 bytes from yuiadrs-in-f138.1e100.net (192.178.155.138): icmp_seq=4 ttl=106 time=1.31 ms

--- google.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/mdev = 1.286/1.300/1.318/0.012 ms

```

**Observation:**
The system has successful network connectivity, with all 4 packets received and 0% packet loss. The average response time was 1.30 ms.

---

## 7. Logs

### 7.1 Check Recent Cron Logs

**Command:**

```bash
journalctl -u cron -n 50
```

**Description:**
Shows the latest 50 log entries for the cron service.

**Output:**

```text
Aug 11 09:36:45 ip-172-31-29-70 systemd[1]: Started cron.service - Regular background program processing daemon.
Aug 11 09:36:45 ip-172-31-29-70 (cron)[887]: cron.service: Referenced but unset environment variable evaluates to an empty string: EXTRA_OPTS
Aug 11 09:36:45 ip-172-31-29-70 cron[887]: (CRON) INFO (pidfile fd = 3)
Aug 11 09:36:45 ip-172-31-29-70 cron[887]: (CRON) INFO (Running @reboot jobs)
Aug 11 10:16:31 ip-172-31-29-70 systemd[1]: Stopping cron.service - Regular background program processing daemon...
Aug 11 10:16:31 ip-172-31-29-70 systemd[1]: cron.service: Deactivated successfully.
Aug 11 10:16:31 ip-172-31-29-70 systemd[1]: Stopped cron.service - Regular background program processing daemon.
-- Boot d8ea9c11747a40fea7bcace2d92b9ab9 --
Aug 11 11:49:47 ip-172-31-29-70 systemd[1]: Started cron.service - Regular background program processing daemon.
Aug 11 11:49:47 ip-172-31-29-70 (cron)[582]: cron.service: Referenced but unset environment variable evaluates to an empty string: EXTRA_OPTS
Aug 11 11:49:47 ip-172-31-29-70 cron[582]: (CRON) INFO (pidfile fd = 3)
Aug 11 11:49:47 ip-172-31-29-70 cron[582]: (CRON) INFO (Running @reboot jobs)
Aug 11 12:17:01 ip-172-31-29-70 CRON[1775]: pam_unix(cron:session): session opened for user root(uid=0) by root(uid=0)
Aug 11 12:17:01 ip-172-31-29-70 CRON[1775]: pam_unix(cron:session): session closed for user root
Aug 11 12:30:32 ip-172-31-29-70 systemd[1]: Stopping cron.service - Regular background program processing daemon...
Aug 11 12:30:32 ip-172-31-29-70 systemd[1]: cron.service: Deactivated successfully.
Aug 11 12:30:32 ip-172-31-29-70 systemd[1]: Stopped cron.service - Regular background program processing daemon.
-- Boot a1b279614afe422bb69ad1f6371fda0a --
Aug 12 06:55:47 ip-172-31-29-70 systemd[1]: Started cron.service - Regular background program processing daemon.
Aug 12 06:55:47 ip-172-31-29-70 (cron)[591]: cron.service: Referenced but unset environment variable evaluates to an empty string: EXTRA_OPTS
Aug 12 06:55:47 ip-172-31-29-70 cron[591]: (CRON) INFO (pidfile fd = 3)
Aug 12 06:55:47 ip-172-31-29-70 cron[591]: (CRON) INFO (Running @reboot jobs)
Aug 12 07:01:06 ip-172-31-29-70 systemd[1]: Stopping cron.service - Regular background program processing daemon...
Aug 12 07:01:06 ip-172-31-29-70 systemd[1]: cron.service: Deactivated successfully.
Aug 12 07:01:06 ip-172-31-29-70 systemd[1]: Stopped cron.service - Regular background program processing daemon.
-- Boot f768eba5c7ce49ae848fa894f6a399cb --
Aug 12 09:23:11 ip-172-31-29-70 systemd[1]: Started cron.service - Regular background program processing daemon.
Aug 12 09:23:11 ip-172-31-29-70 (cron)[587]: cron.service: Referenced but unset environment variable evaluates to an empty string: EXTRA_OPTS
Aug 12 09:23:11 ip-172-31-29-70 cron[587]: (CRON) INFO (pidfile fd = 3)
Aug 12 09:23:11 ip-172-31-29-70 cron[587]: (CRON) INFO (Running @reboot jobs)
Aug 12 10:17:01 AI-Powered-Devops-vaishnavi CRON[2097]: pam_unix(cron:session): session opened for user root(uid=0) by root(uid=0)
Aug 12 10:17:01 AI-Powered-Devops-vaishnavi CRON[2099]: (root) CMD (cd / && run-parts --report /etc/cron.hourly)
Aug 12 10:17:01 AI-Powered-Devops-vaishnavi CRON[2097]: pam_unix(cron:session): session closed for user root

```

**Observation:**
The cron service started successfully and is running scheduled jobs. The logs also show regular hourly cron activity, with no critical errors observed.

---

### 7.2 Check Logs from the Last 30 Minutes

**Command:**

```bash
journalctl -u cron --since "30 minutes ago"
```

**Description:**
Shows cron log entries generated during the last 30 minutes.

**Output:**

```text
-- No entries --

```

**Observation:**
No cron log entries were recorded during the last 30 minutes.

---

## 8. Quick Findings

After checking CPU, memory, disk, network, and logs:

* **Service:** `Active and running`
* **CPU:** `The cron process is using 0.0% CPU, indicating very low CPU usage.`
* **Memory:** `The system has 599 MiB of available memory, with no obvious memory pressure.`
* **Disk:** `The root filesystem is 32% used with 4.6 GB available, so sufficient disk space is available.`
* **Network:** `Network connectivity is working with 0% packet loss and an average response time of 1.30 ms.`
* **Logs:** `Cron is running scheduled jobs successfully. An EXTRA_OPTS environment variable warning is present, but no critical errors were observed.`

**Overall Finding:**
The system and cron service are currently healthy. CPU, memory, disk, and network resources are within normal limits, and no critical errors were found in the recent cron logs.

---

## 9. If This Worsens

If the cron service or system health gets worse, I would:

1. **Check the service logs in more detail** to identify the cause of the problem.
2. **Restart the cron service** if it becomes unresponsive and the logs indicate a service issue.
3. **Check CPU, memory, and disk usage again** to determine whether system resource usage is contributing to the problem.

---

## 10. Cleanup

Remove the temporary directory created during the exercise:

```bash
rm -rf /tmp/runbook-demo
```

---

## 11. What I Learned

* How to capture basic system health information.
* How to check CPU, memory, disk, and network usage.
* How to inspect logs for a specific systemd service.
* How to create a simple and repeatable troubleshooting flow.
* The importance of collecting evidence before taking action.

### #90DaysOfDevOps