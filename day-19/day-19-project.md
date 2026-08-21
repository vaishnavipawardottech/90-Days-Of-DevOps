# Day 19 – Shell Scripting Project: Log Rotation, Backup & Crontab

## Task 1: Log Rotation Script

### `log_rotate.sh`

```bash
#!/bin/bash

LOG_DIR=$1

if [ ! -d "$LOG_DIR" ]; then
    echo "Error: Directory does not exist."
    exit 1
fi

echo "Starting log rotation..."

COMPRESSED=$(find "$LOG_DIR" -type f -name "*.log" -mtime +7 | wc -l)

find "$LOG_DIR" -type f -name "*.log" -mtime +7 -exec gzip {} \;

DELETED=$(find "$LOG_DIR" -type f -name "*.gz" -mtime +30 | wc -l)

find "$LOG_DIR" -type f -name "*.gz" -mtime +30 -delete

echo "Log rotation completed."
echo "Files compressed: $COMPRESSED"
echo "Files deleted: $DELETED"
```

### Run

```bash
chmod +x log_rotate.sh

mkdir -p ~/day19/logs

touch ~/day19/logs/app.log
touch ~/day19/logs/error.log

./log_rotate.sh ~/day19/logs
```

### Output

```text
Starting log rotation...
Log rotation completed.
Files compressed: 0
Files deleted: 0
```

### Test with an Old Log

```bash
touch ~/day19/logs/old-app.log
touch -d "10 days ago" ~/day19/logs/old-app.log

./log_rotate.sh ~/day19/logs
```

### Output

```text
Starting log rotation...
Log rotation completed.
Files compressed: 1
Files deleted: 0
```

### Verify

```bash
ls -lh ~/day19/logs
```

Expected:

```text
app.log
error.log
old-app.log.gz
```

---

## Task 2: Server Backup Script

### `backup.sh`

```bash
#!/bin/bash

SOURCE=$1
BACKUP_DIR=$2

if [ ! -d "$SOURCE" ]; then
    echo "Error: Source directory does not exist."
    exit 1
fi

mkdir -p "$BACKUP_DIR"

DATE=$(date +%Y-%m-%d)
BACKUP_FILE="$BACKUP_DIR/backup-$DATE.tar.gz"

tar -czf "$BACKUP_FILE" "$SOURCE"

if [ $? -eq 0 ]; then
    echo "Backup created successfully."
    echo "Archive: $BACKUP_FILE"
    echo "Size: $(du -h "$BACKUP_FILE" | cut -f1)"
else
    echo "Backup failed."
    exit 1
fi

find "$BACKUP_DIR" -type f -name "*.tar.gz" -mtime +14 -delete

echo "Old backups deleted."
```

### Run

```bash
chmod +x backup.sh

mkdir -p ~/day19/myapp
mkdir -p ~/day19/backups

echo "Application configuration" > ~/day19/myapp/config.txt
echo "Application data" > ~/day19/myapp/data.txt

./backup.sh ~/day19/myapp ~/day19/backups
```

### Output

```text
Backup created successfully.
Archive: /home/ubuntu/day19/backups/backup-2026-08-21.tar.gz
Size: 4.0K
Old backups deleted.
```

> Note: The path, date, and archive size will be different on your EC2 instance.

### Verify

```bash
ls -lh ~/day19/backups
```

Expected:

```text
backup-2026-08-21.tar.gz
```

### Check Archive Contents

```bash
tar -tzf ~/day19/backups/backup-2026-08-21.tar.gz
```

Expected:

```text
home/ubuntu/day19/myapp/
home/ubuntu/day19/myapp/config.txt
home/ubuntu/day19/myapp/data.txt
```

---

## Task 3: Crontab

### Check Current Cron Jobs

```bash
crontab -l
```

### Output

```text
no crontab for ubuntu
```

> If cron jobs already exist on your system, you will see them instead.

### Cron Syntax

```text
* * * * * command
│ │ │ │ │
│ │ │ │ └── Day of week (0-7)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)
```

### Run Log Rotation Every Day at 2 AM

```cron
0 2 * * * /home/ubuntu/day19/log_rotate.sh /home/ubuntu/day19/logs
```

### Run Backup Every Sunday at 3 AM

