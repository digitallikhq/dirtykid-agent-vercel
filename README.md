# Dirty Kid AI Agent

Dirty Kid is an autonomous AI trading agent that publicly logs Bitcoin market observations and small experimental trades.

The agent operates with strict risk controls and publishes activity through the Dirty Kid social account.

This project is designed as a transparent experiment combining AI agents, market analysis, and automated reporting.

---

# Project Purpose

Dirty Kid represents a "street-level AI trader" that studies Bitcoin markets and executes disciplined micro-trades while documenting observations in real time.

The system prioritizes:

- capital preservation
- disciplined execution
- transparent logging
- controlled automation

Dirty Kid does not attempt to predict markets with certainty and avoids overtrading or high-risk behavior.

---

# System Architecture

The Dirty Kid agent is built using multiple specialized modules.

Market Data  
↓  
Market Analyst  
↓  
Risk Manager  
↓  
Execution Gate  
↓  
Trade Execution  
↓  
Posting Controls  
↓  
Post Generation  
↓  
X Publishing  
↓  
Telegram Notifications  

Each module performs a specific function and cannot override other modules.

---

# Trading Parameters

The trading system follows strict rules.

Market: BTC-USD  
Exchange: Coinbase  
Market Type: Spot only  

Position Size: $10  

Maximum Open Positions: 1  
Maximum Trades Per Day: 2  

Daily Loss Limit: $5  
Stop After: 2 Losing Trades  

Forbidden actions:

- leverage
- margin trading
- shorting
- options
- averaging down
- revenge trading
- position size increases

The system prioritizes survival over activity.

If no valid signal exists, the agent does nothing.

---

# Posting Behavior

Dirty Kid shares market observations and trade events publicly.

Posting rules:

Maximum posts per day: 4  
Maximum posts per hour: 1  
Minimum time between posts: 45 minutes  

Allowed post categories:

- morning observation
- trade opened
- trade closed
- daily recap

The system avoids spam and prefers silence over low-quality posts.

---

# Agent Modules

The repository contains several prompt modules that define the behavior of the AI system.

prompts/
01_identity.txt  
02_post_writer.txt  
03_market_analyst.txt  
04_risk_manager.txt  
05_execution_gate.txt  
06_output_format.txt  
07_posting_controls.txt  

Each module performs a distinct role in the agent decision pipeline.

---

# Configuration

Trading rules and system limits are stored in:

config/strategy.yaml

This file defines risk limits, trading parameters, and posting restrictions.

---

# Workflow Documentation

The full decision flow of the agent is documented in:

docs/workflow.md

This explains how market data moves through the system and how decisions are produced.

---

# Disclaimer

This project is an experimental AI automation system.

Nothing produced by Dirty Kid should be interpreted as financial advice.

Trading cryptocurrencies carries significant risk and losses are possible.

The system is designed primarily for research, experimentation, and public documentation of an AI trading agent.

---

# Dirty Kid

Street rule:

If the signal is weak,  
do nothing.
