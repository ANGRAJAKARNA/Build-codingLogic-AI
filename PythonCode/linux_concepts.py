# linux_concepts.py
"""
Linux Concepts - Comprehensive Linux System Administration Knowledge
Senior Linux Engineer-level explanations covering:
- Linux Fundamentals and Architecture
- Boot Process and Internals
- File Systems and Storage
- Permissions and Security
- Command Line and Utilities
- User and Group Management
- Process and Service Management
- Networking
- Security (SELinux, Firewalls)
- Package Management
- Shell Scripting
- Monitoring and Performance
- Logs and Troubleshooting
- Virtualization and Containers
- Production and DevOps
"""

# =============================================================================
# LINUX CONCEPTS DICTIONARY
# =============================================================================

LINUX_CONCEPTS = {

    # =========================================================================
    # LINUX FUNDAMENTALS
    # =========================================================================

    "linux": """## 🐧 Linux Overview

**Definition:** Linux is a free, open-source, Unix-like operating system kernel created by Linus Torvalds in 1991. Combined with GNU tools, it forms complete operating systems called Linux distributions.

### History Timeline
```
1969 - UNIX created at Bell Labs
1983 - GNU Project started by Richard Stallman
1991 - Linux kernel released by Linus Torvalds
1992 - Linux + GNU = complete OS
1993 - Debian, Slackware released
1994 - Red Hat Linux released
2004 - Ubuntu released
2010+ - Linux dominates servers, cloud, mobile (Android)
```

### Linux vs UNIX
| Feature | Linux | UNIX |
|---------|-------|------|
| Source | Open source | Proprietary (mostly) |
| Cost | Free | Licensed |
| Hardware | Any hardware | Specific hardware |
| Examples | Ubuntu, RHEL | Solaris, AIX, HP-UX |

### Why Linux?
```
✓ Free and open source
✓ Highly stable and secure
✓ Runs on any hardware
✓ Dominates servers (96%+ of web servers)
✓ Powers cloud infrastructure
✓ Android (mobile) is Linux-based
✓ Highly customizable
✓ Excellent for development
```

### Linux Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    User Applications                     │
│              (Browsers, Office, Games)                  │
├─────────────────────────────────────────────────────────┤
│                     Shell (bash, zsh)                    │
├─────────────────────────────────────────────────────────┤
│                   System Libraries                       │
│                (glibc, libpthread)                       │
├─────────────────────────────────────────────────────────┤
│                   System Calls                           │
├─────────────────────────────────────────────────────────┤
│                    Linux Kernel                          │
│    ┌─────────┬─────────┬─────────┬─────────────┐        │
│    │Process  │ Memory  │  File   │   Device    │        │
│    │ Mgmt    │  Mgmt   │ System  │   Drivers   │        │
│    └─────────┴─────────┴─────────┴─────────────┘        │
├─────────────────────────────────────────────────────────┤
│                      Hardware                            │
│           (CPU, RAM, Disk, Network, etc.)               │
└─────────────────────────────────────────────────────────┘
```

### Kernel Space vs User Space
```
Kernel Space:
- Direct hardware access
- Privileged operations
- Memory management
- Device drivers
- System calls

User Space:
- Applications run here
- Limited hardware access
- Uses system calls to request kernel services
- Isolated from other processes
```

### Popular Linux Distributions
| Distro | Base | Use Case | Package Manager |
|--------|------|----------|-----------------|
| Ubuntu | Debian | Desktop, Server | apt |
| RHEL | Fedora | Enterprise | dnf/yum |
| CentOS/Rocky | RHEL | Free Enterprise | dnf/yum |
| Debian | - | Stability | apt |
| Fedora | - | Latest features | dnf |
| Arch | - | Customization | pacman |
| Alpine | - | Containers | apk |

### Getting Started
```bash
# Check Linux version
uname -a
cat /etc/os-release

# Check kernel version
uname -r

# Check distribution
lsb_release -a

# System information
hostnamectl
```

**💡 Career Tip:** Linux skills are essential for DevOps, SRE, System Admin, and Cloud Engineering roles.""",

    "linux_distro": """## 📦 Linux Distributions

**Definition:** A Linux distribution (distro) is a complete operating system built around the Linux kernel, including system utilities, package manager, and desktop environment.

### Distribution Families
```
┌─────────────────────────────────────────────────────────┐
│                   Linux Distributions                    │
├─────────────┬─────────────┬─────────────┬──────────────┤
│   Debian    │   Red Hat   │    Arch     │  Independent │
│   Family    │   Family    │   Family    │              │
├─────────────┼─────────────┼─────────────┼──────────────┤
│ Debian      │ RHEL        │ Arch Linux  │ Slackware    │
│ Ubuntu      │ CentOS      │ Manjaro     │ Gentoo       │
│ Linux Mint  │ Rocky Linux │ EndeavourOS │ Alpine       │
│ Kali Linux  │ Fedora      │ Garuda      │ NixOS        │
│ Pop!_OS     │ Amazon Linux│ BlackArch   │ Void Linux   │
└─────────────┴─────────────┴─────────────┴──────────────┘
```

### Choosing a Distribution
| Use Case | Recommended Distro | Why |
|----------|-------------------|-----|
| Server (Enterprise) | RHEL, Rocky Linux | Support, stability |
| Server (Free) | Ubuntu Server, Debian | Community, packages |
| Desktop (Beginner) | Ubuntu, Linux Mint | User-friendly |
| Desktop (Advanced) | Fedora, Arch | Latest software |
| Containers | Alpine | Minimal, secure |
| Security/Pentesting | Kali Linux | Security tools |
| Learning | Ubuntu, Fedora | Good documentation |
| Production/Cloud | Ubuntu LTS, RHEL | Long-term support |

### Debian Family
```
Package Manager: apt (dpkg)
Package Format: .deb

# Update package list
sudo apt update

# Upgrade packages
sudo apt upgrade

# Install package
sudo apt install nginx

# Remove package
sudo apt remove nginx

Key Distros:
- Debian: Stability-focused, long release cycles
- Ubuntu: User-friendly, 6-month releases + LTS
- Linux Mint: Desktop-focused, Cinnamon DE
```

### Red Hat Family
```
Package Manager: dnf/yum (rpm)
Package Format: .rpm

# Update packages
sudo dnf update

# Install package
sudo dnf install nginx

# Remove package
sudo dnf remove nginx

Key Distros:
- RHEL: Enterprise, paid support
- Rocky/AlmaLinux: Free RHEL alternatives
- Fedora: Cutting-edge, upstream of RHEL
- CentOS Stream: Rolling preview of RHEL
```

### Arch Family
```
Package Manager: pacman
Package Format: .pkg.tar.zst

# Sync and update
sudo pacman -Syu

# Install package
sudo pacman -S nginx

# Remove package
sudo pacman -R nginx

Philosophy:
- Rolling release (always latest)
- DIY approach
- Excellent documentation (Arch Wiki)
- AUR (Arch User Repository)
```

### LTS vs Rolling Release
| Feature | LTS (Ubuntu, RHEL) | Rolling (Arch, Fedora) |
|---------|-------------------|------------------------|
| Updates | Major releases | Continuous |
| Stability | High | Variable |
| Software | Tested, older | Latest |
| Support | Years | Ongoing |
| Best for | Servers | Desktops |

**💡 Production Tip:** Use LTS distributions for servers. Ubuntu LTS has 5 years support, RHEL has 10 years.""",

    "linux_kernel": """## ⚙️ Linux Kernel

**Definition:** The kernel is the core of the operating system, managing hardware resources and providing services to user-space applications through system calls.

### Kernel Responsibilities
```
┌─────────────────────────────────────────────────────────┐
│                     Linux Kernel                         │
├──────────────┬──────────────┬──────────────┬────────────┤
│   Process    │    Memory    │     File     │   Device   │
│  Management  │  Management  │    System    │  Drivers   │
├──────────────┼──────────────┼──────────────┼────────────┤
│ - Scheduling │ - Virtual    │ - VFS        │ - Hardware │
│ - Creation   │   memory     │ - ext4, xfs  │   access   │
│ - IPC        │ - Paging     │ - I/O        │ - Modules  │
│ - Signals    │ - Allocation │ - Caching    │ - Drivers  │
└──────────────┴──────────────┴──────────────┴────────────┘
```

### Kernel Types
| Type | Description | Example |
|------|-------------|---------|
| Monolithic | All services in kernel space | Linux |
| Microkernel | Minimal kernel, services in user space | Minix |
| Hybrid | Mix of both | Windows NT |

Linux is **monolithic but modular** - core is monolithic but supports loadable modules.

### Kernel Information Commands
```bash
# Kernel version
uname -r
# Example: 5.15.0-91-generic

# Detailed system info
uname -a

# Kernel parameters
cat /proc/cmdline

# Kernel configuration
cat /boot/config-$(uname -r) | grep CONFIG_SMP

# Loaded modules
lsmod

# Module information
modinfo ext4
```

### Kernel Modules
```bash
# List loaded modules
lsmod

# Load module
sudo modprobe <module_name>
sudo modprobe vfat

# Remove module
sudo modprobe -r <module_name>

# Load module at boot (/etc/modules-load.d/)
echo "vfat" | sudo tee /etc/modules-load.d/vfat.conf

# Blacklist module (/etc/modprobe.d/)
echo "blacklist nouveau" | sudo tee /etc/modprobe.d/blacklist-nouveau.conf

# Module parameters
modinfo -p <module_name>
```

### /proc and /sys Filesystems
```bash
# /proc - Process and kernel information
/proc/cpuinfo      # CPU information
/proc/meminfo      # Memory information
/proc/version      # Kernel version
/proc/<PID>/       # Process-specific info
/proc/sys/         # Kernel tunables

# /sys - Device and driver information
/sys/class/        # Device classes
/sys/block/        # Block devices
/sys/devices/      # All devices
/sys/module/       # Loaded modules

# Read kernel parameter
cat /proc/sys/net/ipv4/ip_forward

# Set kernel parameter (temporary)
echo 1 > /proc/sys/net/ipv4/ip_forward

# Set kernel parameter (permanent)
echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
sysctl -p
```

### System Calls
```
User applications communicate with kernel via system calls:

Application → System Call → Kernel → Hardware

Common System Calls:
- open(), read(), write(), close() - File I/O
- fork(), exec(), exit() - Process management
- socket(), bind(), listen() - Networking
- mmap(), brk() - Memory allocation
```

### Kernel Compilation (Advanced)
```bash
# Get kernel source
wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.15.tar.xz
tar xf linux-5.15.tar.xz
cd linux-5.15

# Configure
make menuconfig

# Compile
make -j$(nproc)

# Install
sudo make modules_install
sudo make install
```

**💡 Production Tip:** Avoid custom kernels in production unless absolutely necessary. Use distribution-provided kernels for stability and security updates.""",


    # =========================================================================
    # LINUX BOOT PROCESS
    # =========================================================================

    "linux_boot": """## 🚀 Linux Boot Process

**Definition:** The boot process is the sequence of events from power-on to a fully running Linux system with login prompt.

### Boot Sequence Overview
```
┌─────────────────────────────────────────────────────────┐
│                    BOOT SEQUENCE                         │
├─────────────────────────────────────────────────────────┤
│  1. Power On                                            │
│       ↓                                                 │
│  2. BIOS/UEFI (POST - Power On Self Test)              │
│       ↓                                                 │
│  3. Boot Loader (GRUB2)                                │
│       ↓                                                 │
│  4. Kernel Loading                                      │
│       ↓                                                 │
│  5. initramfs/initrd                                   │
│       ↓                                                 │
│  6. Init System (systemd)                              │
│       ↓                                                 │
│  7. Target/Runlevel Reached                            │
│       ↓                                                 │
│  8. Login Prompt                                        │
└─────────────────────────────────────────────────────────┘
```

### Stage 1: BIOS vs UEFI
| Feature | BIOS | UEFI |
|---------|------|------|
| Age | 1975+ | 2005+ |
| Interface | Text-based | Graphical |
| Boot disk | MBR (2TB limit) | GPT (9ZB limit) |
| Boot mode | 16-bit real mode | 32/64-bit |
| Secure Boot | No | Yes |
| Boot speed | Slower | Faster |

```bash
# Check boot mode
[ -d /sys/firmware/efi ] && echo "UEFI" || echo "BIOS"

# UEFI variables
ls /sys/firmware/efi/efivars/
```

### Stage 2: GRUB2 (Boot Loader)
```bash
# GRUB configuration
/etc/default/grub              # Default settings
/boot/grub/grub.cfg            # Generated config
/etc/grub.d/                   # Custom scripts

# Edit defaults
sudo nano /etc/default/grub
GRUB_TIMEOUT=5
GRUB_DEFAULT=0
GRUB_CMDLINE_LINUX="quiet splash"

# Regenerate GRUB config
sudo update-grub              # Debian/Ubuntu
sudo grub2-mkconfig -o /boot/grub2/grub.cfg  # RHEL

# Install GRUB to MBR
sudo grub-install /dev/sda
```

### Stage 3: Kernel and initramfs
```
Kernel Loading:
1. GRUB loads kernel (vmlinuz) into memory
2. GRUB loads initramfs (initial RAM filesystem)
3. Kernel initializes hardware
4. Kernel mounts initramfs as temporary root

initramfs Purpose:
- Contains drivers needed to mount real root
- Handles encrypted disks, RAID, LVM
- Transitions to real root filesystem
```

```bash
# View initramfs contents
lsinitramfs /boot/initrd.img-$(uname -r)

# Rebuild initramfs
sudo update-initramfs -u      # Debian/Ubuntu
sudo dracut -f                # RHEL
```

### Stage 4: systemd Initialization
```
systemd takes over from initramfs:
1. Mounts real root filesystem
2. Starts essential services
3. Reaches target (multi-user, graphical)

Boot targets:
- poweroff.target     - Halt system
- rescue.target       - Single user mode
- multi-user.target   - Multi-user, no GUI (runlevel 3)
- graphical.target    - Multi-user with GUI (runlevel 5)
```

```bash
# View default target
systemctl get-default

# Set default target
sudo systemctl set-default multi-user.target
sudo systemctl set-default graphical.target

# Change target (runtime)
sudo systemctl isolate rescue.target
```

### Boot Troubleshooting
```bash
# View boot messages
dmesg
journalctl -b              # Current boot
journalctl -b -1           # Previous boot
journalctl -b --list-boots # List all boots

# Boot into rescue mode (GRUB)
# At GRUB menu, press 'e' to edit
# Add to linux line: systemd.unit=rescue.target
# Press Ctrl+X to boot

# Boot into emergency mode
# Add: systemd.unit=emergency.target

# Common boot issues:
- "Kernel panic" - Hardware/driver issue
- "No init found" - initramfs problem
- "Filesystem check failed" - Disk errors
- "Dependency failed" - Service issues
```

### Kernel Parameters
```bash
# View current parameters
cat /proc/cmdline

# Common parameters:
quiet          - Suppress most boot messages
splash         - Show splash screen
single/1       - Single user mode
init=/bin/bash - Boot to shell
nomodeset      - Disable kernel mode setting
```

**💡 Recovery Tip:** If system won't boot, try rescue mode first, then emergency mode. Use a live USB as last resort.""",

    "grub": """## 🔧 GRUB2 Boot Loader

**Definition:** GRUB (GRand Unified Bootloader) is the default boot loader for most Linux distributions, responsible for loading the kernel and initramfs.

### GRUB Configuration Files
```bash
/etc/default/grub          # User settings
/etc/grub.d/               # Script modules
  ├── 00_header            # GRUB settings
  ├── 10_linux             # Linux entries
  ├── 20_linux_xen         # Xen entries
  ├── 30_os-prober         # Other OS detection
  ├── 40_custom            # Custom entries
  └── 41_custom            # More custom entries
/boot/grub/grub.cfg        # Generated config (DON'T EDIT)
```

### /etc/default/grub Options
```bash
# Timeout before auto-boot
GRUB_TIMEOUT=5

# Default entry (0 = first)
GRUB_DEFAULT=0

# Remember last selection
GRUB_DEFAULT=saved
GRUB_SAVEDEFAULT=true

# Kernel parameters
GRUB_CMDLINE_LINUX="quiet splash"
GRUB_CMDLINE_LINUX_DEFAULT="quiet"

# Show/hide menu
GRUB_TIMEOUT_STYLE=menu    # Show menu
GRUB_TIMEOUT_STYLE=hidden  # Hide menu

# Resolution
GRUB_GFXMODE=1920x1080
```

### Update GRUB
```bash
# After changing /etc/default/grub
# Debian/Ubuntu
sudo update-grub

# RHEL/CentOS
sudo grub2-mkconfig -o /boot/grub2/grub.cfg

# UEFI systems
sudo grub2-mkconfig -o /boot/efi/EFI/redhat/grub.cfg
```

### Add Custom Entry
```bash
# Edit /etc/grub.d/40_custom
sudo nano /etc/grub.d/40_custom

menuentry "My Custom Entry" {
    set root=(hd0,1)
    linux /boot/vmlinuz root=/dev/sda1
    initrd /boot/initrd.img
}

# Update GRUB
sudo update-grub
```

### GRUB Rescue
```bash
# If you see grub rescue> prompt:

# List available partitions
ls
ls (hd0,1)/

# Set root and prefix
set root=(hd0,1)
set prefix=(hd0,1)/boot/grub

# Load modules
insmod normal
normal

# Or boot manually
insmod linux
linux /boot/vmlinuz root=/dev/sda1
initrd /boot/initrd.img
boot
```

### Repair GRUB
```bash
# Boot from Live USB, then:

# Mount root partition
sudo mount /dev/sda1 /mnt

# For UEFI, also mount EFI partition
sudo mount /dev/sda1 /mnt/boot/efi

# Chroot into system
sudo mount --bind /dev /mnt/dev
sudo mount --bind /proc /mnt/proc
sudo mount --bind /sys /mnt/sys
sudo chroot /mnt

# Reinstall GRUB
grub-install /dev/sda           # BIOS
grub-install --target=x86_64-efi --efi-directory=/boot/efi  # UEFI

# Regenerate config
update-grub

# Exit and reboot
exit
sudo reboot
```

### Password Protect GRUB
```bash
# Generate password hash
grub-mkpasswd-pbkdf2

# Add to /etc/grub.d/40_custom
set superusers="admin"
password_pbkdf2 admin grub.pbkdf2.sha512.10000.HASH...

# Update GRUB
sudo update-grub
```

**💡 Security Tip:** Password-protect GRUB in production to prevent unauthorized single-user access.""",

    "systemd": """## ⚡ systemd (System and Service Manager)

**Definition:** systemd is the init system and service manager for modern Linux, replacing SysVinit. It manages system startup, services, logging, and more.

### What systemd Manages
```
systemd Components:
├── systemd        - Init system (PID 1)
├── systemctl      - Service management
├── journald       - Logging
├── logind         - Login management
├── networkd       - Network configuration
├── resolved       - DNS resolution
├── timesyncd      - Time synchronization
└── udevd          - Device management
```

### Unit Types
| Type | Extension | Purpose |
|------|-----------|---------|
| Service | .service | Daemons and services |
| Socket | .socket | Socket activation |
| Target | .target | Group of units |
| Mount | .mount | Filesystem mounts |
| Timer | .timer | Scheduled tasks (cron) |
| Path | .path | Path-based activation |
| Device | .device | Device units |

### systemctl Commands
```bash
# Service Management
systemctl start nginx        # Start service
systemctl stop nginx         # Stop service
systemctl restart nginx      # Restart service
systemctl reload nginx       # Reload config
systemctl status nginx       # Check status

# Enable/Disable at Boot
systemctl enable nginx       # Enable at boot
systemctl disable nginx      # Disable at boot
systemctl is-enabled nginx   # Check if enabled

# List Services
systemctl list-units --type=service
systemctl list-units --type=service --state=running
systemctl list-units --type=service --state=failed
systemctl list-unit-files --type=service

# System State
systemctl is-system-running  # Check overall state
systemctl --failed           # List failed units
```

### Service Unit File
```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
Documentation=https://example.com/docs
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=appuser
Group=appgroup
WorkingDirectory=/opt/myapp
Environment=NODE_ENV=production
ExecStartPre=/opt/myapp/pre-start.sh
ExecStart=/opt/myapp/start.sh
ExecStop=/opt/myapp/stop.sh
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Service Types
| Type | Description |
|------|-------------|
| simple | Default, main process stays in foreground |
| forking | Forks and parent exits |
| oneshot | Short-lived, runs once |
| notify | Sends notification when ready |
| idle | Waits until no jobs pending |

### Create Custom Service
```bash
# Create service file
sudo nano /etc/systemd/system/myapp.service

# Reload systemd
sudo systemctl daemon-reload

# Enable and start
sudo systemctl enable myapp
sudo systemctl start myapp

# Check status
systemctl status myapp
```

### Targets (Runlevels)
```bash
# View current target
systemctl get-default

# Set default target
sudo systemctl set-default multi-user.target
sudo systemctl set-default graphical.target

# Change target now
sudo systemctl isolate rescue.target

# Target equivalents to runlevels:
runlevel 0 = poweroff.target
runlevel 1 = rescue.target
runlevel 3 = multi-user.target
runlevel 5 = graphical.target
runlevel 6 = reboot.target
```

### journalctl (Logs)
```bash
# View all logs
journalctl

# Follow logs (like tail -f)
journalctl -f

# Service logs
journalctl -u nginx
journalctl -u nginx -f

# Boot logs
journalctl -b           # Current boot
journalctl -b -1        # Previous boot

# Time-based
journalctl --since "1 hour ago"
journalctl --since "2024-01-01" --until "2024-01-02"

# Priority
journalctl -p err       # Errors and above
journalctl -p warning   # Warnings and above

# Kernel messages
journalctl -k

# Disk usage
journalctl --disk-usage

# Clean old logs
sudo journalctl --vacuum-time=7d
sudo journalctl --vacuum-size=100M
```

**💡 Best Practice:** Always use `systemctl daemon-reload` after modifying service files.""",


    # =========================================================================
    # LINUX FILE SYSTEM
    # =========================================================================

    "linux_filesystem": """## 📁 Linux File System Hierarchy

**Definition:** The Filesystem Hierarchy Standard (FHS) defines the directory structure and contents in Linux systems.

### Directory Structure
```
/                          # Root directory
├── bin/                   # Essential user binaries
├── boot/                  # Boot loader files
├── dev/                   # Device files
├── etc/                   # System configuration
├── home/                  # User home directories
├── lib/                   # Essential shared libraries
├── media/                 # Removable media mount
├── mnt/                   # Temporary mount point
├── opt/                   # Optional software
├── proc/                  # Process information (virtual)
├── root/                  # Root user's home
├── run/                   # Runtime data
├── sbin/                  # System binaries
├── srv/                   # Service data
├── sys/                   # Kernel/hardware info (virtual)
├── tmp/                   # Temporary files
├── usr/                   # User programs
│   ├── bin/               # User binaries
│   ├── lib/               # Libraries
│   ├── local/             # Locally installed
│   └── share/             # Shared data
└── var/                   # Variable data
    ├── log/               # Log files
    ├── cache/             # Application cache
    ├── spool/             # Print/mail queues
    └── tmp/               # Preserved temp files
```

### Important Directories Explained
| Directory | Purpose | Examples |
|-----------|---------|----------|
| /etc | Configuration files | /etc/passwd, /etc/hosts |
| /var/log | Log files | syslog, auth.log |
| /home | User data | /home/john |
| /tmp | Temporary files | Cleared on reboot |
| /proc | Process info | /proc/cpuinfo |
| /dev | Device files | /dev/sda, /dev/null |
| /opt | Optional software | /opt/google/chrome |

### File Types in Linux
```bash
# Identify file type
ls -l
file filename

File Type Indicators (first character in ls -l):
-  Regular file
d  Directory
l  Symbolic link
c  Character device
b  Block device
s  Socket
p  Named pipe (FIFO)

Examples:
-rw-r--r--  1 user group  1234 Jan 1 10:00 file.txt
drwxr-xr-x  2 user group  4096 Jan 1 10:00 directory
lrwxrwxrwx  1 user group     8 Jan 1 10:00 link -> target
```

### Inodes
```bash
# Every file has an inode containing:
- File type and permissions
- Owner and group
- File size
- Timestamps (atime, mtime, ctime)
- Number of hard links
- Pointers to data blocks

# View inode number
ls -i filename
stat filename

# Check inode usage
df -i

# Find file by inode
find / -inum 12345
```

### Hard Links vs Soft Links
```bash
# Hard Link:
- Points to same inode
- Same file, different name
- Only within same filesystem
- Original deleted? Link still works

ln original.txt hardlink.txt

# Soft Link (Symbolic):
- Points to path/name
- Can cross filesystems
- Can link to directories
- Original deleted? Link breaks

ln -s original.txt softlink.txt

# Comparison
ls -li original.txt hardlink.txt softlink.txt
```

### Mount and Unmount
```bash
# View mounted filesystems
mount
df -h
lsblk

# Mount filesystem
sudo mount /dev/sdb1 /mnt/data
sudo mount -t ext4 /dev/sdb1 /mnt/data
sudo mount -o ro /dev/sdb1 /mnt/data    # Read-only

# Unmount
sudo umount /mnt/data
sudo umount -l /mnt/data    # Lazy unmount (if busy)

# Mount ISO
sudo mount -o loop image.iso /mnt/iso

# Remount (change options)
sudo mount -o remount,rw /mnt/data
```

### /etc/fstab (Persistent Mounts)
```bash
# Format:
# <device>  <mount>  <type>  <options>  <dump>  <pass>

# Examples:
/dev/sda1    /           ext4   defaults        0  1
/dev/sda2    /home       ext4   defaults        0  2
/dev/sdb1    /data       xfs    defaults        0  2
UUID=abc123  /backup     ext4   defaults,noatime 0 2
//server/share /mnt/smb  cifs   credentials=/etc/creds 0 0

# Get UUID
blkid /dev/sda1
lsblk -f

# Apply fstab changes
sudo mount -a
```

### Special Filesystems
```bash
# /proc - Process information (virtual)
cat /proc/cpuinfo
cat /proc/meminfo
cat /proc/version
cat /proc/<PID>/status

# /sys - Kernel/hardware info (virtual)
ls /sys/class/net/
cat /sys/block/sda/size

# /dev - Device files
/dev/sda      # First SATA disk
/dev/sda1     # First partition
/dev/null     # Discard output
/dev/zero     # Source of zeros
/dev/random   # Random data
/dev/tty      # Terminal
```

**💡 Real-World Tip:** Always use UUIDs in /etc/fstab instead of device names (/dev/sda1) as device names can change.""",

    "linux_permissions": """## 🔐 Linux File Permissions

**Definition:** File permissions control who can read, write, or execute files and directories in Linux.

### Permission Basics
```bash
ls -l file.txt
-rw-r--r-- 1 owner group 1234 Jan 1 10:00 file.txt
│├─┤├─┤├─┤
│ │  │  └── Others permissions
│ │  └───── Group permissions
│ └──────── Owner permissions
└────────── File type

r = Read    (4)  - View contents / List directory
w = Write   (2)  - Modify / Create files in directory
x = Execute (1)  - Run / Enter directory
```

### Permission Representation
| Symbolic | Numeric | Meaning |
|----------|---------|---------|
| rwx | 7 | Read, write, execute |
| rw- | 6 | Read, write |
| r-x | 5 | Read, execute |
| r-- | 4 | Read only |
| -wx | 3 | Write, execute |
| -w- | 2 | Write only |
| --x | 1 | Execute only |
| --- | 0 | No permissions |

### chmod (Change Mode)
```bash
# Numeric mode
chmod 755 file.txt    # rwxr-xr-x
chmod 644 file.txt    # rw-r--r--
chmod 600 file.txt    # rw-------
chmod 777 file.txt    # rwxrwxrwx (AVOID!)

# Symbolic mode
chmod u+x file.txt    # Add execute for user
chmod g-w file.txt    # Remove write for group
chmod o=r file.txt    # Set others to read only
chmod a+x file.txt    # Add execute for all
chmod u=rwx,g=rx,o=r file.txt

# Recursive
chmod -R 755 /var/www/

# Reference another file
chmod --reference=file1.txt file2.txt
```

### chown (Change Owner)
```bash
# Change owner
sudo chown user file.txt

# Change owner and group
sudo chown user:group file.txt

# Change group only
sudo chown :group file.txt
sudo chgrp group file.txt

# Recursive
sudo chown -R www-data:www-data /var/www/
```

### Common Permission Patterns
```bash
# Secure private files
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 700 ~/.ssh

# Web server files
chmod 644 /var/www/html/*.html    # Files
chmod 755 /var/www/html           # Directories

# Scripts
chmod 755 script.sh               # Executable
chmod +x script.sh                # Add execute

# Configuration files
chmod 640 /etc/shadow             # Sensitive
chmod 644 /etc/passwd             # Readable
```

### umask (Default Permissions)
```bash
# umask defines default permission REMOVAL
# Default file: 666 - umask = actual
# Default dir:  777 - umask = actual

# View umask
umask           # Shows as number
umask -S        # Shows symbolically

# Common umasks:
umask 022  → Files: 644, Dirs: 755 (default)
umask 027  → Files: 640, Dirs: 750 (secure)
umask 077  → Files: 600, Dirs: 700 (private)

# Set temporarily
umask 027

# Set permanently (~/.bashrc or /etc/profile)
umask 027
```

### Special Permissions
```bash
# SUID (Set User ID) - 4
# File runs as owner, not executor
chmod u+s file
chmod 4755 file
-rwsr-xr-x  ← 's' instead of 'x'

Example: /usr/bin/passwd runs as root

# SGID (Set Group ID) - 2
# File: runs as group
# Directory: new files inherit group
chmod g+s dir
chmod 2755 dir
drwxr-sr-x  ← 's' in group position

# Sticky Bit - 1
# Only owner can delete files in directory
chmod +t /tmp
chmod 1777 /tmp
drwxrwxrwt  ← 't' in others position

Example: /tmp - anyone can create, only owner deletes
```

### ACLs (Access Control Lists)
```bash
# ACLs provide fine-grained permissions beyond rwx

# Check if ACLs are supported
mount | grep acl

# View ACLs
getfacl file.txt

# Set ACL for user
setfacl -m u:john:rwx file.txt

# Set ACL for group
setfacl -m g:developers:rx file.txt

# Set default ACL for directory
setfacl -d -m u:john:rwx /shared

# Remove ACL
setfacl -x u:john file.txt

# Remove all ACLs
setfacl -b file.txt
```

**💡 Security Tip:** Never use 777 permissions. Use specific permissions based on actual requirements.""",

    "linux_commands": """## 💻 Essential Linux Commands

**Definition:** Core command-line utilities for file management, text processing, system information, and administration.

### File and Directory Operations
```bash
# Navigation
pwd                     # Print working directory
cd /path/to/dir         # Change directory
cd ~                    # Go to home
cd -                    # Go to previous directory
cd ..                   # Go up one level

# Listing
ls                      # List files
ls -l                   # Long format
ls -la                  # Include hidden files
ls -lh                  # Human-readable sizes
ls -ltr                 # Sort by time, reverse

# File Operations
cp source dest          # Copy file
cp -r source/ dest/     # Copy directory
mv source dest          # Move/rename
rm file                 # Remove file
rm -r directory/        # Remove directory
rm -rf directory/       # Force remove (CAREFUL!)

# Create
touch file.txt          # Create empty file
mkdir directory         # Create directory
mkdir -p a/b/c          # Create nested directories

# View Files
cat file.txt            # Display entire file
less file.txt           # Page through file
head -n 20 file.txt     # First 20 lines
tail -n 20 file.txt     # Last 20 lines
tail -f log.txt         # Follow file (live updates)
```

### Text Processing
```bash
# grep - Search text
grep "pattern" file.txt
grep -i "pattern" file     # Case insensitive
grep -r "pattern" /dir     # Recursive
grep -v "pattern" file     # Invert match
grep -n "pattern" file     # Show line numbers
grep -c "pattern" file     # Count matches
grep -E "regex" file       # Extended regex

# sed - Stream editor
sed 's/old/new/' file      # Replace first occurrence
sed 's/old/new/g' file     # Replace all
sed -i 's/old/new/g' file  # Edit in place
sed -n '5,10p' file        # Print lines 5-10
sed '/pattern/d' file      # Delete matching lines

# awk - Text processing
awk '{print $1}' file      # Print first column
awk -F: '{print $1}' file  # Custom delimiter
awk '{sum+=$1} END {print sum}' file  # Sum column
awk 'NR==5' file           # Print line 5
awk 'length > 80' file     # Lines longer than 80

# cut - Extract columns
cut -d: -f1 /etc/passwd    # First field
cut -c1-10 file            # First 10 characters

# sort and uniq
sort file.txt              # Sort alphabetically
sort -n file.txt           # Sort numerically
sort -r file.txt           # Reverse sort
sort -u file.txt           # Unique only
uniq file.txt              # Remove adjacent duplicates
sort file | uniq -c        # Count occurrences

# wc - Word count
wc file.txt                # Lines, words, characters
wc -l file.txt             # Lines only
wc -w file.txt             # Words only
```

### File Search
```bash
# find - Search files
find /path -name "*.txt"           # By name
find /path -type f                 # Files only
find /path -type d                 # Directories only
find /path -size +100M             # Larger than 100MB
find /path -mtime -7               # Modified last 7 days
find /path -user john              # Owned by john
find /path -perm 755               # By permissions
find /path -name "*.log" -delete   # Find and delete
find /path -exec cmd {} \\;        # Execute command

# locate - Fast search (uses database)
sudo updatedb                      # Update database
locate filename
locate -i filename                 # Case insensitive

# which/whereis/type
which python                       # Command location
whereis python                     # Binary, source, manual
type ls                            # Command type
```

### Compression and Archives
```bash
# tar - Archive
tar -cvf archive.tar files/        # Create archive
tar -xvf archive.tar               # Extract archive
tar -tvf archive.tar               # List contents
tar -czvf archive.tar.gz files/    # Create gzipped
tar -xzvf archive.tar.gz           # Extract gzipped
tar -cjvf archive.tar.bz2 files/   # Create bzip2
tar -xjvf archive.tar.bz2          # Extract bzip2

# gzip/gunzip
gzip file                          # Compress
gunzip file.gz                     # Decompress
gzip -k file                       # Keep original

# zip/unzip
zip archive.zip file1 file2        # Create zip
zip -r archive.zip directory/      # Recursive
unzip archive.zip                  # Extract
unzip -l archive.zip               # List contents
```

### Pipes and Redirection
```bash
# Redirection
command > file          # Output to file (overwrite)
command >> file         # Output to file (append)
command < file          # Input from file
command 2> file         # Stderr to file
command &> file         # Both stdout and stderr
command 2>&1            # Stderr to stdout

# Pipes
command1 | command2     # Pipe output
ls -la | grep ".txt"    # Example
cat log | sort | uniq   # Chain commands

# tee - Output to file AND screen
command | tee file.txt
command | tee -a file.txt  # Append
```

### System Information
```bash
# System
uname -a                # System info
hostname                # Hostname
uptime                  # Uptime and load
date                    # Current date/time

# Hardware
lscpu                   # CPU info
free -h                 # Memory
df -h                   # Disk space
lsblk                   # Block devices
lspci                   # PCI devices
lsusb                   # USB devices

# Process
ps aux                  # All processes
top                     # Interactive process view
htop                    # Better process view
```

**💡 Power Tip:** Combine commands with pipes. Example: `ps aux | grep nginx | awk '{print $2}' | xargs kill`""",


    # =========================================================================
    # USER AND GROUP MANAGEMENT
    # =========================================================================

    "linux_users": """## 👥 Linux User and Group Management

**Definition:** Linux is a multi-user system where users and groups control access to resources.

### User Information Files
```bash
# /etc/passwd - User accounts
username:x:UID:GID:comment:home:shell
john:x:1001:1001:John Doe:/home/john:/bin/bash

# /etc/shadow - Encrypted passwords (root only)
username:password:lastchange:min:max:warn:inactive:expire
john:$6$hash...:19000:0:99999:7:::

# /etc/group - Group information
groupname:x:GID:members
developers:x:1002:john,jane

# View user info
id username
id            # Current user
groups username
getent passwd username
```

### User Management Commands
```bash
# Add user
sudo useradd username
sudo useradd -m username                    # Create home
sudo useradd -m -s /bin/bash username       # With shell
sudo useradd -m -G sudo,docker username     # With groups
sudo useradd -m -u 1500 username            # Specific UID

# Modify user
sudo usermod -aG docker username            # Add to group
sudo usermod -s /bin/zsh username           # Change shell
sudo usermod -l newname oldname             # Rename
sudo usermod -L username                    # Lock account
sudo usermod -U username                    # Unlock account

# Delete user
sudo userdel username
sudo userdel -r username                    # Remove home too

# Set password
sudo passwd username
passwd                                      # Own password
sudo passwd -l username                     # Lock
sudo passwd -u username                     # Unlock
sudo passwd -e username                     # Expire (force change)

# Alternative: adduser (interactive)
sudo adduser username
```

### Group Management
```bash
# Add group
sudo groupadd developers
sudo groupadd -g 2000 developers   # Specific GID

# Modify group
sudo groupmod -n newname oldname   # Rename

# Delete group
sudo groupdel groupname

# Add user to group
sudo usermod -aG groupname username
sudo gpasswd -a username groupname

# Remove user from group
sudo gpasswd -d username groupname

# List group members
getent group groupname
```

### su and sudo
```bash
# su - Switch User
su username           # Switch to user
su - username         # Switch with environment
su -                  # Switch to root
su -c "command"       # Run single command

# sudo - Execute as another user
sudo command                    # Run as root
sudo -u username command        # Run as user
sudo -i                         # Root shell
sudo -s                         # Shell with current env
sudo !!                         # Repeat last command as root
sudo -l                         # List allowed commands
```

### sudoers Configuration
```bash
# Edit sudoers (ALWAYS use visudo)
sudo visudo

# Syntax: who where=(as_who) what
# user  host=(runas) commands

# Examples:
john    ALL=(ALL) ALL                      # Full sudo access
john    ALL=(ALL) NOPASSWD: ALL            # No password
john    ALL=(root) /usr/bin/apt            # Specific command
%developers ALL=(ALL) /usr/bin/docker      # Group access

# /etc/sudoers.d/ - Drop-in files
sudo visudo -f /etc/sudoers.d/john
```

### Password Policies
```bash
# /etc/login.defs - Default policies
PASS_MAX_DAYS   90
PASS_MIN_DAYS   7
PASS_WARN_AGE   14

# Change aging for existing user
sudo chage -l username          # View settings
sudo chage -M 90 username       # Max days
sudo chage -m 7 username        # Min days
sudo chage -W 14 username       # Warning days
sudo chage -E 2024-12-31 username  # Expiry date
```

### PAM (Pluggable Authentication Modules)
```bash
# PAM configuration
/etc/pam.d/                     # PAM config files
/etc/pam.d/common-auth          # Authentication
/etc/pam.d/common-password      # Password rules
/etc/pam.d/sshd                 # SSH authentication

# PAM module types:
auth      - Authentication
account   - Account verification
password  - Password changing
session   - Session setup/teardown

# Example: Enforce password complexity
# /etc/pam.d/common-password
password requisite pam_pwquality.so retry=3 minlen=12
```

**💡 Security Best Practice:** Use `sudo` instead of logging in as root. Configure sudo with least privilege.""",

    "linux_processes": """## ⚙️ Linux Process Management

**Definition:** A process is a running instance of a program. Linux provides tools to view, control, and manage processes.

### Process Concepts
```
Process has:
- PID (Process ID) - Unique identifier
- PPID (Parent PID) - Parent process
- UID - User who owns it
- State - Running, Sleeping, Stopped, Zombie
- Priority/Nice value
- Memory/CPU usage

Process States:
R - Running/Runnable
S - Interruptible Sleep
D - Uninterruptible Sleep (I/O)
Z - Zombie (terminated, not reaped)
T - Stopped
```

### Viewing Processes
```bash
# ps - Process status
ps                      # Current terminal processes
ps aux                  # All processes (BSD style)
ps -ef                  # All processes (POSIX style)
ps -u username          # User's processes
ps -p PID               # Specific process
ps --forest             # Tree view
ps aux --sort=-%mem     # Sort by memory
ps aux --sort=-%cpu     # Sort by CPU

# ps aux output columns:
USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND

# top - Real-time process view
top
top -u username         # User's processes only
# Inside top:
# k - Kill process
# r - Renice
# M - Sort by memory
# P - Sort by CPU
# q - Quit

# htop - Better interactive viewer
htop                    # Install: apt install htop

# pstree - Process tree
pstree
pstree -p               # Show PIDs
pstree username         # User's processes
```

### Process Control
```bash
# Start process in background
command &

# List jobs
jobs
jobs -l                 # With PIDs

# Foreground/Background
fg                      # Bring to foreground
fg %1                   # Job number 1
bg                      # Send to background
bg %1

# Suspend process
Ctrl+Z                  # Suspend foreground process

# nohup - Ignore hangup
nohup command &
nohup command > output.log 2>&1 &
```

### Signals
```bash
# Common signals
Signal   Number  Description
SIGHUP   1       Hangup (reload config)
SIGINT   2       Interrupt (Ctrl+C)
SIGQUIT  3       Quit (core dump)
SIGKILL  9       Kill (cannot be caught)
SIGTERM  15      Terminate (graceful)
SIGSTOP  19      Stop (cannot be caught)
SIGCONT  18      Continue stopped process

# Send signals
kill PID                # Default: SIGTERM
kill -9 PID             # SIGKILL (force)
kill -15 PID            # SIGTERM
kill -HUP PID           # SIGHUP (reload)
kill -STOP PID          # Pause
kill -CONT PID          # Resume

# Kill by name
killall nginx           # Kill all nginx
killall -9 nginx        # Force kill all
pkill nginx             # Pattern match
pkill -u username       # Kill user's processes
```

### Process Priority (Nice)
```bash
# Nice values: -20 (highest) to 19 (lowest)
# Default: 0
# Only root can set negative values

# Start with nice value
nice -n 10 command      # Lower priority
nice -n -5 command      # Higher priority (root)

# Change running process
renice 10 -p PID        # Set nice to 10
renice -5 -p PID        # Higher priority (root)
renice 15 -u username   # All user's processes

# View nice value
ps -l
top                     # NI column
```

### Process Information
```bash
# /proc filesystem
ls /proc/PID/
cat /proc/PID/status    # Process status
cat /proc/PID/cmdline   # Command line
cat /proc/PID/environ   # Environment
cat /proc/PID/fd        # File descriptors
cat /proc/PID/maps      # Memory maps

# lsof - List open files
lsof                    # All open files
lsof -u username        # User's open files
lsof -p PID             # Process's open files
lsof -i :80             # What's using port 80
lsof +D /path           # Files in directory

# fuser - Find process using file
fuser /path/file
fuser -m /mnt           # Processes using mount
fuser -k /path/file     # Kill process using file
```

### System Resource Limits
```bash
# View limits
ulimit -a

# Set limits (session)
ulimit -n 65535         # Open files
ulimit -u 10000         # Max processes

# Permanent limits (/etc/security/limits.conf)
username soft nofile 65535
username hard nofile 65535
username soft nproc 10000
username hard nproc 10000
```

**💡 Troubleshooting Tip:** High load? Use `top` sorted by CPU/memory. Too many processes? Check for fork bombs or runaway scripts.""",

    "linux_packages": """## 📦 Linux Package Management

**Definition:** Package managers automate installing, updating, configuring, and removing software packages.

### Package Manager Comparison
| Distribution | Package Manager | Package Format |
|--------------|-----------------|----------------|
| Debian/Ubuntu | apt (dpkg) | .deb |
| RHEL/CentOS/Fedora | dnf/yum (rpm) | .rpm |
| Arch Linux | pacman | .pkg.tar.zst |
| Alpine | apk | .apk |
| openSUSE | zypper | .rpm |

### APT (Debian/Ubuntu)
```bash
# Update package list
sudo apt update

# Upgrade packages
sudo apt upgrade                # Upgrade installed
sudo apt full-upgrade           # Upgrade with dependencies
sudo apt dist-upgrade           # Distribution upgrade

# Install/Remove
sudo apt install nginx
sudo apt install nginx=1.18.0-1  # Specific version
sudo apt remove nginx            # Remove (keep config)
sudo apt purge nginx             # Remove with config
sudo apt autoremove              # Remove unused dependencies

# Search/Info
apt search nginx
apt show nginx
apt list --installed
apt list --upgradable

# Download without install
apt download nginx

# Clean cache
sudo apt clean
sudo apt autoclean
```

### DNF/YUM (RHEL/CentOS/Fedora)
```bash
# Update
sudo dnf check-update           # Check for updates
sudo dnf update                 # Update all
sudo dnf update nginx           # Update specific

# Install/Remove
sudo dnf install nginx
sudo dnf install nginx-1.18.0   # Specific version
sudo dnf remove nginx
sudo dnf autoremove             # Remove unused

# Search/Info
dnf search nginx
dnf info nginx
dnf list installed
dnf list available
dnf provides /usr/bin/nginx     # Find package for file

# Groups
dnf group list
dnf group install "Development Tools"

# History
dnf history
dnf history info 5
dnf history undo 5

# Clean cache
sudo dnf clean all
```

### Pacman (Arch Linux)
```bash
# Sync database and update
sudo pacman -Sy                 # Sync database
sudo pacman -Syu                # Sync and update all
sudo pacman -Syyu               # Force sync and update

# Install/Remove
sudo pacman -S nginx            # Install
sudo pacman -R nginx            # Remove
sudo pacman -Rs nginx           # Remove with dependencies
sudo pacman -Rns nginx          # Remove with deps and config

# Search/Info
pacman -Ss nginx                # Search
pacman -Qi nginx                # Info (installed)
pacman -Si nginx                # Info (repo)
pacman -Ql nginx                # List files

# Clean cache
sudo pacman -Sc                 # Clean old packages
sudo pacman -Scc                # Clean all cache
```

### RPM and DPKG (Low-level)
```bash
# RPM (RHEL family)
rpm -ivh package.rpm            # Install
rpm -Uvh package.rpm            # Upgrade
rpm -e package                  # Remove
rpm -qa                         # List installed
rpm -qi package                 # Info
rpm -ql package                 # List files
rpm -qf /path/file              # Find package owning file

# DPKG (Debian family)
sudo dpkg -i package.deb        # Install
sudo dpkg -r package            # Remove
sudo dpkg -P package            # Purge
dpkg -l                         # List installed
dpkg -L package                 # List files
dpkg -S /path/file              # Find package owning file
```

### Repositories
```bash
# APT repositories (/etc/apt/sources.list)
deb http://archive.ubuntu.com/ubuntu focal main restricted
deb-src http://archive.ubuntu.com/ubuntu focal main restricted

# Add PPA (Ubuntu)
sudo add-apt-repository ppa:user/repo
sudo apt update

# DNF repositories (/etc/yum.repos.d/)
[epel]
name=EPEL Repository
baseurl=https://download.fedoraproject.org/pub/epel/$releasever/
enabled=1
gpgcheck=1

# Add EPEL
sudo dnf install epel-release
```

### Build from Source
```bash
# General process
wget https://example.com/software.tar.gz
tar xzf software.tar.gz
cd software
./configure --prefix=/usr/local
make
sudo make install

# Common dependencies
sudo apt install build-essential    # Debian
sudo dnf groupinstall "Development Tools"  # RHEL
```

**💡 Production Tip:** Always use official repositories. Pin versions for critical packages. Test updates in staging first.""",


    # =========================================================================
    # LINUX NETWORKING
    # =========================================================================

    "linux_networking": """## 🌐 Linux Networking

**Definition:** Linux provides powerful networking capabilities for configuration, routing, firewalling, and troubleshooting.

### Network Configuration Commands
```bash
# ip command (modern, preferred)
ip addr show                    # Show IP addresses
ip addr add 192.168.1.100/24 dev eth0   # Add IP
ip addr del 192.168.1.100/24 dev eth0   # Remove IP
ip link show                    # Show interfaces
ip link set eth0 up             # Enable interface
ip link set eth0 down           # Disable interface
ip route show                   # Show routes
ip route add default via 192.168.1.1    # Add default route
ip route add 10.0.0.0/8 via 192.168.1.1 dev eth0
ip neigh show                   # ARP table

# Legacy commands (still work)
ifconfig                        # Show interfaces
ifconfig eth0 192.168.1.100     # Set IP
ifconfig eth0 up/down           # Enable/disable
route -n                        # Show routes
route add default gw 192.168.1.1
arp -a                          # ARP table
```

### Network Configuration Files
```bash
# Debian/Ubuntu (netplan)
# /etc/netplan/01-config.yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: no
      addresses: [192.168.1.100/24]
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]

# Apply netplan
sudo netplan apply

# RHEL/CentOS
# /etc/sysconfig/network-scripts/ifcfg-eth0
DEVICE=eth0
BOOTPROTO=static
IPADDR=192.168.1.100
NETMASK=255.255.255.0
GATEWAY=192.168.1.1
DNS1=8.8.8.8
ONBOOT=yes

# Restart network
sudo systemctl restart NetworkManager
sudo nmcli connection reload
```

### NetworkManager (nmcli)
```bash
# Show connections
nmcli connection show
nmcli device status

# Create connection
nmcli connection add type ethernet con-name "eth0" ifname eth0

# Modify connection
nmcli connection modify eth0 ipv4.addresses 192.168.1.100/24
nmcli connection modify eth0 ipv4.gateway 192.168.1.1
nmcli connection modify eth0 ipv4.dns "8.8.8.8 8.8.4.4"
nmcli connection modify eth0 ipv4.method manual

# Activate/Deactivate
nmcli connection up eth0
nmcli connection down eth0

# WiFi
nmcli device wifi list
nmcli device wifi connect "SSID" password "password"
```

### DNS Configuration
```bash
# /etc/resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
search example.com

# systemd-resolved
systemctl status systemd-resolved
resolvectl status
resolvectl dns eth0 8.8.8.8

# /etc/hosts (local resolution)
127.0.0.1   localhost
192.168.1.10   server.local server
```

### Socket Statistics (ss)
```bash
# ss (modern replacement for netstat)
ss -tuln                        # TCP/UDP listening
ss -tulnp                       # With process
ss -t state established         # Established TCP
ss -s                           # Summary statistics

# Filter by port
ss -tuln sport = :22
ss -tuln dport = :80

# netstat (legacy)
netstat -tuln                   # Listening ports
netstat -an                     # All connections
netstat -rn                     # Routing table
```

### Network Troubleshooting
```bash
# Connectivity
ping host                       # Basic connectivity
ping -c 5 host                  # 5 packets
ping -i 0.2 host                # Fast ping

# Route tracing
traceroute host                 # UDP traceroute
traceroute -T host              # TCP traceroute
mtr host                        # Continuous traceroute

# DNS testing
nslookup domain
dig domain
dig @8.8.8.8 domain
dig domain MX
host domain

# Port testing
nc -zv host port                # Test port
nc -l 8080                      # Listen on port
telnet host port                # Test connection

# Traffic capture
sudo tcpdump -i eth0
sudo tcpdump -i eth0 port 80
sudo tcpdump -i eth0 -w capture.pcap
```

### IP Forwarding and NAT
```bash
# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward
# Permanent
echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
sysctl -p

# NAT with iptables
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

**💡 Troubleshooting Order:** ping gateway → ping external IP (8.8.8.8) → ping domain → check DNS → check routes.""",

    "linux_firewall": """## 🔥 Linux Firewall (iptables, firewalld, nftables)

**Definition:** Linux firewalls filter network traffic based on rules to protect systems from unauthorized access.

### Firewall Options
| Tool | Distributions | Interface |
|------|---------------|-----------|
| iptables | All (legacy) | Command-line |
| firewalld | RHEL/CentOS/Fedora | Zones/services |
| ufw | Ubuntu | Simplified iptables |
| nftables | Modern (replaces iptables) | Command-line |

### iptables
```bash
# Chains: INPUT (incoming), OUTPUT (outgoing), FORWARD (routing)
# Targets: ACCEPT, DROP, REJECT, LOG

# View rules
sudo iptables -L -n -v
sudo iptables -L INPUT -n -v

# Default policies
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT

# Allow established connections
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow loopback
sudo iptables -A INPUT -i lo -j ACCEPT

# Allow specific ports
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT    # SSH
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT    # HTTP
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT   # HTTPS

# Allow from specific IP
sudo iptables -A INPUT -s 192.168.1.100 -j ACCEPT

# Block IP
sudo iptables -A INPUT -s 10.0.0.50 -j DROP

# Delete rule
sudo iptables -D INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -D INPUT 3                # By line number

# Save/Restore
sudo iptables-save > /etc/iptables/rules.v4
sudo iptables-restore < /etc/iptables/rules.v4

# Flush all rules
sudo iptables -F
```

### firewalld (RHEL/CentOS/Fedora)
```bash
# Status
sudo firewall-cmd --state
sudo firewall-cmd --list-all

# Zones
sudo firewall-cmd --get-default-zone
sudo firewall-cmd --get-active-zones
sudo firewall-cmd --set-default-zone=public
sudo firewall-cmd --zone=public --list-all

# Services
sudo firewall-cmd --get-services
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --add-service=https --permanent
sudo firewall-cmd --remove-service=http --permanent

# Ports
sudo firewall-cmd --add-port=8080/tcp --permanent
sudo firewall-cmd --remove-port=8080/tcp --permanent

# Rich rules
sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port port="22" protocol="tcp" accept' --permanent

# Reload
sudo firewall-cmd --reload
```

### ufw (Ubuntu)
```bash
# Enable/Disable
sudo ufw enable
sudo ufw disable
sudo ufw status verbose

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow services/ports
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw allow 8080/tcp

# Allow from IP
sudo ufw allow from 192.168.1.100
sudo ufw allow from 192.168.1.0/24 to any port 22

# Deny
sudo ufw deny from 10.0.0.50
sudo ufw deny 3306/tcp

# Delete rules
sudo ufw delete allow 8080/tcp
sudo ufw status numbered
sudo ufw delete 3
```

### nftables (Modern)
```bash
# List rules
sudo nft list ruleset

# Create table and chain
sudo nft add table inet filter
sudo nft add chain inet filter input { type filter hook input priority 0 \\; policy drop \\; }

# Add rules
sudo nft add rule inet filter input tcp dport 22 accept
sudo nft add rule inet filter input tcp dport {80, 443} accept

# Save rules
sudo nft list ruleset > /etc/nftables.conf

# Load rules
sudo nft -f /etc/nftables.conf
```

### Common Firewall Rules
```bash
# Basic secure server:
1. Default deny incoming
2. Allow established/related
3. Allow loopback
4. Allow SSH (restrict to IP if possible)
5. Allow needed services (HTTP, HTTPS)
6. Log dropped packets (optional)
```

**💡 Security Tip:** Always test firewall rules before applying in production. Have console access as backup.""",

    "selinux": """## 🛡️ SELinux (Security-Enhanced Linux)

**Definition:** SELinux is a mandatory access control (MAC) system that provides an additional layer of security beyond standard Linux permissions.

### SELinux Concepts
```
DAC (Discretionary Access Control):
- Traditional rwx permissions
- Owner controls access

MAC (Mandatory Access Control):
- System-wide security policy
- Even root is restricted
- SELinux implements MAC
```

### SELinux Modes
```bash
# Modes:
Enforcing  - Policies enforced, violations denied and logged
Permissive - Policies not enforced, violations logged only
Disabled   - SELinux completely off

# Check mode
getenforce
sestatus

# Set mode (temporary)
sudo setenforce 0           # Permissive
sudo setenforce 1           # Enforcing

# Set mode (permanent) - /etc/selinux/config
SELINUX=enforcing
# Reboot required for disabled<->enabled
```

### SELinux Labels (Contexts)
```bash
# Every file, process, port has a context:
user:role:type:level

# View file context
ls -Z /var/www/html/
# -rw-r--r--. root root unconfined_u:object_r:httpd_sys_content_t:s0 index.html

# View process context
ps auxZ | grep httpd
# system_u:system_r:httpd_t:s0 ... /usr/sbin/httpd

# View port context
semanage port -l | grep http
```

### Common SELinux Commands
```bash
# Change file context
sudo chcon -t httpd_sys_content_t /var/www/html/file.html

# Restore default context
sudo restorecon -v /var/www/html/file.html
sudo restorecon -Rv /var/www/html/       # Recursive

# View audit log
sudo ausearch -m avc -ts recent
sudo cat /var/log/audit/audit.log | grep denied

# Generate policy module from denials
sudo audit2allow -a
sudo audit2allow -a -M mypolicy
sudo semodule -i mypolicy.pp
```

### SELinux Booleans
```bash
# Booleans are on/off switches for policies

# List booleans
getsebool -a
getsebool -a | grep httpd

# Set boolean (temporary)
sudo setsebool httpd_can_network_connect on

# Set boolean (permanent)
sudo setsebool -P httpd_can_network_connect on

# Common booleans:
httpd_can_network_connect      # Allow web server outbound
httpd_enable_homedirs          # Allow user home pages
ftpd_full_access               # FTP unrestricted access
```

### SELinux Troubleshooting
```bash
# Install troubleshooting tools
sudo yum install setroubleshoot-server

# Analyze audit log
sudo sealert -a /var/log/audit/audit.log

# Real-time monitoring
sudo tail -f /var/log/audit/audit.log | grep denied

# Common issues and fixes:
# Wrong context on web files:
sudo restorecon -Rv /var/www/html/

# Web server can't connect to network:
sudo setsebool -P httpd_can_network_connect on

# Non-standard port:
sudo semanage port -a -t http_port_t -p tcp 8080
```

### SELinux Port Labels
```bash
# List port labels
sudo semanage port -l

# Add port label
sudo semanage port -a -t http_port_t -p tcp 8080

# Delete port label
sudo semanage port -d -t http_port_t -p tcp 8080

# Common types:
http_port_t       - Web server ports
ssh_port_t        - SSH ports
mysqld_port_t     - MySQL ports
```

**💡 Production Tip:** Never disable SELinux. Use permissive mode to troubleshoot, then create proper policies.""",

    "bash_scripting": """## 📜 Bash Shell Scripting

**Definition:** Bash scripting allows automating tasks by writing sequences of commands in executable files.

### Script Basics
```bash
#!/bin/bash
# Shebang tells system which interpreter to use

# Make script executable
chmod +x script.sh

# Run script
./script.sh
bash script.sh
source script.sh    # Run in current shell
```

### Variables
```bash
# Define variables (no spaces around =)
name="John"
count=10
readonly CONSTANT="value"    # Read-only

# Use variables
echo $name
echo ${name}
echo "Hello, $name"
echo "Hello, ${name}!"

# Command substitution
today=$(date)
files=$(ls -la)

# Environment variables
export MY_VAR="value"
echo $HOME $USER $PATH $PWD
```

### Input and Output
```bash
# Read input
read -p "Enter name: " name
read -s -p "Enter password: " password    # Silent
read -t 5 -p "Quick! " answer             # Timeout

# Output
echo "Hello World"
echo -n "No newline"
echo -e "Tab\\tNewline\\n"
printf "Formatted: %s is %d\\n" "$name" "$age"
```

### Conditionals
```bash
# if-else
if [ "$name" = "John" ]; then
    echo "Hello John"
elif [ "$name" = "Jane" ]; then
    echo "Hello Jane"
else
    echo "Hello stranger"
fi

# Test operators:
# Strings: = != -z (empty) -n (not empty)
# Numbers: -eq -ne -lt -le -gt -ge
# Files: -e (exists) -f (file) -d (dir) -r -w -x

# File tests
if [ -f "$file" ]; then
    echo "File exists"
fi

if [ -d "$dir" ]; then
    echo "Directory exists"
fi

# Compound conditions
if [ "$a" -gt 0 ] && [ "$a" -lt 100 ]; then
    echo "Between 0 and 100"
fi

if [[ "$name" =~ ^J ]]; then
    echo "Name starts with J"
fi
```

### Loops
```bash
# For loop
for i in 1 2 3 4 5; do
    echo "Number: $i"
done

for file in *.txt; do
    echo "Processing $file"
done

for i in {1..10}; do
    echo $i
done

for ((i=0; i<10; i++)); do
    echo $i
done

# While loop
count=0
while [ $count -lt 5 ]; do
    echo $count
    ((count++))
done

# Until loop
until [ $count -eq 0 ]; do
    echo $count
    ((count--))
done

# Loop control
break       # Exit loop
continue    # Skip to next iteration
```

### Functions
```bash
# Define function
greet() {
    echo "Hello, $1!"
}

# Function with return
add() {
    local result=$(( $1 + $2 ))
    echo $result
}

# Call functions
greet "World"
sum=$(add 5 3)

# Return values
check_file() {
    [ -f "$1" ]
    return $?
}

if check_file "/etc/passwd"; then
    echo "File exists"
fi
```

### Error Handling
```bash
#!/bin/bash
set -e          # Exit on error
set -u          # Error on undefined variable
set -o pipefail # Catch pipe errors
set -x          # Debug mode

# Check exit status
if command; then
    echo "Success"
else
    echo "Failed with exit code: $?"
fi

# Trap errors
trap 'echo "Error on line $LINENO"' ERR
trap 'cleanup' EXIT

# Redirect errors
command 2>/dev/null         # Discard errors
command 2>&1                # Stderr to stdout
command &>/dev/null         # Discard all output
```

### Practical Script Example
```bash
#!/bin/bash
# Backup script with logging and error handling

set -e
BACKUP_DIR="/backup"
LOG_FILE="/var/log/backup.log"
DATE=$(date +%Y%m%d_%H%M%S)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

cleanup() {
    log "Cleaning up temporary files"
    rm -f /tmp/backup_*
}

trap cleanup EXIT

log "Starting backup"

if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
fi

tar -czvf "$BACKUP_DIR/backup_$DATE.tar.gz" /etc /home

if [ $? -eq 0 ]; then
    log "Backup completed: backup_$DATE.tar.gz"
else
    log "Backup failed!"
    exit 1
fi
```

**💡 Best Practice:** Always use `set -e`, test scripts in development, and add proper logging and error handling.""",


    # =========================================================================
    # MONITORING AND PERFORMANCE
    # =========================================================================

    "linux_monitoring": """## 📊 Linux Monitoring and Performance

**Definition:** Monitoring system resources and performance is essential for maintaining healthy Linux systems and troubleshooting issues.

### System Overview Commands
```bash
# Quick health check
uptime                  # Uptime and load average
top                     # Real-time process view
htop                    # Better interactive view
vmstat 1 5              # System statistics every 1s
sar                     # Historical performance

# Load Average interpretation:
# uptime output: load average: 1.00, 0.75, 0.50
# (1 min, 5 min, 15 min)
# Load = number of processes waiting for CPU
# Good: load < number of CPU cores
# Check cores: nproc or lscpu
```

### CPU Monitoring
```bash
# CPU info
lscpu
cat /proc/cpuinfo
nproc                   # Number of CPUs

# CPU usage
top                     # Press 1 to see per-CPU
htop
mpstat 1                # Per-CPU stats
mpstat -P ALL 1         # All CPUs

# Per-process CPU
pidstat 1               # Process CPU usage
ps aux --sort=-%cpu | head  # Top CPU processes
```

### Memory Monitoring
```bash
# Memory usage
free -h                 # Human-readable
free -m                 # In MB
cat /proc/meminfo

# free output:
#        total   used   free  shared  buff/cache  available
# Mem:    16G    4G     2G     500M      10G         11G
# Swap:    2G    0G     2G

# available = free + reclaimable cache
# High buff/cache is normal (Linux uses free RAM for cache)

# Per-process memory
ps aux --sort=-%mem | head
top -o %MEM
smem                    # Detailed memory report
```

### Disk Monitoring
```bash
# Disk space
df -h                   # Filesystem usage
df -i                   # Inode usage
du -sh /path            # Directory size
du -h --max-depth=1 /   # Top-level directories
ncdu /                  # Interactive disk usage

# Disk I/O
iostat                  # I/O statistics
iostat -x 1             # Extended stats
iotop                   # Per-process I/O
dstat                   # Combined stats

# Disk health
smartctl -a /dev/sda    # SMART info
hdparm -tT /dev/sda     # Read speed test
```

### Network Monitoring
```bash
# Network interfaces
ip -s link              # Interface statistics
ifstat                  # Interface throughput
iftop                   # Real-time bandwidth
nethogs                 # Per-process bandwidth
nload                   # Network load graphs

# Connections
ss -s                   # Socket statistics
netstat -s              # Protocol statistics
ss -tuln                # Listening ports
```

### System Activity (SAR)
```bash
# sar - System Activity Reporter
# Data collected by sysstat package

# Install
sudo apt install sysstat
sudo systemctl enable sysstat

# CPU
sar -u 1 5              # CPU usage, 5 samples
sar -u -f /var/log/sa/sa01  # Historical

# Memory
sar -r 1 5              # Memory
sar -S 1 5              # Swap

# Disk
sar -d 1 5              # Disk I/O

# Network
sar -n DEV 1 5          # Network interfaces
sar -n SOCK 1 5         # Socket statistics

# All data
sar -A                  # Everything
```

### Performance Bottleneck Analysis
```bash
# Methodology: USE (Utilization, Saturation, Errors)

# 1. Check load average
uptime

# 2. Identify bottleneck type:
# High CPU: top, mpstat
# High Memory: free, vmstat
# High Disk I/O: iostat, iotop
# High Network: iftop, ss

# 3. Find culprit process
top -c                  # See full commands
ps aux --sort=-%cpu     # CPU hogs
ps aux --sort=-%mem     # Memory hogs

# 4. Investigate further
strace -p PID           # System calls
lsof -p PID             # Open files
```

### Key Metrics Summary
| Resource | Commands | Warning Signs |
|----------|----------|---------------|
| CPU | top, mpstat, sar -u | Load > cores, %wait high |
| Memory | free, vmstat, sar -r | Swap usage, OOM killer |
| Disk | df, iostat, iotop | %util > 80%, await high |
| Network | ss, iftop, sar -n | Dropped packets, saturation |

**💡 Pro Tip:** Set up monitoring tools like Prometheus/Grafana, Nagios, or Zabbix for continuous monitoring and alerting.""",

    "linux_logs": """## 📋 Linux Logs and Troubleshooting

**Definition:** Log files contain system events, errors, and information crucial for troubleshooting and auditing.

### Log Locations
```bash
/var/log/                   # Main log directory
├── syslog                  # General system log (Debian)
├── messages                # General system log (RHEL)
├── auth.log                # Authentication (Debian)
├── secure                  # Authentication (RHEL)
├── kern.log                # Kernel messages
├── dmesg                   # Boot messages
├── boot.log                # Boot process
├── cron                    # Cron job logs
├── maillog                 # Mail server logs
├── httpd/ or apache2/      # Web server logs
├── nginx/                  # Nginx logs
├── mysql/                  # MySQL logs
└── journal/                # systemd journal
```

### Viewing Logs
```bash
# Traditional log files
tail -f /var/log/syslog     # Follow log
tail -n 100 /var/log/syslog # Last 100 lines
less /var/log/syslog        # Page through
grep "error" /var/log/syslog
zcat /var/log/syslog.1.gz   # View compressed

# journalctl (systemd)
journalctl                  # All logs
journalctl -f               # Follow
journalctl -b               # Current boot
journalctl -b -1            # Previous boot
journalctl --since "1 hour ago"
journalctl --since "2024-01-01" --until "2024-01-02"
journalctl -u nginx         # Service logs
journalctl -u nginx -f      # Follow service
journalctl -p err           # Errors only
journalctl -k               # Kernel messages
journalctl --list-boots     # List boots
```

### Kernel Messages
```bash
# dmesg - Kernel ring buffer
dmesg
dmesg | tail -20
dmesg | grep -i error
dmesg -T                    # Human-readable timestamps
dmesg -w                    # Follow
dmesg -l err,warn           # Errors and warnings
```

### Log Priority Levels
```
0 - emerg    (System unusable)
1 - alert    (Immediate action needed)
2 - crit     (Critical conditions)
3 - err      (Error conditions)
4 - warning  (Warning conditions)
5 - notice   (Normal but significant)
6 - info     (Informational)
7 - debug    (Debug messages)
```

### rsyslog Configuration
```bash
# /etc/rsyslog.conf
# Format: facility.priority destination

# Examples:
*.info;mail.none;auth.none  /var/log/messages
auth.*                      /var/log/auth.log
mail.*                      /var/log/maillog
*.emerg                     :omusrmsg:*
local0.*                    /var/log/myapp.log

# Remote logging
*.* @@192.168.1.100:514     # TCP
*.* @192.168.1.100:514      # UDP

# Restart rsyslog
sudo systemctl restart rsyslog
```

### Log Rotation
```bash
# /etc/logrotate.conf
# /etc/logrotate.d/

# Example: /etc/logrotate.d/nginx
/var/log/nginx/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data adm
    sharedscripts
    postrotate
        systemctl reload nginx > /dev/null
    endscript
}

# Test logrotate
logrotate -d /etc/logrotate.conf    # Debug/test
logrotate -f /etc/logrotate.conf    # Force
```

### Troubleshooting Methodology
```bash
# 1. Gather Information
uname -a                    # System info
uptime                      # Uptime and load
dmesg | tail                # Recent kernel messages
journalctl -p err --since "1 hour ago"

# 2. Check Service Status
systemctl status <service>
systemctl --failed          # Failed services
journalctl -u <service> -n 50

# 3. Check Logs
tail -f /var/log/syslog     # System log
tail -f /var/log/<service>  # Service-specific

# 4. Check Resources
top                         # CPU/Memory
df -h                       # Disk space
free -h                     # Memory

# 5. Check Network
ss -tuln                    # Listening ports
ping gateway                # Connectivity
```

### Common Log Searches
```bash
# Find errors
grep -i "error" /var/log/syslog
journalctl -p err

# Authentication failures
grep "Failed password" /var/log/auth.log
journalctl -u sshd | grep "Failed"

# Disk errors
dmesg | grep -i "error\\|fail"
journalctl -k | grep -i "error"

# OOM (Out of Memory)
grep -i "oom" /var/log/syslog
dmesg | grep -i "oom\\|killed process"
```

**💡 Troubleshooting Tip:** Always check logs first. 80% of issues can be identified from log messages.""",

    "docker_linux": """## 🐳 Docker on Linux

**Definition:** Docker is a containerization platform that packages applications with their dependencies into isolated containers.

### Docker Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    Docker Host                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │               Docker Daemon                      │    │
│  │  ┌────────┐  ┌────────┐  ┌────────┐            │    │
│  │  │Container│  │Container│  │Container│          │    │
│  │  │  App 1  │  │  App 2  │  │  App 3  │          │    │
│  │  └────────┘  └────────┘  └────────┘            │    │
│  │         │          │          │                 │    │
│  │         └──────────┴──────────┘                 │    │
│  │                    │                            │    │
│  │              Docker Engine                      │    │
│  └─────────────────────────────────────────────────┘    │
│                       │                                  │
│                 Linux Kernel                             │
│            (namespaces, cgroups)                        │
└─────────────────────────────────────────────────────────┘
```

### Installing Docker
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io
sudo systemctl enable docker
sudo systemctl start docker

# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in

# Verify
docker --version
docker run hello-world
```

### Docker Commands
```bash
# Images
docker images                   # List images
docker pull nginx               # Download image
docker rmi nginx                # Remove image
docker build -t myapp .         # Build image

# Containers
docker ps                       # Running containers
docker ps -a                    # All containers
docker run nginx                # Run container
docker run -d nginx             # Run detached
docker run -d -p 80:80 nginx    # Port mapping
docker run -d --name web nginx  # Named container
docker run -it ubuntu bash      # Interactive

# Container Management
docker start container_name
docker stop container_name
docker restart container_name
docker rm container_name        # Remove (stopped)
docker rm -f container_name     # Force remove
docker kill container_name      # Force stop

# Logs and Exec
docker logs container_name
docker logs -f container_name   # Follow
docker exec -it container_name bash   # Shell access
```

### Dockerfile
```dockerfile
# Dockerfile example
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install packages
RUN apt-get update && apt-get install -y \\
    python3 \\
    python3-pip \\
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

# Expose port
EXPOSE 8000

# Run command
CMD ["python3", "app.py"]
```

### Docker Volumes
```bash
# Types:
# - Bind mounts (host path)
# - Named volumes (Docker-managed)

# Bind mount
docker run -v /host/path:/container/path nginx

# Named volume
docker volume create mydata
docker run -v mydata:/app/data nginx

# Volume commands
docker volume ls
docker volume inspect mydata
docker volume rm mydata
docker volume prune             # Remove unused
```

### Docker Networking
```bash
# Network types:
# - bridge (default, isolated)
# - host (use host network)
# - none (no networking)
# - overlay (swarm multi-host)

# List networks
docker network ls

# Create network
docker network create mynetwork

# Run on network
docker run -d --network mynetwork --name web nginx
docker run -d --network mynetwork --name db mysql

# Containers on same network can communicate by name
# curl http://web from db container works

# Inspect network
docker network inspect mynetwork
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    image: nginx
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html
    depends_on:
      - app

  app:
    build: ./app
    environment:
      - DATABASE_URL=postgres://db:5432/mydb
    depends_on:
      - db

  db:
    image: postgres:14
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

```bash
# Compose commands
docker-compose up               # Start services
docker-compose up -d            # Detached
docker-compose down             # Stop and remove
docker-compose logs -f          # Follow logs
docker-compose ps               # List services
docker-compose exec web bash    # Shell into service
```

### Container Security
```bash
# Run as non-root
USER appuser

# Read-only filesystem
docker run --read-only nginx

# Limit resources
docker run --memory=512m --cpus=1 nginx

# Drop capabilities
docker run --cap-drop=ALL nginx

# Security scanning
docker scan myimage
```

**💡 Production Tip:** Use specific image tags (nginx:1.21), not latest. Use multi-stage builds to reduce image size.""",

    "cron": """## ⏰ Cron and Scheduled Tasks

**Definition:** Cron is the time-based job scheduler in Linux for running commands or scripts at specified intervals.

### Cron Syntax
```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, Sun=0)
│ │ │ │ │
* * * * * command
```

### Cron Examples
```bash
# Every minute
* * * * * /script.sh

# Every 5 minutes
*/5 * * * * /script.sh

# Every hour at minute 0
0 * * * * /script.sh

# Every day at 2:30 AM
30 2 * * * /script.sh

# Every Monday at 9 AM
0 9 * * 1 /script.sh

# First day of month at midnight
0 0 1 * * /script.sh

# Every weekday at 6 PM
0 18 * * 1-5 /script.sh

# Twice a day (8 AM and 8 PM)
0 8,20 * * * /script.sh
```

### Managing Crontab
```bash
# Edit crontab
crontab -e                  # Edit current user
sudo crontab -e             # Edit root's crontab
sudo crontab -u user -e     # Edit user's crontab

# List crontab
crontab -l
sudo crontab -u user -l

# Remove crontab
crontab -r                  # Remove all
crontab -i -r               # Confirm before remove
```

### Cron Directories
```bash
# System cron directories:
/etc/cron.d/                # Drop-in cron files
/etc/cron.hourly/           # Hourly scripts
/etc/cron.daily/            # Daily scripts
/etc/cron.weekly/           # Weekly scripts
/etc/cron.monthly/          # Monthly scripts

# Drop scripts here (no extension, executable)
sudo cp myscript.sh /etc/cron.daily/myscript
sudo chmod +x /etc/cron.daily/myscript
```

### /etc/cron.d Format
```bash
# /etc/cron.d/myapp
# Includes USER field
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# min hour dom mon dow user command
*/5 * * * * root /opt/myapp/check.sh
0 2 * * * www-data /var/www/backup.sh
```

### Cron Environment
```bash
# Cron runs with minimal environment!
# Specify full paths or set PATH

# In crontab:
PATH=/usr/local/bin:/usr/bin:/bin
MAILTO=admin@example.com
SHELL=/bin/bash

* * * * * /full/path/to/script.sh

# Or source profile in script:
#!/bin/bash
source /etc/profile
```

### systemd Timers (Modern Alternative)
```bash
# List timers
systemctl list-timers

# Create timer: /etc/systemd/system/myapp.timer
[Unit]
Description=Run MyApp Daily

[Timer]
OnCalendar=daily
# Or: OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target

# Create service: /etc/systemd/system/myapp.service
[Unit]
Description=MyApp Service

[Service]
Type=oneshot
ExecStart=/opt/myapp/script.sh

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable myapp.timer
sudo systemctl start myapp.timer
```

### Cron Logging
```bash
# View cron logs
grep CRON /var/log/syslog           # Debian/Ubuntu
cat /var/log/cron                   # RHEL/CentOS
journalctl -u cron

# Log output in script
*/5 * * * * /script.sh >> /var/log/myscript.log 2>&1

# Email output (configure MAILTO)
MAILTO=admin@example.com
* * * * * /script.sh
```

### Common Cron Issues
```bash
# 1. Script not running:
- Check cron service: systemctl status cron
- Check permissions: chmod +x script.sh
- Check syntax: crontab -l
- Check logs: grep CRON /var/log/syslog

# 2. Script runs manually but not in cron:
- Environment issue: use full paths
- Missing interpreter: add shebang

# 3. Email not received:
- Check MAILTO is set
- Check MTA is running
```

**💡 Best Practice:** Log all cron output, use lock files to prevent overlap, and test scripts manually first.""",


    # =========================================================================
    # LINUX ADMINISTRATION & PRODUCTION
    # =========================================================================

    "linux_hardening": """## 🔒 Linux Server Hardening

**Definition:** Server hardening is the process of securing a Linux system by reducing its attack surface and implementing security best practices.

### SSH Hardening
```bash
# /etc/ssh/sshd_config
Port 2222                       # Change default port
PermitRootLogin no              # Disable root login
PasswordAuthentication no       # Use keys only
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
AllowUsers john jane            # Whitelist users

# Generate SSH key
ssh-keygen -t ed25519 -C "comment"

# Copy key to server
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server

# Restart SSH
sudo systemctl restart sshd
```

### System Updates
```bash
# Debian/Ubuntu
sudo apt update && sudo apt upgrade -y
sudo apt install unattended-upgrades
sudo dpkg-reconfigure unattended-upgrades

# RHEL/CentOS
sudo dnf update -y
sudo dnf install dnf-automatic
sudo systemctl enable --now dnf-automatic.timer
```

### Disable Unnecessary Services
```bash
# List enabled services
systemctl list-unit-files --type=service --state=enabled

# Disable unnecessary services
sudo systemctl disable bluetooth
sudo systemctl disable cups
sudo systemctl disable avahi-daemon

# Remove unnecessary packages
sudo apt autoremove
```

### User Security
```bash
# Strong password policy
sudo apt install libpam-pwquality
# /etc/security/pwquality.conf
minlen = 12
dcredit = -1
ucredit = -1
lcredit = -1
ocredit = -1

# Lock inactive accounts
sudo useradd -e 2024-12-31 tempuser

# Audit privileged commands
sudo auditctl -w /usr/bin/sudo -p x -k sudo_usage
```

### File System Security
```bash
# Mount options in /etc/fstab
/dev/sda1 /tmp ext4 defaults,noexec,nosuid,nodev 0 2

# Find world-writable files
find / -perm -002 -type f 2>/dev/null

# Find SUID/SGID files
find / -perm /6000 -type f 2>/dev/null

# Secure important files
chmod 600 /etc/shadow
chmod 644 /etc/passwd
chmod 700 /root
```

### Network Security
```bash
# Disable IPv6 if not needed
echo "net.ipv6.conf.all.disable_ipv6 = 1" >> /etc/sysctl.conf

# Prevent IP spoofing
echo "net.ipv4.conf.all.rp_filter = 1" >> /etc/sysctl.conf

# Ignore ICMP broadcast requests
echo "net.ipv4.icmp_echo_ignore_broadcasts = 1" >> /etc/sysctl.conf

# Apply
sudo sysctl -p
```

### Security Checklist
```
✓ SSH: Key-based auth, disable root login
✓ Firewall: Default deny, allow only needed
✓ Updates: Automatic security updates
✓ Services: Disable unnecessary
✓ Users: Strong passwords, least privilege
✓ Auditing: Enable auditd
✓ Logging: Centralized logging
✓ Backups: Regular, tested restores
✓ Monitoring: Intrusion detection
```

**💡 Security Tip:** Defense in depth - use multiple layers of security. No single measure is enough.""",

    "linux_interview": """## 📝 Linux Interview Questions

**Definition:** Common Linux administration interview questions and answers for RHCSA, RHCE, and professional roles.

### Basic Questions

**Q: What is the difference between hard link and soft link?**
```
Hard Link:
- Same inode as original
- Cannot cross filesystems
- Original deleted? Link works
- Cannot link directories

Soft Link:
- Points to path/name
- Can cross filesystems
- Original deleted? Link breaks
- Can link directories
```

**Q: What are runlevels/targets?**
```
Runlevels (SysVinit):
0 - Halt
1 - Single user
3 - Multi-user (no GUI)
5 - Multi-user (GUI)
6 - Reboot

Targets (systemd):
poweroff.target (0)
rescue.target (1)
multi-user.target (3)
graphical.target (5)
reboot.target (6)
```

**Q: How do you check disk space?**
```bash
df -h         # Filesystem usage
du -sh /path  # Directory size
df -i         # Inode usage
```

### Process Questions

**Q: How do you find and kill a process?**
```bash
# Find
ps aux | grep process
pgrep -f process
pidof process

# Kill
kill PID           # SIGTERM
kill -9 PID        # SIGKILL
pkill -f process
killall process
```

**Q: What is a zombie process? How to handle it?**
```
Zombie: Process terminated but parent hasn't read exit status
- Shows as 'Z' in ps
- Doesn't use resources
- Fix: Kill parent process or reboot
- Prevention: Proper signal handling in code
```

### Networking Questions

**Q: How do you troubleshoot network connectivity?**
```bash
1. ping localhost        # Check TCP/IP stack
2. ping gateway          # Check local network
3. ping 8.8.8.8          # Check internet
4. ping google.com       # Check DNS
5. traceroute            # Find break point
6. ss -tuln              # Check listening ports
```

**Q: What's the difference between TCP and UDP?**
```
TCP: Connection-oriented, reliable, ordered, slower
UDP: Connectionless, unreliable, faster

Use TCP: Web, email, file transfer
Use UDP: DNS, streaming, gaming
```

### Permission Questions

**Q: Explain chmod 755**
```
7 (owner): rwx - read, write, execute
5 (group): r-x - read, execute
5 (others): r-x - read, execute

Owner can do everything
Group and others can read and execute
```

**Q: What is umask?**
```
umask defines default permission REMOVAL

umask 022:
- Default file: 666 - 022 = 644 (rw-r--r--)
- Default dir:  777 - 022 = 755 (rwxr-xr-x)
```

### Advanced Questions

**Q: How does Linux boot?**
```
1. BIOS/UEFI (hardware init)
2. GRUB2 (boot loader)
3. Kernel loading
4. initramfs (temporary root)
5. systemd (PID 1)
6. Services start
7. Login prompt
```

**Q: How do you troubleshoot high load?**
```bash
1. Check load: uptime
2. Identify type: top (CPU/Memory/IO)
3. Find culprit: top -c, iotop
4. Check for:
   - CPU: compute-intensive process
   - Memory: swapping
   - Disk: I/O wait
   - Network: packet storms
```

**Q: How do you recover a server that won't boot?**
```
1. Boot from Live USB
2. Mount root partition
3. chroot into system
4. Check/repair bootloader
5. Check filesystem (fsck)
6. Check logs in /var/log
7. Fix configuration issues
```

### Scenario Questions

**Q: Server running slow. How do you diagnose?**
```bash
uptime                  # Check load average
top -c                  # CPU/memory hogs
free -h                 # Memory usage
iostat -x               # Disk I/O
df -h                   # Disk space
ss -tuln                # Network connections
journalctl -p err       # Recent errors
```

**💡 Interview Tip:** Explain your thought process. Interviewers want to see how you approach problems, not just memorized commands.""",

    # Aliases for bash_scripting
    "bash scripting": """## 📜 Bash Shell Scripting

**Definition:** Bash scripting allows automating tasks by writing sequences of commands in executable files.

See `bash_scripting` for the complete guide with examples.""",

    "bash": """## 📜 Bash Shell

**Definition:** Bash (Bourne Again SHell) is the default command-line shell on most Linux distributions. It provides scripting capabilities for automation.

See `bash_scripting` for detailed scripting guide.

### Quick Reference
```bash
# Basic scripting
#!/bin/bash
echo "Hello World"

# Variables
NAME="Linux"
echo "Welcome to $NAME"

# Conditionals
if [ -f /etc/passwd ]; then
    echo "File exists"
fi

# Loops
for i in 1 2 3; do
    echo $i
done
```

**💡 Tip:** Use `bash_scripting` for comprehensive bash scripting guide.""",

}

