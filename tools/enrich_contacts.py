#!/usr/bin/env python3
"""
Enrich business contacts by extracting emails and phone numbers from websites
Uses Apify's Contact Info Scraper
"""

import os
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()


def enrich_business_contacts(businesses, max_per_business=5):
    """
    Enrich business data by scraping their websites for contact information

    Args:
        businesses: List of business dictionaries (must have 'website' field)
        max_per_business: Maximum contacts to extract per business

    Returns:
        list: Enriched businesses with emails and phones
    """

    print("\n🔍 CONTACT ENRICHMENT")
    print("=" * 60)

    # Filter businesses with websites
    businesses_with_websites = [
        b for b in businesses
        if b.get('website') and b['website'].strip()
    ]

    if not businesses_with_websites:
        print("⚠️  No businesses with websites to enrich")
        return businesses

    print(f"📊 Enriching {len(businesses_with_websites)} businesses with contact data...")

    try:
        api_token = os.getenv('APIFY_TOKEN')
        if not api_token:
            print("❌ Error: APIFY_TOKEN not found in .env file")
            return businesses

        client = ApifyClient(api_token)

        # Prepare URLs for scraping
        start_urls = [
            {"url": b['website']}
            for b in businesses_with_websites
        ]

        run_input = {
            "startUrls": start_urls,
            "maxDepth": 2,  # Crawl 2 levels deep
            "maxPagesPerDomain": 5,  # Check up to 5 pages per domain
            "includePersonalData": True,
        }

        print("\n⏳ Running Apify Contact Scraper (this may take 2-3 minutes)...")
        run = client.actor("vdrmota/contact-info-scraper").call(run_input=run_input)

        print("✅ Scraping complete! Processing contact data...")

        # Create URL to business mapping
        url_to_business = {
            b['website']: b
            for b in businesses_with_websites
        }

        # Process results and enrich businesses
        enriched_count = 0
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            url = item.get('url', '')

            # Find matching business
            matching_business = None
            for business_url, business in url_to_business.items():
                if business_url in url or url in business_url:
                    matching_business = business
                    break

            if not matching_business:
                continue

            # Extract emails
            emails = item.get('emails', [])
            if emails and not matching_business.get('email'):
                matching_business['email'] = emails[0]  # Use first email
                matching_business['all_emails'] = emails[:max_per_business]
                enriched_count += 1

            # Extract phones
            phones = item.get('phones', [])
            if phones and not matching_business.get('phone'):
                matching_business['phone'] = phones[0]  # Use first phone
                matching_business['all_phones'] = phones[:max_per_business]

        print(f"\n✅ Enriched {enriched_count} businesses with contact data!")

        return businesses

    except Exception as e:
        print(f"\n❌ Error during contact enrichment: {e}")
        print("💡 Tip: Check your APIFY_TOKEN and try again")
        return businesses


def test_enrich_contacts():
    """Test function"""
    test_businesses = [
        {
            'name': 'Example Coffee Shop',
            'location': 'San Francisco, CA',
            'website': 'https://www.bluebottlecoffee.com',
            'email': '',
            'phone': ''
        }
    ]

    enriched = enrich_business_contacts(test_businesses)

    print("\n📊 Enrichment Results:")
    for b in enriched:
        print(f"\n{b['name']}")
        print(f"  📧 Email: {b.get('email', 'Not found')}")
        print(f"  📞 Phone: {b.get('phone', 'Not found')}")
        if b.get('all_emails'):
            print(f"  📧 All emails: {', '.join(b['all_emails'])}")


if __name__ == "__main__":
    test_enrich_contacts()
