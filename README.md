# 🧠 Polymarket Prompt Generator

**Polymarket Prompt Generator** is a tool that automates the creation of detailed prompts for analyzing Polymarket events. It extracts and formats real-time market information to help analysts, researchers, or AI agents quickly assess the potential value of speculative markets.

## ✨ Main Features

The app takes a Polymarket event URL and automatically generates a structured prompt containing:

- 📌 Title, description, resolution source, and end date of the event
- 📊 A list of all available markets, including:
  - Option name
  - "Yes" and "No" prices (in percentages)
- 🧾 Detailed instructions for analyzing each market using a JSON response format

## 🔍 Use Cases

- Generate **optimized prompts for LLMs** (Large Language Models) to evaluate prediction markets
- Assist **manual market analysis**, highlighting potential inefficiencies or value
- Serve as an educational tool to understand how **decentralized prediction markets** work

## 📡 Data Source

All event data is retrieved from Polymarket's public API (`https://gamma-api.polymarket.com/`), ensuring accurate and up-to-date information.

## 🛠️ Project Structure

- `get_polymarket_prompt()`: Main function orchestrating the flow of data extraction and prompt formatting
- Helper functions:
  - `get_slug_from_url()`
  - `fetch_event_data()`
  - `parse_market_info()`
  - `build_prompt()`
- A user-friendly interface built with **Streamlit**
- 
## 📄 License

This project is open-source and may be used freely for academic, educational, and personal purposes.
