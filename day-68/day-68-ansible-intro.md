# Day 68: Introduction to Ansible and Inventory Setup

## Overview

Terraform helps us provision infrastructure, but creating servers is only one part of infrastructure management. Once the servers are running, we still need to install packages, configure services, manage files, and maintain consistent configurations.

This is where **Ansible** comes in.

Ansible is an open-source configuration management and automation tool that can configure servers and execute tasks remotely. It is agentless, meaning managed nodes do not need a separate Ansible agent installed. Ansible connects to Linux managed nodes over SSH by default.

In this practical session, I explored Ansible architecture, installed Ansible on a control node, configured an inventory of EC2 instances, and practised running ad-hoc commands against remote servers.

## Objectives

- Understand configuration management and Ansible architecture.
- Install Ansible on a control node.
- Prepare EC2 instances as managed nodes.
- Create an inventory file with multiple host groups.
- Verify connectivity using the Ansible ping module.
- Execute ad-hoc commands to inspect and configure remote servers.
- Understand inventory patterns, privilege escalation, and configuration files.

## 1. Understanding Configuration Management

### What is configuration management?

Configuration management is the process of configuring, maintaining, and managing systems in a consistent and repeatable way.

For example, if we manage three EC2 instances, we may need to install Git, create configuration files, configure services, and ensure that all three servers follow the required setup.

Performing these tasks manually on every server can be repetitive and error-prone. Configuration management tools automate these operations and help maintain consistency.

### What is Ansible?

Ansible is an automation tool used for:

- Installing and managing software packages.
- Configuring services.
- Managing files and users.
- Executing commands on multiple servers.
- Automating repeatable infrastructure operations.

### Ansible vs. other configuration management tools

| Tool | General approach |
|---|---|
| Ansible | Agentless by default; commonly uses SSH for Linux hosts and YAML playbooks. |
| Chef | Typically uses an agent-based model with recipes written in Ruby-based DSL. |
| Puppet | Commonly uses an agent-based model and declarative manifests. |
| Salt | Supports agent-based and agentless approaches, depending on the setup. |

Each tool has its own strengths. Ansible is particularly convenient for getting started because Linux managed nodes generally do not require a dedicated agent.

### What does agentless mean?

Ansible does not require a separate Ansible agent to run continuously on each Linux managed node. Instead, the control node connects over SSH, executes the required operations, and returns the results.

**Important:** Agentless does not mean that no prerequisites are needed. Managed Linux nodes still need SSH access and a suitable Python installation for most Ansible modules.

## 2. Understanding Ansible Architecture

Ansible architecture consists of the following components.

- **Control Node:** The machine where Ansible is installed and commands or playbooks are executed.
- **Managed Nodes:** Remote servers that Ansible configures, such as EC2 instances.
- **Inventory:** A file that lists managed hosts and organizes them into groups.
- **Modules:** Units of work that perform tasks, such as checking connectivity, copying files, or installing packages.
- **Ad-hoc Commands:** Commands used to perform one-off tasks without creating a playbook.
- **Playbooks:** YAML files that define repeatable tasks and the hosts on which they should run.

### Architecture diagram

```text
             Control Node
           (Ansible Installed)
                   |
                   | SSH
                   |
             Inventory File
                   |
         +---------+---------+
         |         |         |
         v         v         v
     Web Server App Server DB Server
      (EC2)       (EC2)     (EC2)
         |         |         |
         +---------+---------+
              Managed Nodes
```

The control node reads the inventory, connects to the selected managed nodes, executes the requested tasks, and displays the results.

### How does Ansible fit into DevOps?

```text
Terraform
    |
    v
Provision EC2 Infrastructure
    |
    v
Ansible
    |
    v
Install Packages and Configure Servers
    |
    v
Deploy and Manage Applications
```

Terraform and Ansible solve different but complementary problems: Terraform provisions infrastructure, while Ansible automates configuration and operations on that infrastructure.

## 3. Setting Up the Lab Environment

For this practical, I used the following lab design.

| Component | Configuration |
|---|---|
| Control node | Ubuntu machine with Ansible installed |
| Managed nodes | Three EC2 instances |
| Operating system | Amazon Linux 2 or Ubuntu 22.04 |
| Instance type | `t2.micro`, subject to availability and account eligibility |
| Connection | SSH |
| Security group | SSH access on port 22 from the control node's IP |
| Authentication | EC2 SSH private key |

The three managed nodes represent:

- **Web server:** The server responsible for the web-facing layer.
- **App server:** The server responsible for application logic.
- **DB server:** The server representing the database layer.

These are lab roles; the task does not require deploying actual web, application, or database services.

### Creating the EC2 instances

I can provision the instances through Terraform or launch them manually from the AWS Console.

If using Terraform, the configuration should define the instances, security group, and required SSH access. The private key must be available to the control node, but should never be committed to GitHub.

### Verify SSH connectivity

For Amazon Linux 2:

```bash
ssh -i ~/your-key.pem ec2-user@<PUBLIC_IP_1>
ssh -i ~/your-key.pem ec2-user@<PUBLIC_IP_2>
ssh -i ~/your-key.pem ec2-user@<PUBLIC_IP_3>
```

