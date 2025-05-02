# README.md

# Multi-Agent News Delivery System

This project implements a sophisticated agent that leverages LlamaIndex tools for data operations, interacts with MCP servers for web automation, and potentially builds a multi-agent system to deliver personalized news content. The system is designed to be modular, robust, and adaptable to complex data and web automation tasks.

## Features

- Utilizes LlamaIndex for efficient data querying and management.
- Interacts with MCP servers for web automation tasks using the MCP SDK.
- Employs Playwright for browser automation.
- Supports asynchronous operations with asyncio.
- Modular design with proper error handling.

## Requirements

Ensure you have Python 3.8+ installed. Install the required libraries:

```bash
pip install llama_index mcp_server_sdk playwright requests
```

Additionally, install Playwright browsers:

```bash
python -m playwright install
```

## Files

- `main.py`: Main script orchestrating the agent's operations.
- `requirements.txt`: List of dependencies.
- `README.md`: This documentation.

## Usage

Run the main script:

```bash
python main.py
```

---

# main.py

import asyncio
import json
import requests
from llama_index import GPTIndex, SimpleDataLoader
from mcp_server_sdk import MCPClient, MCPError
from playwright.async_api import async_playwright
from typing import Any, Dict, Optional

class NewsAgent:
    """
    An agent that performs data operations, web automation, and manages multi-agent interactions
    for personalized news delivery.
    """

    def __init__(self, mcp_server_url: str):
        """
        Initialize the NewsAgent with MCP server URL.
        """
        self.mcp_server_url = mcp_server_url
        self.mcp_client: Optional[MCPClient] = None
        self.index: Optional[GPTIndex] = None

    def initialize_mcp_client(self) -> None:
        """
        Initialize MCP client.
        """
        try:
            self.mcp_client = MCPClient(self.mcp_server_url)
        except MCPError as e:
            print(f"Error initializing MCP client: {e}")
            self.mcp_client = None

    def load_data(self, data_source: str) -> None:
        """
        Load data into LlamaIndex from a data source.
        """
        try:
            data_loader = SimpleDataLoader(data_source)
            documents = data_loader.load()
            self.index = GPTIndex.from_documents(documents)
        except Exception as e:
            print(f"Error loading data: {e}")

    async def automate_web_task(self, url: str) -> None:
        """
        Automate web interactions using Playwright.
        """
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url)
                # Example: Extract page title
                title = await page.title()
                print(f"Page title: {title}")
                await browser.close()
        except Exception as e:
            print(f"Web automation error: {e}")

    def fetch_personalized_news(self, user_preferences: Dict[str, Any]) -> Optional[str]:
        """
        Query the index for personalized news based on user preferences.
        """
        if not self.index:
            print("Index not initialized.")
            return None
        try:
            query = json.dumps(user_preferences)
            response = self.index.query(query)
            return response
        except Exception as e:
            print(f"Error querying index: {e}")
            return None

    def send_request_to_mcp(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Send data to MCP server and handle response.
        """
        if not self.mcp_client:
            print("MCP client not initialized.")
            return None
        try:
            response = self.mcp_client.send(data)
            return response
        except MCPError as e:
            print(f"MCP communication error: {e}")
            return None

    async def run(self):
        """
        Main execution method.
        """
        self.initialize_mcp_client()
        self.load_data("path/to/data_source")  # Replace with actual data source path

        # Example web automation task
        await self.automate_web_task("https://news.example.com")

        # Example user preferences
        user_preferences = {"topics": ["technology", "science"], "regions": ["US"]}
        news = self.fetch_personalized_news(user_preferences)
        if news:
            print(f"Personalized News: {news}")

        # Send data to MCP server
        response = self.send_request_to_mcp({"request": "fetch_news", "preferences": user_preferences})
        if response:
            print(f"MCP Server Response: {response}")

if __name__ == "__main__":
    agent = NewsAgent("https://mcp.server.api")
    asyncio.run(agent.run())

# requirements.txt

llama_index
mcp_server_sdk
playwright
requests
json