```cron
0 3 * * 0 /home/ubuntu/day19/backup.sh /home/ubuntu/day19/myapp /home/ubuntu/day19/backups
```

### Run Health Check Every 5 Minutes

### `health_check.sh`

```bash
#!/bin/bash

echo "Health Check"
echo "Date: $(date)"
echo "Hostname: $(hostname)"
echo "Uptime: $(uptime -p)"
echo "Disk Usage:"
df -h /
echo "Memory Usage:"
free -h
```

### Run

```bash
chmod +x health_check.sh
./health_check.sh
```

### Output

```text
Health Check
Date: Thu Aug 21 14:30:00 IST 2026
Hostname: AI-Powered-Devops-vaishnavi
Uptime: up 2 hours, 15 minutes
Disk Usage:
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        20G  8.0G   12G  40% /

Memory Usage:
               total        used        free      shared  buff/cache   available
Mem:            1.9Gi       500Mi       700Mi       5.0Mi       700Mi       1.3Gi
Swap:              0B          0B          0B
```

> Note: System information will be different on your EC2 instance.

### Cron Entry

```cron
*/5 * * * * /home/ubuntu/day19/health_check.sh
```

> These cron entries are documented for practice. Do not add them to your crontab until you have verified your script paths.

---

## Task 4: Scheduled Maintenance Script

### `maintenance.sh`

```bash
#!/bin/bash

LOG_DIR=$1
SOURCE=$2
BACKUP_DIR=$3

LOG_FILE="$HOME/day19/maintenance.log"

echo "$(date): Starting maintenance..." >> "$LOG_FILE"

echo "$(date): Running log rotation..." >> "$LOG_FILE"

find "$LOG_DIR" -type f -name "*.log" -mtime +7 -exec gzip {} \;

find "$LOG_DIR" -type f -name "*.gz" -mtime +30 -delete

echo "$(date): Log rotation completed." >> "$LOG_FILE"

echo "$(date): Starting backup..." >> "$LOG_FILE"

DATE=$(date +%Y-%m-%d)
BACKUP_FILE="$BACKUP_DIR/backup-$DATE.tar.gz"

mkdir -p "$BACKUP_DIR"

tar -czf "$BACKUP_FILE" "$SOURCE"

if [ $? -eq 0 ]; then
    echo "$(date): Backup completed: $BACKUP_FILE" >> "$LOG_FILE"
else
    echo "$(date): Backup failed." >> "$LOG_FILE"
fi

find "$BACKUP_DIR" -type f -name "*.tar.gz" -mtime +14 -delete

echo "$(date): Maintenance completed." >> "$LOG_FILE"
```

### Run

```bash
chmod +x maintenance.sh

./maintenance.sh \
~/day19/logs \
~/day19/myapp \
~/day19/backups
```

### Check Maintenance Log

```bash
cat ~/day19/maintenance.log
```

### Output

```text
Thu Aug 21 14:40:00 IST 2026: Starting maintenance...
Thu Aug 21 14:40:00 IST 2026: Running log rotation...
Thu Aug 21 14:40:00 IST 2026: Log rotation completed.
Thu Aug 21 14:40:00 IST 2026: Starting backup...
Thu Aug 21 14:40:00 IST 2026: Backup completed: /home/ubuntu/day19/backups/backup-2026-08-21.tar.gz
Thu Aug 21 14:40:00 IST 2026: Maintenance completed.
```

### Cron Entry

Run the maintenance script every day at 1 AM:

```cron
0 1 * * * /home/ubuntu/day19/maintenance.sh /home/ubuntu/day19/logs /home/ubuntu/day19/myapp /home/ubuntu/day19/backups
```

---

# What I Learned

1. **Log rotation** helps manage old log files by compressing logs older than 7 days and deleting compressed logs older than 30 days.

2. **Backup scripts** can automatically create timestamped `.tar.gz` archives and remove backups older than 14 days.

3. **Crontab** allows us to schedule Shell scripts automatically for regular tasks such as backups, log rotation, health checks, and maintenance.

---

# Day 19 Summary

Today I built a Shell Scripting project for basic server maintenance.

I practiced **log rotation, server backups, backup retention, health checks, and cron scheduling**.

This helped me understand how Bash scripts can automate common DevOps tasks instead of performing them manually.