# =============================================================================
# TAGS FOR SEARCH AND CATEGORIZATION
# =============================================================================

LINUX_TAGS = [
    # Core Linux
    "linux", "unix", "kernel", "distribution", "distro", "ubuntu", "debian",
    "centos", "rhel", "fedora", "arch", "alpine",
    
    # Boot and Init
    "boot", "grub", "grub2", "bios", "uefi", "initramfs", "initrd",
    "systemd", "systemctl", "service", "target", "runlevel",
    
    # File System
    "filesystem", "directory", "fhs", "inode", "mount", "fstab", "partition",
    "ext4", "xfs", "btrfs", "lvm", "raid", "swap",
    
    # Permissions
    "permissions", "chmod", "chown", "chgrp", "umask", "acl", "suid", "sgid",
    "sticky bit", "rwx",
    
    # Commands
    "commands", "bash", "shell", "terminal", "cli", "command line",
    "grep", "awk", "sed", "find", "tar", "gzip",
    
    # User Management
    "user", "users", "group", "groups", "useradd", "passwd", "sudo", "su",
    "sudoers", "pam",
    
    # Process Management
    "process", "processes", "pid", "top", "htop", "ps", "kill", "signal",
    "nice", "renice", "jobs", "background",
    
    # Networking
    "network", "networking", "ip", "ifconfig", "route", "dns", "hostname",
    "ss", "netstat", "nmcli", "networkmanager",
    
    # Security
    "security", "firewall", "iptables", "firewalld", "ufw", "nftables",
    "selinux", "apparmor", "hardening", "ssh",
    
    # Packages
    "package", "packages", "apt", "yum", "dnf", "pacman", "rpm", "deb",
    "repository",
    
    # Scripting
    "script", "scripting", "bash script", "shell script", "automation",
    
    # Monitoring
    "monitoring", "performance", "cpu", "memory", "disk", "load",
    "vmstat", "iostat", "sar", "free", "df",
    
    # Logs
    "log", "logs", "logging", "syslog", "journalctl", "dmesg", "rsyslog",
    "logrotate",
    
    # Containers
    "docker", "container", "containers", "dockerfile", "docker-compose",
    "podman", "kubernetes", "k8s",
    
    # Scheduling
    "cron", "crontab", "schedule", "timer", "at",
    
    # Production
    "production", "hardening", "backup", "disaster recovery", "high availability",
    "interview", "troubleshooting",
]
