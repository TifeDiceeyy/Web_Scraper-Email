#!/usr/bin/env python3
"""
Scrape business leads from social media platforms
Uses Apify Actors for Instagram, Facebook, LinkedIn, TikTok
"""

import os
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()


def scrape_instagram_profiles(search_query, max_results=20):
    """
    Scrape Instagram profiles based on search query

    Args:
        search_query: Search term (e.g., "coffee shop san francisco")
        max_results: Maximum number of profiles to scrape

    Returns:
        list: List of Instagram profile dictionaries
    """

    print("\n📸 INSTAGRAM PROFILE SCRAPER")
    print("=" * 60)
    print(f"🔍 Searching: {search_query}")
    print(f"📊 Max results: {max_results}")

    try:
        api_token = os.getenv('APIFY_TOKEN')
        if not api_token:
            print("❌ Error: APIFY_TOKEN not found in .env file")
            return []

        client = ApifyClient(api_token)

        run_input = {
            "search": search_query,
            "resultsLimit": max_results,
            "searchType": "user",
            "searchLimit": max_results,
        }

        print("\n⏳ Running Apify Instagram Scraper...")
        run = client.actor("apify/instagram-profile-scraper").call(run_input=run_input)

        print("✅ Scraping complete! Processing profiles...")

        profiles = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            profiles.append({
                'name': item.get('fullName', ''),
                'username': item.get('username', ''),
                'bio': item.get('biography', ''),
                'website': item.get('externalUrl', ''),
                'email': item.get('businessEmail', ''),
                'phone': item.get('businessPhoneNumber', ''),
                'followers': item.get('followersCount', 0),
                'platform': 'instagram',
                'profile_url': f"https://instagram.com/{item.get('username', '')}",
            })

        print(f"\n✅ Found {len(profiles)} Instagram profiles!")
        return profiles

    except Exception as e:
        print(f"\n❌ Error scraping Instagram: {e}")
        return []


def scrape_facebook_pages(search_query, max_results=20):
    """
    Scrape Facebook business pages

    Args:
        search_query: Search term or page URLs
        max_results: Maximum number of pages to scrape

    Returns:
        list: List of Facebook page dictionaries
    """

    print("\n📘 FACEBOOK PAGE SCRAPER")
    print("=" * 60)
    print(f"🔍 Searching: {search_query}")
    print(f"📊 Max results: {max_results}")

    try:
        api_token = os.getenv('APIFY_TOKEN')
        if not api_token:
            print("❌ Error: APIFY_TOKEN not found in .env file")
            return []

        client = ApifyClient(api_token)

        run_input = {
            "startUrls": [{"url": f"https://www.facebook.com/search/pages/?q={search_query}"}],
            "maxPosts": 0,  # Don't scrape posts, just page info
        }

        print("\n⏳ Running Apify Facebook Scraper...")
        run = client.actor("apify/facebook-pages-scraper").call(run_input=run_input)

        print("✅ Scraping complete! Processing pages...")

        pages = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            if len(pages) >= max_results:
                break

            pages.append({
                'name': item.get('name', ''),
                'category': item.get('category', ''),
                'website': item.get('website', ''),
                'email': item.get('email', ''),
                'phone': item.get('phone', ''),
                'location': item.get('address', ''),
                'likes': item.get('likes', 0),
                'platform': 'facebook',
                'profile_url': item.get('url', ''),
            })

        print(f"\n✅ Found {len(pages)} Facebook pages!")
        return pages

    except Exception as e:
        print(f"\n❌ Error scraping Facebook: {e}")
        return []


def scrape_tiktok_users(search_query, max_results=20):
    """
    Scrape TikTok user profiles

    Args:
        search_query: Search keywords
        max_results: Maximum number of profiles

    Returns:
        list: List of TikTok profile dictionaries
    """

    print("\n🎵 TIKTOK USER SCRAPER")
    print("=" * 60)
    print(f"🔍 Searching: {search_query}")
    print(f"📊 Max results: {max_results}")

    try:
        api_token = os.getenv('APIFY_TOKEN')
        if not api_token:
            print("❌ Error: APIFY_TOKEN not found in .env file")
            return []

        client = ApifyClient(api_token)

        run_input = {
            "searchQueries": [search_query],
            "resultsPerPage": max_results,
            "searchSection": "users",
        }

        print("\n⏳ Running Apify TikTok Scraper...")
        run = client.actor("clockworks/tiktok-user-search-scraper").call(run_input=run_input)

        print("✅ Scraping complete! Processing profiles...")

        profiles = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            profiles.append({
                'name': item.get('nickname', ''),
                'username': item.get('uniqueId', ''),
                'bio': item.get('signature', ''),
                'followers': item.get('followerCount', 0),
                'platform': 'tiktok',
                'profile_url': f"https://tiktok.com/@{item.get('uniqueId', '')}",
            })

        print(f"\n✅ Found {len(profiles)} TikTok profiles!")
        return profiles

    except Exception as e:
        print(f"\n❌ Error scraping TikTok: {e}")
        return []


def scrape_multi_platform(business_type, location, platforms=['instagram', 'facebook'], max_per_platform=10):
    """
    Scrape leads from multiple social media platforms

    Args:
        business_type: Type of business (e.g., "coffee shop")
        location: Location (e.g., "San Francisco")
        platforms: List of platforms to scrape
        max_per_platform: Max results per platform

    Returns:
        list: Combined list of all scraped profiles
    """

    print("\n🌐 MULTI-PLATFORM LEAD SCRAPER")
    print("=" * 60)
    print(f"🔍 Business Type: {business_type}")
    print(f"📍 Location: {location}")
    print(f"📱 Platforms: {', '.join(platforms)}")

    all_leads = []
    search_query = f"{business_type} {location}"

    if 'instagram' in platforms:
        instagram_leads = scrape_instagram_profiles(search_query, max_per_platform)
        all_leads.extend(instagram_leads)

    if 'facebook' in platforms:
        facebook_leads = scrape_facebook_pages(search_query, max_per_platform)
        all_leads.extend(facebook_leads)

    if 'tiktok' in platforms:
        tiktok_leads = scrape_tiktok_users(search_query, max_per_platform)
        all_leads.extend(tiktok_leads)

    print("\n" + "=" * 60)
    print(f"✅ TOTAL LEADS FOUND: {len(all_leads)}")
    print("=" * 60)

    # Print summary by platform
    for platform in platforms:
        count = len([l for l in all_leads if l.get('platform') == platform])
        print(f"  {platform.capitalize()}: {count} leads")

    return all_leads


def test_social_scraper():
    """Test function"""

    # Test Instagram only
    leads = scrape_multi_platform(
        business_type="coffee shop",
        location="San Francisco",
        platforms=['instagram'],
        max_per_platform=3
    )

    print("\n📊 Sample Results:")
    for lead in leads[:3]:
        print(f"\n{lead.get('name', 'N/A')} (@{lead.get('username', 'N/A')})")
        print(f"  Platform: {lead.get('platform', 'N/A')}")
        print(f"  Website: {lead.get('website', 'Not provided')}")
        print(f"  Email: {lead.get('email', 'Not provided')}")


if __name__ == "__main__":
    test_social_scraper()
