# Day 70 — Variables, Facts, Conditionals and Loops

## Overview

Day 70 focuses on making Ansible playbooks dynamic and adaptable. Variables allow values to be reused and overridden, facts provide information about managed hosts, conditionals control task execution, and loops repeat tasks for multiple items.

Instead of writing separate playbooks for every server, these features help us create reusable automation that adapts to different operating systems, host groups, and environments.

### Objectives

- Understand variables and variable precedence in Ansible.
- Organize variables using `group_vars` and `host_vars`.
- Gather and use Ansible facts.
- Execute tasks conditionally using `when`.
- Use loops to manage multiple users, directories, and packages.
- Capture task output using `register` and display it using `debug`.
- Generate a server health report using facts and command output.

---

## Task 1: Variables in Playbooks

Variables allow us to store values and reuse them throughout a playbook. They make automation easier to customize without changing the tasks themselves.

### File: `variables-demo.yml`

```yaml
---
- name: Variable demo
  hosts: all
  become: true

  vars:
    app_name: terraweek-app
    app_port: 8080
    app_dir: "/opt/{{ app_name }}"
    packages:
      - git
      - curl
      - wget

  tasks:
    - name: Print app details
      debug:
        msg: "Deploying {{ app_name }} on port {{ app_port }} to {{ app_dir }}"

    - name: Create application directory
      file:
        path: "{{ app_dir }}"
        state: directory
        mode: '0755'

    - name: Install required packages
      package:
        name: "{{ packages }}"
        state: present
```

**Explanation:**

- `vars`: Defines variables for the play.
- `app_name`: Stores the application name.
- `app_port`: Stores the application port.
- `app_dir`: Uses variable interpolation to construct the application directory.
- `packages`: Defines a list of packages to install.
- `debug`: Displays a message containing variable values.
- `file`: Creates the application directory.
- `package`: Ensures the required packages are installed.

The `package` module works with the package manager available on the managed host. Package names and availability may differ between Linux distributions.

### Execute the Playbook

Check the syntax:

```bash
ansible-playbook -i inventory.ini variables-demo.yml --syntax-check
```

Preview changes:

```bash
ansible-playbook -i inventory.ini variables-demo.yml --check --diff
```

Run the playbook:

```bash
ansible-playbook -i inventory.ini variables-demo.yml
```

Override variables using the command line:

```bash
ansible-playbook -i inventory.ini variables-demo.yml -e "app_name=my-custom-app app_port=9090"
```

### Verification

Check the output of the `debug` task. It should display the overridden application name and port.

The application directory should resolve to:

```text
/opt/my-custom-app
```

### Answer: Does the CLI variable override the playbook variable?

**Yes.** Variables passed through `-e` (extra variables) have higher precedence than ordinary playbook variables.

For example:

- Playbook variable: `app_name: terraweek-app`
- CLI variable: `app_name=my-custom-app`
- Effective value: `my-custom-app`

This allows us to customize a playbook at runtime without modifying its source file.

---

## Task 2: group_vars and host_vars

Variables do not always need to be defined inside playbooks. Ansible allows us to organize variables into separate files based on inventory groups or individual hosts.

This approach improves maintainability and makes it easier to manage different environments.

### Directory Structure

```text
ansible-practice/
├── inventory.ini
├── ansible.cfg
├── group_vars/
│   ├── all.yml
│   ├── web.yml
│   └── db.yml
├── host_vars/
│   └── web-server.yml
└── playbooks/
    └── site.yml
```

Keep `group_vars` and `host_vars` in a location Ansible recognizes relative to the inventory or playbook. The examples below assume the inventory is in the project root.

### `group_vars/all.yml`

These variables apply to all hosts in the inventory.

```yaml
---
ntp_server: pool.ntp.org
app_env: development

common_packages:
  - vim
  - htop
  - tree
```

### `group_vars/web.yml`

These variables apply to hosts belonging to the `web` group.

```yaml
---
http_port: 80
max_connections: 1000

web_packages:
  - nginx
```

### `group_vars/db.yml`

These variables apply to hosts belonging to the `db` group.

```yaml
---
db_port: 3306

db_packages:
  - mysql-server
```

Note: The package name `mysql-server` is distribution-dependent. Verify the correct package name on your managed hosts before installing it.

### `host_vars/web-server.yml`

These variables apply only to the inventory host named `web-server`.

```yaml
---
max_connections: 2000
custom_message: "This is the primary web server"
```

### Example Inventory: `inventory.ini`

