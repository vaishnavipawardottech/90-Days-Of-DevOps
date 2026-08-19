# Day 15 – Networking Concepts: DNS, IP, Subnets & Ports

## Task

Today I built on the networking fundamentals from Day 14 and focused on the core networking concepts used in DevOps:

* DNS and name resolution
* IPv4 addressing
* Public and private IP addresses
* CIDR notation and subnetting
* Common network ports
* How DNS, IP addresses, ports, and services work together

---

# Task 1: DNS – How Names Become IPs

## 1. What happens when you type `google.com` in a browser?

When I type `google.com` in a browser, the system first needs to find the IP address associated with the domain name.

DNS (Domain Name System) translates the domain name into an IP address.

After getting the IP address, the browser establishes a network connection with the server and sends an HTTP/HTTPS request.

The server then sends the response back to the browser.


---

## 2. DNS Record Types

### A Record

An `A` record maps a domain name to an **IPv4 address**.

Example:

```text
google.com → 142.x.x.x
```

### AAAA Record

An `AAAA` record maps a domain name to an **IPv6 address**.

### CNAME Record

A `CNAME` record maps one domain name to another domain name.

Example:

```text
www.example.com → example.com
```

### MX Record

An `MX` record specifies the **mail servers** responsible for receiving email for a domain.

### NS Record

An `NS` record identifies the **authoritative name servers** for a domain.

---

## 3. Check DNS Using `dig`

### Command

```bash
dig google.com
```

### Short command

```bash
dig +short google.com
```

The full `dig` output contains an **ANSWER SECTION**.

Example:

```text
;; ANSWER SECTION:
google.com.    300    IN    A    <IP_ADDRESS>
```

From this output:

```text
Record Type: A
IP Address: <IP_ADDRESS>
TTL: 300 seconds
```

### My Result

```text
A Record IP: 172.253.63.102

TTL: 96 seconds
```

> Replace the above values with the actual values from the `dig google.com` output.

---

# Task 2: IP Addressing

## 1. What is an IPv4 Address?

An IPv4 address is a logical address used to identify a device/interface on an IP network.

An IPv4 address contains **32 bits**, divided into four 8-bit sections called octets.

Example:

```text
192.168.1.10
```

Each octet can have a value from:

```text
0 – 255
```

The four octets together make a 32-bit IPv4 address.

```text
192     .     168     .     1     .     10
 ↓             ↓            ↓          ↓
8 bits       8 bits       8 bits     8 bits

Total = 32 bits
```

---

## 2. Public vs Private IP Addresses

### Private IP

A private IP is used inside private networks such as home networks, company networks, and AWS VPCs.

Example:

```text
10.0.1.25
```

Private IP addresses are not directly routable over the public internet.

### Public IP

A public IP is an address that can be used for communication over the internet.

Example:

```text
8.8.8.8
```

An EC2 instance can have both:

```text
Private IP → Used inside the AWS VPC
Public IP  → Used for communication with the internet
```

---

## 3. Private IPv4 Address Ranges

The three private IPv4 ranges are:

| Range                           | CIDR             |
| ------------------------------- | ---------------- |
| `10.0.0.0 – 10.255.255.255`     | `10.0.0.0/8`     |
| `172.16.0.0 – 172.31.255.255`   | `172.16.0.0/12`  |
| `192.168.0.0 – 192.168.255.255` | `192.168.0.0/16` |

In short:

```text
10.x.x.x
172.16.x.x – 172.31.x.x
192.168.x.x
```

---

## 4. Check IP Addresses on EC2

### Command

```bash
ip addr show
```

This displays the network interfaces and IP addresses assigned to my EC2 instance.

I can also use:

```bash
hostname -I
```

### My EC2 IP

```text
Private IP: 172.31.6.158
```

### How I identified it

The IP address assigned to my EC2 network interface falls within one of the private ranges:

```text
10.x.x.x
172.16.x.x – 172.31.x.x
192.168.x.x
```

Therefore, it is a **private IP address**.

---

# Task 3: CIDR & Subnetting

## 1. What does `/24` mean?

Consider:

```text
192.168.1.0/24
```

The `/24` means that the first **24 bits** are used for the network portion.

