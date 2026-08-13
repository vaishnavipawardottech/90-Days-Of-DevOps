# Day 02 – Linux Architecture, Processes, and systemd

## 1. Linux Architecture

Linux works through different layers:

```text
Applications
     ↓
   Shell
     ↓
   Kernel
     ↓
  Hardware
```

* **Applications** – Programs that we use, such as Terminal, browsers, editors, or other software.
* **Shell** – Provides an interface to interact with Linux using commands.
* **Kernel** – The core of Linux that manages CPU, memory, files, devices, and hardware resources.
* **Hardware** – Physical components such as CPU, RAM, disk, and network devices.

---

## 2. Linux Boot Process

When a Linux system starts:

```text
BIOS / UEFI
     ↓
Bootloader
     ↓
Kernel
     ↓
systemd
     ↓
Services
     ↓
Login / User
```

1. **BIOS / UEFI** – Initializes the hardware and checks that the system is ready to start.
2. **Bootloader** – Loads the Linux kernel into memory.
3. **Kernel** – Initializes hardware and starts managing system resources.
4. **systemd** – Starts and manages the required system services. The default init system having PID 1.
5. **Services** – Background services are started and prepared for use.
6. **Login / User** – The system becomes ready for the user to log in and work.

---

## 3. What is a Process?

* A **process** is a program that is currently running.
* Every process has a unique **PID (Process ID)**.
* Linux creates processes using fork() and exec().
* fork() creates a new process, and exec() runs a new program in that process.
* Linux manages processes by allocating CPU and memory resources to them.
* Linux creates and manages processes when applications or commands run.

For example:

```bash
ls
```

When we run `ls`, Linux creates a process to execute that command.

---

## 4. Process States

A process can have different states:

* **Running (R)** – Process is running or ready to run.
* **Sleeping (S)** – Process is waiting for something.
* **Stopped (T)** – Process is paused.
* **Zombie (Z)** – Process has finished but is still remains in the Linux kernel's process table.

---

## 5. 5 Useful Linux Commands

1. ps – View running processes.
2. top – Monitor CPU and memory usage in real time.
3. systemctl – Manage system services.
4. df -h – Check disk usage.
5. free -h – Check memory usage.

---

## 6. Why This Matters for DevOps

Linux is commonly used for servers and cloud infrastructure.

Understanding **Linux architecture, processes, and systemd** helps us:

* Understand how Linux works.
* Check running processes.
* Check whether services are running.
* Troubleshoot basic server issues.

---

### #90DaysOfDevops