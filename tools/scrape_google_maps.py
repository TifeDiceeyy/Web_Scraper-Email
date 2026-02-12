#!/usr/bin/env python3
"""
Scrape businesses from Google Maps

NOTE: This is a simplified version. For production, consider using:
- Outscraper API (paid, reliable)
- Apify Google Maps Scraper (paid)
- Selenium for browser automation (free but slow)

This version provides a structure for manual entry or API integration.
"""

import requests
import time
import os
from apify_client import ApifyClient


def scrape_google_maps(business_type, location, max_results=20):
    """
    Scrape businesses from Google Maps

    Args:
        business_type: Type of business (e.g., "Dentist")
        location: Location (e.g., "San Francisco, CA")
        max_results: Maximum number of results

    Returns:
        list: List of business dictionaries
    """

    print("\n" + "="*60)
    print("🗺️  GOOGLE MAPS SCRAPER")
    print("="*60)
    print("\n⚠️  NOTE: Google Maps scraping requires external services.")
    print("\nOptions:")
    print("1. Use Outscraper API (recommended, paid)")
    print("2. Use Apify Google Maps Scraper (paid)")
    print("3. Manual browser extension export")
    print("4. Enter sample data for testing")
    print("\n" + "="*60)

    choice = input("\nChoose option (1-4): ").strip()

    if choice == "1":
        return scrape_with_outscraper(business_type, location, max_results)
    elif choice == "2":
        return scrape_with_apify(business_type, location, max_results)
    elif choice == "3":
        print("\n📋 Steps to export from Google Maps:")
        print("1. Search '{} in {}' on Google Maps".format(business_type, location))
        print("2. Use a browser extension like 'Data Miner' or 'Web Scraper'")
        print("3. Export to JSON")
        print("4. Use the 'Load from JSON' option in main menu")
        return []
    else:
        # Generate sample data for testing
        return generate_sample_businesses(business_type, location, max_results)


def scrape_with_outscraper(business_type, location, max_results):
    """
    Use Outscraper API to scrape Google Maps
    Docs: https://outscraper.com/
    """

    print("\n📝 To use Outscraper:")
    print("1. Sign up at https://outscraper.com/")
    print("2. Get your API key")
    print("3. pip install outscraper")
    print("4. Uncomment the code below")

    # Uncomment and configure when you have an API key:
    """
    from outscraper import ApiClient

    api_key = os.getenv('OUTSCRAPER_API_KEY')
    client = ApiClient(api_key=api_key)

    query = f"{business_type} in {location}"
    results = client.google_maps_search([query], limit=max_results)

    businesses = []
    for place in results[0]:
        businesses.append({
            'name': place.get('name', ''),
            'location': place.get('full_address', ''),
            'email': place.get('emails', [''])[0],
            'phone': place.get('phone', ''),
            'website': place.get('site', ''),
            'contact_person': ''
        })

    return businesses
    """

    return []


def scrape_with_apify(business_type, location, max_results):
    """
    Use Apify to scrape Google Maps
    Docs: https://apify.com/
    """

    print("\n🚀 Using Apify Google Maps Scraper...")
    print(f"   Searching: {business_type} in {location}")
    print(f"   Max results: {max_results}")

    try:
        api_token = os.getenv('APIFY_TOKEN')
        if not api_token:
            print("❌ Error: APIFY_TOKEN not found in .env file")
            return []

        client = ApifyClient(api_token)

        run_input = {
            "searchStringsArray": [f"{business_type} in {location}"],
            "maxCrawledPlacesPerSearch": max_results,
        }

        print("\n⏳ Running Apify Actor (this may take 1-2 minutes)...")
        run = client.actor("compass/crawler-google-places").call(run_input=run_input)

        print("✅ Scraping complete! Processing results...")

        businesses = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            businesses.append({
                'name': item.get('title', ''),
                'location': item.get('address', ''),
                'email': item.get('email', ''),
                'phone': item.get('phoneNumber', ''),
                'website': item.get('website', ''),
                'contact_person': ''
            })

        print(f"\n✅ Found {len(businesses)} businesses!")
        return businesses

    except Exception as e:
        print(f"\n❌ Error scraping with Apify: {e}")
        print("💡 Tip: Check your APIFY_TOKEN in .env file")
        return []


def generate_sample_businesses(business_type, location, max_results):
    """Generate sample data for testing"""

    print(f"\n🧪 Generating {max_results} sample {business_type}s in {location}...")

    businesses = []
    for i in range(1, min(max_results, 5) + 1):
        businesses.append({
            'name': f'Sample {business_type} #{i}',
            'location': location,
            'email': f'contact{i}@sample{business_type.lower()}.com',
            'phone': f'(555) {100+i:03d}-{1000+i:04d}',
            'website': f'https://sample{business_type.lower()}{i}.com',
            'contact_person': f'Dr. Smith #{i}' if business_type == 'Dentist' else ''
        })

    return businesses


if __name__ == "__main__":
    businesses = scrape_google_maps("Dentist", "San Francisco, CA", 5)
    print(f"\nScraped {len(businesses)} businesses")
    for b in businesses:
        print(f"  - {b['name']}")
