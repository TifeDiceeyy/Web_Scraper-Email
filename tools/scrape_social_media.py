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
    Scrape Instagram profiles based on hashtag search

    Note: Instagram doesn't have a direct profile search API.
    This function searches for posts by hashtag and extracts profile info from posters.

    Args:
        search_query: Search term (e.g., "coffeesf" or "sanfranciscocoffee")
                     Will be converted to hashtag format
        max_results: Maximum number of posts to scrape (profiles extracted from these)

    Returns:
        list: List of Instagram profile dictionaries
    """

    print("\n📸 INSTAGRAM PROFILE SCRAPER (Hashtag-based)")
    print("=" * 60)
    print(f"🔍 Searching hashtag: #{search_query.replace(' ', '')}")
    print(f"📊 Max posts to scrape: {max_results}")
    print("⚠️  Note: Extracts profiles from hashtag posts")

    try:
        api_token = os.getenv('APIFY_TOKEN')
        if not api_token:
            print("❌ Error: APIFY_TOKEN not found in .env file")
            return []

        client = ApifyClient(api_token)

        # Convert search query to hashtag format
        hashtag = search_query.replace(" ", "").lower()

        run_input = {
            "hashtags": [hashtag],
            "resultsLimit": max_results,
        }

        print(f"\n⏳ Running Apify Instagram Hashtag Scraper for #{hashtag}...")
        run = client.actor("apify/instagram-hashtag-scraper").call(run_input=run_input)

        print("✅ Scraping complete! Extracting unique profiles...")

        # Extract unique profiles from posts
        seen_usernames = set()
        profiles = []

        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            username = item.get('ownerUsername', '')

            # Skip duplicates
            if username in seen_usernames or not username:
                continue

            seen_usernames.add(username)

            profiles.append({
                'name': item.get('ownerFullName', ''),
                'username': username,
                'bio': '',  # Not available in hashtag scraper
                'website': '',  # Not available in hashtag scraper
                'email': '',  # Not available in hashtag scraper
                'phone': '',  # Not available in hashtag scraper
                'followers': 0,  # Not available in hashtag scraper
                'platform': 'instagram',
                'profile_url': f"https://instagram.com/{username}",
                'post_caption': item.get('caption', '')[:100],  # First 100 chars of their post
            })

            if len(profiles) >= max_results:
                break

        print(f"\n✅ Found {len(profiles)} unique Instagram profiles!")
        print(f"💡 Tip: Use 'Enrich Contact Info' to get full profile details")
        return profiles

    except Exception as e:
        print(f"\n❌ Error scraping Instagram: {e}")
        print("💡 Try: Using a single-word hashtag like 'coffee' or 'coffeeshop'")
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
