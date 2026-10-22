
# Day 71: Ansible Roles, Templates, Galaxy and Vault

## 1. Introduction

As Ansible playbooks grow, managing all tasks, variables, handlers, and configuration files in a single YAML file becomes difficult. In real-world projects, we need a way to organize automation, reuse existing configurations, generate dynamic files, and protect sensitive information.

In this task, I explored four important Ansible concepts:

- **Ansible Roles:** Organize automation into reusable components.
- **Jinja2 Templates:** Generate dynamic configuration files using variables and facts.
- **Ansible Galaxy:** Discover and install reusable community roles.
- **Ansible Vault:** Encrypt sensitive information such as passwords and API keys.

### Objectives

- Create a custom webserver role.
- Generate Nginx configuration files using Jinja2 templates.
- Install and use a role from Ansible Galaxy.
- Encrypt and manage secrets using Ansible Vault.
- Combine roles, templates, and encrypted variables in a playbook.

---

## 2. Task 1: Jinja2 Templates

### What are Jinja2 Templates?

Jinja2 is a templating engine used by Ansible to generate configuration files dynamically.

Instead of hardcoding values in configuration files, we can use variables and facts that Ansible replaces with actual values when rendering the template.

Common Jinja2 syntax:

| Syntax | Purpose |
|---|---|
| `{{ variable }}` | Displays a variable's value. |
| `{% if condition %}` | Executes a template block conditionally. |
| `{% for item in items %}` | Iterates over a collection. |
| `{{ variable \| default(value) }}` | Provides a fallback when a variable is undefined. |

### Step 1: Create the template

Create a file named `templates/nginx-vhost.conf.j2`.

```jinja2
# Managed by Ansible -- do not edit manually
server {
    listen {{ http_port | default(80) }};
    server_name {{ ansible_hostname }};

    root /var/www/{{ app_name }};
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    access_log /var/log/nginx/{{ app_name }}_access.log;
    error_log /var/log/nginx/{{ app_name }}_error.log;
}
```

Here:

- `http_port` defines the HTTP port.
- `ansible_hostname` is a fact gathered from the managed node.
- `app_name` defines the application name.
- `default(80)` uses port 80 if `http_port` is undefined.

### Step 2: Create the playbook

Create `template-demo.yml`.

```yaml
---
- name: Deploy Nginx with template
  hosts: web
  become: true

  vars:
    app_name: terraweek-app
    http_port: 80

  tasks:
    - name: Install Nginx
      ansible.builtin.package:
        name: nginx
        state: present

    - name: Create web root
      ansible.builtin.file:
        path: "/var/www/{{ app_name }}"
        state: directory
        mode: '0755'

    - name: Deploy virtual host configuration
      ansible.builtin.template:
        src: templates/nginx-vhost.conf.j2
        dest: "/etc/nginx/conf.d/{{ app_name }}.conf"
        owner: root
        group: root
        mode: '0644'
      notify: Restart Nginx

    - name: Deploy index page
      ansible.builtin.copy:
        content: |
          <h1>{{ app_name }}</h1>
          <p>Host: {{ ansible_hostname }}</p>
          <p>IP: {{ ansible_default_ipv4.address }}</p>
        dest: "/var/www/{{ app_name }}/index.html"
        mode: '0644'

  handlers:
    - name: Restart Nginx
      ansible.builtin.service:
        name: nginx
        state: restarted
```

**Note:** This example assumes an Nginx installation whose configuration loads files from `/etc/nginx/conf.d/`. Verify the default virtual host configuration for your target operating system before testing the application.

### Step 3: Execute the playbook

```bash
ansible-playbook -i inventory.ini template-demo.yml --syntax-check

ansible-playbook -i inventory.ini template-demo.yml --diff
```

The `--diff` option displays configuration changes made by Ansible. Review the output carefully before using it with sensitive configuration files.

### Step 4: Verify the generated configuration

Connect to the managed webserver and execute:

