# Day 09 – Linux User & Group Management Challenge

## Users & Groups Created

### Users
- tokyo
- berlin
- professor
- nairobi

### Groups
- developers
- admins
- project-team

---

## Group Assignments

| User | Groups |
|------|--------|
| tokyo | developers, project-team |
| berlin | developers, admins |
| professor | admins |
| nairobi | project-team |

---

## Directories Created

| Directory | Group Owner | Permissions |
|-----------|-------------|------------|
| /opt/dev-project | developers | 775 (rwxrwxr-x) |
| /opt/team-workspace | project-team | 775 (rwxrwxr-x) |

---

## Commands Used

### User Management

```bash
sudo useradd -m tokyo
sudo useradd -m berlin
sudo useradd -m professor
sudo useradd -m nairobi

sudo passwd tokyo
sudo passwd berlin
sudo passwd professor
sudo passwd nairobi
```

### Group Management

```bash
sudo groupadd developers
sudo groupadd admins
sudo groupadd project-team

sudo usermod -aG developers tokyo
sudo usermod -aG developers,admins berlin
sudo usermod -aG admins professor
sudo usermod -aG project-team nairobi
sudo usermod -aG project-team tokyo
```

### Directory Permissions

```bash
sudo mkdir -p /opt/dev-project
sudo mkdir -p /opt/team-workspace
sudo 
sudo chgrp developers /opt/dev-project
sudo chgrp project-team /opt/team-workspace
sudo 
sudo chmod 775 /opt/dev-project
sudo chmod 775 /opt/team-workspace
```

### Testing

```bash
sudo -u tokyo touch /opt/dev-project/tokyo.txt
sudo -u berlin touch /opt/dev-project/berlin.txt
sudo -u nairobi touch /opt/team-workspace/nairobi.txt

sudo groups tokyo
sudo groups berlin
sudo groups professor
sudo groups nairobi

ls -ld /opt/dev-project
ls -ld /opt/team-workspace
```

---

## What I Learned

1. Created Linux users with home directories and secured them using passwords.
2. Managed primary and supplementary groups using `groupadd` and `usermod -aG`.
3. Configured shared directories with group ownership and `775` permissions to enable team collaboration.

---

## Screenshots Included

- User creation verification
- Group creation verification
- Group membership
- Shared directory permissions and file creation
- Team workspace permissions and testing