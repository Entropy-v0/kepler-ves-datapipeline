# Kepler Miner 🛰️

Kepler is a robust P2P market sentinel designed to monitor and collect historical data from the Binance P2P marketplace. It automates the process of capturing advertisements, processing merchant information, and logging market trends for financial data science analysis.

## ✨ Features

- **Automated Data Collection**: Captures multiple pages of P2P advertisements at regular intervals.
- **Smart Processing**: Extracts key metrics including price, availability, transaction limits, merchant success rates, and payment methods.
- **CSV Persistence**: Automatically appends captured data to a structured CSV file for long-term analysis.
- **Modular Architecture**: Clean separation between scraping, processing, logging, and configuration.
- **Robust Logging**: Dual-handler system providing detailed console output (DEBUG) and persistent file logs (INFO).
- **Anti-Detection**: Implements random delays and randomized User-Agents to ensure stable collection cycles.

## 📂 Project Structure

```text
.
├── config/
│   └── settings.py      # API URLs, assets, and collection parameters
├── core/
│   ├── logger.py        # Centralized logging configuration
│   ├── processor.py     # Data parsing and cleaning logic
│   └── scraper.py       # HTTP request orchestration
├── output/
│   └── p2p_history.csv  # Collected market data
├── scripts/
├── main.py              # Main execution orchestrator
└── requirements.txt     # Project dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd p2p-market-sentinel
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Usage

To start the miner, simply run:

```bash
python main.py
```

The miner will initiate cycles every few minutes (randomized) and dump the collected data into `output/p2p_history.csv`.

## ⚙️ Configuration

You can customize the miner's behavior in `config/settings.py`:

- `ASSET`: The cryptocurrency to monitor (e.g., "USDT").
- `FIAT`: The local currency (e.g., "VES").
- `PAGES`: Number of pages to capture per cycle.
- `OUTPUT_FILE`: Path to the CSV storage.


## 📝 Logging

Kepler generates logs in `kepler.log`. The logs follow a rotating strategy to manage disk space efficiently.

---
*Developed for Financial Data Science Analysis.*