```ini
[web]
web-server ansible_host=<WEB_SERVER_PUBLIC_IP>

[db]
db-server ansible_host=<DB_SERVER_PUBLIC_IP>

[all:vars]
ansible_user=ec2-user
```

Replace the placeholder IP addresses and use the correct SSH username for your managed operating system.

### File: `playbooks/site.yml`

```yaml
---
- name: Apply common config
  hosts: all
  become: true

  tasks:
    - name: Install common packages
      package:
        name: "{{ common_packages }}"
        state: present

    - name: Show environment
      debug:
        msg: "Environment: {{ app_env }}"

- name: Configure web servers
  hosts: web
  become: true

  tasks:
    - name: Show web config
      debug:
        msg: "HTTP port: {{ http_port }}, Max connections: {{ max_connections }}"

    - name: Show host-specific message
      debug:
        msg: "{{ custom_message }}"
      when: custom_message is defined
```

The `when` condition ensures that the host-specific message is displayed only when the variable exists.

### Execute the Playbook

```bash
ansible-playbook -i inventory.ini playbooks/site.yml --syntax-check
ansible-playbook -i inventory.ini playbooks/site.yml
```

### Understanding Variable Precedence

Ansible has a detailed variable-precedence system. A simplified order, from lower to higher precedence, is:

1. Role defaults.
2. Group variables.
3. Host variables.
4. Play-level variables.
5. Task-level variables.
6. Extra variables supplied using `-e`.

The precise ordering depends on the source and context. In particular, host variables override group variables when both define the same variable, and extra variables have very high precedence.

### Answer: What is variable precedence?

Variable precedence determines which value Ansible uses when the same variable is defined in multiple places.

For example:

- `group_vars/web.yml` defines `max_connections: 1000`.
- `host_vars/web-server.yml` defines `max_connections: 2000`.
- For `web-server`, the effective value is `2000`.

If we run:

```bash
ansible-playbook -i inventory.ini playbooks/site.yml -e "max_connections=5000"
```

The extra variable overrides the ordinary values, so the effective value becomes `5000`.

---

## Task 3: Ansible Facts — Gathering System Information

Ansible facts are system details collected from managed hosts. They include operating system information, hostname, memory, IP addresses, CPU information, and network interfaces.

Fact gathering is enabled by default for most plays unless disabled.

### 1. Display All Facts

```bash
ansible -i inventory.ini web-server -m setup
```

### 2. Filter Specific Facts

```bash
ansible -i inventory.ini web-server -m setup -a "filter=ansible_os_family"
```

```bash
ansible -i inventory.ini web-server -m setup -a "filter=ansible_distribution*"
```

```bash
ansible -i inventory.ini web-server -m setup -a "filter=ansible_memtotal_mb"
```

```bash
ansible -i inventory.ini web-server -m setup -a "filter=ansible_default_ipv4"
```

### 3. Use Facts in a Playbook

Create `facts-demo.yml`:

```yaml
---
- name: Facts demo
  hosts: all

  tasks:
    - name: Show OS information
      debug:
        msg: >
          Hostname: {{ ansible_hostname }},
          OS: {{ ansible_distribution }} {{ ansible_distribution_version }},
          RAM: {{ ansible_memtotal_mb }}MB,
          IP: {{ ansible_default_ipv4.address | default('Not available') }}

    - name: Show all network interfaces
      debug:
        var: ansible_interfaces
```

Run it:

```bash
ansible-playbook -i inventory.ini facts-demo.yml
```

### Answer: Name five useful Ansible facts and explain their uses.

| Fact | Use |
|---|---|
| `ansible_hostname` | Identifies the system hostname in reports and logs. |
| `ansible_distribution` | Selects tasks based on the operating system. |
| `ansible_distribution_version` | Applies configuration for a specific OS version. |
| `ansible_memtotal_mb` | Checks whether a host meets a memory requirement. |
| `ansible_default_ipv4.address` | Retrieves the default IPv4 address for reporting or configuration. |

Other useful facts include `ansible_interfaces`, `ansible_processor_vcpus`, and `ansible_mounts`.

---

## Task 4: Conditionals with when

The `when` keyword allows Ansible to execute tasks only when specified conditions are true.

For example, web servers may require Nginx, while database servers may require database packages.

### File: `conditional-demo.yml`

