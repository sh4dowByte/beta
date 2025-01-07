<p align="center">
  <img src="icon.png" alt="app"  width="300">
</p>

<p align="center">
    <img src="https://badgen.net/badge/Python/≥3.12.2/yellow?icon=pypi" alt="Python Badge" style="max-width: 100%;">
    <img src="https://badgen.net/badge/Learning/Purposes/purple?icon=terminal" alt="Learning Badge" style="max-width: 100%;">
    <img src="https://badgen.net/badge/Under/Development/blue?icon=github" alt="Development Badge" style="max-width: 100%;">
</p>

## 📜 Description

**Beta** is a **Port Scanner** application developed as a learning tool in the fields of cybersecurity and Python programming. Beta aims to provide practical insights into scanning and analyzing open ports on target machines. This application is designed for use in a testing and learning environment with a focus on network security and software development.

### Key Features:

- **Port Scanning**: Efficiently scans for open ports on specified IP addresses or network ranges. Provides detailed information about discovered services and their associated ports.
- **Multi-threading**: Utilizes multi-threading to perform concurrent scans, significantly reducing the time required to scan large networks.
- **Customizable Scans**: Allows users to specify target ports, IP addresses, and scanning options, making it adaptable to different scenarios.
- **Result Reporting**: Generates structured and formatted scan reports, making it easy to interpret and analyze the results.
- **Interactive CLI**: Features a command-line interface built using `rich.console` to display real-time progress and results in a user-friendly manner.

### Learning Objectives:

- **Understanding Port Scanning**: Learn about the importance of port scanning in network security and how it can be used to identify vulnerabilities.
- **Python Programming**: Enhance skills in Python programming, particularly in networking and concurrent programming. Learn how to utilize libraries such as `socket`, `threading`, and `rich.console` to build effective and responsive applications.
- **Application Development**: Understand techniques and best practices for developing CLI applications, with a focus on usability and performance.

**Note**: Beta is designed for educational and testing purposes. Use of this application should be conducted in a safe and legal environment and adhere to applicable cybersecurity laws and ethics.

## ⚙️ Installation

### Using pipx (Recommended)
`pipx` is a tool to install and run Python applications in isolated environments. Follow these steps to install Beta:

1. Install pipx:
   ```bash
   sudo apt install pipx
   pipx ensurepath
   ```

2. Clone the Beta repository:
   ```bash
   git clone https://github.com/sh4dowByte/beta.git
   cd beta
   ```

3. Install Beta using pipx:
   ```bash
   pipx install .
   ```

### Alternative Setup - Using Alias
If you prefer not to use `pipx`, you can set up an alias to run `beta.py` directly from your terminal.

1. Clone the Beta repository:
   ```bash
   git clone https://github.com/sh4dowByte/beta.git
   cd beta
   ```

2. Install the required dependencies from `requirements.txt`:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. Open your terminal and add the following alias to your shell configuration file (e.g., `~/.bashrc` or `~/.zshrc`):
   ```bash
   alias beta='python3 ~/Pentest/beta/beta.py'
   ```

4. After adding the alias, run `source ~/.bashrc` (or `source ~/.zshrc` for zsh) to reload your shell configuration.

Now, you can run `beta` directly from your terminal!

## 📝 Examples

#### Single IP

```bash
beta 192.168.1.1
```

#### IPs from a file

```bash
beta -l ip_list.txt
```

#### Multiple IPs and Domains

```bash
beta 192.168.1.1 example.com 192.168.1.2
```

#### CIDR Range

```bash
beta 192.168.1.0/24
```

#### IP Range

```bash
beta 192.168.1.0-192.168.2.254
```

## 📚 Reference Tools

- **Nmap** by [nmap.org](https://nmap.org) - A well-known network scanning tool used for discovering hosts and services on a computer network.

## 📽️ Demo App

<img src="https://raw.githubusercontent.com/sh4dowByte/media/main/beta/Beta.gif"  style="max-width: 80%;">