```bash
sudo cat /etc/nginx/conf.d/terraweek-app.conf

sudo nginx -t
```

Test the application:

```bash
curl http://<WEB_SERVER_IP>
```

Replace `<WEB_SERVER_IP>` with the actual IP address of your webserver.

### Expected rendered output

The generated configuration should resemble the following. The hostname depends on the actual managed node.

```nginx
# Managed by Ansible -- do not edit manually
server {
    listen 80;
    server_name web1;

    root /var/www/terraweek-app;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    access_log /var/log/nginx/terraweek-app_access.log;
    error_log /var/log/nginx/terraweek-app_error.log;
}
```

### Answer: Were the variables replaced with actual values?

Yes. When Ansible processes the template, it replaces Jinja2 expressions with the corresponding variable values and host facts.

For example:

- `{{ http_port }}` becomes `80`.
- `{{ app_name }}` becomes `terraweek-app`.
- `{{ ansible_hostname }}` becomes the managed server's hostname.

This allows the same template to generate different configurations for different applications or environments without maintaining separate static configuration files.

---

## 3. Task 2: Understanding Ansible Role Structure

### What is an Ansible Role?

An Ansible role is a reusable collection of tasks, handlers, variables, templates, files, and metadata organized into a standard directory structure.

Roles make playbooks easier to read, maintain, test, and reuse across multiple environments.

### Step 1: Generate a role structure

```bash
ansible-galaxy init roles/webserver
```

This command creates a standard role skeleton.

### Step 2: Understand the directory structure

```text
roles/
└── webserver/
    ├── defaults/
    │   └── main.yml
    ├── files/
    │   └── index.html
    ├── handlers/
    │   └── main.yml
    ├── meta/
    │   └── main.yml
    ├── tasks/
    │   └── main.yml
    ├── templates/
    │   └── nginx.conf.j2
    ├── vars/
    │   └── main.yml
    └── README.md
```

| Directory | Purpose |
|---|---|
| `tasks/` | Contains the tasks executed by the role. |
| `handlers/` | Contains handlers triggered by notifications. |
| `templates/` | Stores Jinja2 templates. |
| `files/` | Stores static files copied to managed hosts. |
| `defaults/` | Contains default variables that are easy to override. |
| `vars/` | Contains role variables with higher precedence. |
| `meta/` | Contains role metadata and dependencies. |

Ansible automatically loads the main task, handler, default-variable, and role-variable files from their respective directories when applicable. Only the directories needed by a role have to be retained.

### Answer: What is the difference between `vars/main.yml` and `defaults/main.yml`?

**`defaults/main.yml`**

- Contains default values for role variables.
- Has the lowest variable precedence.
- Allows users to customize the role through inventory variables, play variables, or variables supplied when calling the role.

Example:

```yaml
---
http_port: 80
app_name: myapp
max_connections: 512
```

**`vars/main.yml`**

- Contains role variables with higher precedence.
- Is useful for values that should not normally be overridden by callers.
- Can make customization more difficult because its variables take precedence over many other variable sources.

**Conclusion:** Use `defaults/main.yml` for configurable settings such as application names, ports, and environment values. Use `vars/main.yml` only when higher precedence is intentional.

---

## 4. Task 3: Build a Custom Webserver Role

In this task, I structured the webserver automation into a reusable role.

### Step 1: Define default variables

File: `roles/webserver/defaults/main.yml`

```yaml
---
http_port: 80
app_name: myapp
max_connections: 512
```

These values can be overridden when the role is called from a playbook.

### Step 2: Define the tasks

File: `roles/webserver/tasks/main.yml`

