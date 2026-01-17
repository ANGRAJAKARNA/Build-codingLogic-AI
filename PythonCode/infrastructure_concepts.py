# infrastructure_concepts.py
"""
Infrastructure Concepts - Networking, Servers, and Storage
Comprehensive explanations for IT infrastructure topics including:
- Networking protocols and concepts
- Server administration and configuration
- Storage systems and management
"""

# =============================================================================
# INFRASTRUCTURE CONCEPTS DICTIONARY
# =============================================================================

INFRASTRUCTURE_CONCEPTS = {

    # =========================================================================
    # NETWORKING CONCEPTS
    # =========================================================================

    "tcp": """## 🔄 TCP (Transmission Control Protocol)

**Definition:** Connection-oriented, reliable protocol that ensures data delivery in order.

### Key Characteristics
- **Connection-oriented**: 3-way handshake before data transfer
- **Reliable**: Guarantees delivery with acknowledgments
- **Ordered**: Packets arrive in sequence
- **Error checking**: Checksums for data integrity
- **Flow control**: Prevents overwhelming receiver
- **Congestion control**: Adjusts to network conditions

### TCP 3-Way Handshake
```
Client                    Server
  |                          |
  |-------- SYN ---------->  |  Step 1: Client initiates
  |                          |
  |<----- SYN-ACK ---------  |  Step 2: Server acknowledges
  |                          |
  |-------- ACK ---------->  |  Step 3: Client confirms
  |                          |
  |===== Connection Open ====|
```

### TCP Connection Termination (4-Way)
```
Client                    Server
  |                          |
  |-------- FIN ---------->  |  Client wants to close
  |<------- ACK -----------  |  Server acknowledges
  |<------- FIN -----------  |  Server ready to close
  |-------- ACK ---------->  |  Client confirms
  |                          |
  |===== Connection Closed ==|
```

### TCP vs UDP Comparison
| Feature | TCP | UDP |
|---------|-----|-----|
| Connection | Connection-oriented | Connectionless |
| Reliability | Guaranteed delivery | No guarantee |
| Order | Ordered packets | No ordering |
| Speed | Slower (overhead) | Faster |
| Header Size | 20-60 bytes | 8 bytes |
| Use Cases | HTTP, FTP, Email | DNS, Streaming, Gaming |

### Common TCP Ports
| Port | Service | Description |
|------|---------|-------------|
| 20/21 | FTP | File Transfer |
| 22 | SSH | Secure Shell |
| 23 | Telnet | Remote Login (insecure) |
| 25 | SMTP | Email Sending |
| 80 | HTTP | Web Traffic |
| 443 | HTTPS | Secure Web |
| 3306 | MySQL | Database |
| 5432 | PostgreSQL | Database |
| 6379 | Redis | Cache/Database |

### TCP States
```
LISTEN       -> Waiting for connection request
SYN_SENT     -> Connection request sent
SYN_RECEIVED -> Received SYN, sent SYN-ACK
ESTABLISHED  -> Connection is active
FIN_WAIT_1   -> Sent FIN, waiting for ACK
FIN_WAIT_2   -> Received ACK, waiting for FIN
CLOSE_WAIT   -> Received FIN, waiting to close
CLOSING      -> Both sides closing simultaneously
TIME_WAIT    -> Waiting before final close (2MSL)
CLOSED       -> Connection terminated
```

### Check TCP Connections
```bash
# View all TCP connections
netstat -ant

# View connections on specific port
netstat -ant | grep :80

# Using ss (modern alternative)
ss -t -a

# Count connections by state
netstat -ant | awk '{print $6}' | sort | uniq -c
```

**💡 When to Use TCP:** File transfers, web browsing, email, database connections - any application requiring reliable, ordered data delivery.""",

    "udp": """## 📡 UDP (User Datagram Protocol)

**Definition:** Connectionless, lightweight protocol for fast data transmission without delivery guarantees.

### Key Characteristics
- **Connectionless**: No handshake, just send
- **Unreliable**: No delivery confirmation
- **No ordering**: Packets may arrive out of order
- **Fast**: Minimal overhead (8-byte header)
- **Stateless**: No connection tracking
- **Broadcast/Multicast**: Supports one-to-many

### UDP Header Structure (8 bytes)
```
 0               16              32
+---------------+---------------+
| Source Port   | Dest Port     |
+---------------+---------------+
| Length        | Checksum      |
+---------------+---------------+
|           Data...             |
```

### Common UDP Ports
| Port | Service | Purpose |
|------|---------|---------|
| 53 | DNS | Domain Name Resolution |
| 67/68 | DHCP | IP Address Assignment |
| 69 | TFTP | Trivial File Transfer |
| 123 | NTP | Time Synchronization |
| 161/162 | SNMP | Network Management |
| 514 | Syslog | System Logging |
| 1194 | OpenVPN | VPN (default) |
| 500 | IKE | IPSec Key Exchange |

### When to Use UDP vs TCP
| Use UDP | Use TCP |
|---------|---------|
| Real-time video/audio | File downloads |
| Online gaming | Email |
| Live streaming | Web browsing |
| VoIP calls | Database queries |
| DNS queries | API requests |
| IoT sensors | Financial transactions |

### UDP Use Case Examples
```
Video Streaming (Netflix, YouTube):
- Lost packet = minor glitch
- Retransmitting old frame is useless
- UDP preferred for live content

Online Gaming:
- Low latency is critical
- Old position data is worthless
- Some packet loss acceptable

DNS Queries:
- Small request/response
- Fast turnaround needed
- Can retry if no response

VoIP (Zoom, Skype):
- Real-time audio critical
- Can tolerate some loss
- Latency matters more than perfection
```

### UDP Socket Example (Python)
```python
import socket

# UDP Server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('0.0.0.0', 9999))
data, addr = server.recvfrom(1024)
print(f"Received from {addr}: {data}")

# UDP Client
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b"Hello", ('localhost', 9999))
```

### Test UDP Connectivity
```bash
# Using netcat
nc -u -l 9999          # Listen on UDP port
nc -u localhost 9999   # Connect to UDP port

# Using nmap
nmap -sU -p 53 8.8.8.8  # Scan UDP port
```

**💡 Key Insight:** UDP trades reliability for speed. Perfect when data is time-sensitive and occasional loss is acceptable.""",

    "http": """## 🌐 HTTP (HyperText Transfer Protocol)

**Definition:** Application-layer protocol for transmitting hypermedia documents, the foundation of web communication.

### HTTP Methods
| Method | Purpose | Safe | Idempotent | Body |
|--------|---------|------|------------|------|
| GET | Retrieve resource | Yes | Yes | No |
| POST | Create resource | No | No | Yes |
| PUT | Replace resource | No | Yes | Yes |
| PATCH | Partial update | No | No | Yes |
| DELETE | Remove resource | No | Yes | Optional |
| HEAD | Get headers only | Yes | Yes | No |
| OPTIONS | Get allowed methods | Yes | Yes | No |

### HTTP Status Codes

**1xx - Informational**
```
100 Continue           - Continue with request
101 Switching Protocols - Upgrade to WebSocket
```

**2xx - Success**
```
200 OK                 - Request succeeded
201 Created            - Resource created
204 No Content         - Success, no body
```

**3xx - Redirection**
```
301 Moved Permanently  - Resource moved (cache)
302 Found              - Temporary redirect
304 Not Modified       - Use cached version
307 Temporary Redirect - Keep method
308 Permanent Redirect - Keep method
```

**4xx - Client Errors**
```
400 Bad Request        - Malformed request
401 Unauthorized       - Authentication required
403 Forbidden          - Access denied
404 Not Found          - Resource doesn't exist
405 Method Not Allowed - Wrong HTTP method
408 Request Timeout    - Client too slow
429 Too Many Requests  - Rate limited
```

**5xx - Server Errors**
```
500 Internal Error     - Server error
502 Bad Gateway        - Upstream error
503 Service Unavailable - Server overloaded
504 Gateway Timeout    - Upstream timeout
```

### HTTP Request Structure
```
GET /api/users/123 HTTP/1.1
Host: api.example.com
User-Agent: Mozilla/5.0
Accept: application/json
Authorization: Bearer eyJhbGc...
Content-Type: application/json
Cookie: session=abc123

{"optional": "request body"}
```

### HTTP Response Structure
```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 256
Cache-Control: max-age=3600
Set-Cookie: session=xyz789; HttpOnly

{"id": 123, "name": "John Doe"}
```

### Common Request Headers
| Header | Purpose | Example |
|--------|---------|---------|
| Host | Target server | api.example.com |
| User-Agent | Client info | Mozilla/5.0 |
| Accept | Expected format | application/json |
| Authorization | Auth token | Bearer token123 |
| Content-Type | Body format | application/json |
| Cookie | Session data | session=abc |
| Cache-Control | Caching rules | no-cache |

### Common Response Headers
| Header | Purpose | Example |
|--------|---------|---------|
| Content-Type | Response format | application/json |
| Content-Length | Body size | 1234 |
| Cache-Control | Caching rules | max-age=3600 |
| Set-Cookie | Store cookie | session=xyz |
| Location | Redirect URL | /new-location |
| ETag | Resource version | "abc123" |

### HTTP vs HTTPS
| Feature | HTTP | HTTPS |
|---------|------|-------|
| Port | 80 | 443 |
| Security | Unencrypted | TLS encrypted |
| Certificate | Not required | Required |
| SEO | Lower rank | Higher rank |
| Performance | Faster | HTTP/2 can be faster |

### Test HTTP Requests
```bash
# GET request
curl -X GET https://api.example.com/users

# POST with JSON
curl -X POST https://api.example.com/users \\
  -H "Content-Type: application/json" \\
  -d '{"name": "John"}'

# View headers only
curl -I https://example.com

# Verbose output
curl -v https://example.com
```

**💡 Best Practice:** Always use HTTPS in production for security. HTTP/2 provides better performance with multiplexing.""",


    "dns": """## 🔍 DNS (Domain Name System)

**Definition:** Hierarchical distributed naming system that translates human-readable domain names to IP addresses.

### How DNS Resolution Works
```
1. User types: www.example.com
2. Browser checks local cache
3. OS checks hosts file & local cache
4. Query sent to DNS resolver (ISP/configured)
5. Resolver queries root server (.)
6. Root directs to TLD server (.com)
7. TLD directs to authoritative server
8. Authoritative returns IP: 93.184.216.34
9. Result cached at each level
10. Browser connects to IP
```

### DNS Hierarchy
```
                    . (Root)
                   /   |   \\
              .com   .org   .net
              /        |       \\
         example    google    amazon
         /    \\
       www    mail
```

### DNS Record Types
| Type | Purpose | Example |
|------|---------|---------|
| A | IPv4 address | example.com -> 192.0.2.1 |
| AAAA | IPv6 address | example.com -> 2001:db8::1 |
| CNAME | Alias/Canonical name | www -> example.com |
| MX | Mail server | Priority 10: mail.example.com |
| TXT | Text info (SPF, DKIM) | v=spf1 include:_spf.google.com |
| NS | Name server | ns1.example.com |
| SOA | Start of Authority | Primary DNS, serial, refresh |
| PTR | Reverse lookup | 1.2.0.192.in-addr.arpa -> example.com |
| SRV | Service location | _sip._tcp.example.com |

### DNS Query Types
```
Recursive Query:
- Client asks resolver for complete answer
- Resolver does all the work
- Returns final IP or error

Iterative Query:
- Client asks DNS server
- Server returns referral or answer
- Client follows referrals
```

### DNS Lookup Commands
```bash
# Basic lookup
nslookup example.com
nslookup -type=MX example.com

# dig (detailed)
dig example.com
dig example.com MX
dig example.com +short
dig @8.8.8.8 example.com  # Use specific DNS

# host (simple)
host example.com
host -t MX example.com

# Reverse lookup
dig -x 8.8.8.8
nslookup 8.8.8.8
```

### DNS Caching Levels
```
1. Browser Cache (minutes)
2. OS Cache (hours)
3. Router Cache
4. ISP DNS Cache
5. Authoritative TTL
```

### Common DNS Servers
| Provider | Primary | Secondary |
|----------|---------|-----------|
| Google | 8.8.8.8 | 8.8.4.4 |
| Cloudflare | 1.1.1.1 | 1.0.0.1 |
| OpenDNS | 208.67.222.222 | 208.67.220.220 |
| Quad9 | 9.9.9.9 | 149.112.112.112 |

### DNS Configuration (/etc/resolv.conf)
```bash
# View current DNS
cat /etc/resolv.conf

# Example configuration
nameserver 8.8.8.8
nameserver 8.8.4.4
search example.com
options timeout:2 attempts:3
```

### Flush DNS Cache
```bash
# Linux (systemd-resolved)
sudo systemd-resolve --flush-caches

# macOS
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder

# Windows
ipconfig /flushdns
```

### Common DNS Issues
```
Problem: DNS Server Not Responding
Solution: Check network, try 8.8.8.8

Problem: Domain Not Found (NXDOMAIN)
Solution: Check spelling, domain registration

Problem: Slow Resolution
Solution: Use faster DNS, clear cache

Problem: DNS Propagation Delay
Solution: Wait 24-48 hours, lower TTL beforehand
```

**💡 Performance Tip:** Use DNS servers geographically close to you, or use anycast DNS like Cloudflare (1.1.1.1) for best performance.""",

    "dhcp": """## 📋 DHCP (Dynamic Host Configuration Protocol)

**Definition:** Network protocol that automatically assigns IP addresses and network configuration to devices.

### What DHCP Provides
- IP Address
- Subnet Mask
- Default Gateway
- DNS Servers
- Lease Duration
- Optional: NTP, WINS, Domain Name

### DHCP DORA Process
```
Client                           Server
   |                                |
   |------ DISCOVER (broadcast) -->|  "Any DHCP server?"
   |                                |
   |<------ OFFER -----------------|  "Here's an IP: 192.168.1.100"
   |                                |
   |------ REQUEST --------------->|  "I'll take 192.168.1.100"
   |                                |
   |<------ ACK -------------------|  "Confirmed, it's yours"
   |                                |
   |====== IP Assigned ============|
```

### DHCP Message Types
| Type | Purpose | Direction |
|------|---------|-----------|
| DISCOVER | Find DHCP servers | Client -> Broadcast |
| OFFER | Offer IP address | Server -> Client |
| REQUEST | Accept offered IP | Client -> Server |
| ACK | Confirm assignment | Server -> Client |
| NAK | Deny request | Server -> Client |
| RELEASE | Give up lease | Client -> Server |
| INFORM | Request config only | Client -> Server |

### DHCP Lease Lifecycle
```
                      ┌──────────┐
         ┌───────────>│ UNBOUND  │
         │            └────┬─────┘
         │                 │ DISCOVER
    RELEASE                ▼
         │            ┌──────────┐
         │            │ SELECTING│
         │            └────┬─────┘
         │                 │ OFFER/REQUEST
         │                 ▼
         │            ┌──────────┐
         └────────────│  BOUND   │<──────┐
                      └────┬─────┘       │
                           │ 50% lease   │ RENEW
                           ▼             │
                      ┌──────────┐       │
                      │ RENEWING │───────┘
                      └────┬─────┘
                           │ 87.5% lease
                           ▼
                      ┌──────────┐
                      │REBINDING │
                      └──────────┘
```

### DHCP Server Configuration (Linux dhcpd)
```bash
# /etc/dhcp/dhcpd.conf
subnet 192.168.1.0 netmask 255.255.255.0 {
    range 192.168.1.100 192.168.1.200;
    option routers 192.168.1.1;
    option domain-name-servers 8.8.8.8, 8.8.4.4;
    option domain-name "example.com";
    default-lease-time 86400;    # 24 hours
    max-lease-time 172800;       # 48 hours
}

# Static reservation
host server1 {
    hardware ethernet 00:11:22:33:44:55;
    fixed-address 192.168.1.10;
}
```

### DHCP Client Commands
```bash
# Release current lease
sudo dhclient -r

# Request new lease
sudo dhclient

# View lease info
cat /var/lib/dhcp/dhclient.leases

# Renew lease (Windows)
ipconfig /release
ipconfig /renew
```

### DHCP Relay Agent
```
DHCP clients broadcast, but broadcasts don't cross routers.
DHCP Relay forwards requests between subnets.

Subnet A              Router            Subnet B
[Clients] --broadcast--> | <--relay-->   [DHCP Server]
```

### DHCP vs Static IP
| Feature | DHCP | Static |
|---------|------|--------|
| Configuration | Automatic | Manual |
| IP Consistency | May change | Fixed |
| Use Case | Workstations | Servers |
| Maintenance | Lower | Higher |
| Scalability | Easy | Complex |

### Common DHCP Issues
```
Problem: No IP assigned (169.254.x.x)
Solution: Check DHCP server, cable, scope

Problem: IP conflict
Solution: Check for static IPs, reservations

Problem: Wrong gateway/DNS
Solution: Verify DHCP scope options
```

**💡 Best Practice:** Use DHCP reservations for devices that need consistent IPs (printers, servers) but still want centralized management.""",

    "ip": """## 🌍 IP (Internet Protocol) Addressing

**Definition:** Network layer protocol for logical addressing and routing packets across networks.

### IPv4 vs IPv6
| Feature | IPv4 | IPv6 |
|---------|------|------|
| Address Size | 32-bit | 128-bit |
| Format | Dotted decimal | Hexadecimal |
| Example | 192.168.1.1 | 2001:db8::1 |
| Total Addresses | 4.3 billion | 340 undecillion |
| Header Size | 20-60 bytes | 40 bytes |
| NAT | Required | Optional |
| Broadcast | Yes | No (multicast) |

### IPv4 Address Classes
| Class | First Octet | Default Mask | Use |
|-------|-------------|--------------|-----|
| A | 1-126 | 255.0.0.0 (/8) | Large networks |
| B | 128-191 | 255.255.0.0 (/16) | Medium networks |
| C | 192-223 | 255.255.255.0 (/24) | Small networks |
| D | 224-239 | N/A | Multicast |
| E | 240-255 | N/A | Reserved |

### Private IP Ranges (RFC 1918)
```
Class A: 10.0.0.0    - 10.255.255.255    (10.0.0.0/8)
Class B: 172.16.0.0  - 172.31.255.255    (172.16.0.0/12)
Class C: 192.168.0.0 - 192.168.255.255   (192.168.0.0/16)
```

### Special IP Addresses
```
0.0.0.0           - Default route / Any address
127.0.0.1         - Localhost (loopback)
127.0.0.0/8       - Loopback range
169.254.0.0/16    - Link-local (APIPA)
224.0.0.0/4       - Multicast
255.255.255.255   - Broadcast
```

### IPv4 Address Structure
```
IP: 192.168.1.100
Binary: 11000000.10101000.00000001.01100100

With /24 subnet mask (255.255.255.0):
Network:   192.168.1.0   (first 24 bits)
Host:      .100          (last 8 bits)
Broadcast: 192.168.1.255 (all host bits = 1)
```

### IPv6 Address Format
```
Full:       2001:0db8:0000:0042:0000:0000:0000:0001
Compressed: 2001:db8:0:42::1

Rules:
1. Remove leading zeros: 0db8 -> db8
2. Replace longest zeros with :: (once only)
3. :: can represent multiple groups of zeros
```

### IPv6 Address Types
```
Global Unicast:   2000::/3  (Internet routable)
Link-Local:       fe80::/10 (Auto-configured, local only)
Unique Local:     fc00::/7  (Private, like RFC1918)
Multicast:        ff00::/8  (One-to-many)
Loopback:         ::1       (Like 127.0.0.1)
```

### IP Configuration Commands
```bash
# View IP addresses
ip addr show
ip a                    # Short form
ifconfig               # Legacy

# Add IP address
sudo ip addr add 192.168.1.100/24 dev eth0

# Remove IP address
sudo ip addr del 192.168.1.100/24 dev eth0

# View routing table
ip route show
route -n               # Legacy
netstat -rn            # Legacy
```

### Network Configuration Files
```bash
# Debian/Ubuntu (/etc/network/interfaces)
auto eth0
iface eth0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 8.8.8.8

# RHEL/CentOS (/etc/sysconfig/network-scripts/ifcfg-eth0)
DEVICE=eth0
BOOTPROTO=static
IPADDR=192.168.1.100
NETMASK=255.255.255.0
GATEWAY=192.168.1.1
DNS1=8.8.8.8
ONBOOT=yes

# Netplan (Ubuntu 18.04+)
# /etc/netplan/01-config.yaml
network:
  version: 2
  ethernets:
    eth0:
      addresses: [192.168.1.100/24]
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```

**💡 Future Ready:** IPv6 adoption is growing. Start learning and implementing dual-stack networks.""",


    "osi": """## 📚 OSI Model (7 Layers)

**Definition:** Reference model that divides network communication into 7 distinct layers.

### The 7 Layers
```
Layer 7: Application   - User interface & services
Layer 6: Presentation  - Data format & encryption
Layer 5: Session       - Connection management
Layer 4: Transport     - End-to-end delivery
Layer 3: Network       - Routing & addressing
Layer 2: Data Link     - Frame transmission
Layer 1: Physical      - Bits on wire
```

**Mnemonic:** Please Do Not Throw Sausage Pizza Away

### Layer Details

**Layer 7 - Application**
```
Protocols: HTTP, HTTPS, FTP, SMTP, DNS, SSH, SNMP
Function:  User-facing network services
Examples:  Web browser, email client
```

**Layer 6 - Presentation**
```
Function:  Data translation, encryption, compression
Examples:  SSL/TLS, JPEG, GIF, ASCII, EBCDIC
Role:      Makes data readable between systems
```

**Layer 5 - Session**
```
Function:  Establish, manage, terminate sessions
Examples:  NetBIOS, RPC, SQL sessions
Role:      Dialog control, synchronization
```

**Layer 4 - Transport**
```
Protocols: TCP, UDP
Function:  Segmentation, flow control, error recovery
Unit:      Segment (TCP) / Datagram (UDP)
Addressing: Port numbers
```

**Layer 3 - Network**
```
Protocols: IP, ICMP, IGMP, IPSec, OSPF, BGP
Function:  Logical addressing, routing
Device:    Router
Unit:      Packet
Addressing: IP addresses
```

**Layer 2 - Data Link**
```
Protocols: Ethernet, PPP, MAC, ARP
Function:  Physical addressing, error detection
Device:    Switch, Bridge
Unit:      Frame
Addressing: MAC addresses
```

**Layer 1 - Physical**
```
Examples:  Cables, Fiber, Wi-Fi, Hubs
Function:  Bit transmission on physical medium
Device:    Hub, Repeater, Network Interface
Unit:      Bits
```

### Data Encapsulation
```
Sending Data:
Application ─┐
Presentation │  Data
Session      │  ↓
Transport    │  Segment (TCP header added)
Network      │  Packet (IP header added)
Data Link    │  Frame (MAC header + trailer)
Physical     └─ Bits on wire

Receiving Data:
Physical     ┌─ Bits received
Data Link    │  Frame (check MAC, remove header)
Network      │  Packet (check IP, remove header)
Transport    │  Segment (check port, remove header)
Session      │  Data
Presentation │  ↓
Application ─┘  Original Data
```

### OSI vs TCP/IP Model
| OSI Layer | TCP/IP Layer | Protocols |
|-----------|--------------|-----------|
| Application | Application | HTTP, FTP, DNS |
| Presentation | Application | SSL, TLS |
| Session | Application | NetBIOS |
| Transport | Transport | TCP, UDP |
| Network | Internet | IP, ICMP |
| Data Link | Link | Ethernet |
| Physical | Link | Physical medium |

### Devices at Each Layer
| Layer | Devices |
|-------|---------|
| 7-Application | Firewall (L7), Load Balancer |
| 4-Transport | Firewall (stateful) |
| 3-Network | Router, L3 Switch |
| 2-Data Link | Switch, Bridge |
| 1-Physical | Hub, Repeater, Cables |

### Troubleshooting with OSI
```
Layer 1: Check cables, lights, physical connections
         ping localhost (check TCP/IP stack)

Layer 2: Check MAC addresses, switch ports
         arp -a (check ARP table)

Layer 3: Check IP config, routing, ping
         ping gateway, traceroute

Layer 4: Check port numbers, firewall rules
         telnet host port, netstat

Layer 5-7: Check application logs, configurations
           Check service status
```

**💡 Interview Tip:** Know which protocols and devices operate at each layer. This is a common interview topic!""",

    "subnet": """## 🔢 Subnetting

**Definition:** Dividing a network into smaller sub-networks for better organization, security, and efficiency.

### Why Subnet?
- Reduce broadcast domain size
- Improve network performance
- Enhance security (isolate segments)
- Efficient IP address allocation
- Better network management

### CIDR Notation Quick Reference
```
/8  = 255.0.0.0         = 16,777,214 hosts
/16 = 255.255.0.0       = 65,534 hosts
/24 = 255.255.255.0     = 254 hosts
/25 = 255.255.255.128   = 126 hosts
/26 = 255.255.255.192   = 62 hosts
/27 = 255.255.255.224   = 30 hosts
/28 = 255.255.255.240   = 14 hosts
/29 = 255.255.255.248   = 6 hosts
/30 = 255.255.255.252   = 2 hosts (point-to-point)
/31 = 255.255.255.254   = 2 hosts (point-to-point, no broadcast)
/32 = 255.255.255.255   = 1 host (single IP)
```

### Subnet Mask Binary
```
/24 = 11111111.11111111.11111111.00000000 = 255.255.255.0
/25 = 11111111.11111111.11111111.10000000 = 255.255.255.128
/26 = 11111111.11111111.11111111.11000000 = 255.255.255.192
/27 = 11111111.11111111.11111111.11100000 = 255.255.255.224
/28 = 11111111.11111111.11111111.11110000 = 255.255.255.240
```

### Subnetting Example 1
```
Given: 192.168.1.0/24
Need: 4 subnets

Solution:
- /24 has 8 host bits
- Need 2 bits for 4 subnets (2^2 = 4)
- New prefix: /26 (24 + 2)

Subnets:
Subnet 1: 192.168.1.0/26
  - Network: 192.168.1.0
  - First usable: 192.168.1.1
  - Last usable: 192.168.1.62
  - Broadcast: 192.168.1.63

Subnet 2: 192.168.1.64/26
  - Network: 192.168.1.64
  - First usable: 192.168.1.65
  - Last usable: 192.168.1.126
  - Broadcast: 192.168.1.127

Subnet 3: 192.168.1.128/26
  - Network: 192.168.1.128
  - Range: 192.168.1.129 - 192.168.1.190
  - Broadcast: 192.168.1.191

Subnet 4: 192.168.1.192/26
  - Network: 192.168.1.192
  - Range: 192.168.1.193 - 192.168.1.254
  - Broadcast: 192.168.1.255
```

### Subnetting Example 2
```
Given: 10.0.0.0/8
Need: Subnets with ~500 hosts each

Solution:
- Need 500 hosts -> need 9 host bits (2^9 = 512)
- 512 - 2 (network + broadcast) = 510 usable
- Host bits: 9, so prefix = 32 - 9 = /23

Each /23 subnet:
- 510 usable hosts
- Subnet increment: 512 addresses (2 x 256)

First subnets:
10.0.0.0/23   (10.0.0.1 - 10.0.1.254)
10.0.2.0/23   (10.0.2.1 - 10.0.3.254)
10.0.4.0/23   (10.0.4.1 - 10.0.5.254)
...
```

### Quick Formulas
```
Usable Hosts = 2^(32 - prefix) - 2
Example: /26 -> 2^(32-26) - 2 = 62 hosts

Number of Subnets = 2^(borrowed_bits)
Example: /24 to /26 = 2^(26-24) = 4 subnets

Subnet Size = 256 - last_octet_of_mask
Example: 255.255.255.192 -> 256 - 192 = 64
```

### VLSM (Variable Length Subnet Mask)
```
Network: 10.0.0.0/8
Requirements:
- HQ: 1000 hosts    -> /22 (1022 hosts)
- Branch1: 200 hosts -> /24 (254 hosts)
- Branch2: 50 hosts  -> /26 (62 hosts)
- WAN Links: 2 hosts -> /30 (2 hosts)

Allocation:
10.0.0.0/22   -> HQ (10.0.0.0 - 10.0.3.255)
10.0.4.0/24   -> Branch1
10.0.5.0/26   -> Branch2
10.0.5.64/30  -> WAN Link 1
10.0.5.68/30  -> WAN Link 2
```

### ipcalc Command
```bash
# Calculate subnet info
ipcalc 192.168.1.0/26

Address:   192.168.1.0
Netmask:   255.255.255.192 = 26
Network:   192.168.1.0/26
HostMin:   192.168.1.1
HostMax:   192.168.1.62
Broadcast: 192.168.1.63
Hosts/Net: 62
```

**💡 Practice Tip:** Use subnet calculators to verify, but learn to do it manually for interviews!""",

    "nat": """## 🔄 NAT (Network Address Translation)

**Definition:** Translates private IP addresses to public IP addresses, enabling internet access for multiple devices.

### Why NAT?
- **IPv4 Conservation**: Share one public IP among many devices
- **Security**: Hide internal network structure
- **Flexibility**: Change ISP without re-addressing

### Types of NAT

**1. Static NAT (One-to-One)**
```
Private IP          <->    Public IP
192.168.1.10        <->    203.0.113.10
192.168.1.11        <->    203.0.113.11

Use Case: Servers needing consistent public IP
```

**2. Dynamic NAT (Many-to-Many Pool)**
```
Private Network      <->    Public IP Pool
192.168.1.0/24       <->    203.0.113.10-50

Assigns from pool on demand
Returns to pool when done
```

**3. PAT / NAT Overload (Many-to-One) - Most Common**
```
Private IP:Port          <->    Public IP:Port
192.168.1.10:50000       <->    203.0.113.5:50000
192.168.1.11:50001       <->    203.0.113.5:50001
192.168.1.12:50002       <->    203.0.113.5:50002

Use Case: Home/small office routers
```

### How NAT Works (PAT Example)
```
Outbound:
1. PC (192.168.1.10:5000) -> google.com:80
2. Router receives packet
3. Router changes source to 203.0.113.1:60000
4. Router stores mapping in NAT table
5. Packet forwarded to internet

Inbound:
1. Response arrives at 203.0.113.1:60000
2. Router checks NAT table
3. Router changes dest to 192.168.1.10:5000
4. Forwards to internal PC
```

### NAT Table Example
| Internal | External | Destination | Protocol |
|----------|----------|-------------|----------|
| 192.168.1.10:50000 | 203.0.113.1:60000 | 8.8.8.8:53 | UDP |
| 192.168.1.11:50001 | 203.0.113.1:60001 | 142.250.185.46:443 | TCP |

### Port Forwarding
```
External access to internal servers:

Public Port    ->    Private Server
203.0.113.1:80 ->    192.168.1.100:80  (Web)
203.0.113.1:443 ->   192.168.1.100:443 (HTTPS)
203.0.113.1:22 ->    192.168.1.50:22   (SSH)
```

### NAT Configuration (Linux iptables)
```bash
# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# Or permanently
echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
sysctl -p

# NAT/Masquerading (outbound)
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Port forwarding (inbound)
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 \\
    -j DNAT --to-destination 192.168.1.100:80

# Allow forwarding
iptables -A FORWARD -i eth0 -o eth1 -m state \\
    --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT
```

### NAT Limitations
```
Issues:
- Breaks end-to-end connectivity
- Some protocols don't work (FTP active, SIP)
- Peer-to-peer applications struggle
- Gaming/VoIP complications

Solutions:
- STUN (Session Traversal Utilities for NAT)
- TURN (Traversal Using Relays around NAT)
- ICE (Interactive Connectivity Establishment)
- UPnP (Universal Plug and Play)
```

### Double NAT Problem
```
Internet
    |
ISP Router (NAT 1)     <- 100.64.1.1
    |
Your Router (NAT 2)    <- 192.168.1.1
    |
Your Devices           <- 192.168.1.x

Problems: Port forwarding fails, gaming issues

Solutions:
- Set ISP router to bridge mode
- DMZ your router on ISP router
- Request public IP from ISP
```

**💡 Real World:** Most home internet uses PAT. Your router tracks thousands of connections with one public IP!""",


    "firewall": """## 🔥 Firewall

**Definition:** Network security system that monitors and controls traffic based on predefined security rules.

### Firewall Types

**1. Packet Filtering (Stateless)**
- Examines each packet independently
- Checks: Source/Dest IP, Port, Protocol
- Fast but limited security

**2. Stateful Inspection**
- Tracks connection state
- Remembers previous packets
- More secure, industry standard

**3. Application Layer (Proxy/WAF)**
- Inspects application data
- Can filter content
- Higher overhead, more security

**4. Next-Generation (NGFW)**
- Deep packet inspection
- Application awareness
- IPS integration
- Malware detection

### iptables (Linux)
```bash
# List all rules
iptables -L -n -v

# Default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT

# Allow SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow from specific IP
iptables -A INPUT -s 192.168.1.100 -j ACCEPT

# Block specific IP
iptables -A INPUT -s 10.0.0.50 -j DROP

# Save rules
iptables-save > /etc/iptables/rules.v4

# Restore rules
iptables-restore < /etc/iptables/rules.v4
```

### firewalld (RHEL/CentOS)
```bash
# Check status
firewall-cmd --state

# List all
firewall-cmd --list-all

# Add service
firewall-cmd --add-service=http --permanent
firewall-cmd --add-service=https --permanent

# Add port
firewall-cmd --add-port=8080/tcp --permanent

# Remove service
firewall-cmd --remove-service=http --permanent

# Add rich rule
firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port port="22" protocol="tcp" accept' --permanent

# Reload
firewall-cmd --reload
```

### ufw (Ubuntu)
```bash
# Enable/Disable
ufw enable
ufw disable

# Default policies
ufw default deny incoming
ufw default allow outgoing

# Allow services
ufw allow ssh
ufw allow http
ufw allow https

# Allow specific port
ufw allow 8080/tcp

# Allow from IP
ufw allow from 192.168.1.100

# Allow subnet to port
ufw allow from 192.168.1.0/24 to any port 22

# Delete rule
ufw delete allow 8080/tcp

# Status
ufw status verbose
ufw status numbered
```

### Firewall Rule Structure
```
Priority | Action | Source      | Dest        | Port | Proto
---------|--------|-------------|-------------|------|-------
1        | Allow  | 192.168.1.0 | Any         | 22   | TCP
2        | Allow  | Any         | Any         | 80   | TCP
3        | Allow  | Any         | Any         | 443  | TCP
4        | Deny   | 10.0.0.0/8  | Any         | Any  | Any
5        | Deny   | Any         | Any         | Any  | Any

Rules processed top-down, first match wins
```

### Best Practices
```
1. Default Deny Policy
   - Block everything, allow only needed

2. Principle of Least Privilege
   - Minimum required access

3. Log Everything
   - Monitor and audit

4. Regular Rule Review
   - Remove obsolete rules

5. Defense in Depth
   - Network + Host firewalls
```

**💡 Security Tip:** Always test firewall changes in a maintenance window. Getting locked out is common!""",

    "vpn": """## 🔐 VPN (Virtual Private Network)

**Definition:** Creates an encrypted tunnel over a public network to securely connect to a private network.

### VPN Types

**Remote Access VPN**
- Individual user to corporate network
- Work from home scenario
- Client software required

**Site-to-Site VPN**
- Connect entire networks
- Office to office
- Always-on connection

### VPN Protocols
| Protocol | Speed | Security | Use Case |
|----------|-------|----------|----------|
| WireGuard | Fast | High | Modern, recommended |
| OpenVPN | Medium | High | Widely supported |
| IPSec/IKEv2 | Fast | High | Enterprise, mobile |
| L2TP/IPSec | Medium | Medium | Legacy support |
| PPTP | Fast | Low | Avoid - insecure |

### How VPN Works
```
Your Device                VPN Server            Internet
    |                          |                    |
    |--- Encrypted Tunnel ---->|                    |
    |   (All traffic)          |                    |
    |                          |--- Normal --->     |
    |                          |<-- Traffic ---     |
    |<-- Encrypted Response ---|                    |
    |                          |                    |

Your real IP is hidden, VPN server IP is visible
```

### OpenVPN Configuration
```bash
# Install
sudo apt install openvpn

# Connect using config file
sudo openvpn --config client.ovpn

# Run as service
sudo systemctl enable openvpn@client
sudo systemctl start openvpn@client

# Sample client config
client
dev tun
proto udp
remote vpn.example.com 1194
resolv-retry infinite
nobind
persist-key
persist-tun
ca ca.crt
cert client.crt
key client.key
cipher AES-256-GCM
auth SHA256
verb 3
```

### WireGuard Configuration
```bash
# Install
sudo apt install wireguard

# Generate keys
wg genkey | tee privatekey | wg pubkey > publickey

# Server config (/etc/wireguard/wg0.conf)
[Interface]
PrivateKey = <server_private_key>
Address = 10.0.0.1/24
ListenPort = 51820

[Peer]
PublicKey = <client_public_key>
AllowedIPs = 10.0.0.2/32

# Client config
[Interface]
PrivateKey = <client_private_key>
Address = 10.0.0.2/24

[Peer]
PublicKey = <server_public_key>
Endpoint = vpn.example.com:51820
AllowedIPs = 0.0.0.0/0  # Route all traffic

# Start WireGuard
sudo wg-quick up wg0
sudo wg-quick down wg0

# Check status
sudo wg show
```

### IPSec Configuration
```bash
# Check IPSec status
ipsec status
ipsec statusall

# strongSwan config (/etc/ipsec.conf)
conn myvpn
    type=tunnel
    left=192.168.1.1
    leftsubnet=192.168.1.0/24
    right=203.0.113.1
    rightsubnet=10.0.0.0/24
    ike=aes256-sha256-modp2048
    esp=aes256-sha256
    auto=start

# Secrets (/etc/ipsec.secrets)
192.168.1.1 203.0.113.1 : PSK "shared_secret"
```

### Split Tunneling
```
Full Tunnel:
All traffic -> VPN -> Internet
(More secure, slower)

Split Tunnel:
Work traffic -> VPN -> Corporate
Other traffic -> Direct -> Internet
(Faster, less secure)
```

### VPN Security Checklist
```
✓ No-logs policy (provider)
✓ Kill switch enabled
✓ DNS leak protection
✓ IPv6 leak protection
✓ Strong encryption (AES-256)
✓ Secure protocol (WireGuard/OpenVPN)
```

**💡 Enterprise Tip:** Always use VPN on untrusted networks (airports, cafes, hotels)!""",

    "ssl": """## 🔒 SSL/TLS (Secure Sockets Layer / Transport Layer Security)

**Definition:** Cryptographic protocols that provide secure communication over networks, commonly used for HTTPS.

### SSL vs TLS
| Version | Status | Notes |
|---------|--------|-------|
| SSL 2.0 | Deprecated | Insecure |
| SSL 3.0 | Deprecated | POODLE vulnerability |
| TLS 1.0 | Deprecated | Should disable |
| TLS 1.1 | Deprecated | Should disable |
| TLS 1.2 | Current | Widely supported |
| TLS 1.3 | Latest | Recommended |

### TLS Handshake (Simplified)
```
Client                              Server
   |                                   |
   |---- Client Hello ---------------->|
   |     (TLS version, cipher suites)  |
   |                                   |
   |<--- Server Hello ----------------|
   |     (chosen cipher, certificate)  |
   |                                   |
   |---- Key Exchange ---------------->|
   |     (pre-master secret)           |
   |                                   |
   |<--- Finished --------------------|
   |---- Finished -------------------->|
   |                                   |
   |==== Encrypted Communication =====|
```

### Certificate Types
| Type | Validation | Use Case |
|------|------------|----------|
| DV (Domain) | Domain ownership | Basic sites |
| OV (Organization) | Business verification | Business sites |
| EV (Extended) | Extensive verification | E-commerce, banking |
| Wildcard | *.domain.com | Multiple subdomains |
| SAN/UCC | Multiple domains | Multiple sites |

### Certificate Commands (OpenSSL)
```bash
# Generate private key
openssl genrsa -out server.key 2048

# Generate CSR (Certificate Signing Request)
openssl req -new -key server.key -out server.csr

# Self-signed certificate (testing only)
openssl req -x509 -nodes -days 365 \\
    -newkey rsa:2048 \\
    -keyout server.key \\
    -out server.crt

# View certificate details
openssl x509 -in server.crt -text -noout

# Verify certificate chain
openssl verify -CAfile ca-bundle.crt server.crt

# Check certificate expiration
openssl x509 -enddate -noout -in server.crt

# Test SSL connection
openssl s_client -connect example.com:443
```

### Let's Encrypt (Free Certificates)
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate (Nginx)
sudo certbot --nginx -d example.com -d www.example.com

# Get certificate (Apache)
sudo certbot --apache -d example.com

# Standalone (no web server)
sudo certbot certonly --standalone -d example.com

# Renew certificates
sudo certbot renew

# Auto-renewal (cron)
0 0,12 * * * certbot renew --quiet
```

### Nginx SSL Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    # Modern configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=63072000" always;
    
    # Other headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

### Check SSL Configuration
```bash
# Test SSL Labs grade
# https://www.ssllabs.com/ssltest/

# Command line test
nmap --script ssl-enum-ciphers -p 443 example.com

# Check supported protocols
openssl s_client -connect example.com:443 -tls1_2
openssl s_client -connect example.com:443 -tls1_3
```

**💡 Security:** Use TLS 1.2+ only. Get A+ on SSL Labs for production sites!""",

    "network_tools": """## 🛠️ Network Troubleshooting Tools

**Definition:** Essential command-line tools for diagnosing and troubleshooting network issues.

### ping - Test Connectivity
```bash
# Basic ping
ping google.com
ping 8.8.8.8

# Specify count
ping -c 5 google.com

# Set interval
ping -i 0.5 google.com

# Set packet size
ping -s 1000 google.com

# Flood ping (requires root)
sudo ping -f localhost
```

### traceroute / tracepath - Trace Route
```bash
# Trace route to destination
traceroute google.com

# UDP traceroute
traceroute -U google.com

# TCP traceroute
traceroute -T -p 443 google.com

# tracepath (no root needed)
tracepath google.com

# Windows
tracert google.com
```

### netstat - Network Statistics
```bash
# All connections
netstat -a

# TCP connections
netstat -at

# UDP connections
netstat -au

# Listening ports
netstat -l

# With process info
netstat -tulpn

# Connection count by state
netstat -ant | awk '{print $6}' | sort | uniq -c
```

### ss - Socket Statistics (Modern netstat)
```bash
# All sockets
ss -a

# TCP listening
ss -tln

# Established TCP
ss -t state established

# With process info
ss -tulpn

# Filter by port
ss -t sport = :22
ss -t dport = :443
```

### nslookup / dig - DNS Lookup
```bash
# Basic lookup
nslookup example.com
dig example.com

# Specific record
nslookup -type=MX example.com
dig example.com MX

# Use specific DNS
nslookup example.com 8.8.8.8
dig @8.8.8.8 example.com

# Short output
dig +short example.com

# Reverse lookup
dig -x 8.8.8.8
```

### curl / wget - HTTP Testing
```bash
# GET request
curl https://api.example.com/users
wget https://example.com/file.zip

# POST request
curl -X POST -d '{"name":"test"}' \\
    -H "Content-Type: application/json" \\
    https://api.example.com/users

# View headers
curl -I https://example.com
curl -v https://example.com

# Follow redirects
curl -L https://example.com

# Download file
curl -O https://example.com/file.zip
wget https://example.com/file.zip
```

### tcpdump - Packet Capture
```bash
# Capture on interface
sudo tcpdump -i eth0

# Capture specific port
sudo tcpdump -i eth0 port 80

# Capture host traffic
sudo tcpdump -i eth0 host 192.168.1.100

# Save to file
sudo tcpdump -i eth0 -w capture.pcap

# Read from file
tcpdump -r capture.pcap

# Verbose output
sudo tcpdump -i eth0 -vvv
```

### nmap - Network Scanner
```bash
# Scan single host
nmap 192.168.1.1

# Scan network
nmap 192.168.1.0/24

# Scan specific ports
nmap -p 22,80,443 192.168.1.1

# Service version detection
nmap -sV 192.168.1.1

# OS detection
nmap -O 192.168.1.1

# Aggressive scan
nmap -A 192.168.1.1

# UDP scan
nmap -sU 192.168.1.1
```

### ip - Network Configuration
```bash
# Show addresses
ip addr show
ip a

# Show routes
ip route show
ip r

# Show neighbors (ARP)
ip neigh show

# Add address
sudo ip addr add 192.168.1.100/24 dev eth0

# Delete address
sudo ip addr del 192.168.1.100/24 dev eth0

# Set interface up/down
sudo ip link set eth0 up
sudo ip link set eth0 down
```

### Troubleshooting Flow
```
1. ping localhost      -> Check TCP/IP stack
2. ping gateway        -> Check local network
3. ping 8.8.8.8        -> Check internet (IP)
4. ping google.com     -> Check DNS
5. traceroute          -> Find where it breaks
6. nmap port scan      -> Check service ports
7. tcpdump/wireshark   -> Deep packet analysis
```

**💡 Tip:** Master these tools - they're essential for any network troubleshooting!""",


    # =========================================================================
    # SERVER CONCEPTS
    # =========================================================================

    "server": """## 🖥️ Servers Overview

**Definition:** A server is a computer or system that provides resources, data, services, or programs to other computers (clients) over a network.

### Types of Servers

| Server Type | Purpose | Examples |
|-------------|---------|----------|
| Web Server | Serve web pages | Apache, Nginx |
| Database Server | Store/manage data | MySQL, PostgreSQL, MongoDB |
| Application Server | Run applications | Tomcat, Gunicorn, Node.js |
| File Server | Store/share files | Samba, NFS |
| Mail Server | Handle email | Postfix, Exchange |
| DNS Server | Domain name resolution | BIND, dnsmasq |
| DHCP Server | IP address assignment | ISC DHCP |
| Proxy Server | Intermediate requests | Squid, HAProxy |

### Web Servers
```
Apache HTTP Server:
- Most widely used web server
- .htaccess support
- Extensive module system

Nginx:
- High performance, event-driven
- Excellent for static content
- Great reverse proxy
- Lower memory usage
```

### Database Servers
```
Relational (SQL):
- MySQL/MariaDB - Popular, easy to use
- PostgreSQL - Advanced features, standards-compliant
- Oracle - Enterprise, commercial
- SQL Server - Microsoft ecosystem

NoSQL:
- MongoDB - Document database
- Redis - In-memory key-value
- Cassandra - Distributed, scalable
- Elasticsearch - Search engine
```

### Server Management
```bash
# Service control (systemd)
sudo systemctl start <service>
sudo systemctl stop <service>
sudo systemctl restart <service>
sudo systemctl status <service>
sudo systemctl enable <service>   # Start at boot

# View running services
systemctl list-units --type=service --state=running

# View logs
journalctl -u <service>
journalctl -u <service> -f  # Follow
```

### Common Server Ports
| Port | Service |
|------|---------|
| 22 | SSH |
| 25 | SMTP |
| 53 | DNS |
| 80 | HTTP |
| 443 | HTTPS |
| 3306 | MySQL |
| 5432 | PostgreSQL |
| 27017 | MongoDB |

### Server Best Practices
```
Security:
✓ Keep software updated
✓ Use firewalls
✓ Disable unused services
✓ Use SSH keys, not passwords
✓ Regular security audits

Performance:
✓ Monitor resources (CPU, RAM, Disk)
✓ Configure appropriate limits
✓ Use caching where possible
✓ Regular log rotation

Reliability:
✓ Implement backups
✓ Use redundancy/clustering
✓ Monitor with alerting
✓ Document configurations
```

**💡 Tip:** Ask about specific servers: `apache`, `nginx`, `mysql`, `postgresql`, `mongodb`, or `server_admin` for detailed information.""",

    "servers": """## 🖥️ Servers Overview

**Definition:** Servers are computers or systems that provide resources, data, services, or programs to other computers (clients) over a network.

### Types of Servers

| Server Type | Purpose | Examples |
|-------------|---------|----------|
| Web Server | Serve web pages | Apache, Nginx |
| Database Server | Store/manage data | MySQL, PostgreSQL, MongoDB |
| Application Server | Run applications | Tomcat, Gunicorn, uWSGI |
| File Server | Store/share files | NFS, Samba |
| Mail Server | Handle email | Postfix, Dovecot |
| DNS Server | Domain resolution | BIND |
| Proxy Server | Intermediate requests | HAProxy, Squid |

### Popular Web Servers
- **Apache**: Most widely used, extensive modules
- **Nginx**: High performance, reverse proxy

### Popular Database Servers
- **MySQL**: Relational, widely used
- **PostgreSQL**: Advanced SQL features
- **MongoDB**: Document-oriented NoSQL

### Server Management Commands
```bash
# Start/Stop/Restart services
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx

# Check service status
sudo systemctl status nginx

# Enable at boot
sudo systemctl enable nginx

# View logs
journalctl -u nginx -f
```

### Learn More
Ask about specific servers:
- `apache` - Apache HTTP Server
- `nginx` - Nginx Web Server
- `mysql` - MySQL Database
- `postgresql` - PostgreSQL Database
- `mongodb` - MongoDB NoSQL
- `server_admin` - Server Administration""",

    "apache": """## 🌐 Apache HTTP Server

**Definition:** Open-source, cross-platform web server software, one of the most widely used web servers.

### Installation
```bash
# Debian/Ubuntu
sudo apt update
sudo apt install apache2

# RHEL/CentOS
sudo yum install httpd
sudo dnf install httpd

# Start and enable
sudo systemctl start apache2    # or httpd
sudo systemctl enable apache2
```

### Key Directories
```
/etc/apache2/               # Main config (Debian)
/etc/httpd/                 # Main config (RHEL)
├── apache2.conf            # Main configuration
├── sites-available/        # Virtual host configs
├── sites-enabled/          # Enabled virtual hosts
├── mods-available/         # Available modules
├── mods-enabled/           # Enabled modules
└── conf-available/         # Additional configs

/var/www/html/              # Default document root
/var/log/apache2/           # Log files
```

### Basic Configuration
```apache
# /etc/apache2/apache2.conf
ServerRoot "/etc/apache2"
Listen 80
ServerAdmin admin@example.com
ServerName www.example.com

DocumentRoot "/var/www/html"
<Directory "/var/www/html">
    Options Indexes FollowSymLinks
    AllowOverride All
    Require all granted
</Directory>

ErrorLog ${APACHE_LOG_DIR}/error.log
CustomLog ${APACHE_LOG_DIR}/access.log combined
```

### Virtual Hosts
```apache
# /etc/apache2/sites-available/example.com.conf
<VirtualHost *:80>
    ServerName example.com
    ServerAlias www.example.com
    DocumentRoot /var/www/example.com/public
    
    <Directory /var/www/example.com/public>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    ErrorLog ${APACHE_LOG_DIR}/example.com-error.log
    CustomLog ${APACHE_LOG_DIR}/example.com-access.log combined
</VirtualHost>
```

### Enable/Disable Sites and Modules
```bash
# Enable site
sudo a2ensite example.com.conf

# Disable site
sudo a2dissite example.com.conf

# Enable module
sudo a2enmod rewrite
sudo a2enmod ssl
sudo a2enmod headers

# Disable module
sudo a2dismod autoindex

# Reload configuration
sudo systemctl reload apache2
```

### SSL Configuration
```apache
<VirtualHost *:443>
    ServerName example.com
    DocumentRoot /var/www/example.com/public
    
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/example.com.crt
    SSLCertificateKeyFile /etc/ssl/private/example.com.key
    SSLCertificateChainFile /etc/ssl/certs/ca-bundle.crt
    
    # Security headers
    Header always set Strict-Transport-Security "max-age=31536000"
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set X-Content-Type-Options "nosniff"
</VirtualHost>

# Redirect HTTP to HTTPS
<VirtualHost *:80>
    ServerName example.com
    Redirect permanent / https://example.com/
</VirtualHost>
```

### Common Modules
| Module | Purpose |
|--------|---------|
| mod_rewrite | URL rewriting |
| mod_ssl | HTTPS support |
| mod_headers | HTTP headers |
| mod_proxy | Reverse proxy |
| mod_security | Web application firewall |
| mod_deflate | Compression |

### Useful Commands
```bash
# Test configuration
sudo apache2ctl configtest
sudo apachectl -t

# Show loaded modules
apache2ctl -M

# Show virtual hosts
apache2ctl -S

# Reload without restart
sudo systemctl reload apache2

# View access log
tail -f /var/log/apache2/access.log

# View error log
tail -f /var/log/apache2/error.log
```

**💡 Tip:** Apache is highly configurable. Use .htaccess for directory-level configs but prefer main config for performance.""",

    "nginx": """## ⚡ Nginx Web Server

**Definition:** High-performance, event-driven web server and reverse proxy server, known for efficiency and low resource usage.

### Installation
```bash
# Debian/Ubuntu
sudo apt update
sudo apt install nginx

# RHEL/CentOS
sudo yum install epel-release
sudo yum install nginx

# Start and enable
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Key Directories
```
/etc/nginx/
├── nginx.conf              # Main configuration
├── sites-available/        # Server block configs
├── sites-enabled/          # Enabled server blocks
├── conf.d/                 # Additional configs
├── snippets/               # Reusable config snippets
└── mime.types              # MIME type mappings

/var/www/html/              # Default document root
/var/log/nginx/             # Log files
```

### Basic Configuration
```nginx
# /etc/nginx/nginx.conf
user www-data;
worker_processes auto;
pid /run/nginx.pid;

events {
    worker_connections 1024;
    multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
    
    gzip on;
    gzip_types text/plain application/json application/javascript text/css;
    
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

### Server Block (Virtual Host)
```nginx
# /etc/nginx/sites-available/example.com
server {
    listen 80;
    listen [::]:80;
    
    server_name example.com www.example.com;
    root /var/www/example.com;
    index index.html index.php;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    location ~ \\.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    }
    
    location ~ /\\.ht {
        deny all;
    }
    
    access_log /var/log/nginx/example.com.access.log;
    error_log /var/log/nginx/example.com.error.log;
}
```

### SSL Configuration
```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    
    server_name example.com;
    root /var/www/example.com;
    
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

### Reverse Proxy
```nginx
server {
    listen 80;
    server_name app.example.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Load Balancing
```nginx
upstream backend {
    least_conn;  # or: round-robin (default), ip_hash
    server backend1.example.com:8080 weight=3;
    server backend2.example.com:8080;
    server backend3.example.com:8080 backup;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

### Useful Commands
```bash
# Test configuration
sudo nginx -t

# Reload configuration
sudo systemctl reload nginx

# Show Nginx version and modules
nginx -V

# Enable site
sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/

# Disable site
sudo rm /etc/nginx/sites-enabled/example.com

# View logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Apache vs Nginx
| Feature | Apache | Nginx |
|---------|--------|-------|
| Architecture | Process-based | Event-driven |
| Static Content | Good | Excellent |
| Dynamic Content | Good (mod_php) | Via FastCGI |
| Memory Usage | Higher | Lower |
| Configuration | .htaccess supported | Main config only |
| Modules | Loadable at runtime | Compiled in |

**💡 Performance Tip:** Nginx excels at serving static files and as a reverse proxy. Use it in front of application servers!""",

    "mysql": """## 🐬 MySQL Database Server

**Definition:** Open-source relational database management system (RDBMS), widely used for web applications.

### Installation
```bash
# Debian/Ubuntu
sudo apt update
sudo apt install mysql-server

# RHEL/CentOS
sudo yum install mysql-server
sudo dnf install mysql-server

# Start and enable
sudo systemctl start mysql
sudo systemctl enable mysql

# Secure installation
sudo mysql_secure_installation
```

### Basic Configuration
```ini
# /etc/mysql/mysql.conf.d/mysqld.cnf
[mysqld]
bind-address = 127.0.0.1
port = 3306
datadir = /var/lib/mysql
socket = /var/run/mysqld/mysqld.sock

# Performance
max_connections = 150
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M

# Logging
log_error = /var/log/mysql/error.log
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2
```

### User Management
```sql
-- Connect as root
mysql -u root -p

-- Create user
CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';
CREATE USER 'username'@'%' IDENTIFIED BY 'password';  -- Remote

-- Grant privileges
GRANT ALL PRIVILEGES ON database.* TO 'username'@'localhost';
GRANT SELECT, INSERT, UPDATE ON database.* TO 'username'@'localhost';

-- Revoke privileges
REVOKE ALL PRIVILEGES ON database.* FROM 'username'@'localhost';

-- Show grants
SHOW GRANTS FOR 'username'@'localhost';

-- Change password
ALTER USER 'username'@'localhost' IDENTIFIED BY 'newpassword';

-- Delete user
DROP USER 'username'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;
```

### Database Operations
```sql
-- Show databases
SHOW DATABASES;

-- Create database
CREATE DATABASE myapp CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use database
USE myapp;

-- Show tables
SHOW TABLES;

-- Show table structure
DESCRIBE users;
SHOW CREATE TABLE users;

-- Drop database
DROP DATABASE myapp;
```

### Backup and Restore
```bash
# Backup single database
mysqldump -u root -p myapp > myapp_backup.sql

# Backup all databases
mysqldump -u root -p --all-databases > all_backup.sql

# Backup with compression
mysqldump -u root -p myapp | gzip > myapp_backup.sql.gz

# Restore database
mysql -u root -p myapp < myapp_backup.sql

# Restore compressed
gunzip < myapp_backup.sql.gz | mysql -u root -p myapp
```

### Remote Access
```bash
# Edit config to allow remote
# bind-address = 0.0.0.0

# Grant remote access
mysql> CREATE USER 'admin'@'%' IDENTIFIED BY 'password';
mysql> GRANT ALL ON *.* TO 'admin'@'%';
mysql> FLUSH PRIVILEGES;

# Open firewall
sudo ufw allow 3306/tcp
```

### Performance Monitoring
```sql
-- Show process list
SHOW PROCESSLIST;

-- Show status variables
SHOW STATUS;
SHOW STATUS LIKE 'Threads%';
SHOW STATUS LIKE 'Conn%';

-- Show variables
SHOW VARIABLES;
SHOW VARIABLES LIKE 'max_connections';

-- Show engine status
SHOW ENGINE INNODB STATUS;
```

### Useful Commands
```bash
# Check service status
sudo systemctl status mysql

# Check error log
sudo tail -f /var/log/mysql/error.log

# Check slow query log
sudo tail -f /var/log/mysql/slow.log

# Reset root password
sudo mysqld_safe --skip-grant-tables &
mysql -u root
> UPDATE mysql.user SET authentication_string=PASSWORD('newpass') WHERE User='root';
> FLUSH PRIVILEGES;
```

**💡 Security Tip:** Never use root for application connections. Create specific users with minimal required privileges.""",


    "postgresql": """## 🐘 PostgreSQL Database Server

**Definition:** Advanced open-source relational database with strong SQL compliance and extensibility.

### Installation
```bash
# Debian/Ubuntu
sudo apt update
sudo apt install postgresql postgresql-contrib

# RHEL/CentOS
sudo dnf install postgresql-server postgresql-contrib
sudo postgresql-setup --initdb

# Start and enable
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Key Directories
```
/etc/postgresql/<version>/main/   # Config (Debian)
├── postgresql.conf               # Main config
├── pg_hba.conf                   # Authentication
└── pg_ident.conf                 # User mapping

/var/lib/postgresql/<version>/main/  # Data directory
/var/log/postgresql/                 # Logs
```

### Configuration
```bash
# /etc/postgresql/14/main/postgresql.conf
listen_addresses = 'localhost'    # or '*' for all
port = 5432
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 16MB

# Logging
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_statement = 'all'
```

### Authentication (pg_hba.conf)
```bash
# TYPE  DATABASE  USER      ADDRESS         METHOD
local   all       postgres                  peer
local   all       all                       peer
host    all       all       127.0.0.1/32    md5
host    all       all       192.168.1.0/24  md5
host    all       all       ::1/128         md5
```

### User Management
```sql
-- Connect as postgres
sudo -u postgres psql

-- Create user
CREATE USER myuser WITH PASSWORD 'password';

-- Create user with options
CREATE USER admin WITH 
    SUPERUSER 
    CREATEDB 
    CREATEROLE 
    LOGIN 
    PASSWORD 'adminpass';

-- Alter user
ALTER USER myuser WITH PASSWORD 'newpassword';
ALTER USER myuser CREATEDB;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO myuser;

-- Drop user
DROP USER myuser;

-- List users
\\du
```

### Database Operations
```sql
-- Create database
CREATE DATABASE mydb OWNER myuser;
CREATE DATABASE mydb ENCODING 'UTF8';

-- List databases
\\l

-- Connect to database
\\c mydb

-- List tables
\\dt

-- Describe table
\\d tablename

-- Drop database
DROP DATABASE mydb;
```

### Backup and Restore
```bash
# Backup single database
pg_dump -U postgres mydb > mydb_backup.sql

# Backup with compression
pg_dump -U postgres mydb | gzip > mydb_backup.sql.gz

# Backup all databases
pg_dumpall -U postgres > all_backup.sql

# Backup in custom format (parallel restore)
pg_dump -U postgres -Fc mydb > mydb.dump

# Restore SQL dump
psql -U postgres mydb < mydb_backup.sql

# Restore custom format
pg_restore -U postgres -d mydb mydb.dump
```

### Performance Monitoring
```sql
-- Active connections
SELECT * FROM pg_stat_activity;

-- Table statistics
SELECT * FROM pg_stat_user_tables;

-- Index usage
SELECT * FROM pg_stat_user_indexes;

-- Database size
SELECT pg_size_pretty(pg_database_size('mydb'));

-- Table size
SELECT pg_size_pretty(pg_total_relation_size('tablename'));

-- Running queries
SELECT pid, query, state, query_start
FROM pg_stat_activity
WHERE state = 'active';

-- Kill query
SELECT pg_terminate_backend(pid);
```

### Useful Commands
```bash
# Connect to database
psql -U username -d database -h host

# Execute SQL file
psql -U username -d database -f script.sql

# Execute single command
psql -U postgres -c "SELECT version();"

# Check version
psql --version

# Service status
sudo systemctl status postgresql
```

### PostgreSQL vs MySQL
| Feature | PostgreSQL | MySQL |
|---------|------------|-------|
| SQL Compliance | High | Medium |
| JSON Support | Excellent (JSONB) | Good |
| Full-Text Search | Built-in | Good |
| Replication | Streaming, Logical | Various options |
| Extensions | Rich ecosystem | Limited |

**💡 Best Practice:** PostgreSQL excels for complex queries, data integrity, and advanced features. Great for analytics and GIS applications!""",

    "mongodb": """## 🍃 MongoDB

**Definition:** Document-oriented NoSQL database that stores data in flexible, JSON-like documents.

### Installation
```bash
# Ubuntu
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install mongodb-org

# Start and enable
sudo systemctl start mongod
sudo systemctl enable mongod
```

### Configuration
```yaml
# /etc/mongod.conf
storage:
  dbPath: /var/lib/mongodb
  journal:
    enabled: true

systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log

net:
  port: 27017
  bindIp: 127.0.0.1

security:
  authorization: enabled
```

### Basic Operations
```javascript
// Connect
mongosh
mongosh "mongodb://localhost:27017"

// Show databases
show dbs

// Use/create database
use mydb

// Show collections
show collections

// Insert documents
db.users.insertOne({
    name: "John",
    email: "john@example.com",
    age: 30
});

db.users.insertMany([
    { name: "Alice", age: 25 },
    { name: "Bob", age: 35 }
]);

// Find documents
db.users.find()
db.users.find({ age: { $gt: 25 } })
db.users.findOne({ name: "John" })

// Update documents
db.users.updateOne(
    { name: "John" },
    { $set: { age: 31 } }
);

db.users.updateMany(
    { age: { $lt: 30 } },
    { $inc: { age: 1 } }
);

// Delete documents
db.users.deleteOne({ name: "John" })
db.users.deleteMany({ age: { $lt: 25 } })

// Drop collection
db.users.drop()
```

### Indexes
```javascript
// Create index
db.users.createIndex({ email: 1 })
db.users.createIndex({ name: 1, age: -1 })

// Create unique index
db.users.createIndex({ email: 1 }, { unique: true })

// List indexes
db.users.getIndexes()

// Drop index
db.users.dropIndex("email_1")
```

### User Management
```javascript
// Create admin user
use admin
db.createUser({
    user: "admin",
    pwd: "password",
    roles: ["root"]
});

// Create database user
use mydb
db.createUser({
    user: "appuser",
    pwd: "password",
    roles: [
        { role: "readWrite", db: "mydb" }
    ]
});

// Authenticate
db.auth("username", "password")

// List users
db.getUsers()

// Drop user
db.dropUser("username")
```

### Aggregation
```javascript
// Aggregation pipeline
db.orders.aggregate([
    { $match: { status: "completed" } },
    { $group: {
        _id: "$customerId",
        totalAmount: { $sum: "$amount" },
        orderCount: { $sum: 1 }
    }},
    { $sort: { totalAmount: -1 } },
    { $limit: 10 }
]);
```

### Backup and Restore
```bash
# Backup
mongodump --db mydb --out /backup/

# Backup with compression
mongodump --db mydb --gzip --archive=backup.gz

# Restore
mongorestore --db mydb /backup/mydb/

# Restore from archive
mongorestore --gzip --archive=backup.gz
```

### SQL vs MongoDB
| SQL | MongoDB |
|-----|---------|
| Database | Database |
| Table | Collection |
| Row | Document |
| Column | Field |
| Index | Index |
| JOIN | $lookup |
| Primary Key | _id |

**💡 Use Case:** MongoDB is great for flexible schemas, rapid development, and document-based data models.""",

    "server_admin": """## 🖥️ Server Administration

**Definition:** Management and maintenance of servers including processes, services, monitoring, and system health.

### Process Management
```bash
# View processes
ps aux                    # All processes
ps -ef                    # Full format
ps aux | grep nginx       # Find specific process
top                       # Interactive process viewer
htop                      # Better interactive viewer

# Process details
ps -p <pid> -o pid,ppid,cmd,stat,time
pstree                    # Process tree
pstree -p                 # With PIDs

# Kill processes
kill <pid>                # SIGTERM (graceful)
kill -9 <pid>             # SIGKILL (force)
killall nginx             # Kill by name
pkill -f "python app.py"  # Kill by pattern

# Background processes
command &                 # Run in background
nohup command &           # Ignore hangup
jobs                      # List background jobs
fg %1                     # Bring to foreground
bg %1                     # Send to background
```

### Service Management (systemd)
```bash
# Service control
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl reload nginx     # Reload config
sudo systemctl status nginx

# Enable/disable at boot
sudo systemctl enable nginx
sudo systemctl disable nginx

# List services
systemctl list-units --type=service
systemctl list-units --type=service --state=running
systemctl list-units --type=service --state=failed

# View service logs
journalctl -u nginx
journalctl -u nginx -f          # Follow
journalctl -u nginx --since today
journalctl -u nginx -n 100      # Last 100 lines

# Service file location
/etc/systemd/system/            # Custom services
/lib/systemd/system/            # Package services
```

### Custom Service File
```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/python3 /opt/myapp/app.py
Restart=always
RestartSec=5
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

### System Monitoring
```bash
# System overview
uptime                    # Uptime and load
uname -a                  # System info
hostname                  # Hostname
hostnamectl               # Detailed host info

# Memory
free -h                   # Memory usage
vmstat 1                  # Virtual memory stats
cat /proc/meminfo         # Detailed memory info

# CPU
lscpu                     # CPU info
mpstat 1                  # CPU statistics
cat /proc/cpuinfo         # Detailed CPU info

# Disk
df -h                     # Disk space
du -sh /var/*             # Directory sizes
iostat                    # I/O statistics
iotop                     # I/O by process

# Network
ss -tuln                  # Listening ports
netstat -tuln             # Listening ports (legacy)
iftop                     # Network bandwidth
```

### Log Management
```bash
# System logs
/var/log/syslog           # General system log
/var/log/messages         # System messages (RHEL)
/var/log/auth.log         # Authentication
/var/log/kern.log         # Kernel messages
/var/log/dmesg            # Boot messages

# View logs
tail -f /var/log/syslog   # Follow log
less /var/log/syslog      # Page through log
grep ERROR /var/log/syslog # Search log

# Log rotation
logrotate                 # Rotate logs
/etc/logrotate.conf       # Configuration
/etc/logrotate.d/         # Per-service configs
```

### Scheduled Tasks (Cron)
```bash
# Edit crontab
crontab -e                # Edit user crontab
sudo crontab -e           # Edit root crontab
crontab -l                # List crontab

# Cron format
# MIN HOUR DOM MON DOW COMMAND
# 0-59 0-23 1-31 1-12 0-6

# Examples
0 * * * * /script.sh        # Every hour
0 2 * * * /backup.sh        # 2 AM daily
0 0 * * 0 /weekly.sh        # Sunday midnight
*/5 * * * * /check.sh       # Every 5 minutes
0 9-17 * * 1-5 /work.sh     # Weekdays 9AM-5PM

# Cron directories
/etc/cron.d/              # Drop-in cron files
/etc/cron.daily/          # Daily scripts
/etc/cron.hourly/         # Hourly scripts
/etc/cron.weekly/         # Weekly scripts
/etc/cron.monthly/        # Monthly scripts
```

### System Performance
```bash
# Quick health check
uptime                    # Load average
free -h                   # Memory
df -h                     # Disk
top -bn1 | head -20       # Top processes

# Performance analysis
sar                       # System activity
vmstat 1 5                # Memory/CPU every 1s
iostat -x 1 5             # Disk I/O
pidstat 1                 # Per-process stats
```

**💡 Best Practice:** Set up monitoring (Prometheus, Grafana, Nagios) and alerting for production servers!""",


    # =========================================================================
    # STORAGE CONCEPTS
    # =========================================================================

    "filesystem": """## 📁 File Systems

**Definition:** Method for organizing and storing data on storage devices, defining how data is named, stored, and retrieved.

### Common File Systems
| File System | OS | Max File Size | Max Volume | Features |
|-------------|-----|---------------|------------|----------|
| ext4 | Linux | 16 TB | 1 EB | Journaling, most common |
| XFS | Linux | 8 EB | 8 EB | High performance, scalable |
| Btrfs | Linux | 16 EB | 16 EB | Copy-on-write, snapshots |
| NTFS | Windows | 16 EB | 256 TB | ACLs, encryption |
| FAT32 | All | 4 GB | 2 TB | Universal compatibility |
| exFAT | All | 16 EB | 128 PB | Flash drives |

### ext4 (Fourth Extended Filesystem)
```bash
# Create ext4 filesystem
sudo mkfs.ext4 /dev/sdb1

# With options
sudo mkfs.ext4 -L "DataDisk" -m 1 /dev/sdb1
# -L: Label
# -m: Reserved blocks percentage

# Check filesystem
sudo e2fsck -f /dev/sdb1

# Tune filesystem
sudo tune2fs -L "NewLabel" /dev/sdb1
sudo tune2fs -m 2 /dev/sdb1

# Show info
sudo tune2fs -l /dev/sdb1
sudo dumpe2fs /dev/sdb1 | head -50
```

### XFS
```bash
# Create XFS filesystem
sudo mkfs.xfs /dev/sdb1
sudo mkfs.xfs -L "DataDisk" /dev/sdb1

# Check filesystem
sudo xfs_repair /dev/sdb1

# Show info
sudo xfs_info /dev/sdb1

# Grow filesystem (online)
sudo xfs_growfs /mount/point
```

### Mount File Systems
```bash
# Manual mount
sudo mount /dev/sdb1 /mnt/data
sudo mount -t ext4 /dev/sdb1 /mnt/data
sudo mount -o ro /dev/sdb1 /mnt/data    # Read-only

# Unmount
sudo umount /mnt/data

# Show mounted filesystems
mount
df -hT
lsblk -f

# Persistent mount (/etc/fstab)
# Device          Mount        Type  Options         Dump Pass
/dev/sdb1        /mnt/data    ext4  defaults        0    2
UUID=abc123      /mnt/backup  xfs   defaults,noatime 0   2
//server/share   /mnt/share   cifs  credentials=/etc/cred 0 0

# Get UUID
blkid /dev/sdb1
lsblk -f

# Apply fstab changes
sudo mount -a
```

### Disk Management
```bash
# List disks and partitions
lsblk
fdisk -l
parted -l

# Partition with fdisk
sudo fdisk /dev/sdb
# n: New partition
# p: Primary
# w: Write and exit

# Partition with parted
sudo parted /dev/sdb
(parted) mklabel gpt
(parted) mkpart primary ext4 1MiB 100%
(parted) print
(parted) quit
```

### Disk Space Management
```bash
# Check disk usage
df -h                     # Filesystem usage
df -i                     # Inode usage
du -sh /var/*             # Directory sizes
du -h --max-depth=1 /     # Top-level directories

# Find large files
find / -type f -size +100M -exec ls -lh {} \\;
find / -type f -size +1G 2>/dev/null

# Find large directories
du -h / 2>/dev/null | sort -rh | head -20

# Clean up
sudo apt clean            # Package cache
journalctl --vacuum-size=100M  # Logs
```

**💡 Recommendation:** Use XFS for large files and high-performance workloads. Use ext4 for general-purpose Linux systems.""",

    "permissions": """## 🔐 File Permissions

**Definition:** Access control mechanism that determines who can read, write, or execute files and directories.

### Permission Basics
```
-rwxr-xr-x  1  owner  group  size  date  filename
│└┬┘└┬┘└┬┘
│ │  │  └── Others (world) permissions
│ │  └───── Group permissions
│ └──────── Owner (user) permissions
└────────── File type (- file, d directory, l link)

r = Read    (4)
w = Write   (2)
x = Execute (1)
```

### Numeric Permissions
```
7 = rwx = 4+2+1 = read, write, execute
6 = rw- = 4+2   = read, write
5 = r-x = 4+1   = read, execute
4 = r-- = 4     = read only
0 = --- = 0     = no permissions

Common patterns:
755 = rwxr-xr-x (directories, executables)
644 = rw-r--r-- (regular files)
600 = rw------- (private files)
700 = rwx------ (private directories)
777 = rwxrwxrwx (avoid - full access)
```

### chmod - Change Permissions
```bash
# Numeric mode
chmod 755 file
chmod 644 file
chmod 600 private.key

# Symbolic mode
chmod u+x file            # Add execute for user
chmod g-w file            # Remove write for group
chmod o=r file            # Set others to read only
chmod a+x file            # Add execute for all
chmod u=rwx,g=rx,o=rx file

# Recursive
chmod -R 755 /var/www/

# Reference another file
chmod --reference=file1 file2
```

### chown - Change Ownership
```bash
# Change owner
sudo chown user file
sudo chown user:group file

# Change group only
sudo chown :group file
sudo chgrp group file

# Recursive
sudo chown -R www-data:www-data /var/www/
```

### Special Permissions
```
SUID (4): Execute as file owner
    chmod u+s file   or   chmod 4755 file
    -rwsr-xr-x
    
SGID (2): Execute as group / inherit directory group
    chmod g+s file   or   chmod 2755 dir
    -rwxr-sr-x
    
Sticky Bit (1): Only owner can delete (directories)
    chmod +t dir     or   chmod 1777 /tmp
    drwxrwxrwt

Examples:
/usr/bin/passwd   -> SUID (runs as root)
/tmp              -> Sticky bit (only owner deletes)
```

### umask - Default Permissions
```bash
# View current umask
umask
umask -S          # Symbolic format

# Set umask
umask 022         # Files: 644, Dirs: 755
umask 027         # Files: 640, Dirs: 750
umask 077         # Files: 600, Dirs: 700

# How umask works:
# Default file:      666
# Default directory: 777
# umask 022:         022
# Result file:       644 (666 - 022)
# Result directory:  755 (777 - 022)

# Persistent (in ~/.bashrc or /etc/profile)
umask 022
```

### ACLs (Access Control Lists)
```bash
# Check if ACLs supported
mount | grep acl

# View ACLs
getfacl file

# Set ACL for user
setfacl -m u:username:rwx file

# Set ACL for group
setfacl -m g:groupname:rx file

# Set default ACL (directory)
setfacl -d -m u:username:rwx directory

# Remove ACL
setfacl -x u:username file

# Remove all ACLs
setfacl -b file

# Copy ACLs
getfacl file1 | setfacl --set-file=- file2
```

### Common Permission Scenarios
```bash
# Web server files
sudo chown -R www-data:www-data /var/www/
sudo find /var/www/ -type d -exec chmod 755 {} \\;
sudo find /var/www/ -type f -exec chmod 644 {} \\;

# SSH keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 600 ~/.ssh/authorized_keys

# Scripts
chmod +x script.sh
chmod 755 /usr/local/bin/myscript
```

**💡 Security Tip:** Follow principle of least privilege. Never use 777 in production!""",

    "raid": """## 💾 RAID (Redundant Array of Independent Disks)

**Definition:** Technology combining multiple physical disks into a single logical unit for performance, redundancy, or both.

### RAID Levels Overview
| Level | Min Disks | Redundancy | Performance | Capacity | Use Case |
|-------|-----------|------------|-------------|----------|----------|
| RAID 0 | 2 | None | Excellent | 100% | Temp data, performance |
| RAID 1 | 2 | Mirroring | Good read | 50% | OS, critical data |
| RAID 5 | 3 | Parity | Good | (N-1)/N | General purpose |
| RAID 6 | 4 | Double parity | Good | (N-2)/N | Large arrays |
| RAID 10 | 4 | Mirror+Stripe | Excellent | 50% | Databases, high I/O |

### RAID 0 (Striping)
```
Disk 1    Disk 2
┌─────┐   ┌─────┐
│  A1 │   │  A2 │
│  A3 │   │  A4 │
│  A5 │   │  A6 │
└─────┘   └─────┘

Pros: Best performance, full capacity
Cons: No redundancy - any disk failure = total data loss
Use: Temporary data, caches, performance-critical non-critical data
```

### RAID 1 (Mirroring)
```
Disk 1    Disk 2
┌─────┐   ┌─────┐
│  A  │   │  A  │  (identical)
│  B  │   │  B  │
│  C  │   │  C  │
└─────┘   └─────┘

Pros: Full redundancy, good read performance
Cons: 50% capacity, write overhead
Use: OS drives, critical data
```

### RAID 5 (Striping with Parity)
```
Disk 1    Disk 2    Disk 3
┌─────┐   ┌─────┐   ┌─────┐
│  A1 │   │  A2 │   │ Ap  │
│  B1 │   │ Bp  │   │  B2 │
│ Cp  │   │  C1 │   │  C2 │
└─────┘   └─────┘   └─────┘
(p = parity block, distributed)

Pros: Good balance of performance and redundancy
Cons: Slow writes (parity calculation), long rebuild
Use: File servers, general storage
```

### RAID 6 (Double Parity)
```
Similar to RAID 5 but with TWO parity blocks
Can survive 2 disk failures simultaneously

Pros: Better fault tolerance than RAID 5
Cons: Even slower writes, more overhead
Use: Large arrays where rebuild time is long
```

### RAID 10 (1+0, Mirror then Stripe)
```
Mirror 1      Mirror 2
┌─────┬─────┐ ┌─────┬─────┐
│  A  │  A  │ │  B  │  B  │
│  C  │  C  │ │  D  │  D  │
│  E  │  E  │ │  F  │  F  │
└─────┴─────┘ └─────┴─────┘
  Disk1 Disk2   Disk3 Disk4

Pros: Excellent performance AND redundancy
Cons: 50% capacity
Use: Databases, high-performance applications
```

### Software RAID (mdadm)
```bash
# Create RAID 1
sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1

# Create RAID 5
sudo mdadm --create /dev/md0 --level=5 --raid-devices=3 /dev/sdb1 /dev/sdc1 /dev/sdd1

# Create RAID 10
sudo mdadm --create /dev/md0 --level=10 --raid-devices=4 /dev/sdb1 /dev/sdc1 /dev/sdd1 /dev/sde1

# Check RAID status
cat /proc/mdstat
sudo mdadm --detail /dev/md0

# Save configuration
sudo mdadm --detail --scan >> /etc/mdadm/mdadm.conf

# Add spare disk
sudo mdadm /dev/md0 --add /dev/sdf1

# Remove disk
sudo mdadm /dev/md0 --fail /dev/sdc1
sudo mdadm /dev/md0 --remove /dev/sdc1

# Stop RAID
sudo mdadm --stop /dev/md0
```

### RAID Monitoring
```bash
# Check status
cat /proc/mdstat
sudo mdadm --detail /dev/md0

# Monitor for failures
sudo mdadm --monitor --mail=admin@example.com --delay=1800 /dev/md0

# Check rebuild progress
watch cat /proc/mdstat
```

### RAID Best Practices
```
1. Same disk size and speed
2. Use disks from different batches/manufacturers
3. Always have hot spare for critical arrays
4. Regular monitoring and alerting
5. Test rebuild procedures
6. RAID is not backup!
```

**💡 Important:** RAID provides redundancy, NOT backup! Always maintain separate backups.""",

    "lvm": """## 📊 LVM (Logical Volume Manager)

**Definition:** Flexible disk management system allowing dynamic resizing, snapshots, and spanning volumes across multiple disks.

### LVM Architecture
```
Physical Disks/Partitions
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐
│  PV   │ │  PV   │  Physical Volumes
│ sda1  │ │ sdb1  │
└───┬───┘ └───┬───┘
    │         │
    └────┬────┘
         ▼
    ┌─────────┐
    │   VG    │        Volume Group
    │  vg0    │
    └────┬────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐
│  LV   │ │  LV   │  Logical Volumes
│ root  │ │ data  │
└───────┘ └───────┘
    │         │
    ▼         ▼
  /dev/     /dev/
  vg0/      vg0/
  root      data
```

### Create LVM Setup
```bash
# 1. Create Physical Volumes
sudo pvcreate /dev/sdb1
sudo pvcreate /dev/sdc1

# View PVs
sudo pvs
sudo pvdisplay

# 2. Create Volume Group
sudo vgcreate vg_data /dev/sdb1 /dev/sdc1

# View VGs
sudo vgs
sudo vgdisplay

# 3. Create Logical Volumes
sudo lvcreate -L 50G -n lv_home vg_data
sudo lvcreate -l 100%FREE -n lv_data vg_data

# View LVs
sudo lvs
sudo lvdisplay

# 4. Create filesystem
sudo mkfs.ext4 /dev/vg_data/lv_home

# 5. Mount
sudo mount /dev/vg_data/lv_home /home
```

### Extend Logical Volume
```bash
# Extend LV by size
sudo lvextend -L +10G /dev/vg_data/lv_data

# Extend LV to size
sudo lvextend -L 100G /dev/vg_data/lv_data

# Extend to use all free space
sudo lvextend -l +100%FREE /dev/vg_data/lv_data

# Resize filesystem (ext4)
sudo resize2fs /dev/vg_data/lv_data

# Resize filesystem (XFS)
sudo xfs_growfs /mount/point

# Extend and resize in one command
sudo lvextend -r -L +10G /dev/vg_data/lv_data
```

### Extend Volume Group
```bash
# Add new disk to VG
sudo pvcreate /dev/sdd1
sudo vgextend vg_data /dev/sdd1

# Check new size
sudo vgs
```

### Reduce Logical Volume (CAREFUL!)
```bash
# 1. Unmount
sudo umount /mount/point

# 2. Check filesystem
sudo e2fsck -f /dev/vg_data/lv_data

# 3. Reduce filesystem first
sudo resize2fs /dev/vg_data/lv_data 40G

# 4. Reduce LV
sudo lvreduce -L 40G /dev/vg_data/lv_data

# 5. Remount
sudo mount /dev/vg_data/lv_data /mount/point
```

### LVM Snapshots
```bash
# Create snapshot
sudo lvcreate -L 5G -s -n lv_data_snap /dev/vg_data/lv_data

# Mount snapshot (read-only)
sudo mount -o ro /dev/vg_data/lv_data_snap /mnt/snapshot

# Restore from snapshot (DANGEROUS)
sudo lvconvert --merge /dev/vg_data/lv_data_snap

# Remove snapshot
sudo lvremove /dev/vg_data/lv_data_snap
```

### Remove LVM
```bash
# Unmount
sudo umount /mount/point

# Remove LV
sudo lvremove /dev/vg_data/lv_data

# Remove VG
sudo vgremove vg_data

# Remove PV
sudo pvremove /dev/sdb1 /dev/sdc1
```

### LVM Commands Summary
| Command | Purpose |
|---------|---------|
| pvcreate | Create physical volume |
| pvs, pvdisplay | Show PV info |
| vgcreate | Create volume group |
| vgs, vgdisplay | Show VG info |
| vgextend | Add PV to VG |
| lvcreate | Create logical volume |
| lvs, lvdisplay | Show LV info |
| lvextend | Extend LV |
| lvreduce | Reduce LV |

**💡 Best Practice:** Always use LVM for servers. It provides flexibility for future growth and maintenance.""",


    "san": """## 🗄️ SAN (Storage Area Network)

**Definition:** High-speed network providing access to block-level storage, typically using Fibre Channel or iSCSI.

### SAN vs NAS vs DAS
| Feature | SAN | NAS | DAS |
|---------|-----|-----|-----|
| Access Type | Block | File | Block |
| Protocol | FC, iSCSI | NFS, SMB | SATA, SAS |
| Network | Dedicated | LAN | Direct attach |
| Performance | Excellent | Good | Excellent |
| Sharing | Multi-host | Multi-host | Single host |
| Use Case | Databases, VMs | File sharing | Local storage |

### SAN Architecture
```
┌──────────────────────────────────────────┐
│              SAN Fabric                   │
│  ┌─────────────────────────────────────┐ │
│  │         FC / iSCSI Switch           │ │
│  └─────────────────────────────────────┘ │
│     │          │          │         │    │
│     ▼          ▼          ▼         ▼    │
│ ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  │
│ │Server│  │Server│  │Server│  │Server│  │
│ │ (HBA)│  │ (HBA)│  │(iSCSI)│ │(iSCSI)│ │
│ └──────┘  └──────┘  └──────┘  └──────┘  │
│                                          │
│  ┌─────────────────────────────────────┐ │
│  │        Storage Array                │ │
│  │   ┌─────┐ ┌─────┐ ┌─────┐          │ │
│  │   │ LUN │ │ LUN │ │ LUN │          │ │
│  │   └─────┘ └─────┘ └─────┘          │ │
│  └─────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

### iSCSI Configuration (Linux Initiator)
```bash
# Install iSCSI initiator
sudo apt install open-iscsi

# Configure initiator name
sudo nano /etc/iscsi/initiatorname.iscsi
InitiatorName=iqn.2024-01.com.example:server1

# Discover targets
sudo iscsiadm -m discovery -t sendtargets -p 192.168.1.100

# Login to target
sudo iscsiadm -m node -T iqn.2024-01.com.example:storage -p 192.168.1.100 --login

# List sessions
sudo iscsiadm -m session

# Logout
sudo iscsiadm -m node -T iqn.2024-01.com.example:storage -p 192.168.1.100 --logout

# Auto-login at boot
sudo iscsiadm -m node -T iqn.2024-01.com.example:storage -p 192.168.1.100 -o update -n node.startup -v automatic
```

### iSCSI Target Setup (Linux)
```bash
# Install target software
sudo apt install targetcli-fb

# Configure using targetcli
sudo targetcli

/> /backstores/block create disk1 /dev/sdb1
/> /iscsi create iqn.2024-01.com.example:storage
/> /iscsi/iqn.../tpg1/luns create /backstores/block/disk1
/> /iscsi/iqn.../tpg1/acls create iqn.2024-01.com.example:server1
/> saveconfig
/> exit
```

### Multipath I/O (MPIO)
```bash
# Install multipath
sudo apt install multipath-tools

# Configure multipath
sudo nano /etc/multipath.conf
defaults {
    user_friendly_names yes
    path_grouping_policy multibus
    failback immediate
}

# Show multipath devices
sudo multipath -ll

# Flush and reload
sudo multipath -F
sudo multipath -v2
```

### SAN Best Practices
```
1. Redundant paths (multipathing)
2. Separate SAN network/VLAN
3. Zone for security (Fibre Channel)
4. Monitor performance and capacity
5. Regular firmware updates
6. Document LUN mappings
```

**💡 Use Case:** SANs are ideal for databases, virtualization, and applications requiring high-performance block storage with shared access.""",

    "nas": """## 📂 NAS (Network Attached Storage)

**Definition:** File-level storage connected to network, allowing multiple clients to access shared files.

### NFS (Network File System)
```bash
# Server Setup (Linux)
# Install NFS server
sudo apt install nfs-kernel-server

# Create export directory
sudo mkdir -p /srv/nfs/share
sudo chown nobody:nogroup /srv/nfs/share

# Configure exports
sudo nano /etc/exports
/srv/nfs/share  192.168.1.0/24(rw,sync,no_subtree_check)
/srv/nfs/readonly  192.168.1.0/24(ro,sync,no_subtree_check)

# Export options:
# rw/ro: read-write / read-only
# sync: synchronous writes
# no_subtree_check: disable subtree checking
# no_root_squash: allow root access (security risk)

# Apply exports
sudo exportfs -a
sudo systemctl restart nfs-kernel-server

# Show exports
sudo exportfs -v
```

```bash
# Client Setup
# Install NFS client
sudo apt install nfs-common

# Show server exports
showmount -e 192.168.1.100

# Mount NFS share
sudo mount -t nfs 192.168.1.100:/srv/nfs/share /mnt/nfs

# Persistent mount (/etc/fstab)
192.168.1.100:/srv/nfs/share  /mnt/nfs  nfs  defaults,_netdev  0  0

# Unmount
sudo umount /mnt/nfs
```

### SMB/CIFS (Samba)
```bash
# Server Setup (Linux)
# Install Samba
sudo apt install samba

# Configure share
sudo nano /etc/samba/smb.conf
[share]
    path = /srv/samba/share
    browseable = yes
    read only = no
    valid users = @smbgroup
    create mask = 0664
    directory mask = 0775

# Create Samba user
sudo smbpasswd -a username

# Restart service
sudo systemctl restart smbd

# Test config
testparm
```

```bash
# Client Setup (Linux)
# Install CIFS utils
sudo apt install cifs-utils

# Mount SMB share
sudo mount -t cifs //server/share /mnt/smb -o username=user,password=pass

# Persistent mount (/etc/fstab)
//server/share  /mnt/smb  cifs  credentials=/etc/samba/cred,uid=1000  0  0

# Credentials file
# /etc/samba/cred
username=myuser
password=mypassword

# Access from Windows
\\\\server\\share
```

### NFS vs SMB Comparison
| Feature | NFS | SMB/CIFS |
|---------|-----|----------|
| Origin | Unix/Linux | Windows |
| Protocol | NFS v3/v4 | SMB 2/3 |
| Authentication | Host-based | User-based |
| Performance | Generally faster | Good |
| Cross-platform | Linux/Unix native | Windows native |
| ACL Support | NFSv4 | Full Windows ACLs |

### NAS Best Practices
```
1. Use NFSv4 (better security)
2. Implement proper access controls
3. Regular backups
4. Monitor disk space
5. Use dedicated network/VLAN
6. Enable quotas if needed
```

### Auto-mount with autofs
```bash
# Install autofs
sudo apt install autofs

# Configure master map
sudo nano /etc/auto.master
/mnt/auto  /etc/auto.nfs  --timeout=60

# Configure NFS mounts
sudo nano /etc/auto.nfs
share  -fstype=nfs,rw  192.168.1.100:/srv/nfs/share

# Restart autofs
sudo systemctl restart autofs

# Access (auto-mounts)
cd /mnt/auto/share
```

**💡 Recommendation:** Use NFS for Linux environments, SMB for mixed Windows/Linux environments.""",

    "backup": """## 💾 Backup Strategies

**Definition:** Process of creating copies of data to protect against data loss from hardware failure, human error, or disasters.

### Backup Types
| Type | Description | Speed | Storage | Restore |
|------|-------------|-------|---------|---------|
| Full | Complete copy | Slowest | Highest | Fastest |
| Incremental | Changes since last backup | Fastest | Lowest | Slowest |
| Differential | Changes since last full | Medium | Medium | Medium |

### Backup Types Diagram
```
Day 1: Full Backup (100GB)
Day 2: Incremental (5GB changed)
Day 3: Incremental (3GB changed)
Day 4: Incremental (4GB changed)
Day 5: Incremental (2GB changed)

Restore Day 5: Full + Inc2 + Inc3 + Inc4 + Inc5

vs Differential:
Day 1: Full Backup (100GB)
Day 2: Differential (5GB since full)
Day 3: Differential (8GB since full)
Day 4: Differential (12GB since full)

Restore Day 4: Full + Diff4 only
```

### 3-2-1 Backup Rule
```
3 copies of data (original + 2 backups)
2 different storage media
1 offsite copy

Example:
- Primary data (server)
- Local backup (NAS/external drive)
- Cloud backup (AWS S3, Backblaze)
```

### rsync (Incremental Backup)
```bash
# Basic sync
rsync -av /source/ /destination/

# With delete (mirror)
rsync -av --delete /source/ /destination/

# Remote sync
rsync -avz -e ssh /source/ user@server:/backup/

# Exclude files
rsync -av --exclude '*.log' --exclude 'tmp/' /source/ /dest/

# Dry run
rsync -av --dry-run /source/ /destination/

# With progress
rsync -av --progress /source/ /destination/

# Backup with timestamp
rsync -av /source/ /backup/$(date +%Y%m%d)/
```

### tar (Archive Backup)
```bash
# Create archive
tar -cvf backup.tar /data/
tar -czvf backup.tar.gz /data/     # Compressed

# Extract archive
tar -xvf backup.tar
tar -xzvf backup.tar.gz

# List contents
tar -tvf backup.tar

# Incremental backup
tar -cvf full.tar -g snapshot.file /data/
tar -cvf inc1.tar -g snapshot.file /data/
```

### Backup Rotation Schemes

**GFS (Grandfather-Father-Son)**
```
Daily (Son):     Keep 7 days
Weekly (Father): Keep 4 weeks (Fridays)
Monthly (Grandfather): Keep 12 months (1st of month)

Schedule:
Mon-Thu: Daily backup
Fri: Weekly backup
1st: Monthly backup
```

**Tower of Hanoi**
```
More complex rotation providing longer retention
with same number of tapes/storage
```

### Backup Script Example
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup"
SOURCE_DIR="/data"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$DATE.tar.gz"

# Create backup
tar -czvf "$BACKUP_FILE" "$SOURCE_DIR"

# Remove backups older than 30 days
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +30 -delete

# Log
echo "Backup completed: $BACKUP_FILE" >> /var/log/backup.log
```

### Database Backup
```bash
# MySQL
mysqldump -u root -p --all-databases > all_db.sql
mysqldump -u root -p mydb | gzip > mydb_$(date +%Y%m%d).sql.gz

# PostgreSQL
pg_dump -U postgres mydb > mydb.sql
pg_dumpall -U postgres > all_db.sql
```

### Backup Verification
```bash
# Test restore periodically!
# Document restore procedures
# Calculate RTO (Recovery Time Objective)
# Calculate RPO (Recovery Point Objective)
```

### Backup Checklist
```
✓ Regular schedule (automated)
✓ Multiple copies (3-2-1 rule)
✓ Offsite/cloud copy
✓ Encryption for sensitive data
✓ Regular restore testing
✓ Monitoring and alerts
✓ Documented procedures
```

**💡 Golden Rule:** Untested backups are not backups. Regularly test your restore process!""",

    "cloud_storage": """## ☁️ Cloud Storage

**Definition:** Storage services provided over the internet, offering scalability, durability, and accessibility.

### Cloud Storage Types
| Type | Description | Use Case |
|------|-------------|----------|
| Object Storage | S3, Blob | Media, backups, static files |
| Block Storage | EBS, Azure Disk | VMs, databases |
| File Storage | EFS, Azure Files | Shared file systems |

### AWS S3 (Simple Storage Service)
```bash
# Install AWS CLI
pip install awscli
aws configure

# Create bucket
aws s3 mb s3://my-bucket-name

# List buckets
aws s3 ls

# Upload file
aws s3 cp file.txt s3://my-bucket/
aws s3 cp folder/ s3://my-bucket/folder/ --recursive

# Download file
aws s3 cp s3://my-bucket/file.txt .

# Sync directories
aws s3 sync /local/dir s3://my-bucket/dir
aws s3 sync s3://my-bucket/dir /local/dir

# Delete
aws s3 rm s3://my-bucket/file.txt
aws s3 rb s3://my-bucket --force  # Remove bucket
```

### S3 Storage Classes
| Class | Use Case | Availability | Cost |
|-------|----------|--------------|------|
| Standard | Frequent access | 99.99% | Highest |
| Intelligent-Tiering | Unknown patterns | 99.9% | Auto-optimized |
| Standard-IA | Infrequent access | 99.9% | Lower |
| One Zone-IA | Non-critical | 99.5% | Lower |
| Glacier | Archive | 99.99% | Lowest |
| Glacier Deep Archive | Long-term archive | 99.99% | Lowest |

### S3 Bucket Policy Example
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my-bucket/*"
        }
    ]
}
```

### Azure Blob Storage
```bash
# Install Azure CLI
pip install azure-cli
az login

# Create storage account
az storage account create -n mystorageaccount -g myresourcegroup

# Create container
az storage container create -n mycontainer --account-name mystorageaccount

# Upload
az storage blob upload -f file.txt -c mycontainer -n file.txt --account-name mystorageaccount

# Download
az storage blob download -c mycontainer -n file.txt -f downloaded.txt --account-name mystorageaccount

# List blobs
az storage blob list -c mycontainer --account-name mystorageaccount
```

### Google Cloud Storage
```bash
# Install gcloud SDK
# Create bucket
gsutil mb gs://my-bucket-name

# Upload
gsutil cp file.txt gs://my-bucket/
gsutil -m cp -r folder/ gs://my-bucket/  # Parallel

# Download
gsutil cp gs://my-bucket/file.txt .

# Sync
gsutil rsync -r /local/dir gs://my-bucket/dir

# List
gsutil ls gs://my-bucket/
```

### Mount Cloud Storage as Filesystem
```bash
# s3fs (S3)
sudo apt install s3fs
echo "ACCESS_KEY:SECRET_KEY" > ~/.passwd-s3fs
chmod 600 ~/.passwd-s3fs
s3fs my-bucket /mnt/s3 -o passwd_file=~/.passwd-s3fs

# rclone (Multiple providers)
# Install rclone
curl https://rclone.org/install.sh | sudo bash

# Configure
rclone config

# Mount
rclone mount remote:bucket /mnt/cloud --daemon

# Sync
rclone sync /local/path remote:bucket
```

### Cloud Storage Best Practices
```
1. Enable versioning
2. Set lifecycle policies
3. Enable encryption (at rest and in transit)
4. Use appropriate storage class
5. Implement access controls (IAM)
6. Enable logging and monitoring
7. Consider cross-region replication
8. Use transfer acceleration for large files
```

### Cost Optimization
```
- Use lifecycle policies to move old data to cheaper tiers
- Delete incomplete multipart uploads
- Monitor and analyze access patterns
- Use compression before upload
- Consider reserved capacity for predictable workloads
```

**💡 Tip:** Cloud storage is great for backups, but remember egress costs! Design your architecture to minimize data transfer charges.""",

    # =========================================================================
    # NUTANIX CONCEPTS
    # =========================================================================

    "nutanix": """## 🔷 Nutanix Hyperconverged Infrastructure (HCI)

**Definition:** Software-defined infrastructure platform that combines compute, storage, and virtualization in a single cluster.

### What is Nutanix?
Nutanix is a leader in Hyperconverged Infrastructure (HCI), providing:
- Software-defined storage
- Built-in virtualization (AHV)
- Single management plane (Prism)
- Web-scale architecture

### Nutanix Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    NUTANIX CLUSTER                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Node 1    │  │   Node 2    │  │   Node 3    │   ...   │
│  │  ┌───────┐  │  │  ┌───────┐  │  │  ┌───────┐  │         │
│  │  │  CVM  │  │  │  │  CVM  │  │  │  │  CVM  │  │         │
│  │  └───────┘  │  │  └───────┘  │  │  └───────┘  │         │
│  │  ┌───────┐  │  │  ┌───────┐  │  │  ┌───────┐  │         │
│  │  │  AHV  │  │  │  │  AHV  │  │  │  │  AHV  │  │         │
│  │  └───────┘  │  │  └───────┘  │  │  └───────┘  │         │
│  │  ┌───────┐  │  │  ┌───────┐  │  │  ┌───────┐  │         │
│  │  │ SSD/  │  │  │  │ SSD/  │  │  │  │ SSD/  │  │         │
│  │  │ HDD   │  │  │  │ HDD   │  │  │  │ HDD   │  │         │
│  │  └───────┘  │  │  └───────┘  │  │  └───────┘  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│              Distributed Storage Fabric (DSF)               │
├─────────────────────────────────────────────────────────────┤
│                    Prism Management                         │
└─────────────────────────────────────────────────────────────┘
```

### Key Components
| Component | Description |
|-----------|-------------|
| CVM | Controller VM - manages storage on each node |
| AHV | Acropolis Hypervisor - native hypervisor |
| Prism | Web-based management interface |
| DSF | Distributed Storage Fabric |
| AOS | Acropolis Operating System |

### Nutanix vs Traditional 3-Tier
| Feature | Traditional | Nutanix HCI |
|---------|-------------|-------------|
| Architecture | SAN + Servers + Switches | Converged nodes |
| Storage | Dedicated SAN | Distributed (DSF) |
| Management | Multiple consoles | Single pane (Prism) |
| Scaling | Complex | Simple (add nodes) |
| Failover | Manual/complex | Automatic |
| TCO | Higher | Lower |

### Nutanix Products
```
Nutanix Cloud Platform:
├── AOS (Acropolis Operating System)
│   ├── Storage Services
│   ├── Data Protection
│   └── Disaster Recovery
├── AHV (Acropolis Hypervisor)
├── Prism (Management)
│   ├── Prism Element (local)
│   └── Prism Central (multi-cluster)
├── Nutanix Files (File Services)
├── Nutanix Objects (Object Storage)
├── Nutanix Volumes (Block Storage)
├── Flow (Microsegmentation)
├── Calm (Automation/Orchestration)
└── Era (Database Management)
```

### Cluster Requirements
```
Minimum Cluster:
- 3 nodes (for RF2)
- 5 nodes (for RF3)

Hardware per Node:
- CPU: Intel Xeon
- RAM: 64GB+ recommended
- Storage: SSD + HDD (hybrid) or all-flash
- Network: 2x 10GbE minimum
```

**💡 Key Benefit:** Nutanix eliminates the need for separate SAN infrastructure, reducing complexity and cost.""",

    "nutanix_prism": """## 🎛️ Nutanix Prism (Management Interface)

**Definition:** Web-based management interface for Nutanix clusters, available as Prism Element (local) and Prism Central (multi-cluster).

### Prism Element vs Prism Central
| Feature | Prism Element | Prism Central |
|---------|---------------|---------------|
| Scope | Single cluster | Multi-cluster |
| Access | Per cluster IP | Centralized |
| Features | Basic management | Advanced features |
| Licensing | Included | Separate license |
| Deployment | On each cluster | Separate VM |

### Prism Element Features
```
Dashboard:
- Cluster health overview
- Storage utilization
- VM performance
- Alerts and events

VM Management:
- Create/Clone/Delete VMs
- Power operations
- Console access
- Resource allocation

Storage:
- Container management
- Data protection policies
- Storage analytics
```

### Prism Central Features
```
Advanced Management:
- Multi-cluster management
- Capacity planning
- One-click upgrades
- Global policies

Automation:
- Calm blueprints
- Self-service portal
- API automation

Security:
- Flow microsegmentation
- Security policies
- RBAC across clusters

Analytics:
- Prism Pro (ML-based)
- Capacity planning
- Performance analysis
```

### Accessing Prism
```bash
# Prism Element (local cluster)
https://<cluster-ip>:9440

# Prism Central
https://<prism-central-ip>:9440

# Default credentials (first login)
Username: admin
Password: nutanix/4u (change immediately)
```

### Common CLI Commands (acli/ncli)
```bash
# SSH to CVM
ssh nutanix@<cvm-ip>

# Cluster status
ncli cluster get-params
ncli cluster info

# List VMs
acli vm.list

# VM operations
acli vm.on <vm-name>
acli vm.off <vm-name>
acli vm.delete <vm-name>

# Storage containers
ncli container ls
ncli container create name=<name>

# Network
acli net.list
acli net.create <network-name> vlan=<vlan-id>

# Host information
ncli host ls
```

### REST API Access
```bash
# Get cluster info
curl -k -u admin:password \\
  https://<cluster-ip>:9440/api/nutanix/v3/clusters/list \\
  -X POST -H "Content-Type: application/json" \\
  -d '{"kind": "cluster"}'

# List VMs
curl -k -u admin:password \\
  https://<cluster-ip>:9440/api/nutanix/v3/vms/list \\
  -X POST -H "Content-Type: application/json" \\
  -d '{"kind": "vm"}'
```

### Prism Dashboards
```
Home Dashboard:
├── Cluster Health Score
├── Storage Summary
├── VM Summary
├── Alerts (Critical/Warning/Info)
└── Performance Graphs

Analysis Dashboard:
├── Performance metrics
├── Capacity trends
├── Bottleneck detection
└── Recommendations
```

### Alert Categories
| Category | Description |
|----------|-------------|
| Critical | Immediate attention needed |
| Warning | Potential issues |
| Info | Informational events |

**💡 Best Practice:** Deploy Prism Central for multi-cluster environments. Enable Prism Pro for AI-driven insights and capacity planning.""",

    "nutanix_ahv": """## 🖥️ Nutanix AHV (Acropolis Hypervisor)

**Definition:** Nutanix's native, enterprise-grade hypervisor included at no additional cost with Nutanix clusters.

### AHV Overview
```
AHV is built on:
- KVM (Kernel-based Virtual Machine)
- Linux kernel
- Nutanix-optimized

Features:
- Free with Nutanix
- Tight integration with AOS
- No per-VM licensing
- Native management via Prism
```

### AHV vs Other Hypervisors
| Feature | AHV | VMware ESXi | Hyper-V |
|---------|-----|-------------|---------|
| Cost | Free | Licensed | Licensed |
| Management | Prism | vCenter | SCVMM |
| Integration | Native | Supported | Supported |
| Live Migration | AHV Turbo | vMotion | Live Migration |
| HA | Built-in | Requires vSphere | Requires Cluster |

### VM Management (Prism)
```
Create VM:
1. Prism > VM > Create VM
2. Configure:
   - Name
   - vCPUs, Memory
   - Disks (thin/thick)
   - Networks (NICs)
   - Boot order
3. Power on

Clone VM:
1. Select VM > Clone
2. Specify name and count
3. Clone completes quickly (redirect-on-write)
```

### VM Operations (CLI)
```bash
# Connect to CVM
ssh nutanix@<cvm-ip>

# List all VMs
acli vm.list

# Create VM
acli vm.create <vm-name> num_vcpus=2 memory=4G

# Add disk to VM
acli vm.disk_create <vm-name> create_size=50G container=<container>

# Add NIC to VM
acli vm.nic_create <vm-name> network=<network-name>

# Power operations
acli vm.on <vm-name>
acli vm.off <vm-name>
acli vm.force_off <vm-name>
acli vm.reset <vm-name>

# Delete VM
acli vm.delete <vm-name>

# Live migrate
acli vm.migrate <vm-name> host=<target-host>

# Snapshot
acli vm.snapshot_create <vm-name> snapshot_name=<snap-name>
acli vm.snapshot_list <vm-name>
acli vm.snapshot_restore <vm-name> snapshot_name=<snap-name>
```

### VM Configuration
```
Compute:
- vCPUs: 1-64 per VM
- Memory: Up to 6TB per VM
- CPU pinning supported
- NUMA awareness

Storage:
- SCSI, IDE, SATA controllers
- VirtIO for performance
- Thin provisioning default
- Instant clones

Network:
- VirtIO NICs (best performance)
- E1000 for compatibility
- Multiple NICs supported
- VLAN tagging
```

### Guest Tools
```bash
# Nutanix Guest Tools (NGT)
Features:
- Self-service restore
- Application-consistent snapshots
- VSS integration (Windows)
- File-level recovery

Install NGT:
1. Mount NGT ISO to VM
2. Run installer
3. Reboot if required
```

### AHV Networking
```
Network Types:
- Managed: IPAM by AHV
- Unmanaged: External DHCP/static

VLAN Configuration:
acli net.create <name> vlan=100 ip_config=<subnet/prefix>
acli net.update <name> ip_config=<dhcp-start>-<dhcp-end>

# Enable IPAM
acli net.add_dhcp_pool <network> start=192.168.1.100 end=192.168.1.200
```

**💡 Migration Tip:** Nutanix Move tool helps migrate VMs from VMware/Hyper-V to AHV seamlessly.""",

    "nutanix_storage": """## 💾 Nutanix Storage (Distributed Storage Fabric)

**Definition:** Software-defined storage layer that pools all local storage from cluster nodes into a unified, distributed storage system.

### Distributed Storage Fabric (DSF)
```
┌─────────────────────────────────────────────────────────────┐
│                  Distributed Storage Fabric                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Node 1 Storage    Node 2 Storage    Node 3 Storage       │
│   ┌───────────┐     ┌───────────┐     ┌───────────┐        │
│   │ SSD Tier  │     │ SSD Tier  │     │ SSD Tier  │        │
│   ├───────────┤     ├───────────┤     ├───────────┤        │
│   │ HDD Tier  │     │ HDD Tier  │     │ HDD Tier  │        │
│   └───────────┘     └───────────┘     └───────────┘        │
│         ↑                 ↑                 ↑               │
│         └─────────────────┼─────────────────┘               │
│                           │                                 │
│                    ┌──────┴──────┐                          │
│                    │  Storage    │                          │
│                    │    Pool     │                          │
│                    └─────────────┘                          │
│                           │                                 │
│              ┌────────────┼────────────┐                    │
│              ↓            ↓            ↓                    │
│         Container    Container    Container                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Storage Concepts
| Term | Description |
|------|-------------|
| Storage Pool | Aggregation of physical disks |
| Container | Logical storage for VMs (like datastore) |
| vDisk | Virtual disk attached to VM |
| Extent | Fixed-size data block (1MB) |
| Extent Group | Collection of extents on disk |

### Replication Factor (RF)
```
RF2 (Replication Factor 2):
- 2 copies of data
- Survives 1 node failure
- 50% effective capacity
- Minimum 3 nodes

RF3 (Replication Factor 3):
- 3 copies of data
- Survives 2 node failures
- 33% effective capacity
- Minimum 5 nodes
```

### Data Locality
```
Nutanix keeps data local to the VM for best performance:

┌──────────────────┐
│     VM           │
│   ┌──────────┐   │
│   │   Read   │───┼──> Local SSD (fastest)
│   │   Write  │───┼──> Local SSD → Replicate to remote
│   └──────────┘   │
└──────────────────┘

When VM migrates:
- Data follows VM over time
- Background data migration
- Immediate reads from remote (if needed)
```

### Storage Containers
```bash
# List containers
ncli container ls

# Create container
ncli container create name=VMs replication-factor=2

# Container with compression
ncli container create name=VMs \\
  replication-factor=2 \\
  compression-enabled=true \\
  compression-delay=0

# Container with dedup
ncli container create name=VDI \\
  replication-factor=2 \\
  on-disk-dedup=true

# Delete container
ncli container delete name=<container-name>
```

### Storage Optimization Features
```
Inline Features (real-time):
├── Compression (LZ4, Snappy)
├── Erasure Coding (EC-X)
├── Deduplication
└── Data locality

Post-process Features:
├── Cold data tiering
├── Background dedup
└── Data rebalancing

Intelligent Tiering:
┌─────────────────────────────┐
│ Hot Data → SSD Tier         │
│ Warm Data → HDD Tier        │
│ Cold Data → Cloud/Archive   │
└─────────────────────────────┘
```

### Erasure Coding (EC-X)
```
Alternative to RF for cold data:
- Better space efficiency
- EC-X strips + parity
- Use for cold/archival data

Example: EC(4,2)
- 4 data strips
- 2 parity strips
- Can lose any 2 strips
- ~67% efficiency vs 50% for RF2
```

### Storage CLI Commands
```bash
# Storage pool info
ncli sp ls

# Disk info
ncli disk ls
ncli disk get-rack-config

# Container stats
ncli container stats container-name=<name>

# Storage summary
ncli storage-pool ls

# vDisk info
acli vdisk.list
acli vdisk.get <vdisk-id>
```

### Data Protection
```bash
# Protection Domain (PD)
ncli pd create name=<pd-name>
ncli pd add-vms name=<pd-name> vm-names=<vm1,vm2>

# Local snapshot
ncli pd add-one-time-snapshot name=<pd-name>

# Replication to remote site
ncli pd add-remote-site name=<pd-name> remote-site=<site>
```

**💡 Best Practice:** Enable compression and dedup for VDI workloads. Use RF2 for most workloads, RF3 for mission-critical data.""",

    "nutanix_network": """## 🌐 Nutanix Networking

**Definition:** Network architecture and configuration for Nutanix clusters including AHV networking, Flow microsegmentation, and integration options.

### Network Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Physical Network                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│    ┌──────────┐    ┌──────────┐    ┌──────────┐            │
│    │ ToR Sw 1 │    │ ToR Sw 2 │    │ Spine Sw │            │
│    └────┬─────┘    └────┬─────┘    └────┬─────┘            │
│         │               │               │                   │
│    ┌────┴───────────────┴───────────────┴────┐             │
│    │                                         │             │
│    │   ┌─────────────────────────────────┐   │             │
│    │   │      Nutanix Node (AHV)         │   │             │
│    │   │  ┌─────────────────────────┐    │   │             │
│    │   │  │    Virtual Switch       │    │   │             │
│    │   │  │  ┌─────┐ ┌─────┐ ┌─────┐│    │   │             │
│    │   │  │  │VM 1 │ │VM 2 │ │ CVM ││    │   │             │
│    │   │  │  └─────┘ └─────┘ └─────┘│    │   │             │
│    │   │  └─────────────────────────┘    │   │             │
│    │   │       │eth0│    │eth1│          │   │             │
│    │   └───────┴────┴────┴────┴──────────┘   │             │
│    │           10GbE     10GbE               │             │
│    └─────────────────────────────────────────┘             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### AHV Network Types
| Type | Description | Use Case |
|------|-------------|----------|
| Managed | AHV provides IPAM | Simplified management |
| Unmanaged | External DHCP/Static | Integration with existing |

### Network Configuration
```bash
# List networks
acli net.list

# Create unmanaged network (VLAN)
acli net.create <network-name> vlan=100

# Create managed network with IPAM
acli net.create <network-name> vlan=200 \\
  ip_config=192.168.200.0/24

# Add DHCP pool
acli net.add_dhcp_pool <network-name> \\
  start=192.168.200.100 \\
  end=192.168.200.200

# Set gateway/DNS
acli net.update_ip_config <network-name> \\
  default_gateway=192.168.200.1 \\
  dns_servers=8.8.8.8,8.8.4.4

# Delete network
acli net.delete <network-name>
```

### Virtual Switch (OVS)
```
AHV uses Open vSwitch (OVS):
- Software-defined networking
- VLAN support
- Bond/LAG support
- Port mirroring

Bond Modes:
- active-backup (failover)
- balance-slb (load balancing)
- LACP (802.3ad)
```

### Node Network Configuration
```bash
# View host networks
ncli host ls

# View network details
ncli network list

# CVM network (management)
- cvm_internal_address: Internal CVM IP
- external_address: Management IP

# Recommended design:
10GbE Port 1 → Management + CVM
10GbE Port 2 → VM Traffic
(Bond for redundancy)
```

### Flow Network Security
```
Nutanix Flow provides microsegmentation:

┌─────────────────────────────────────────┐
│          Application Tiers               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │   Web   │  │   App   │  │   DB    │  │
│  │  Tier   │  │  Tier   │  │  Tier   │  │
│  └────┬────┘  └────┬────┘  └────┬────┘  │
│       │            │            │       │
│       └──────┬─────┴─────┬──────┘       │
│              │           │              │
│       Flow Security Policies             │
│    (Allow Web→App, App→DB only)         │
└─────────────────────────────────────────┘

Features:
- Application-centric policies
- Zero-trust model
- Visualization
- Quarantine capability
```

### Network Best Practices
```
Physical Network:
✓ Minimum 2x 10GbE per node
✓ Redundant switches (ToR)
✓ Jumbo frames (MTU 9000) for storage
✓ Separate VLANs for management/storage/VMs

Logical Network:
✓ Use managed networks for simpler management
✓ Implement Flow for microsegmentation
✓ Plan IP addressing carefully
✓ Document VLAN assignments

CVM Network:
✓ CVM on management network
✓ Ensure CVM-to-CVM communication
✓ Don't put CVM on isolated network
```

### Troubleshooting Network
```bash
# Check CVM connectivity
ssh nutanix@<cvm-ip>
ping <other-cvm-ip>

# View OVS bridges
ovs-vsctl show

# Check bond status
cat /proc/net/bonding/br0-up

# Network diagnostics
ncc health_checks network_checks run_all

# View ARP table
arp -a

# Trace route
traceroute <destination>
```

**💡 Network Design:** Always use bonding for redundancy. Separate management, storage, and VM traffic on different VLANs when possible.""",

    "nutanix_files": """## 📁 Nutanix Files (File Services)

**Definition:** Software-defined file storage service providing SMB and NFS file shares natively on Nutanix clusters.

### Nutanix Files Overview
```
┌─────────────────────────────────────────────────────────────┐
│                    Nutanix Files                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              File Server VMs (FSVMs)                │   │
│   │  ┌─────────┐  ┌─────────┐  ┌─────────┐             │   │
│   │  │ FSVM 1  │  │ FSVM 2  │  │ FSVM 3  │   (3+ VMs)  │   │
│   │  └─────────┘  └─────────┘  └─────────┘             │   │
│   └─────────────────────────────────────────────────────┘   │
│                           │                                  │
│                    ┌──────┴──────┐                          │
│                    │   Shares    │                          │
│                    └──────┬──────┘                          │
│              ┌────────────┼────────────┐                    │
│              ↓            ↓            ↓                    │
│         SMB Share    NFS Export   Home Dirs                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Protocols:
- SMB 2.1, 3.0, 3.1.1
- NFSv3, NFSv4
```

### Key Features
| Feature | Description |
|---------|-------------|
| Scale-out | Add FSVMs for capacity/performance |
| HA | Multiple FSVMs with failover |
| Snapshots | Self-service file restore |
| Analytics | File Analytics for insights |
| Tiering | Smart data placement |
| Quotas | User/share quotas |

### Deploying Nutanix Files
```
Prerequisites:
1. Prism Central deployed
2. AD/LDAP for SMB
3. Network configured
4. Storage container

Deployment Steps:
1. Prism > File Server > Create
2. Configure:
   - Name
   - Domain (AD)
   - Network
   - Storage container
   - FSVM count (3 minimum)
3. Deploy (takes ~30 minutes)
```

### Creating Shares
```
SMB Share:
1. File Server > Shares > Create Share
2. Type: SMB
3. Configure:
   - Name
   - Size (quota)
   - Access: AD groups/users
   - Self-service restore

NFS Export:
1. File Server > Shares > Create Share
2. Type: NFS
3. Configure:
   - Name
   - Size
   - Client access (IP/subnet)
   - Authentication: sys/krb5

Home Directories:
1. Enable home directory feature
2. Configure: \\\\fileserver\\homes\\%username%
3. Auto-creates user folders
```

### File Analytics
```
Nutanix File Analytics provides:
- Capacity trends
- User activity
- Permission auditing
- Anomaly detection
- Data age analysis

Insights:
├── Top users by capacity
├── File type distribution
├── Inactive data identification
├── Permission reports
└── Ransomware detection
```

### Management Commands
```bash
# File server CLI (SSH to FSVM)
ssh nutanix@<fsvm-ip>

# List shares
afs share.list

# Share statistics
afs share.stats share_name=<name>

# File server health
afs info.fsvm_status

# Capacity info
afs info.capacity

# Connected users (SMB)
smbstatus

# NFS exports
exportfs -v
```

### Integration
```
Active Directory:
- Join domain during deployment
- Machine account created
- DNS records (A, PTR, SPN)

Backup Integration:
- NDMP support
- Veeam integration
- Commvault integration
- Native snapshots

Distributed File System:
- DFS-N support
- Namespace integration
- Referral configuration
```

### Best Practices
```
Deployment:
✓ Minimum 3 FSVMs for HA
✓ Dedicated container for Files
✓ Separate network for file traffic
✓ Enable File Analytics

Performance:
✓ Scale FSVMs for throughput
✓ Use SSDs for metadata
✓ Monitor capacity regularly

Security:
✓ Enable SMB signing
✓ Use SMB encryption
✓ Implement quotas
✓ Regular permission audits
```

**💡 Use Case:** Nutanix Files replaces traditional NAS appliances, providing scalable file services on the same HCI platform.""",

    "nutanix_objects": """## 🗄️ Nutanix Objects (Object Storage)

**Definition:** S3-compatible object storage service running natively on Nutanix clusters for unstructured data.

### Nutanix Objects Overview
```
┌─────────────────────────────────────────────────────────────┐
│                    Nutanix Objects                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│     ┌───────────────────────────────────────────────┐       │
│     │            Object Store Cluster                │       │
│     │  ┌─────────┐  ┌─────────┐  ┌─────────┐       │       │
│     │  │  Node   │  │  Node   │  │  Node   │  ...  │       │
│     │  └─────────┘  └─────────┘  └─────────┘       │       │
│     └───────────────────────────────────────────────┘       │
│                           │                                  │
│              ┌────────────┼────────────┐                    │
│              ↓            ↓            ↓                    │
│          Bucket 1     Bucket 2     Bucket 3                 │
│          (backup)     (archive)    (media)                  │
│                                                             │
│     Access: S3 API (AWS SDK compatible)                     │
└─────────────────────────────────────────────────────────────┘
```

### S3 Compatibility
| Feature | Support |
|---------|---------|
| PUT/GET/DELETE | ✅ |
| Multipart Upload | ✅ |
| Versioning | ✅ |
| Lifecycle Policies | ✅ |
| Object Lock (WORM) | ✅ |
| Bucket Policies | ✅ |
| Access Keys | ✅ |

### Deploying Objects
```
Prerequisites:
1. Prism Central with Objects license
2. DNS configuration
3. SSL certificates
4. Network planning

Deployment:
1. Prism Central > Objects > Create Object Store
2. Configure:
   - Name
   - Domain
   - Capacity
   - Network
   - Node count
3. Deploy
```

### Creating Buckets
```python
# Using boto3 (Python AWS SDK)
import boto3

# Configure endpoint
s3 = boto3.client('s3',
    endpoint_url='https://objects.example.com',
    aws_access_key_id='ACCESS_KEY',
    aws_secret_access_key='SECRET_KEY'
)

# Create bucket
s3.create_bucket(Bucket='my-backup-bucket')

# List buckets
response = s3.list_buckets()
for bucket in response['Buckets']:
    print(bucket['Name'])

# Upload file
s3.upload_file('local-file.txt', 'my-bucket', 'remote-file.txt')

# Download file
s3.download_file('my-bucket', 'remote-file.txt', 'local-copy.txt')

# List objects
response = s3.list_objects_v2(Bucket='my-bucket')
for obj in response.get('Contents', []):
    print(obj['Key'], obj['Size'])
```

### CLI Access (s3cmd, aws-cli)
```bash
# Configure aws-cli
aws configure --profile nutanix
# Enter: Access Key, Secret Key, Region (any), Output format

# Set endpoint
export AWS_ENDPOINT_URL=https://objects.example.com

# List buckets
aws s3 ls --endpoint-url https://objects.example.com

# Create bucket
aws s3 mb s3://my-bucket --endpoint-url https://objects.example.com

# Upload file
aws s3 cp file.txt s3://my-bucket/ --endpoint-url https://objects.example.com

# Sync directory
aws s3 sync /local/dir s3://my-bucket/dir --endpoint-url https://objects.example.com
```

### Object Lifecycle
```json
{
  "Rules": [
    {
      "ID": "Move to archive after 90 days",
      "Status": "Enabled",
      "Filter": {"Prefix": "logs/"},
      "Transitions": [
        {
          "Days": 90,
          "StorageClass": "ARCHIVE"
        }
      ]
    },
    {
      "ID": "Delete after 365 days",
      "Status": "Enabled",
      "Filter": {"Prefix": "temp/"},
      "Expiration": {
        "Days": 365
      }
    }
  ]
}
```

### WORM (Write Once Read Many)
```
Object Lock for compliance:
- Governance Mode: Admins can override
- Compliance Mode: No one can delete
- Legal Hold: Indefinite retention

Use Cases:
- Regulatory compliance
- Financial records
- Healthcare data (HIPAA)
- Legal discovery
```

### Use Cases
```
Backup Target:
- Veeam backup repository
- Commvault backup
- Native Nutanix backup

Archive Storage:
- Cold data tiering
- Long-term retention
- Compliance archives

Application Data:
- Media files
- Log aggregation
- Big data lake
- ML/AI datasets
```

### Best Practices
```
Security:
✓ Use HTTPS only
✓ Rotate access keys
✓ Enable bucket versioning
✓ Implement bucket policies

Performance:
✓ Use multipart for large files
✓ Appropriate bucket sizing
✓ Monitor capacity

Integration:
✓ Test S3 compatibility
✓ Use lifecycle policies
✓ Implement WORM for compliance
```

**💡 Tip:** Nutanix Objects is ideal as a backup target, providing S3-compatible storage without separate object storage infrastructure.""",

    "nutanix_volumes": """## 📀 Nutanix Volumes (Block Storage)

**Definition:** iSCSI block storage service providing external block storage from Nutanix clusters to non-Nutanix hosts.

### Nutanix Volumes Overview
```
┌─────────────────────────────────────────────────────────────┐
│                    Nutanix Cluster                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              Volume Groups (VGs)                     │   │
│   │  ┌─────────────┐  ┌─────────────┐                   │   │
│   │  │   VG 1      │  │   VG 2      │                   │   │
│   │  │ ┌─────────┐ │  │ ┌─────────┐ │                   │   │
│   │  │ │ Disk 1  │ │  │ │ Disk 1  │ │                   │   │
│   │  │ │ Disk 2  │ │  │ │ Disk 2  │ │                   │   │
│   │  │ └─────────┘ │  │ └─────────┘ │                   │   │
│   │  └─────────────┘  └─────────────┘                   │   │
│   └─────────────────────────────────────────────────────┘   │
│                           │                                  │
│                       iSCSI Target                           │
│                           │                                  │
└───────────────────────────┼──────────────────────────────────┘
                            │
              ┌─────────────┼─────────────┐
              ↓             ↓             ↓
         Bare Metal    Physical     External
          Server       Database      Hosts
```

### Use Cases
| Use Case | Description |
|----------|-------------|
| Bare Metal | Storage for physical servers |
| Oracle RAC | Shared storage for clusters |
| MS Failover | Cluster shared volumes |
| External Apps | Non-virtualized workloads |

### Creating Volume Groups
```bash
# Via Prism
1. Storage > Volume Groups > Create
2. Configure:
   - Name
   - iSCSI target name
   - Container
   - Flash mode (optional)

# Via CLI
acli vg.create <vg-name>

# Add disk to VG
acli vg.disk_create <vg-name> size=100G container=<container>

# List volume groups
acli vg.list

# VG details
acli vg.get <vg-name>
```

### iSCSI Configuration
```bash
# Volume Group iSCSI settings
acli vg.update <vg-name> iscsi_target_name=<iqn>

# Add client (initiator)
acli vg.attach_external_client <vg-name> \\
  initiator_iqn=<client-iqn> \\
  client_address=<client-ip>

# Attach to VM (internal)
acli vg.attach_vm <vg-name> vm_name=<vm-name>

# Detach
acli vg.detach_external_client <vg-name> initiator_iqn=<iqn>
```

### Client Configuration (Linux)
```bash
# Install iSCSI initiator
sudo apt install open-iscsi

# Configure initiator name
sudo nano /etc/iscsi/initiatorname.iscsi
InitiatorName=iqn.2024-01.com.client:server1

# Discover targets
sudo iscsiadm -m discovery -t sendtargets -p <cluster-data-ip>

# Login to target
sudo iscsiadm -m node -T <target-iqn> -p <cluster-ip> --login

# Verify disk
lsblk
sudo fdisk -l

# Format and mount
sudo mkfs.ext4 /dev/sdb
sudo mount /dev/sdb /mnt/iscsi

# Persistent login
sudo iscsiadm -m node -T <target-iqn> -o update -n node.startup -v automatic
```

### Client Configuration (Windows)
```powershell
# Open iSCSI Initiator
# Control Panel > iSCSI Initiator

# Discovery Tab:
# Add portal: <cluster-data-ip>

# Targets Tab:
# Select target > Connect
# Enable multi-path if using MPIO

# Initialize disk in Disk Management
# Create partition and format
```

### Multipath (MPIO)
```bash
# Linux MPIO
sudo apt install multipath-tools

# Configure multipath
sudo nano /etc/multipath.conf
defaults {
    user_friendly_names yes
}

blacklist {
    devnode "^sd[a-z]"
}

multipaths {
    multipath {
        wwid <volume-wwid>
        alias nutanix-vol1
    }
}

# Restart and verify
sudo systemctl restart multipathd
sudo multipath -ll
```

### Flash Mode
```
Flash Mode features:
- All writes go to SSD tier
- Consistent low latency
- Ideal for databases

Enable:
1. Edit Volume Group
2. Enable "Flash Mode"
3. Requires available SSD capacity
```

### Best Practices
```
Performance:
✓ Use Flash Mode for latency-sensitive
✓ Enable MPIO for redundancy
✓ Separate data network for iSCSI
✓ Jumbo frames (MTU 9000)

Design:
✓ Plan capacity requirements
✓ Consider VG per application
✓ Document initiator mappings

Security:
✓ Use CHAP authentication
✓ Limit client access by IQN
✓ Network segmentation
```

**💡 Tip:** Nutanix Volumes extends Nutanix storage to non-virtualized workloads, consolidating storage infrastructure.""",

    "nutanix_dr": """## 🔄 Nutanix Disaster Recovery

**Definition:** Built-in data protection and disaster recovery capabilities including snapshots, replication, and automated failover.

### Data Protection Overview
```
┌─────────────────────────────────────────────────────────────┐
│              Nutanix Data Protection                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Local Protection           Remote Protection              │
│   ┌─────────────────┐       ┌─────────────────┐            │
│   │   Snapshots     │       │   Replication   │            │
│   │   (Same site)   │──────>│   (DR site)     │            │
│   └─────────────────┘       └─────────────────┘            │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              Protection Domain (PD)                  │   │
│   │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                   │   │
│   │  │ VM1 │ │ VM2 │ │ VM3 │ │ VG  │                   │   │
│   │  └─────┘ └─────┘ └─────┘ └─────┘                   │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Protection Domains (PD)
```bash
# Create protection domain
ncli pd create name=Production-PD

# Add VMs to PD
ncli pd add-vms name=Production-PD vm-names=VM1,VM2,VM3

# Add volume groups
ncli pd add-volume-groups name=Production-PD volume-group-names=VG1

# List PDs
ncli pd ls

# PD details
ncli pd get name=Production-PD
```

### Snapshot Schedules
```bash
# Create schedule
ncli pd add-schedule name=Production-PD \\
  type=HOURLY \\
  every-nth-hour=1 \\
  user-local-retention-count=24

# Multiple schedules
ncli pd add-schedule name=Production-PD \\
  type=DAILY \\
  user-local-retention-count=7

ncli pd add-schedule name=Production-PD \\
  type=WEEKLY \\
  user-local-retention-count=4

# Manual snapshot
ncli pd add-one-time-snapshot name=Production-PD
```

### Remote Site Configuration
```bash
# Add remote site (Prism Central recommended)
ncli remote-site create name=DR-Site \\
  addresses=<dr-cluster-ip> \\
  username=admin \\
  password=<password>

# Add remote site to PD
ncli pd add-remote-site name=Production-PD \\
  remote-site-name=DR-Site

# Configure replication schedule
ncli pd add-remote-schedule name=Production-PD \\
  remote-site-name=DR-Site \\
  type=HOURLY \\
  every-nth-hour=1 \\
  remote-retention-count=24
```

### Async vs NearSync Replication
| Feature | Async | NearSync |
|---------|-------|----------|
| RPO | Minutes-Hours | Seconds |
| Network | Standard WAN | Low latency |
| Distance | Any | Limited |
| Use Case | Standard DR | Near-zero RPO |

### Failover Types
```
Planned Failover:
- Graceful migration to DR
- VMs shut down cleanly
- Final replication occurs
- Zero data loss

Unplanned Failover:
- Source site unavailable
- Activate from last snapshot
- Potential data loss (RPO)
- Emergency recovery
```

### Failover Process
```bash
# Planned failover (DR site)
ncli pd activate name=Production-PD \\
  type=planned-failover

# Unplanned failover (DR site)
ncli pd activate name=Production-PD \\
  type=unplanned-failover

# After activation
# VMs appear on DR cluster
# Update DNS/networking
# Verify application functionality
```

### Nutanix Leap (PC-based DR)
```
Prism Central Leap provides:
- Orchestrated failover
- Recovery plans
- Network mappings
- Runbook automation
- Non-disruptive testing

Features:
├── Automated recovery plans
├── Test failover (isolated network)
├── Multi-VM coordination
├── Progress monitoring
└── Detailed reporting
```

### Recovery Plans (Leap)
```
Recovery Plan includes:
1. VM power-on sequence
2. Network mappings
3. IP address updates
4. Script execution
5. Validation steps

Example Plan:
Stage 1: Database servers
Stage 2: Application servers (wait for DB)
Stage 3: Web servers (wait for App)
Stage 4: Validation scripts
```

### DR Best Practices
```
RPO/RTO Planning:
✓ Define RPO per application
✓ Define RTO requirements
✓ Size bandwidth accordingly
✓ Test regularly

Network:
✓ Dedicated replication network
✓ Adequate bandwidth
✓ Plan IP mappings for DR
✓ DNS failover strategy

Testing:
✓ Regular DR tests (quarterly)
✓ Document procedures
✓ Test failback
✓ Update runbooks
```

**💡 Tip:** Use Leap in Prism Central for orchestrated, automated DR. Regular testing is essential for DR success.""",

    "nutanix_cli": """## 💻 Nutanix CLI Commands Reference

**Definition:** Command-line interfaces for managing Nutanix clusters: nCLI, aCLI, and other administrative commands.

### Accessing CLI
```bash
# SSH to CVM (Controller VM)
ssh nutanix@<cvm-ip>
# Default password: nutanix/4u

# SSH to any CVM in cluster
ssh nutanix@<cluster-virtual-ip>
```

### nCLI (Nutanix CLI)
```bash
# Cluster Information
ncli cluster info
ncli cluster get-params
ncli cluster get-build-info

# List all options
ncli help

# Specific command help
ncli cluster help

# Host management
ncli host ls
ncli host get id=<host-id>

# Storage containers
ncli container ls
ncli container get name=<container-name>
ncli container create name=<name> replication-factor=2

# Disks
ncli disk ls
ncli disk get id=<disk-id>

# Network
ncli network list

# Alerts
ncli alert ls
ncli alert acknowledge id=<alert-id>

# Health checks
ncc health_checks run_all
ncc health_checks list
```

### aCLI (Acropolis CLI)
```bash
# VM Management
acli vm.list
acli vm.get <vm-name>
acli vm.create <vm-name> num_vcpus=2 memory=4G
acli vm.update <vm-name> num_vcpus=4
acli vm.delete <vm-name>

# VM Power Operations
acli vm.on <vm-name>
acli vm.off <vm-name>
acli vm.force_off <vm-name>
acli vm.reset <vm-name>
acli vm.guest_shutdown <vm-name>

# VM Disks
acli vm.disk_create <vm-name> create_size=50G container=<container>
acli vm.disk_update <vm-name> disk_addr=scsi.0 size=100G
acli vm.disk_delete <vm-name> disk_addr=scsi.0

# VM NICs
acli vm.nic_create <vm-name> network=<network-name>
acli vm.nic_delete <vm-name> nic_addr=<mac>

# VM Migration
acli vm.migrate <vm-name> host=<target-host>

# Snapshots
acli vm.snapshot_create <vm-name> snapshot_name=<name>
acli vm.snapshot_list <vm-name>
acli vm.snapshot_restore <vm-name> snapshot_name=<name>

# Clone
acli vm.clone <source-vm> clone_name=<new-name>

# Networks
acli net.list
acli net.create <name> vlan=<vlan-id>
acli net.delete <name>

# Images
acli image.list
acli image.create <name> source_url=<url> container=<container>

# Volume Groups
acli vg.list
acli vg.create <name>
acli vg.disk_create <vg-name> size=100G
```

### NCC (Nutanix Cluster Check)
```bash
# Run all health checks
ncc health_checks run_all

# Run specific checks
ncc health_checks hardware_checks run_all
ncc health_checks network_checks run_all
ncc health_checks cluster_checks run_all

# List available checks
ncc health_checks list

# View results
ncc health_checks show_results
```

### Useful System Commands
```bash
# Cluster services
genesis status                 # Core services status
cluster status                 # Cluster health
allssh "genesis status"        # All CVMs

# CVM restart services
genesis restart                # Restart all services
genesis restart <service>      # Restart specific service

# Log collection
logbay collect                 # Collect logs for support

# Upgrade
ncli software upload software-type=nos file-path=<path>
ncli cluster upgrade-apply

# Password management
ncli user reset-password user-name=admin
```

### API Commands (nuclei)
```bash
# List VMs via API
nuclei vm.list

# VM details
nuclei vm.get <vm-uuid>

# Cluster info
nuclei cluster.list
```

### Common Troubleshooting
```bash
# Check cluster health
ncc health_checks run_all

# Check services
genesis status
cluster status

# Check CVM connectivity
allssh "ping -c 3 <cvm-ip>"

# Check storage
ncli sp ls
ncli disk ls

# Check network
ping <gateway>
traceroute <destination>

# View logs
tail -f /home/nutanix/data/logs/stargate.INFO
tail -f /home/nutanix/data/logs/cerebro.INFO

# Support bundle
logbay collect -t <case-number>
```

### Quick Reference Table
| Task | Command |
|------|---------|
| List VMs | `acli vm.list` |
| Start VM | `acli vm.on <name>` |
| Stop VM | `acli vm.off <name>` |
| List containers | `ncli container ls` |
| Cluster status | `cluster status` |
| Health check | `ncc health_checks run_all` |
| Service status | `genesis status` |
| List hosts | `ncli host ls` |

**💡 Pro Tip:** Use `allssh` to run commands on all CVMs: `allssh "command"`""",

    # Aliases for better matching
    "prism": """## 🎛️ Nutanix Prism (Management Interface)

**Definition:** Web-based management interface for Nutanix clusters, available as Prism Element (local) and Prism Central (multi-cluster).

For detailed information, ask about `nutanix_prism`.

### Quick Overview
- **Prism Element**: Per-cluster management
- **Prism Central**: Multi-cluster management

### Access
```bash
# Prism Element
https://<cluster-ip>:9440

# Prism Central
https://<prism-central-ip>:9440
```

### Key Features
- Dashboard with cluster health
- VM management
- Storage management
- Network configuration
- Alerts and events""",

    "ahv": """## 🖥️ AHV (Acropolis Hypervisor)

**Definition:** Nutanix's native hypervisor based on KVM, included free with all Nutanix clusters.

For detailed information, ask about `nutanix_ahv`.

### Quick Overview
- Built on KVM
- No licensing cost
- Managed via Prism
- Tight AOS integration

### Key Commands
```bash
# List VMs
acli vm.list

# Start/Stop VM
acli vm.on <vm-name>
acli vm.off <vm-name>

# Create VM
acli vm.create <name> num_vcpus=2 memory=4G
```""",

    "cvm": """## 🔧 Nutanix CVM (Controller VM)

**Definition:** The Controller Virtual Machine runs on each Nutanix node and manages all storage and cluster operations.

### CVM Overview
```
Each Nutanix node has:
┌─────────────────────┐
│    Nutanix Node     │
│  ┌───────────────┐  │
│  │      CVM      │  │ ← Controller VM
│  │  - Stargate   │  │   (manages storage)
│  │  - Curator    │  │
│  │  - Cassandra  │  │
│  │  - Cerebro    │  │
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │  AHV / ESXi   │  │ ← Hypervisor
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │   User VMs    │  │ ← Workloads
│  └───────────────┘  │
└─────────────────────┘
```

### Key CVM Services
| Service | Function |
|---------|----------|
| Stargate | I/O handling |
| Curator | Background tasks |
| Cassandra | Metadata store |
| Cerebro | Replication |
| Zookeeper | Configuration |

### Accessing CVM
```bash
ssh nutanix@<cvm-ip>
# Default password: nutanix/4u
```""",

    "hci": """## 🔷 HCI (Hyperconverged Infrastructure)

**Definition:** IT infrastructure that combines compute, storage, and networking in a single software-defined platform.

Nutanix is a leader in HCI. For detailed information, ask about `nutanix`.

### What is HCI?
```
Traditional 3-Tier:          HCI:
┌─────────────────┐         ┌─────────────────┐
│   Compute       │         │  ┌───────────┐  │
│   (Servers)     │         │  │ Compute + │  │
├─────────────────┤    →    │  │ Storage + │  │
│   Network       │         │  │ Network   │  │
│   (SAN)         │         │  └───────────┘  │
├─────────────────┤         └─────────────────┘
│   Storage       │              Single
│   (SAN Array)   │              Platform
└─────────────────┘
```

### HCI Benefits
- Simplified management
- Reduced complexity
- Lower TCO
- Linear scalability
- Built-in data protection""",

}

