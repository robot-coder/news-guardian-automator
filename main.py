import asyncio
import json
import requests
from llama_index import GPTIndex, SimpleDocument, ServiceContext
from mcp_server_sdk import MCPClient, MCPError
from playwright.async_api import async_playwright
from typing import List, Dict, Any, Optional

class NewsAgent:
    """
    An agent that uses LlamaIndex for data operations, interacts with MCP servers for web automation,
    and manages multi-agent workflows to deliver personalized news.
    """

    def __init__(self, mcp_server_url: str, index_api_key: str):
        """
        Initialize the NewsAgent with MCP server URL and LlamaIndex API key.
        """
        self.mcp_server_url = mcp_server_url
        self.index_api_key = index_api_key
        self.mcp_client = MCPClient(self.mcp_server_url)
        self.service_context = ServiceContext.from_defaults(api_key=self.index_api_key)
        self.index: Optional[GPTIndex] = None

    def load_data(self, documents: List[str]) -> None:
        """
        Load documents into LlamaIndex.
        """
        try:
            docs = [SimpleDocument(text=doc) for doc in documents]
            self.index = GPTIndex.from_documents(docs, service_context=self.service_context)
        except Exception as e:
            print(f"Error loading data into index: {e}")

    def query_index(self, query: str) -> str:
        """
        Query the LlamaIndex with a given question.
        """
        if not self.index:
            return "Index not initialized."
        try:
            response = self.index.query(query)
            return response.response
        except Exception as e:
            return f"Error querying index: {e}"

    async def automate_web_task(self, url: str, actions: List[Dict[str, Any]]) -> str:
        """
        Use Playwright to automate web interactions.
        """
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url)
                for action in actions:
                    if action['type'] == 'click':
                        await page.click(action['selector'])
                    elif action['type'] == 'fill':
                        await page.fill(action['selector'], action['value'])
                    elif action['type'] == 'wait':
                        await page.wait_for_timeout(action['timeout'])
                content = await page.content()
                await browser.close()
                return content
        except Exception as e:
            return f"Web automation error: {e}"

    def fetch_personalized_news(self, user_preferences: Dict[str, Any]) -> List[str]:
        """
        Fetch personalized news based on user preferences.
        """
        try:
            # Example: send preferences to MCP server to get news
            response = self.mcp_client.post('/get_news', json=user_preferences)
            if response.status_code == 200:
                news_items = response.json().get('news', [])
                return news_items
            else:
                print(f"Failed to fetch news: {response.status_code}")
                return []
        except MCPError as e:
            print(f"MCP server error: {e}")
            return []

    async def run(self):
        """
        Main execution method to coordinate data loading, querying, web automation, and news delivery.
        """
        # Example documents
        documents = [
            "Breaking news: Market hits all-time high.",
            "Sports update: Local team wins championship.",
            "Weather forecast: Sunny days ahead."
        ]
        self.load_data(documents)

        # Query the index
        query_result = self.query_index("Latest news about the economy")
        print(f"Query Result: {query_result}")

        # Automate web task (e.g., scrape a news site)
        url = "https://example-news-site.com"
        actions = [
            {'type': 'click', 'selector': '#accept-cookies'},
            {'type': 'wait', 'timeout': 2000},
            {'type': 'fill', 'selector': '#search-box', 'value': 'latest news'},
            {'type': 'click', 'selector': '#search-button'}
        ]
        page_content = await self.automate_web_task(url, actions)
        print(f"Web Page Content Length: {len(page_content)}")

        # Fetch personalized news
        user_preferences = {'topics': ['technology', 'sports'], 'location': 'NY'}
        news = self.fetch_personalized_news(user_preferences)
        print("Personalized News:")
        for item in news:
            print(f"- {item}")

if __name__ == "__main__":
    agent = NewsAgent(mcp_server_url="https://mcp-server.example.com", index_api_key="your-llamaindex-api-key")
    asyncio.run(agent.run())