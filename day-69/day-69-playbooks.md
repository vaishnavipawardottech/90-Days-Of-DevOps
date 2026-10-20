# Day 69 — Ansible Playbooks and Modules

## Overview

Day 69 focuses on Ansible Playbooks and Modules, which help automate server configuration through reusable YAML files.

Ad-hoc commands are useful for quick operations, but playbooks make it possible to define repeatable configuration tasks, such as installing packages, managing services, copying files, and configuring application directories.

### Objectives

- Understand plays, tasks, modules, and handlers.
- Write playbooks to install packages and manage services.
- Practice essential Ansible modules.
- Understand idempotency and handler execution.
- Use check mode, diff mode, and verbosity for troubleshooting.
- Execute multiple plays against different server groups.

---

## Task 1: Your First Playbook

### File: `install-nginx.yml`

```yaml
---
- name: Install and start Nginx on web servers
  hosts: web
  become: true

  tasks:
    - name: Install Nginx
      package:
        name: nginx
        state: present

    - name: Start and enable Nginx
      service:
        name: nginx
        state: started
        enabled: true

    - name: Create a custom index page
      copy:
        content: "<h1>Deployed by Ansible - TerraWeek Server</h1>"
        dest: /usr/share/nginx/html/index.html
        mode: '0644'
```

**Note:** The `package` module is used here to support package management across different Linux distributions. Alternatively, use `apt` for Ubuntu/Debian or `dnf`/`yum` for compatible RPM-based systems.

### Explanation

| Component | Purpose |
|---|---|
| `---` | Marks the beginning of a YAML document. |
| `name` | Describes the play or task. |
| `hosts: web` | Targets hosts belonging to the `web` inventory group. |
| `become: true` | Enables privilege escalation, usually through sudo. |
| `tasks` | Contains the ordered list of operations to execute. |
| `package` | Installs Nginx if it is not already installed. |
| `service` | Starts Nginx and enables it at boot. |
| `copy` | Creates or updates the custom HTML page. |

### Execute the Playbook

Check syntax:

```bash
ansible-playbook install-nginx.yml --syntax-check
```

Preview changes:

```bash
ansible-playbook install-nginx.yml --check --diff
```

Apply the configuration:

```bash
ansible-playbook install-nginx.yml
```

Run it a second time:

```bash
ansible-playbook install-nginx.yml
```

Verify the web server:

```bash
curl http://<WEB_SERVER_PUBLIC_IP>
```

Replace `<WEB_SERVER_PUBLIC_IP>` with the actual public IP address of a managed web server. Ensure the security group permits HTTP traffic on port 80.

### Understanding Idempotency

Idempotency means that repeatedly applying the same desired configuration should not cause additional changes once the system reaches that state.

- `changed`: Ansible made a change to the managed system.
- `ok`: The task completed without requiring a change.
- `failed`: The task encountered an error.

On the second run, tasks that are already in the desired state should generally report `ok`.

---

## Task 2: Understand Playbook Structure

A playbook can contain one or more plays. Each play targets a host group and contains tasks that describe the configuration to apply.

### Play vs Task

| Play | Task |
|---|---|
| Defines which hosts to configure and which tasks to execute. | Represents one individual operation. |
| Contains settings such as `hosts` and `become`. | Uses a module to perform an operation. |
| Can contain multiple tasks. | Executes as part of a play. |

### Can a Playbook Have Multiple Plays?

Yes. A playbook can contain multiple plays that target different inventory groups, such as web servers, application servers, and database servers.

### `become: true` at Play and Task Levels

- **Play level:** Applies privilege escalation to all tasks in that play by default.
- **Task level:** Applies privilege escalation only to the specified task, unless overridden by other applicable configuration.

### What Happens When a Task Fails?

By default, Ansible marks the task as failed and skips subsequent tasks for that host in the same play. Other hosts can continue executing their tasks. Error-handling features such as `block`/`rescue`, `ignore_errors`, and `any_errors_fatal` can change this behavior.

---

## Task 3: Essential Ansible Modules

Create `essential-modules.yml` to practice package management, services, file operations, command execution, and configuration management.

### File: `essential-modules.yml`

```yaml
---
- name: Practice essential Ansible modules
  hosts: all
  become: true

  tasks:
    - name: Install multiple packages
      package:
        name:
          - git
          - curl
          - wget
          - tree
        state: present

    - name: Ensure Nginx is running
      service:
        name: nginx
        state: started
        enabled: true

    - name: Copy application configuration
      copy:
        src: files/app.conf
        dest: /etc/app.conf
        owner: root
        group: root
        mode: '0644'

    - name: Create application directory
      file:
        path: /opt/myapp
        state: directory
        owner: root
        group: root
        mode: '0755'

    - name: Check disk space
      command: df -h
      register: disk_output
      changed_when: false

    - name: Print disk space
      debug:
        var: disk_output.stdout_lines

    - name: Count running processes
      shell: ps aux | wc -l
      register: process_count
      changed_when: false

    - name: Show process count
      debug:
        msg: "Total processes: {{ process_count.stdout }}"

    - name: Set timezone in environment
      lineinfile:
        path: /etc/environment
        line: 'TZ=Asia/Kolkata'
        create: true
```