# =============================================================================
# TAGS FOR SEARCH AND CATEGORIZATION
# =============================================================================

INFRASTRUCTURE_TAGS = [
    # Networking Protocols
    "tcp", "udp", "http", "https", "dns", "dhcp", "ip", "ipv4", "ipv6",
    "ftp", "ssh", "smtp", "snmp", "icmp", "arp",
    
    # Networking Concepts
    "osi", "osi model", "tcp/ip", "subnet", "subnetting", "cidr", "nat", "pat",
    "firewall", "vpn", "ssl", "tls", "routing", "switching", "vlan",
    
    # Network Tools
    "ping", "traceroute", "netstat", "nslookup", "dig", "tcpdump",
    "wireshark", "nmap", "curl", "wget", "iptables", "ufw",
    
    # Web Servers
    "apache", "nginx", "httpd", "web server", "reverse proxy", "load balancer",
    
    # Databases
    "mysql", "postgresql", "postgres", "mongodb", "database", "sql", "nosql",
    
    # Server Administration
    "server", "systemd", "systemctl", "service", "process", "cron",
    "monitoring", "logging", "logs",
    
    # Storage
    "filesystem", "ext4", "xfs", "ntfs", "permissions", "chmod", "chown",
    "raid", "raid0", "raid1", "raid5", "raid10", "lvm",
    "san", "nas", "iscsi", "nfs", "smb", "cifs", "samba",
    "backup", "rsync", "tar", "cloud storage", "s3", "azure", "gcp",
    
    # Nutanix
    "nutanix", "hci", "hyperconverged", "prism", "prism central", "prism element",
    "ahv", "acropolis", "cvm", "controller vm", "dsf", "distributed storage",
    "nutanix storage", "nutanix network", "nutanix files", "nutanix objects",
    "nutanix volumes", "volume group", "protection domain", "nutanix dr",
    "leap", "ncli", "acli", "ncc", "nutanix cli",
]