```yaml
---
- name: Conditional tasks demo
  hosts: all
  become: true

  tasks:
    - name: Install Nginx only on web servers
      package:
        name: nginx
        state: present
      when: "'web' in group_names"

    - name: Install MySQL only on database servers
      package:
        name: mysql-server
        state: present
      when: "'db' in group_names"

    - name: Show warning on low-memory hosts
      debug:
        msg: "WARNING: This host has less than 1GB RAM"
      when: ansible_memtotal_mb < 1024

    - name: Run only on Amazon Linux
      debug:
        msg: "This is an Amazon Linux machine"
      when: ansible_distribution == "Amazon"

    - name: Run only on Ubuntu
      debug:
        msg: "This is an Ubuntu machine"
      when: ansible_distribution == "Ubuntu"

    - name: Run only in production
      debug:
        msg: "Production settings applied"
      when: app_env is defined and app_env == "production"

    - name: Multiple conditions (AND)
      debug:
        msg: "Web server with enough memory"
      when:
        - "'web' in group_names"
        - ansible_memtotal_mb >= 512

    - name: OR condition
      debug:
        msg: "Either web or app server"
      when: "'web' in group_names or 'app' in group_names"
```

The package names in this example may need adjustment for your Linux distribution.

### Execute the Playbook

```bash
ansible-playbook -i inventory.ini conditional-demo.yml --syntax-check
ansible-playbook -i inventory.ini conditional-demo.yml
```

To test the production condition:

```bash
ansible-playbook -i inventory.ini conditional-demo.yml -e "app_env=production"
```

### Understanding the Conditions

- `"'web' in group_names"` checks whether the current host belongs to the web group.
- `ansible_memtotal_mb < 1024` checks whether the host has less than 1 GB of memory.
- `ansible_distribution == "Ubuntu"` checks the detected operating system.
- Multiple entries in a YAML list under `when` are evaluated as AND conditions.
- An `or` expression runs the task if either condition is true.

### Answer: Are tasks correctly skipped on hosts that do not match the condition?

**Yes.** When a condition evaluates to false, Ansible skips that task for the affected host.

For example:

- A host in the `web` group runs the Nginx installation task.
- A host in the `db` group runs the MySQL installation task.
- A host with at least 1 GB of RAM skips the low-memory warning.
- A host running Ubuntu skips the Amazon Linux message.

The exact output depends on the inventory groups and facts of the managed hosts.

---

## Task 5: Loops

Loops allow a task to run for each item in a list. Instead of writing separate tasks to create several users or directories, we can define the items once and reuse a single task.

### File: `loops-demo.yml`

```yaml
---
- name: Loops demo
  hosts: all
  become: true

  vars:
    users:
      - name: deploy
        groups: wheel
      - name: monitor
        groups: wheel
      - name: appuser
        groups: users

    directories:
      - /opt/app/logs
      - /opt/app/config
      - /opt/app/data
      - /opt/app/tmp

  tasks:
    - name: Create multiple users
      user:
        name: "{{ item.name }}"
        groups: "{{ item.groups }}"
        append: true
        state: present
      loop: "{{ users }}"

    - name: Create multiple directories
      file:
        path: "{{ item }}"
        state: directory
        mode: '0755'
      loop: "{{ directories }}"

    - name: Install multiple packages
      package:
        name: "{{ item }}"
        state: present
      loop:
        - git
        - curl
        - unzip
        - jq

    - name: Print each user
      debug:
        msg: "Ensured user {{ item.name }} belongs to group {{ item.groups }}"
      loop: "{{ users }}"
```

**Important:** Verify that the `wheel` and `users` groups exist on your managed hosts. Some distributions use `sudo` instead of `wheel` for administrative access. The `append: true` option preserves existing supplementary group memberships.

### Execute the Playbook

```bash
ansible-playbook -i inventory.ini loops-demo.yml --syntax-check
ansible-playbook -i inventory.ini loops-demo.yml --check --diff
ansible-playbook -i inventory.ini loops-demo.yml
```

### Answer: What is the difference between `loop` and `with_items`?

- `loop` is the modern, recommended syntax for iterating over a list.
- `with_items` is an older syntax found in existing playbooks.
- For straightforward lists, `loop` is generally clearer and easier to maintain.
- When converting older playbooks, check the data structure because specialized `with_*` constructs can have different behavior.

Ansible displays the result of each iteration separately, making it easier to identify which items changed, succeeded, or failed.

---

## Task 6: Register, Debug, and Combine Everything

The `register` keyword stores the result of a task in a variable. The result can then be used in later tasks to display information, make decisions, or generate reports.

### File: `server-report.yml`

