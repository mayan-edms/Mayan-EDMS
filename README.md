<div align="center">

# 📄 Mayan EDMS 📄

*Free Open Source Electronic Document Management System* ✨

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryproject.org/)

<a href="http://www.mayan-edms.com">
    <img width="200" src="https://gitlab.com/mayan-edms/mayan-edms/raw/master/docs/_static/mayan_logo.png" alt="Mayan EDMS Logo">
</a>

</div>

---

## 🌟 Welcome to Mayan EDMS

**Experience the perfect blend of document management and business automation!**

Mayan EDMS is a document management system. Its main purpose is to store, introspect, and categorize files, with a strong emphasis on preserving the contextual and business information of documents. It can also OCR, preview, label, sign, send, and receive those files.

---

## 🚀 What Makes Mayan Special?

<table>
<tr>
<td width="50%">

### 🎨 **Advanced Document Control**
- **Intelligent OCR** backend for text extraction
- **Automatic Preview Generation** for many file formats
- **Digital Signatures** and verification
- **Versioning** to keep track of document history

</td>
<td width="50%">

### ⚡ **Powerful Automation**
- **Workflow System** to automate business processes
- **Smart Links** for dynamic document relationships
- **Role Based Access Control** for granular security
- **REST API** for third-party integration

</td>
</tr>
</table>

---

## 🎯 Key Features

<div align="center">

| 📁 **Document Management** | 🔐 **Security & Compliance** | 🔧 **Technical Excellence** |
|:---:|:---:|:---:|
| File Storage & Retrieval | Role Based Access Control | Modern Tech Stack |
| Metadata Tagging | Audit Logging | RESTful API |
| Full Text Search | Digital Signatures | Docker Deployment |
| OCR Integration | User Authentication | Scalable Architecture |
| File Conversions | Permissions Management | Pluggable Backends |

</div>

---

## 🛠️ Tech Stack

<div align="center">

### Core Architecture
```
Python + Django + Celery
├── 🐍 Python Core Logic
├── 🌐 Django Web Framework
├── ⚡ Celery Task Queue
└── 🔄 REST API Endpoints
```

### Infrastructure & Data
```
Docker + PostgreSQL + Redis
├── 🐳 Docker Containerization
├── 🗃️ PostgreSQL Database
├── 🚀 Redis Cache & Broker
└── 🔍 ElasticSearch (Optional)
```

</div>

---

## 🚀 Quick Start Guide

### Prerequisites
- **Docker** (Installed and running)
- **Hardware**: 2GB RAM (1GB if OCR off), Multi-core CPU

### 🔧 Installation

<details>
<summary><b>🐳 Docker Setup (Recommended)</b></summary>

The easiest way to use Mayan EDMS is by using the official Docker image.

```bash
# Pull the image
docker pull mayanedms/mayanedms

# Run the container
docker run -d --name mayan-edms -p 80:8000 -v mayan_data:/var/lib/mayan mayanedms/mayanedms
```

For the complete set of installation instructions visit the [Mayan EDMS documentation](https://docs.mayan-edms.com/parts/installation.html).

</details>

### 🌐 Access Your Application

| Service | URL | Description |
|---------|-----|-------------|
| 🏠 **Web Interface** | http://localhost:80 | Main User Interface |
| 📚 **Documentation** | https://docs.mayan-edms.com | Official Docs |
| 💬 **Forum** | https://forum.mayan-edms.com | Community Support |

---

## 📁 Project Structure

```
Mayan-EDMS/
├── 📂 contrib/             # Scripts, git hooks, and helper tools
├── 🐳 docker/              # Docker configuration and compose files
├── 📚 docs/                # Documentation source files (Sphinx)
├── 🐍 mayan/               # Main application source code
│   ├── 🧩 apps/            # Django apps (core logic modules)
│   ├── ⚙️ settings/        # Configuration settings
│   ├── 🌐 urls/            # URL routing
│   └── 🚀 bin/             # Command line utilities
├── 📦 requirements/        # Python dependencies
└── 📜 README.md            # You are here! 👋
```

---

## 🎨 Overview

<div align="center">

### 🏠 Dashboard & Interface
*Intuitive interface for managing your document repository*

<img width="600" src="https://gitlab.com/mayan-edms/mayan-edms/raw/master/docs/_static/overview.gif" alt="Mayan EDMS Overview">

</div>

---

## 🤝 Contributing

We welcome contributions from the community!

<details>
<summary><b>🔧 Development Guidelines</b></summary>

1.  **Fork** the repository
2.  **Create** a feature branch
3.  **Commit** your changes
4.  **Push** to the branch
5.  **Open** a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

</details>

---

## 📚 Resources & Links

<div align="center">

| [Homepage](http://www.mayan-edms.com) | [Source Code](https://gitlab.com/mayan-edms/mayan-edms) | [Translations](https://www.transifex.com/rosarior/mayan-edms/) | [Videos](https://www.youtube.com/channel/UCJOOXHP1MJ9lVA7d8ZTlHPw) |
|:---:|:---:|:---:|:---:|

[![Support](https://img.shields.io/badge/Get_support-brightgreen)](https://www.mayan-edms.com/support/)
[![Store](https://img.shields.io/badge/Online_store-black)](https://teespring.com/stores/mayan-edms)
[![Donation](https://img.shields.io/badge/donation-PayPal-brightgreen)](https://paypal.me/MayanEDMS)

</div>

---

## 📜 License

This project is licensed under the **Apache 2.0 License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### 📄 *"Free Open Source Electronic Document Management System"* 📄

**Made with ❤️ by the Mayan EDMS Community**

---

*⭐ Don't forget to star this repository if you found it helpful! ⭐*

</div>

