# 🔐 MARS-11 Zip-Crack: Advanced Archive Password Recovery Tool

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Repo Size](https://img.shields.io/github/repo-size/MARS-11/Zip-Crack)]()

![MARS-11 Zip-Crack Screenshot](screenshot.jpg)

**MARS-11 Zip-Crack** is a high-performance, multi-threaded ZIP archive password recovery tool designed for ethical penetration testing and digital forensics. Built with Python 3, it combines advanced cryptographic checks with an intuitive terminal interface.

## ✨ Features

- 🚀 Multi-core processing for maximum speed
- 🔍 CRC32 validation for instant password verification
- 📊 Real-time progress tracking with tqdm
- 🎨 Dynamic ASCII art interface
- 🛠️ Automatic encrypted file detection
- 📈 Password validation and filtering
- 🧠 Intelligent workload distribution
- 🎯 Support for multiple encoding formats
- 📉 Comprehensive statistics and ETA tracking

## ⚙️ Installation

### Linux/Termux
```bash
apt update && apt upgrade -y
apt install git python3 -y
pip3 install -r requirements.txt
git clone https://github.com/MARS-11/Zip-Crack
cd Zip-Crack
python3 mars.py
```

### Windows/MacOS
1. Install [Python 3.10+](https://www.python.org/downloads/)
2. Install [Git](https://git-scm.com/downloads)
3. Run in command prompt/terminal:
```bash
git clone https://github.com/MARS-11/Zip-Crack
cd Zip-Crack
pip install -r requirements.txt
python mars.py
```

## 📖 Usage

1. Prepare your password wordlist (one password per line)
2. Launch MARS-11 Zip-Crack:
```bash
python3 mars.py
```
3. Follow the interactive prompts
4. View real-time cracking statistics
5. Recover password with success notification

## 🛠️ Technical Specifications

- **Algorithm**: AES-256/ZipCrypto
- **Validation**: CRC32 checksum verification
- **Parallelism**: CPU cores ×6 worker threads
- **Compatibility**: Windows/Linux/MacOS/Android (Termux)
- **Performance**: 500k+ passwords/minute (i7-11800H)

## ⚠️ Legal Disclaimer

This tool is intended for:
- Legal penetration testing
- Password recovery of personal files
- Educational cybersecurity purposes

**Never use for unauthorized access!** The developer assume no liability for misuse.

## 🤝 Contributing

We welcome contributions! Please read our [Contribution Guidelines](CONTRIBUTING.md) before submitting PRs.

## 📜 License

Distributed under MIT License. See `LICENSE` for full text.

## 👨💻 Developer

**MasterX** : 
[![Telegram](https://img.shields.io/badge/-Telegram-0088CC?style=flat&logo=telegram)](https://t.me/MasterX_00)
[![GitHub](https://img.shields.io/badge/-GitHub-181717?style=flat&logo=github)](https://github.com/MasterX-0)

```
