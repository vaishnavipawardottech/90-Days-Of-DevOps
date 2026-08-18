# Day 14 – Networking Fundamentals & Hands-on Checks

## Task

Today I practiced Linux networking fundamentals and used common networking commands for connectivity, troubleshooting, DNS, ports, and HTTP checks.

The goal was to understand how different networking layers work and how to troubleshoot a network issue using simple Linux commands.

---

## 1. OSI Model vs TCP/IP Model

### OSI Model

The OSI model has 7 layers:

1. **Layer 7 – Application**
   Provides network services directly to applications.
   Examples: HTTP, HTTPS, DNS, SSH

2. **Layer 6 – Presentation**
   Handles data formatting, encryption, and compression.

3. **Layer 5 – Session**
   Establishes and manages communication sessions.

4. **Layer 4 – Transport**
   Provides end-to-end communication.
   Examples: TCP and UDP

5. **Layer 3 – Network**
   Handles IP addressing and routing.
   Example: IPv4/IPv6

6. **Layer 2 – Data Link**
   Handles communication between devices on the same network.
   Examples: Ethernet, MAC addresses

7. **Layer 1 – Physical**
   Deals with physical transmission of bits through cables, radio, or other media.

### TCP/IP Model

The TCP/IP model commonly has 4 layers:

* **Application** → HTTP, HTTPS, DNS, SSH
* **Transport** → TCP, UDP
* **Internet** → IP
* **Link** → Ethernet, ARP and physical/network access

### OSI vs TCP/IP Mapping

| OSI          | TCP/IP      |
| ------------ | ----------- |
| Application  | Application |
| Presentation | Application |
| Session      | Application |
| Transport    | Transport   |
| Network      | Internet    |
| Data Link    | Link        |
| Physical     | Link        |

---

## 2. Where Common Protocols Fit

* **IP** → Network layer in OSI / Internet layer in TCP/IP
* **TCP/UDP** → Transport layer
* **HTTP/HTTPS** → Application layer
* **DNS** → Application layer

### Real Example

```text
curl https://example.com
        ↓
HTTP/HTTPS (Application)
        ↓
TCP (Transport)
        ↓
IP (Internet/Network)
        ↓
Ethernet/Network Interface (Link)
```

The `curl` command works at the application level, while the request is transported using TCP and addressed using IP.

---

# 3. Hands-on Networking Checks

For this practice, I used:

```text
Target host: google.com
```

---

## 3.1 Check My IP Address

### Command

```bash
hostname -I
```

### Alternative

```bash
ip addr show
```

### What it does

`hostname -I` displays the IP addresses assigned to the machine.

`ip addr show` provides more detailed information about network interfaces, IP addresses, and interface status.

### Observation

```text
My EC2 instance has a private IP address assigned to its network interface.
```

---

## 3.2 Check Reachability

### Command

```bash
ping -c 4 google.com
```

### What it does

`ping` checks whether the target host is reachable over the network.

The `-c 4` option sends 4 packets and then stops.

Example output:

```text
4 packets transmitted, 4 received, 0% packet loss
```

### What to check

* Packets transmitted
* Packets received
* Packet loss
* Average latency

### Observation

```text
google.com was reachable with 0% packet loss.
The average latency was approximately 3005 ms.
```

---

## 3.3 Trace the Network Path

### Command

```bash
traceroute google.com
```

If `traceroute` is not installed:

```bash
sudo apt update
sudo apt install traceroute -y
```

Alternative:

```bash
tracepath google.com
```

### What it does

`traceroute` shows the network hops between your machine and the destination.

Each hop represents a router/network device through which the packet travels.

### Observation

```text
The request passed through multiple network hops before reaching google.com.
Some hops may show timeouts (* * *), which can happen when routers do not respond to traceroute packets.
```

---

## 3.4 Check Listening Ports

### Command

```bash
sudo ss -tulpn
```

### What it does

`ss` displays socket and network connection information.

Options:

* `-t` → TCP sockets
* `-u` → UDP sockets
* `-l` → Listening sockets
* `-p` → Show process information
* `-n` → Show numerical addresses and ports

Example:

```text
LISTEN 0 128 0.0.0.0:22
```

This means a service is listening on port `22`.

### Observation

```text
SSH is listening on port 22 on my EC2 instance.
```

If you see another service such as Nginx:

```text
0.0.0.0:80
```

then HTTP is listening on port 80.

---

## 3.5 DNS / Name Resolution

### Command

```bash
dig google.com
```

If `dig` is not installed:

```bash
sudo apt update
sudo apt install dnsutils -y
```

### Short version

```bash
dig +short google.com
```

### What it does

DNS converts a domain name such as:

```text
google.com
```

into an IP address.

`dig +short` shows only the resolved IP address.

### Observation

```text
DNS successfully resolved google.com to an IP address.
```

---

## 3.6 HTTP Check

### Command

```bash
curl -I https://google.com
```

### What it does

`curl` makes an HTTP request.

The `-I` option requests only the HTTP response headers.

Example:

```text
HTTP/2 200
```

### What the status means

* `200` → Request successful
* `301/302` → Redirect
* `400` → Bad request
* `403` → Forbidden
* `404` → Not found
* `500` → Internal server error
* `502` → Bad gateway
* `503` → Service unavailable

### Observation

```text
The HTTP request was successful and returned status code 200/301.
```

---

# 4. Connections Snapshot

### Command

```bash
sudo netstat -an | head
```

If `netstat` is not installed:

```bash
sudo apt update
sudo apt install net-tools -y
```

### Alternative

```bash
sudo ss -tan
```

### What it does

`netstat -an` displays network connections and listening sockets.

Important states include:

* `LISTEN` → Waiting for incoming connections
* `ESTABLISHED` → Active connection
* `TIME_WAIT` → Connection recently closed

The `head` command shows only the first few lines.

### Observation

```text
I checked the current network connections and identified LISTEN and ESTABLISHED connections.
```

---

# 5. Mini Task – Port Probe

## Step 1: Identify a Listening Port

Run:

```bash
sudo ss -tulpn
```

For example, if SSH is running:

```text
0.0.0.0:22
```

The listening port is:

```text
22
```

---

## Step 2: Test the Port

Install netcat if required:

```bash
sudo apt update
sudo apt install netcat-openbsd -y
```

Then test:

```bash
nc -zv localhost 22
```

Example successful output:

```text
Connection to localhost 22 port [tcp/ssh] succeeded!
```

### What it does

`nc` (netcat) can be used to test network connections.

Options:

* `-z` → Scan without sending data
* `-v` → Verbose output

### Observation

```text
Port 22 was reachable from the same machine, which confirms that the SSH service is listening locally.
```

---

# 6. Quick Networking Troubleshooting Flow

When something is not working, I can check the network step by step:

```text
1. Check IP
      ↓
hostname -I

2. Check basic connectivity
      ↓
ping google.com

3. Check network path
      ↓
traceroute google.com

4. Check DNS
      ↓
dig google.com

5. Check listening ports
      ↓
sudo ss -tulpn

6. Check HTTP service
      ↓
curl -I https://google.com
```

This helps identify whether the problem is related to the local network, routing, DNS, ports, or the application.

---

# 7. Reflection

### Which command gives the fastest signal when something is broken?

`ping` gives a quick indication of basic network reachability.

However, `ping` alone does not prove that a specific application or port is working.

For example, a server can respond to ping while its HTTP service is down.

---

### What layer would I inspect if DNS fails?

DNS operates at the **Application layer**.

If DNS fails, I would check:

```bash
dig google.com
```

Then I would check the configured DNS servers:

```bash
cat /etc/resolv.conf
```

I could also check basic network connectivity:

```bash
ping -c 4 8.8.8.8
```

This helps determine whether the problem is DNS-specific or a more general network problem.

---

### What layer would I inspect if HTTP 500 appears?

HTTP 500 is an **Application-layer** error.

It usually means that the request reached the server, but something went wrong inside the application/server.

I would check:

```bash
curl -I https://example.com
```

Then check the application or web server logs.

For example, for Nginx:

```bash
sudo tail -f /var/log/nginx/error.log
```

For a systemd service:

```bash
sudo journalctl -u <service-name>
```

---

## 8. Two Follow-up Checks in a Real Incident

### Check 1 – Verify the service

```bash
sudo systemctl status <service-name>
```

This tells me whether the required service is running.

### Check 2 – Check the firewall

```bash
sudo ufw status
```

This helps determine whether the required port is being blocked by the server firewall.

I would also check AWS Security Group rules when troubleshooting an EC2 instance.

---

# 9. Commands Practiced

```bash
hostname -I
ip addr show

ping -c 4 google.com

traceroute google.com
tracepath google.com

sudo ss -tulpn

dig +short google.com
nslookup google.com

curl -I https://google.com

sudo netstat -an | head

nc -zv localhost 22

sudo systemctl status <service-name>
sudo ufw status
```