```yaml
---
- name: Install Nginx
  ansible.builtin.package:
    name: nginx
    state: present

- name: Deploy Nginx configuration
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: '0644'
  notify: Restart Nginx

- name: Deploy virtual host configuration
  ansible.builtin.template:
    src: vhost.conf.j2
    dest: "/etc/nginx/conf.d/{{ app_name }}.conf"
    owner: root
    group: root
    mode: '0644'
  notify: Restart Nginx

- name: Create web root
  ansible.builtin.file:
    path: "/var/www/{{ app_name }}"
    state: directory
    mode: '0755'

- name: Deploy index page
  ansible.builtin.template:
    src: index.html.j2
    dest: "/var/www/{{ app_name }}/index.html"
    mode: '0644'

- name: Start and enable Nginx
  ansible.builtin.service:
    name: nginx
    state: started
    enabled: true
```

The `package` module lets Ansible select the appropriate package manager for supported systems. However, the Nginx configuration paths and service-user details still need to match the target operating system.

### Step 3: Create a handler

File: `roles/webserver/handlers/main.yml`

```yaml
---
- name: Restart Nginx
  ansible.builtin.service:
    name: nginx
    state: restarted
```

The handler restarts Nginx when a configuration task notifies it. This avoids restarting the service unnecessarily when configuration files have not changed.

### Step 4: Create the HTML template

File: `roles/webserver/templates/index.html.j2`

```html
<h1>{{ app_name }}</h1>
<p>Server: {{ ansible_hostname }}</p>
<p>IP: {{ ansible_default_ipv4.address }}</p>
<p>Environment: {{ app_env | default('development') }}</p>
<p>Managed by Ansible</p>
```

The application name, hostname, IP address, and environment are generated dynamically.

### Step 5: Create the virtual host template

File: `roles/webserver/templates/vhost.conf.j2`

```jinja2
server {
    listen {{ http_port | default(80) }};
    server_name {{ ansible_hostname }};

    root /var/www/{{ app_name }};
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    access_log /var/log/nginx/{{ app_name }}_access.log;
    error_log /var/log/nginx/{{ app_name }}_error.log;
}
```

### Step 6: Create the main Nginx template

File: `roles/webserver/templates/nginx.conf.j2`

```jinja2
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
    worker_connections {{ max_connections | default(512) }};
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    sendfile on;
    keepalive_timeout 65;

    include /etc/nginx/conf.d/*.conf;
}
```

This is a minimal example for a compatible Nginx installation. Check the existing configuration and service-user settings before replacing a distribution's default `nginx.conf`.

### Step 7: Call the role from a playbook

Create `site.yml`:

```yaml
---
- name: Configure web servers
  hosts: web
  become: true

  roles:
    - role: webserver
      vars:
        app_name: terraweek
        http_port: 80
        max_connections: 512
```

### Step 8: Execute and verify

```bash
ansible-playbook -i inventory.ini site.yml --syntax-check

ansible-playbook -i inventory.ini site.yml
```

Verify the Nginx configuration on the managed host:

```bash
sudo nginx -t

curl http://<WEB_SERVER_IP>
```

### Answer: Why use a role instead of keeping everything in one playbook?

A role separates related automation into organized, reusable files. The same webserver role can be called from multiple playbooks with different variables, allowing different applications or environments to share the same automation logic.

For example, development and production environments can use the same role with different `app_name` or `http_port` values.

---

## 5. Task 4: Ansible Galaxy — Community Roles

### What is Ansible Galaxy?

Ansible Galaxy provides a way to discover, download, install, and manage reusable community roles and collections.

Instead of writing every task from scratch, we can use existing roles after checking their documentation, compatibility, dependencies, and security.

### Step 1: Search for roles

```bash
ansible-galaxy search nginx --platforms EL

ansible-galaxy search mysql
```

These commands help discover roles relevant to Nginx and MySQL.

### Step 2: Install a Docker role

```bash
ansible-galaxy install geerlingguy.docker
```

List installed roles:

```bash
ansible-galaxy list
```

### Step 3: Use the role in a playbook

Create `docker-setup.yml`:

```yaml
---
- name: Install Docker using Galaxy role
  hosts: app
  become: true

  roles:
    - geerlingguy.docker
```