**Note:** The `service` task assumes Nginx is available on the managed hosts. If it is not installed, install it first. The ownership of `/opt/myapp` is set to root for compatibility with common Linux systems; change it to an existing application user when required.

### Create the Supporting File

Directory structure:

```text
ansible-project/
├── inventory.ini
├── essential-modules.yml
└── files/
    └── app.conf
```

Example `files/app.conf`:

```ini
APP_NAME=myapp
APP_ENV=development
APP_PORT=3000
```

Run the playbook:

```bash
ansible-playbook -i inventory.ini essential-modules.yml --syntax-check
ansible-playbook -i inventory.ini essential-modules.yml --check --diff
ansible-playbook -i inventory.ini essential-modules.yml
```

### Seven Essential Modules

#### 1. `package` — Package Management

Installs or removes software packages.

- `state: present`: Ensures a package is installed.
- `state: absent`: Ensures a package is removed.

#### 2. `service` — Service Management

Starts, stops, restarts, or manages the boot-time status of services.

- `state: started`: Starts the service if it is not running.
- `state: stopped`: Stops the service.
- `state: restarted`: Restarts the service.
- `enabled: true`: Enables the service at boot.

#### 3. `copy` — File Copying

Copies files from the control node to managed hosts or writes inline content to a destination file. It can also set file ownership and permissions.

#### 4. `file` — Files and Directories

Creates, removes, or changes the attributes of files and directories.

- `state: directory`: Ensures a directory exists.
- `mode: '0755'`: Sets the directory permissions.

#### 5. `command` — Command Execution

Executes a command without invoking a shell. Shell operators such as pipes and redirects are not interpreted.

Example:

```yaml
- name: Check disk space
  command: df -h
  register: disk_output
  changed_when: false
```

#### 6. `shell` — Shell Command Execution

Executes commands through a shell, allowing pipes, redirects, and shell expansions.

Example:

```yaml
- name: Count running processes
  shell: ps aux | wc -l
  register: process_count
  changed_when: false
```

Use `shell` only when shell functionality is necessary. Prefer `command` when it can perform the operation.

#### 7. `lineinfile` — Line Management

Adds, replaces, or removes a specific line in a file, making it useful for managing configuration settings without rewriting the entire file.

Example:

```yaml
- name: Set timezone in environment
  lineinfile:
    path: /etc/environment
    line: 'TZ=Asia/Kolkata'
    create: true
```

### Difference Between `command` and `shell`

| `command` | `shell` |
|---|---|
| Executes a command directly without a shell. | Executes a command through a shell. |
| Does not interpret pipes or redirects. | Supports pipes, redirects, and shell expansions. |
| Preferred for straightforward commands. | Used when shell-specific features are required. |
| Usually has fewer shell-related risks. | Requires additional care when handling variable input. |

---

## Task 4: Handlers — Restart Services Only When Needed

Handlers are special tasks that execute when notified by another task. They are commonly used to restart services after a configuration file changes.

### File: `nginx-config.yml`

```yaml
---
- name: Configure Nginx with a custom config
  hosts: web
  become: true

  tasks:
    - name: Install Nginx
      package:
        name: nginx
        state: present

    - name: Deploy Nginx config
      copy:
        src: files/nginx.conf
        dest: /etc/nginx/nginx.conf
        owner: root
        group: root
        mode: '0644'
      notify: Restart Nginx

    - name: Deploy custom index page
      copy:
        content: "<h1>Managed by Ansible</h1><p>Server: {{ inventory_hostname }}</p>"
        dest: /usr/share/nginx/html/index.html
        mode: '0644'

    - name: Ensure Nginx is running
      service:
        name: nginx
        state: started
        enabled: true

  handlers:
    - name: Restart Nginx
      service:
        name: nginx
        state: restarted
```

### Create `files/nginx.conf`

Use a valid Nginx configuration compatible with the target distribution. A basic configuration for a standard Linux Nginx installation is:

```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    access_log /var/log/nginx/access.log;

    sendfile on;
    keepalive_timeout 65;

    server {
        listen 80;
        server_name _;

        root /usr/share/nginx/html;
        index index.html;

        location / {
            try_files $uri $uri/ =404;
        }
    }
}
```

Some distributions use different default configuration paths or service users. Validate the configuration against the target host before applying it.

### Execute and Verify

```bash
ansible-playbook -i inventory.ini nginx-config.yml --syntax-check
ansible-playbook -i inventory.ini nginx-config.yml --check --diff
ansible-playbook -i inventory.ini nginx-config.yml
ansible-playbook -i inventory.ini nginx-config.yml
```

### Expected Behavior

**First run:**
- Nginx is installed if required.
- The configuration file is created or updated.
- The copy task notifies the `Restart Nginx` handler if the file changes.
- The handler restarts Nginx at the end of the play.

**Second run:**
- If the configuration is unchanged, the copy task reports `ok`.
- The handler is not notified and does not run.

Handlers normally execute once at the end of a play, even if notified multiple times. A handler can also be explicitly flushed earlier with `meta: flush_handlers`.

