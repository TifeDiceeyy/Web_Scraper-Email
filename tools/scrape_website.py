#!/usr/bin/env python3
"""
Scrape business website content
"""

import requests
from bs4 import BeautifulSoup


def scrape_website(url):
    """
    Scrape a business website and extract key information

    Args:
        url: Website URL

    Returns:
        str: Extracted text content (max 1000 chars)
    """

    try:
        # Add http:// if not present
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # Set user agent to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        # Fetch the page
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse HTML (using built-in html.parser)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()

        # Get text
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        # Limit to 1000 characters
        return text[:1000]

    except Exception as e:
        print(f"   ⚠️  Could not scrape website: {str(e)}")
        return ""


def test_scrape_website():
    """Test function"""
    url = "https://example.com"
    content = scrape_website(url)
    print(f"Scraped content ({len(content)} chars):")
    print(content[:200] + "...")


if __name__ == "__main__":
    test_scrape_website()