Execute:

```bash
ansible-playbook -i inventory.ini docker-setup.yml
```

Check the role's documentation for supported operating systems, required variables, and prerequisites before running it on a managed server.

### Step 4: Manage dependencies using `requirements.yml`

Create `requirements.yml`:

```yaml
---
roles:
  - name: geerlingguy.docker
    version: "7.4.1"

  - name: geerlingguy.ntp
```

Install all declared roles:

```bash
ansible-galaxy install -r requirements.yml
```

Verify the installed roles:

```bash
ansible-galaxy list
```

### Answer: Why use `requirements.yml` instead of installing roles manually?

A requirements file defines the roles and versions required by a project in one place.

Its benefits include:

- **Consistency:** Team members can install the same declared dependencies.
- **Version control:** Role versions can be pinned to reduce unexpected changes.
- **Convenience:** Multiple roles can be installed using one command.
- **CI/CD integration:** Automation pipelines can install project dependencies before executing playbooks.
- **Maintainability:** Dependencies are documented alongside the automation code.

Pinning a version helps with repeatability, but it does not replace reviewing the role's source, dependencies, and security.

---

## 6. Task 5: Ansible Vault — Encrypt Secrets

### What is Ansible Vault?

Ansible Vault is a feature that encrypts sensitive data used by Ansible, including passwords, API keys, and database credentials.

It allows encrypted variables and files to remain encrypted at rest while Ansible decrypts them when needed to execute a playbook.

### Step 1: Create an encrypted file

Create the directory:

```bash
mkdir -p group_vars/db
```

Create the Vault file:

```bash
ansible-vault create group_vars/db/vault.yml
```

Enter test-only variables in the editor:

```yaml
---
vault_db_password: "REPLACE_WITH_TEST_PASSWORD"
vault_db_root_password: "REPLACE_WITH_TEST_ROOT_PASSWORD"
vault_api_key: "REPLACE_WITH_TEST_API_KEY"
```

Save and exit. Ansible Vault encrypts the file.

**Important:** These are placeholders, not real credentials. Never use actual passwords or API keys in public documentation.

### Step 2: Verify that the file is encrypted

```bash
head -n 3 group_vars/db/vault.yml
```

An encrypted Vault file begins with a header similar to:

```text
$ANSIBLE_VAULT;1.1;AES256
```

The remaining contents should be encrypted rather than readable YAML.

### Step 3: Edit the encrypted file

```bash
ansible-vault edit group_vars/db/vault.yml
```

Ansible prompts for the Vault password, decrypts the file for editing, and saves it encrypted again.

### Step 4: View the decrypted contents

```bash
ansible-vault view group_vars/db/vault.yml
```

This displays the decrypted values in the terminal. Do not capture or share the output if it contains real secrets.

### Step 5: Encrypt an existing file

Create a test YAML file, then encrypt it:

```bash
ansible-vault encrypt group_vars/db/secrets.yml
```

### Step 6: Decrypt an encrypted file

```bash
ansible-vault decrypt group_vars/db/secrets.yml
```

**Security note:** Decryption converts the file back to plaintext. Keep it out of source control and re-encrypt it when appropriate.

### Step 7: Use Vault variables in a playbook

Create `db-setup.yml`:

```yaml
---
- name: Configure database
  hosts: db
  become: true

  tasks:
    - name: Check whether the database password is configured
      ansible.builtin.debug:
        msg: "DB password is configured: {{ vault_db_password | length > 0 }}"
```

Run the playbook:

```bash
ansible-playbook -i inventory.ini db-setup.yml --ask-vault-pass
```

The playbook uses the encrypted variables from `group_vars/db/vault.yml` because the file belongs to the `db` inventory group.

The debug task checks whether a password is configured without displaying its actual value.

### Step 8: Use a Vault password file

For a local practice environment, create a password file:

```bash
printf '%s\n' 'REPLACE_WITH_YOUR_VAULT_PASSWORD' > .vault_pass

chmod 600 .vault_pass

printf '%s\n' '.vault_pass' >> .gitignore
```

Run the playbook:

```bash
ansible-playbook -i inventory.ini db-setup.yml \
  --vault-password-file .vault_pass
```

Never commit `.vault_pass` to Git. If it was already tracked, adding it to `.gitignore` does not remove it from Git history.

For production CI/CD, use the platform's protected secret store to supply the Vault password securely rather than storing a plaintext password file in the repository.

### Answer: Why is `--vault-password-file` useful in automated pipelines?

`--ask-vault-pass` requires interactive input, which is usually unsuitable for unattended CI/CD pipelines.

`--vault-password-file` allows Ansible to obtain the password non-interactively. In a production pipeline, the password must still be protected and supplied securely through a secret store or another controlled mechanism.

A password file should never be committed to the repository, printed in logs, or uploaded as a build artifact.

### Optional: Configure the password-file path

In `ansible.cfg`:

```ini
[defaults]
vault_password_file = .vault_pass
```

This tells Ansible which file to use by default. The password file itself must remain protected.

---

## 7. Task 6: Combine Roles, Templates and Vault

In this task, I combined the custom webserver role, a Galaxy Docker role, and encrypted database credentials in a single playbook.

### Step 1: Create the database template

Create `templates/db-config.j2`:

```jinja2
# Database Configuration -- Managed by Ansible
DB_HOST={{ ansible_default_ipv4.address }}
DB_PORT={{ db_port | default(3306) }}
DB_PASSWORD={{ vault_db_password }}
DB_ROOT_PASSWORD={{ vault_db_root_password }}
```

This template renders database settings using the managed server's IP address, a configurable port, and encrypted Vault variables.

### Step 2: Create the combined playbook

Create or update `site.yml`:

```yaml
---
- name: Configure web servers
  hosts: web
  become: true

  roles:
    - role: webserver
      vars:
        app_name: terraweek
        http_port: 80

- name: Configure application servers with Docker
  hosts: app
  become: true

  roles:
    - geerlingguy.docker

- name: Configure database servers
  hosts: db
  become: true

  tasks:
    - name: Create database configuration with secrets
      ansible.builtin.template:
        src: templates/db-config.j2
        dest: /etc/db-config.env
        owner: root
        group: root
        mode: '0600'
      no_log: true
```

The `no_log: true` option prevents this task's details from being printed in normal Ansible output. It does not encrypt the destination file or prevent privileged users from reading it.

### Step 3: Execute the playbook

Using an interactive Vault password prompt:

```bash
ansible-playbook -i inventory.ini site.yml --ask-vault-pass
```

Or, for the practice password-file setup:

```bash
ansible-playbook -i inventory.ini site.yml \
  --vault-password-file .vault_pass
```

Ensure the Galaxy role is installed and that the inventory contains the `web`, `app`, and `db` groups.

### Step 4: Verify the database configuration

On the database server:

```bash
sudo stat -c '%a %U:%G %n' /etc/db-config.env
```

Expected permission mode:

```text
600 root:root /etc/db-config.env
```

The hostname, ownership, and file path should match your actual setup.

Check the permissions programmatically:

```bash
sudo test "$(stat -c '%a' /etc/db-config.env)" = "600" \
  && echo "Permissions OK"
```

Check that the file exists and is non-empty without printing its secrets:

```bash
sudo test -s /etc/db-config.env \
  && echo "Configuration file exists"
```

### Answer: Are the secrets rendered correctly, and is the permission mode 600?

The template is designed to render the Vault variables into the destination file when the playbook runs with a valid Vault password.

The file permission mode `600` means:

- Owner: read and write.
- Group: no permissions.
- Others: no permissions.

Verify the rendered configuration on your own database server without displaying real credentials. A successful playbook run and a permission mode of `600` should be confirmed from your actual environment before documenting the task as complete.

---