For Ubuntu managed nodes, replace `ec2-user` with `ubuntu`.

Before proceeding, verify that all three connections work and that the security group allows SSH from the control node.

## 4. Installing Ansible

Ansible must be installed on the control node, not on every managed node.

If using Windows, an Ubuntu WSL environment or a dedicated Ubuntu EC2 instance can serve as the control node. The following commands assume Ubuntu or Debian.

### Update package lists

```bash
sudo apt update
```

### Install Ansible

```bash
sudo apt install ansible -y
```

### Verify the installation

```bash
ansible --version
```

The output should display information such as the Ansible version, configuration file location, and Python version.

### Why install Ansible only on the control node?

The control node runs Ansible and initiates connections to managed nodes. The managed nodes receive and execute the required operations over SSH without needing a continuously running Ansible agent.

## 5. Creating the Inventory File

An inventory tells Ansible which machines it can manage. It can also organize machines into groups so that commands can target specific servers.

### Step 1: Create the project directory

```bash
mkdir ansible-practice
cd ansible-practice
```

### Step 2: Create `inventory.ini`

```ini
[web]
web-server ansible_host=<PUBLIC_IP_1>

[app]
app-server ansible_host=<PUBLIC_IP_2>

[db]
db-server ansible_host=<PUBLIC_IP_3>

[all:vars]
ansible_user=ec2-user
ansible_ssh_private_key_file=/absolute/path/to/your-key.pem
```

Replace the IP placeholders with the actual public IP addresses of your EC2 instances. Replace the private key path with the real absolute path to your key.

For Ubuntu managed nodes, change:

```ini
ansible_user=ubuntu
```

The `web`, `app`, and `db` entries are inventory groups. Each host alias maps to an actual server through `ansible_host`.

### Step 3: Protect the SSH private key

On a Linux control node, run:

```bash
chmod 400 /absolute/path/to/your-key.pem
```

This restricts access to the private key. Keep the key outside your public repository.

### Step 4: Test connectivity

```bash
ansible all -i inventory.ini -m ping
```

A successful result resembles:

```text
web-server | SUCCESS => {
    "changed": false,
    "ping": "pong"
}

app-server | SUCCESS => {
    "changed": false,
    "ping": "pong"
}

db-server | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

*These are illustrative outputs. Replace them with your actual terminal output when documenting your lab.*

The Ansible `ping` module verifies that Ansible can connect to the host and execute the module. It is not an ICMP network ping.

### Troubleshooting connectivity

If the command fails, check the following:

- The public IP addresses in `inventory.ini` are correct.
- The EC2 security group allows SSH from the control node.
- The private key path is valid and its permissions are restricted.
- The username matches the managed node's operating system.
- The SSH service is running and the instance is reachable.
- Python is available on the managed node.
- The instance's network configuration allows SSH traffic.

## 6. Running Ad-hoc Commands

Ad-hoc commands let us execute one-off tasks without writing a playbook.

The general syntax is:

```bash
ansible <host-pattern> -i inventory.ini -m <module> -a "<arguments>"
```

Here:

- `host-pattern` selects the target hosts or groups.
- `-i` specifies the inventory file.
- `-m` selects the module.
- `-a` supplies the module arguments.

### Command 1: Check connectivity

```bash
ansible all -i inventory.ini -m ping
```

**Purpose:** Verify that Ansible can reach all managed nodes and execute a module.

**Expected result:** Each host reports `SUCCESS` with `"ping": "pong"`.

### Command 2: Check system uptime

```bash
ansible all -i inventory.ini -m command -a "uptime"
```

**Purpose:** Display how long each server has been running and its system load averages.

**Expected result:** Each host returns its uptime information.

### Command 3: Check memory on web servers

```bash
ansible web -i inventory.ini -m command -a "free -h"
```

**Purpose:** Display memory usage in a human-readable format on the web server group only.

**Expected result:** Memory information is returned for hosts in the `web` group.

### Command 4: Check disk usage

```bash
ansible all -i inventory.ini -m command -a "df -h"
```

**Purpose:** Display mounted filesystems and their disk usage on all managed nodes.

**Expected result:** Each host returns its filesystem usage information.

### Command 5: Copy and verify a file

Create a local file on the control node:

```bash
echo "Hello from Ansible" > hello.txt
```

Copy it to every managed node:

```bash
ansible all -i inventory.ini -m copy \
  -a "src=hello.txt dest=/tmp/hello.txt"
```

Verify the file contents:

```bash
ansible all -i inventory.ini -m command \
  -a "cat /tmp/hello.txt"
```

**Purpose:** Demonstrate remote file distribution and verification.

**Expected result:** Each managed node should display `Hello from Ansible`.

### Additional task: Install Git on the web group

For Amazon Linux 2:

```bash
ansible web -i inventory.ini -m yum \
  -a "name=git state=present" --become
```

For Ubuntu managed nodes:

```bash
ansible web -i inventory.ini -m apt \
  -a "name=git state=present update_cache=yes" --become
