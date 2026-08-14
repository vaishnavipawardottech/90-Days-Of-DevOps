# Day 08 – Cloud Server Setup: Docker, Nginx & Web Deployment

## Objective

Deploy a web server on an AWS EC2 cloud instance and practice basic cloud server management.

In this task, I:

- Launched an AWS EC2 instance
- Connected to the server using SSH
- Installed Docker and Nginx
- Configured the EC2 Security Group to allow HTTP traffic on port 80
- Verified that Nginx is running
- Accessed the Nginx web page from the internet
- Viewed Nginx logs
- Extracted Nginx logs into a separate file

---

# Part 1: Launch Cloud Instance & SSH Access

## Step 1: Create a Cloud Instance

I launched an Ubuntu Server instance using AWS EC2.

The EC2 instance provides a virtual Linux server running in the AWS cloud.

## Step 2: Connect via SSH

I connected to the EC2 instance using SSH with the private key associated with the instance.

```bash
ssh -i <your-key.pem> ubuntu@<your-instance-public-ip>
```

After successfully connecting, I verified the server using:

```bash
whoami
```

```bash
hostname
```

```bash
uname -a
```

These commands confirmed that I was connected to the remote Ubuntu server.

---

# Part 2: Install Docker & Nginx

## Step 1: Update System

I updated the package information before installing new software.

```bash
sudo apt update
```

I also upgraded the installed packages:

```bash
sudo apt upgrade -y
```

## Step 2: Install Docker

I installed Docker using the Ubuntu package manager.

```bash
sudo apt install docker.io -y
```

I verified the Docker installation:

```bash
docker --version
```

I checked the Docker service:

```bash
sudo systemctl status docker
```

I also verified that Docker is enabled:

```bash
sudo systemctl is-enabled docker
```

## Step 3: Install Nginx

I installed Nginx using the Ubuntu package manager.

```bash
sudo apt install nginx -y
```

## Verify Nginx is Running

I checked the status of the Nginx service:

```bash
sudo systemctl status nginx
```

I also verified that Nginx is enabled:

```bash
sudo systemctl is-enabled nginx
```

I checked the Nginx version:

```bash
nginx -v
```

---

# Part 3: Security Group Configuration

The EC2 Security Group controls inbound and outbound network traffic for the instance.

I configured an inbound rule to allow HTTP traffic on port `80`.

## Inbound Rule

```text
Type: HTTP
Protocol: TCP
Port: 80
Source: 0.0.0.0/0
```

This allows users on the internet to access the Nginx web server through HTTP.

## Test Web Access

I opened the following URL in my browser:

```text
http://<your-instance-public-ip>
```

The Nginx welcome page was displayed successfully.

---

# Part 4: Extract Nginx Logs

## Step 1: View Nginx Logs

Nginx access logs are stored in:

```text
/var/log/nginx/access.log
```

I viewed the access logs using:

```bash
sudo cat /var/log/nginx/access.log
```

I viewed the latest log entries using:

```bash
sudo tail -n 20 /var/log/nginx/access.log
```

I also checked the Nginx error logs:

```bash
sudo tail -n 20 /var/log/nginx/error.log
```

## Step 2: Save Logs to File

I extracted the Nginx access logs into a file named `nginx-logs.txt`.

```bash
sudo cat /var/log/nginx/access.log > ~/nginx-logs.txt
```

I verified the file:

```bash
ls -l ~/nginx-logs.txt
```

I checked its contents:

```bash
cat ~/nginx-logs.txt
```

## Step 3: Verify the Extracted Log File

I checked the number of lines:

```bash
wc -l ~/nginx-logs.txt
```

I also checked the latest entries:

```bash
tail -n 10 ~/nginx-logs.txt
```

---

# Commands Used

## AWS / SSH

```bash
ssh -i <your-key.pem> ubuntu@<your-instance-public-ip>
```

```bash
whoami
```

```bash
hostname
```

```bash
uname -a
```

## System Update

```bash
sudo apt update
```

```bash
sudo apt upgrade -y
```

## Docker

```bash
sudo apt install docker.io -y
```

```bash
docker --version
```

```bash
sudo systemctl status docker
```

```bash
sudo systemctl is-enabled docker
```

## Nginx

```bash
sudo apt install nginx -y
```

```bash
sudo systemctl status nginx
```

```bash
sudo systemctl is-enabled nginx
```

```bash
nginx -v
```

## Nginx Logs

```bash
sudo cat /var/log/nginx/access.log
```

```bash
sudo tail -n 20 /var/log/nginx/access.log
```

```bash
sudo tail -n 20 /var/log/nginx/error.log
```

```bash
sudo cat /var/log/nginx/access.log > ~/nginx-logs.txt
```

```bash
ls -l ~/nginx-logs.txt
```

```bash
cat ~/nginx-logs.txt
```

```bash
wc -l ~/nginx-logs.txt
```

---

# Challenges Faced

- 

---

# What I Learned

- Learned how to launch and manage a Linux server using AWS EC2.
- Learned how to connect to a remote cloud server using SSH.
- Learned how Security Groups control inbound network access to an EC2 instance.
- Learned how to install and manage Docker and Nginx using Linux commands.
- Learned how to verify whether services are running using `systemctl`.
- Learned how to access Nginx from the internet using the server's public IP.
- Learned where Nginx access and error logs are stored.
- Learned how to extract server logs into a separate file for further analysis.

---

# Why This Matters for DevOps

- **Cloud Infrastructure:** DevOps engineers regularly provision and manage cloud servers for applications and services.
- **Remote Server Management:** SSH is one of the fundamental ways to securely access and manage Linux servers.
- **Security:** Security Groups control which network traffic can reach cloud resources.
- **Service Deployment:** Installing and managing services such as Nginx is a common server administration task.
- **Log Management:** Logs are essential for monitoring applications, investigating errors, and troubleshooting production issues.
- **Web Deployment:** Configuring a server and making a web application accessible over the internet is a fundamental DevOps workflow.

---

# Screenshots

The following screenshots were captured during the task:



---
