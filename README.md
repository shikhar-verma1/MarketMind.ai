 MarketMind 
An Autonomous, Multi-Agent financial AI  Human-in-the-Loop Security
MarketMind is a production-grade AI financial analysis pipeline. It utilizes a multi-agent LangGraph architecture to simulate an institutional financial environment, where specialized AI personas (a Fundamental Analyst and a Risk Manager) analyze live market data and debate investment viability. 
To ensure enterprise-level safety, the swarm operates behind a strict Human-in-the-Loop (HITL) security checkpoint, pausing all autonomous execution until a human operator authorizes the final risk assessment.
Key Features

* **Multi-Agent Orchestration:** Powered by LangGraph, the system passes context seamlessly between a brilliant Fundamental Analyst and a pessimistic Risk Manager to generate unbiased, multi-perspective financial reports.
* **Live Data Harvesting:** A custom Python scraper that pulls real-time financial news and automatically falls back to SEC institutional data if web firewalls (like Yahoo Finance) block the connection.
* **Human-in-the-Loop (HITL) Security:** Utilizes LangGraph's `MemorySaver` to create save-states, physically pausing the AI's execution to request human authorization before proceeding to the final risk-assessment phase.
* **Streamlit Web Dashboard:** A sleek, interactive web application that completely replaces the terminal, allowing users to enter stock tickers and watch the AI debate in real-time.
* **Dynamic PDF Export:** Packages the AI's final dual-perspective analysis into a clean, professional PDF document for local saving or client distribution.
* **100% Open-Source Engine:** Fully integrated with the free Hugging Face Serverless API, running Meta's Llama-3-8B model locally without requiring expensive API subscriptions.