```

The `--become` option enables privilege escalation, usually to root, similar to using `sudo`. It is commonly needed for package installation and system-level configuration.

**Security note:** Use privilege escalation only when necessary and ensure the remote account has the appropriate permissions.

## 7. Exploring Inventory Groups and Patterns

Inventory groups make it possible to target several servers with one command.

Add the following group definitions to `inventory.ini`:

```ini
[application:children]
web
app

[all_servers:children]
application
db
```

Here, `application` contains the `web` and `app` groups. The `all_servers` group contains `application` and `db`.

### Run commands against groups

```bash
ansible application -i inventory.ini -m ping
```

Targets web and app servers.

```bash
ansible db -i inventory.ini -m ping
```

Targets only the database group.

```bash
ansible all_servers -i inventory.ini -m ping
```

Targets all three groups of managed servers.

### Use inventory patterns

```bash
ansible 'web:app' -i inventory.ini -m ping
```

Targets hosts in either the `web` or `app` group.

```bash
ansible 'all:!db' -i inventory.ini -m ping
```

Targets all hosts except those in the `db` group.

Inventory groups and patterns help us run tasks against the correct servers without repeating commands for individual hosts.

## 8. Configuring `ansible.cfg`

To avoid specifying the inventory and SSH settings repeatedly, create a file named `ansible.cfg` in the project directory.

```ini
[defaults]
inventory = inventory.ini
remote_user = ec2-user
private_key_file = /absolute/path/to/your-key.pem
```

For Ubuntu managed nodes, change `remote_user` to `ubuntu`.

I can now run:

```bash
ansible all -m ping
```

Ansible reads the local project configuration when it is eligible to do so. The local `ansible.cfg` should be in the current working directory and must be the configuration Ansible selects.

To verify the active configuration file:

```bash
ansible --version
```

**Security note:** Avoid disabling SSH host-key checking in shared or production environments. For a disposable lab, host-key issues should be investigated rather than automatically bypassed. Keep SSH authentication and host verification secure.

## 9. Difference Between `command` and `shell`

Both modules execute commands on managed nodes, but they handle command interpretation differently.

| Feature | `command` module | `shell` module |
|---|---|---|
| Execution | Runs a command directly | Runs a command through a shell |
| Pipes (`|`) | Not interpreted as shell pipes | Supported |
| Redirection (`>`, `>>`) | Not interpreted as shell redirection | Supported |
| Environment expansion | No normal shell expansion | Supports shell expansion |
| Security | Preferred for simple commands | Use when shell features are required |

Example using `command`:

```bash
ansible all -m command -a "uptime"
```

Example using `shell`:

```bash
ansible all -m shell -a "df -h | grep '/dev/'"
```

**Best practice:** Prefer `command` for straightforward commands. Use `shell` when you specifically need shell features such as pipes, redirection, or variable expansion.

## 10. Troubleshooting Reference

| Problem | What to check |
|---|---|
| SSH connection fails | IP address, security group, routing, SSH service, and key path |
| Permission denied | SSH username, correct private key, and key permissions |
| Host unreachable | Instance status, network connectivity, and public/private IP selection |
| Python-related module failure | Python availability and compatibility on the managed node |
| Package installation fails | Correct package manager, repository availability, and `--become` permissions |
| Inventory host not found | Host alias, group names, inventory path, and INI syntax |
| Configuration file not applied | Current directory and the file reported by `ansible --version` |

## 11. Evidence and Screenshots

Add your own screenshots and actual command outputs before publishing this documentation.

- [ ] Ansible installation and `ansible --version` output
- [ ] EC2 instances running in AWS
- [ ] `inventory.ini` with grouped hosts (redact public IPs and sensitive paths if needed)
- [ ] Successful `ansible all -m ping` output for every managed node
- [ ] Uptime output from all servers
- [ ] Memory output from the web group
- [ ] Disk usage output from all servers
- [ ] File-copy and verification output
- [ ] Group-pattern command results

**Screenshot placeholders**

### Ansible installation

_Add screenshot here._

### Inventory setup

_Add screenshot here._

### Successful connectivity test

_Add screenshot here._

### Ad-hoc command results

_Add screenshots here._

## 12. Key Learnings

- Configuration management helps maintain consistent server configurations.
- Ansible uses a control node, inventory, modules, and playbooks to automate tasks.
- Ansible is agentless by default and commonly connects to Linux hosts through SSH.
- Inventory groups and patterns make it easier to target the correct servers.
- Ad-hoc commands are useful for one-off operations, while playbooks are better for repeatable automation.
- `--become` enables privilege escalation for tasks that require elevated permissions.
- The `command` module is suitable for simple commands, while `shell` supports shell-specific features.
- Terraform and Ansible complement each other: Terraform provisions infrastructure, and Ansible configures the servers.

## Conclusion

Day 68 introduced Ansible and its role in configuration management. By setting up a control node, connecting to EC2 managed nodes, organizing an inventory, and running ad-hoc commands, I practised the fundamentals of server automation.

This foundation will help me move towards writing Ansible playbooks for repeatable configuration, package installation, service management, and application deployment.

#90DaysOfDevOps | Ansible | AWS | ConfigurationManagement | Automation