```yaml
---
- name: Server Health Report
  hosts: all
  become: true
  gather_facts: true

  tasks:
    - name: Check disk space
      command: df -h /
      register: disk_result
      changed_when: false

    - name: Check memory
      command: free -m
      register: memory_result
      changed_when: false

    - name: Check running services
      shell: systemctl list-units --type=service --state=running --no-pager | head -20
      register: services_result
      changed_when: false
      failed_when: false

    - name: Generate report
      debug:
        msg:
          - "========== {{ inventory_hostname }} =========="
          - "OS: {{ ansible_distribution }} {{ ansible_distribution_version }}"
          - "IP: {{ ansible_default_ipv4.address | default('Not available') }}"
          - "RAM: {{ ansible_memtotal_mb }}MB"
          - "Disk: {{ disk_result.stdout_lines | default([]) }}"
          - "Memory: {{ memory_result.stdout_lines | default([]) }}"
          - "Running services (first 20 lines): {{ services_result.stdout_lines | default([]) | length }}"

    - name: Flag if disk usage is critically high
      debug:
        msg: "ALERT: Check disk space on {{ inventory_hostname }}"
      when: disk_result.stdout is search('\\s(9[0-9]|100)%\\s')

    - name: Save report to file
      copy:
        content: |
          Server: {{ inventory_hostname }}
          Hostname: {{ ansible_hostname }}
          OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
          IP: {{ ansible_default_ipv4.address | default('Not available') }}
          RAM: {{ ansible_memtotal_mb }}MB

          Disk:
          {{ disk_result.stdout }}

          Memory:
          {{ memory_result.stdout }}

          Running services (first 20 lines):
          {{ services_result.stdout }}

          Checked at: {{ ansible_date_time.iso8601 }}
        dest: "/tmp/server-report-{{ inventory_hostname }}.txt"
        mode: '0644'
```

### Execute the Playbook

```bash
ansible-playbook -i inventory.ini server-report.yml --syntax-check
ansible-playbook -i inventory.ini server-report.yml
```

### Verify the Report

SSH into a managed host and run:

```bash
cat /tmp/server-report-<INVENTORY_HOSTNAME>.txt
```

Replace `<INVENTORY_HOSTNAME>` with the host's inventory name.

The file should contain the hostname, OS information, IP address, RAM, disk usage, memory output, running-service output, and report timestamp.

### Understanding `register` and `debug`

- `register` stores the result returned by a task.
- `stdout` contains command output as a string.
- `stdout_lines` contains command output split into lines.
- `stderr` contains error output when available.
- `rc` contains the command's return code.
- `debug: var:` displays a variable's value.
- `debug: msg:` displays a formatted message.

The `changed_when: false` setting prevents read-only checks from being reported as changes. The `failed_when: false` setting on the service check allows the report to continue if the service-listing command fails, although its output may then be empty or contain an error.

---

## Key Learnings

- Variables make playbooks reusable and configurable.
- `group_vars` and `host_vars` organize configuration for groups and individual hosts.
- Extra variables passed with `-e` have very high precedence.
- Facts provide system information about managed hosts.
- `when` conditions control whether tasks run.
- Loops eliminate repetitive tasks.
- `register` stores task output for use in later tasks.
- `debug` helps inspect variables and display reports.
- Combining these features creates flexible automation for different servers and environments.

---

## Evidence and Screenshots

Add your actual terminal screenshots after executing the playbooks.

### 1. Variables and CLI Override

Show the default variable values and the overridden values using `-e`.

<!-- Add screenshot of variables-demo.yml execution here. -->

### 2. group_vars and host_vars

Show the directory structure and output demonstrating group-level and host-specific values.

<!-- Add screenshot of site.yml execution here. -->

### 3. Ansible Facts

Show selected facts such as operating system, memory, and IP address.

<!-- Add screenshot of facts-demo.yml execution here. -->

### 4. Conditional Tasks

Show tasks that execute on matching hosts and are skipped on non-matching hosts.

<!-- Add screenshot of conditional-demo.yml execution here. -->

### 5. Loops

Show multiple iterations for users, directories, and packages.

<!-- Add screenshot of loops-demo.yml execution here. -->

### 6. Server Health Report

Show the terminal report and the contents of the generated report file.

<!-- Add screenshot of server-report.yml output here. -->

---

## Conclusion

Day 70 covered variables, facts, conditionals, loops, and registered task results in Ansible. These features help create playbooks that adapt to different operating systems, host groups, and environments while reducing repetitive code and improving maintainability.