## 8. Roles vs Playbooks vs Ad-hoc Commands

| Feature | Purpose | Example |
|---|---|---|
| Ad-hoc commands | Run a quick, one-time task against selected hosts. | `ansible web -i inventory.ini -m ping` |
| Playbooks | Define a sequence of tasks to execute against hosts. | `ansible-playbook -i inventory.ini site.yml` |
| Roles | Organize related automation into reusable components. | `roles: - webserver` |

### When should each be used?

**Ad-hoc commands:** Useful for quick connectivity checks, gathering information, and simple one-time operations.

**Playbooks:** Useful when multiple tasks must run in a defined sequence and the automation needs to be repeatable.

**Roles:** Useful when tasks, variables, handlers, templates, and files need to be organized into reusable components shared across multiple playbooks.

### Answer: When should we use roles, playbooks, and ad-hoc commands?

Use ad-hoc commands for quick tasks, playbooks to orchestrate automation, and roles to structure and reuse related tasks. In a larger project, playbooks commonly call multiple roles to configure different components of the infrastructure.

---

## 9. Troubleshooting

| Problem | What to check |
|---|---|
| Managed node is unreachable | Inventory IP, SSH key, remote user, and security group rules. |
| Nginx installation fails | Target OS and package availability. |
| Template variables are undefined | Variable names, inventory variables, and fact gathering. |
| Nginx configuration is invalid | Run `sudo nginx -t` on the managed host. |
| Role cannot be found | Check `ansible-galaxy list`, role paths, and `requirements.yml`. |
| Vault decryption fails | Confirm the Vault password and file encryption status. |
| Database file has incorrect permissions | Verify ownership and mode using `stat`. |
| Secrets appear in logs | Avoid printing sensitive values; use `no_log: true` where appropriate. |

Useful validation commands:

```bash
ansible-inventory -i inventory.ini --graph

ansible-playbook -i inventory.ini site.yml --syntax-check

ansible-galaxy list

ansible-vault --help
```

---

## 10. Verification and Screenshots

After completing the practical tasks, capture your actual terminal outputs and add them to the repository.

### Screenshot 1: Role directory structure

Show the `roles/webserver/` directory and its subdirectories.

### Screenshot 2: Template execution

Show the successful execution of:

```bash
ansible-playbook -i inventory.ini template-demo.yml --diff
```

Remove or redact any sensitive information.

### Screenshot 3: Custom role execution

Show the successful execution of:

```bash
ansible-playbook -i inventory.ini site.yml
```

Also verify the generated web page using `curl` or a browser.

### Screenshot 4: Ansible Galaxy

Show the role installation and verification using:

```bash
ansible-galaxy install geerlingguy.docker

ansible-galaxy list
```

### Screenshot 5: Ansible Vault

Show the encrypted file header, not the decrypted credentials.

```bash
head -n 3 group_vars/db/vault.yml
```

### Screenshot 6: Database file permissions

Show the result of:

```bash
sudo stat -c '%a %U:%G %n' /etc/db-config.env
```

Do not capture the contents of a file containing real passwords or API keys.

---

## 11. Key Learnings

- **Roles** provide a structured way to organize and reuse Ansible automation.
- **Jinja2 templates** generate dynamic configuration files using variables and facts.
- **Handlers** execute actions such as restarting services when notified.
- **Ansible Galaxy** simplifies the reuse and management of community roles.
- **Ansible Vault** protects sensitive variables and configuration files through encryption.
- **Requirements files** help make role dependencies more consistent and reproducible.
- **Secure permissions and logging practices** are essential when deploying sensitive configuration files.

## Conclusion

Day 71 focused on structuring Ansible automation for better reusability, maintainability, and security.

By combining roles, templates, Galaxy dependencies, and Vault-encrypted variables, we can build more organized automation that is easier to adapt to different servers and environments.

The next step is to validate these workflows in the target environment, document the actual results, and keep sensitive information out of source control.

