# 🧠 Allora Multi-Topic Reputer

Easily deploy a **Reputer** for **multiple Allora topics** using a **single Python codebase**.

This repo helps you:

- ✅ Source ground truth data (e.g., CoinGecko)
- ✅ Stake to secure Allora topics
- ✅ Run multiple topics with a single config

---

## ⚙️ Installation Guide

### 1️⃣ Install Go (v1.22.4)

```bash
sudo rm -rf /usr/local/go
curl -L https://go.dev/dl/go1.22.4.linux-amd64.tar.gz | sudo tar -xzf - -C /usr/local
echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> $HOME/.bash_profile
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> $HOME/.bash_profile
source $HOME/.bash_profile
go version
```

### 2️⃣ Install Allora CLI (v0.12.1)

```bash
git clone https://github.com/allora-network/allora-chain.git
cd allora-chain
git checkout v0.12.1
make all
allorad version
```

---

## 🔐 Wallet Management

| Command                                | Description            |
| -------------------------------------- | ---------------------- |
| `allorad keys add mywallet`           | Create a new wallet    |
| `allorad keys add mywallet --recover` | Recover from mnemonic  |
| `allorad keys list`                   | View all local wallets |

👉 Claim Testnet Tokens: [Allora Testnet Faucet](https://faucet.testnet.allora.network/)

---

## 📥 Stake in a Topic

Stake before running your Reputer:

```bash
allorad tx emissions add-stake [Your wallet address] [TOPIC_ID] [stake_amount] \
--from [Your wallet address] \
--node https://rpc.ankr.com/allora_testnet \
--chain-id allora-testnet-1 \
--fees 2000000uallo
```

---

## 📦 Clone This Repository

```bash
git clone https://github.com/HarbhagwanDhaliwal/allora_reputer.git
cd allora_reputer
```

---

## 🧩 Topic Configuration

Define supported topics in `config.py`:

```python
SUPPORT_TOPICS = ["13"]
```

Customize `reputer_topics.py`:

```python
from config import SUPPORT_TOPICS
from api_price import get_token_price

def get_truth(topic, token, block_height):
    if topic in SUPPORT_TOPICS:
        if topic == "13":
            return get_token_price(token, block_height)
        else:
            print("This topic logic not implemented yet.")
            return None
    else:
        print("This topic is not supported.")
        return None
```

✅ Add custom logic for more topics (e.g., volatility, volume, etc.)

---

## 🔑 CoinGecko API Keys

Add your keys in `api_price.py` to avoid rate limits:

```python
api_keys_coingecko = [
    "YOUR_COINGECKO_API_KEY_1",
    "YOUR_COINGECKO_API_KEY_2"
]
```

---

## 📁 Setup Worker Data Directory

```bash
mkdir -p worker-data
chmod -R 777 worker-data
```

---

## 📝 Update Wallet in `config.json`

Edit the config file:

```bash
nano config.json
```

Replace with your wallet mnemonic and topic setup:

```json
{
  "wallet": {
    "addressKeyName": "AlloraX",
    "chainId": "allora-testnet-1",
    "addressRestoreMnemonic": "your wallet seed phrase here",
    "alloraHomeDir": "/root/.allorad",
    "gasPrices": "auto",
    "gasPriceUpdateInterval": 5,
    "maxFees": 50000000,
    "gasAdjustment": 1.2,
    "simulateGasFromStart": true,
    "GasPerByte": 1,
    "BaseGas": 200000,
    "nodeRpcs": ["https://allora-rpc.testnet.allora.network"],
    "nodegRpcs": [
      "allora-grpc.testnet.allora.network:443",
      "testnet-allora.lavenderfive.com:443"
    ],
    "maxRetries": 5,
    "retryDelay": 3,
    "accountSequenceRetryDelay": 5,
    "launchRoutineDelay": 5,
    "submitTx": true,
    "blockDurationEstimated": 6,
    "windowCorrectionFactor": 0.8,
    "timeoutRPCSecondsQuery": 60,
    "timeoutRPCSecondsTx": 300,
    "timeoutRPCSecondsRegistration": 300,
    "timeoutHTTPConnection": 10
  },
  "reputer": [
    {
      "topicId": 13,
      "groundTruthEntrypointName": "apiAdapter",
      "lossFunctionEntrypointName": "apiAdapter",
      "loopSeconds": 30,
      "minStake": 100000,
      "groundTruthParameters": {
        "GroundTruthEndpoint": "http://truth:8099/reputer/{Topic}/{Token}/{BlockHeight}",
        "Token": "ethereum",
        "Topic:": "13"
      }
    }
  ]
}
```

Save and exit: `CTRL+X`, then `Y` and `Enter`

---

## 🚀 Initialize Config

```bash
chmod +x init.config
./init.config
```

---

## 🐳 Run Reputer with Docker

```bash
sudo docker compose up --build -d
```

📜 View logs:

```bash
docker compose logs -f
```

---

## ✅ You're Done!

Your Reputer is now live, running on multiple topics with a single Python-based setup.  
Join the Allora ecosystem and earn rewards while contributing valuable intelligence.

---