IPv4 has 32 bits total:

```text
Network bits       Host bits
<------24------>   <-8->
```

Therefore:

```text
32 - 24 = 8 host bits
```

The equivalent subnet mask is:

```text
255.255.255.0
```

---

## 2. Number of IPs and Usable Hosts

The number of addresses can be calculated using:

```text
Total IPs = 2^(host bits)
```

For traditional IPv4 subnets:

```text
Usable hosts = Total IPs - 2
```

The two reserved addresses are generally:

```text
Network address
Broadcast address
```

---

## 3. CIDR Table

| CIDR  | Subnet Mask       | Total IPs | Usable Hosts |
| ----- | ----------------- | --------: | -----------: |
| `/24` | `255.255.255.0`   |       256 |          254 |
| `/16` | `255.255.0.0`     |    65,536 |       65,534 |
| `/28` | `255.255.255.240` |        16 |           14 |

### Example: `/24`

```text
32 - 24 = 8 host bits

2^8 = 256 total IPs

256 - 2 = 254 usable hosts
```

### Example: `/28`

```text
32 - 28 = 4 host bits

2^4 = 16 total IPs

16 - 2 = 14 usable hosts
```

---

## 4. Why Do We Subnet?

Subnetting divides a larger network into smaller networks.

We subnet networks to:

* Use IP addresses efficiently
* Separate different groups of systems
* Reduce unnecessary network traffic
* Improve network organization
* Apply different security and routing rules

### Example

Instead of having one large network:

```text
10.0.0.0/16
```

we can divide it into smaller networks:

```text
10.0.1.0/24 → Application servers

10.0.2.0/24 → Database servers

10.0.3.0/24 → DevOps/management systems
```

This makes the network easier to manage and secure.

---

# Task 4: Ports – The Doors to Services

## 1. What is a Port?

A port is a logical number used to identify a specific service or application running on a device.

An IP address identifies the **machine**.

A port identifies the **service/application** on that machine.

For example:

```text
10.0.1.50:3306
```

Here:

```text
10.0.1.50 → IP address of the machine
3306      → Port used by MySQL
```

### Simple Example

Think of:

```text
IP Address = Building address
Port       = Door number
Service    = Person/office behind the door
```

---

## 2. Common Ports

|    Port | Service | Purpose                               |
| ------: | ------- | ------------------------------------- |
|    `22` | SSH     | Secure remote access to Linux servers |
|    `80` | HTTP    | Unencrypted web traffic               |
|   `443` | HTTPS   | Encrypted web traffic                 |
|    `53` | DNS     | Domain name resolution                |
|  `3306` | MySQL   | MySQL database                        |
|  `6379` | Redis   | Redis database/cache                  |
| `27017` | MongoDB | MongoDB database                      |

---

## 3. Check Listening Ports

Run:

```bash
sudo ss -tulpn
```

This shows TCP and UDP sockets that are currently listening.

Important options:

```text
-t → TCP
-u → UDP
-l → Listening
-p → Process
-n → Numeric output
```

### Example

```text
LISTEN 0 128 0.0.0.0:22
```

This means a service is listening on port `22`.

---

## My EC2 Listening Ports

Run:

```bash
sudo ss -tulpn
```

Then identify at least two ports.

|       Port | Service    | Status    |
| ---------: | ---------- | --------- |
|       `22` | SSH        | Listening |
|      `323` | cron     | Listening |


---

# Task 5: Putting It Together

## 1. `curl http://myapp.com:8080`

If I run:

```bash
curl http://myapp.com:8080
```

DNS is used to resolve `myapp.com` to an IP address. Port `8080` identifies the application/service running on the destination. HTTP is then used to communicate with that service over the network.


---

## 2. Application cannot reach `10.0.1.50:3306`

If my application cannot connect to:

```text
10.0.1.50:3306
```

I would first check whether the database server is reachable and whether port `3306` is listening.

I would check:

```bash
ping -c 4 10.0.1.50
```

Then:

```bash
nc -zv 10.0.1.50 3306
```

I would also check the database service, firewall/security group rules, and whether MySQL is configured to accept remote connections.


---

These concepts are important for troubleshooting connectivity and understanding how applications communicate in cloud and DevOps environments.
