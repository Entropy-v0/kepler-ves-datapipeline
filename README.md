# P2P Market Sentinel 🛰️

P2P Market Sentinel is a robust and resilient data pipeline designed to monitor and collect historical data from the Binance P2P marketplace. It automates the process of capturing advertisements, processing merchant information, and ensuring high-quality data persistence for financial science analysis.

---

## ✨ Key Features

- **Resilient Data Collection**: Implements a robust retry strategy with **Exponential Backoff** using `urllib3` to handle network micro-outages and API Rate Limiting (429).
- **Graceful Shutdown**: Handles `SIGINT` (Ctrl+C) and `SIGTERM` signals to ensure data integrity and clean resource closure.
- **Dual Persistence**: Simultaneously secures data in structured **CSV** files (for local analysis) and **PostgreSQL** (for scalable applications).
- **Secure Configuration**: Fully integrates `python-dotenv` for credential management and uses SQLAlchemy's secure URL construction to prevent injection.
- **Docker Ready**: Includes an optimized containerization setup for easy deployment and environment consistency.
- **Data Quality Oriented**: Architecture prepared for contract testing and cross-storage integrity audits.

---

## 📂 Project Structure

```text
.
├── config/
│   └── settings.py      # Centralized dynamic configuration
├── core/
│   ├── logger.py        # Dual-handler logging system
│   ├── processor.py     # Data transformation logic
│   ├── scraper.py       # Robust HTTP extraction with retries
│   ├── services.py      # Payload construction utilities
│   └── storage.py       # Dual persistence (CSV/SQL) handlers
├── data/
│   └── raw/             # Historical P2P data (CSV)
├── logs/                # System execution logs
├── Dockerfile           # Optimized Python 3.11-slim image
├── docker-compose.yml   # Multi-container orchestration (App + DB)
├── main.py              # Main orchestrator (Entry point)
└── requirements.txt     # Project dependencies
```

---

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose (Recommended)
- OR Python 3.11+ and PostgreSQL

### Fast Track with Docker
1. Configure your credentials in `.env`:
   ```env
   DB_USER=postgres
   DB_PASS=your_password
   DB_NAME=kepler_db
   DB_PORT=5432
   ```
2. Launch the experiment:
   ```bash
   docker-compose up --build
   ```

### Manual Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the orchestrator:
   ```bash
   python main.py
   ```

---

## ⚙️ Configuration
The system is highly configurable via `config/settings.py`:
- `ASSET`: Cryptocurrency to monitor (default: `USDT`).
- `FIAT`: Local currency (default: `VES`).
- `PAGES`: Number of pages to capture per cycle.
- `RAW_DATA_DIR`: Path for CSV storage (`data/raw`).
- `LOGS_DIR`: Path for system logs (`logs`).

---

## 📝 Quality and Audit
This project underwent a professional software audit. Detailed findings, remediation steps, and the quality assurance plan can be found in the `audit-workspace/` directory.

---
*Developed for Financial Data Science Experiments.*