---

## Task 5: Dry Run, Diff, and Verbosity

Ansible provides several options to preview changes and troubleshoot playbooks.

### Check Mode

```bash
ansible-playbook -i inventory.ini install-nginx.yml --check
```

Check mode simulates supported changes without applying them. Some modules or tasks cannot predict their changes accurately in check mode, so it is not a guarantee that a real run will succeed.

### Diff Mode

```bash
ansible-playbook -i inventory.ini nginx-config.yml --diff
```

Diff mode displays supported file changes, such as differences between the current and proposed configuration.

Combine both options:

```bash
ansible-playbook -i inventory.ini nginx-config.yml --check --diff
```

This previews supported changes and displays relevant file differences without applying them.

### Verbosity

```bash
ansible-playbook -i inventory.ini install-nginx.yml -v
ansible-playbook -i inventory.ini install-nginx.yml -vv
ansible-playbook -i inventory.ini install-nginx.yml -vvv
```

- `-v`: Provides additional execution details.
- `-vv`: Provides more diagnostic information.
- `-vvv`: Provides detailed troubleshooting information, including connection-related details.

Be careful when sharing verbose output because it may contain sensitive operational information.

### Limit Execution to Specific Hosts

```bash
ansible-playbook -i inventory.ini install-nginx.yml --limit web-server
```

### List Target Hosts and Tasks

```bash
ansible-playbook -i inventory.ini install-nginx.yml --list-hosts
ansible-playbook -i inventory.ini install-nginx.yml --list-tasks
```

### Why Is `--check --diff` Important for Production?

The combination helps operators review intended changes before applying them. It can reveal unexpected file modifications and configuration differences, reducing the risk of accidental changes to production systems.

However, check mode is only a preview. A real execution can behave differently, so production changes should also follow appropriate testing, review, backup, and rollback procedures.

---

## Task 6: Multiple Plays in One Playbook

A single playbook can configure different server groups with separate plays.

### File: `multi-play.yml`

```yaml
---
- name: Configure web servers
  hosts: web
  become: true

  tasks:
    - name: Install Nginx
      package:
        name: nginx
        state: present

    - name: Start Nginx
      service:
        name: nginx
        state: started
        enabled: true

- name: Configure app servers
  hosts: app
  become: true

  tasks:
    - name: Install Node.js build dependencies
      package:
        name:
          - gcc
          - make
        state: present

    - name: Create app directory
      file:
        path: /opt/app
        state: directory
        mode: '0755'

- name: Configure database servers
  hosts: db
  become: true

  tasks:
    - name: Install MySQL client
      package:
        name: mysql
        state: present

    - name: Create data directory
      file:
        path: /var/lib/appdata
        state: directory
        mode: '0700'
```

**Important:** Package names vary across distributions. On Ubuntu, for example, the MySQL client package is typically `mysql-client`; on Amazon Linux, use the appropriate available client package. Validate package names for your operating system.

### Example Inventory

```ini
[web]
web-server ansible_host=<WEB_SERVER_IP>

[app]
app-server ansible_host=<APP_SERVER_IP>

[db]
db-server ansible_host=<DB_SERVER_IP>

[all:vars]
ansible_user=ec2-user
```

Replace the placeholder IP addresses and set `ansible_user` to the appropriate account for your operating system. Configure SSH access and privilege escalation before execution.

### Execute

```bash
ansible-playbook -i inventory.ini multi-play.yml --syntax-check
ansible-playbook -i inventory.ini multi-play.yml --check --diff
ansible-playbook -i inventory.ini multi-play.yml
```

### Verification

- Nginx tasks target only the `web` group.
- Build dependency and application-directory tasks target only the `app` group.
- MySQL client and data-directory tasks target only the `db` group.

The playbook applies each configuration to the hosts matched by its `hosts` declaration.

---

## Key Learnings

- Playbooks describe desired server configuration in YAML.
- Plays target host groups, while tasks perform individual operations.
- Modules provide reusable functionality for packages, services, files, commands, and configuration.
- Idempotency makes repeated runs safe when tasks correctly describe the desired state.
- Handlers avoid unnecessary service restarts.
- `--check --diff` helps preview changes before deployment.
- Multiple plays allow web, application, and database servers to be managed in a single playbook.

## Evidence and Screenshots

Add your actual terminal screenshots below after executing the playbooks.

### 1. First Playbook Execution

Show the task results, including `changed` and `ok`.

<!-- Add screenshot of the first playbook run here. -->

### 2. Idempotency Verification

Show the second run, where already-correct tasks report `ok`.

<!-- Add screenshot of the second playbook run here. -->

### 3. Handler Verification

Capture the first run when the configuration changes and the second run when the handler is not triggered.

<!-- Add screenshots comparing both runs here. -->

### 4. Multi-Play Execution

Show the output for the web, application, and database server plays.

<!-- Add screenshot of the multi-play run here. -->

---

## Conclusion

Day 69 covered Ansible Playbooks, essential modules, handlers, idempotency, and safe execution practices. These concepts provide a foundation for automating repeatable server configuration and managing multiple infrastructure environments consistently.
