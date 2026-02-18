#!/usr/bin/env python3
"""
Test script for social media scrapers
Tests Instagram, Facebook, and TikTok scrapers with small batches
"""

import sys
from pathlib import Path

# Add tools directory to path
tools_dir = Path(__file__).parent / "tools"
sys.path.insert(0, str(tools_dir))

from scrape_social_media import (
    scrape_instagram_profiles,
    scrape_facebook_pages,
    scrape_tiktok_users
)


def test_instagram():
    """Test Instagram scraper with 3 results"""
    print("\n" + "="*60)
    print("🧪 TESTING INSTAGRAM SCRAPER")
    print("="*60)

    try:
        results = scrape_instagram_profiles("coffee shop sf", max_results=3)

        print(f"\n📊 Results: {len(results)} profiles")

        if results:
            print("\n✅ Instagram scraper working!")
            print("\n📋 Sample profile:")
            profile = results[0]
            print(f"   Name: {profile.get('name', 'N/A')}")
            print(f"   Username: @{profile.get('username', 'N/A')}")
            print(f"   Followers: {profile.get('followers', 0):,}")
            print(f"   Website: {profile.get('website', 'None')}")
            print(f"   Email: {profile.get('email', 'None')}")
            return True
        else:
            print("❌ No results returned")
            return False

    except Exception as e:
        print(f"\n❌ Instagram test failed: {e}")
        return False


def test_facebook():
    """Test Facebook scraper with 3 results"""
    print("\n" + "="*60)
    print("🧪 TESTING FACEBOOK SCRAPER")
    print("="*60)

    try:
        results = scrape_facebook_pages("coffee shop sf", max_results=3)

        print(f"\n📊 Results: {len(results)} pages")

        if results:
            print("\n✅ Facebook scraper working!")
            print("\n📋 Sample page:")
            page = results[0]
            print(f"   Name: {page.get('name', 'N/A')}")
            print(f"   Category: {page.get('category', 'N/A')}")
            print(f"   Likes: {page.get('likes', 0):,}")
            print(f"   Website: {page.get('website', 'None')}")
            print(f"   Email: {page.get('email', 'None')}")
            return True
        else:
            print("❌ No results returned")
            return False

    except Exception as e:
        print(f"\n❌ Facebook test failed: {e}")
        return False


def test_tiktok():
    """Test TikTok scraper with 3 results"""
    print("\n" + "="*60)
    print("🧪 TESTING TIKTOK SCRAPER")
    print("="*60)

    try:
        results = scrape_tiktok_users("coffee shop sf", max_results=3)

        print(f"\n📊 Results: {len(results)} profiles")

        if results:
            print("\n✅ TikTok scraper working!")
            print("\n📋 Sample profile:")
            profile = results[0]
            print(f"   Name: {profile.get('name', 'N/A')}")
            print(f"   Username: @{profile.get('username', 'N/A')}")
            print(f"   Followers: {profile.get('followers', 0):,}")
            print(f"   URL: {profile.get('profile_url', 'None')}")
            return True
        else:
            print("❌ No results returned")
            return False

    except Exception as e:
        print(f"\n❌ TikTok test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 SOCIAL MEDIA SCRAPER TEST SUITE")
    print("="*60)
    print("\nThis will test all 3 scrapers with small batches (3 results each)")
    print("Estimated time: 2-3 minutes")
    print("\n" + "="*60)

    input("\nPress Enter to start testing...")

    results = {
        'Instagram': test_instagram(),
        'Facebook': test_facebook(),
        'TikTok': test_tiktok()
    }

    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)

    for platform, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{platform}: {status}")

    total_passed = sum(results.values())
    total_tests = len(results)

    print(f"\nTotal: {total_passed}/{total_tests} tests passed")

    if total_passed == total_tests:
        print("\n🎉 All tests passed! Social media scrapers are working!")
    else:
        print(f"\n⚠️  {total_tests - total_passed} test(s) failed")
        print("Check error messages above for details")

    print("\n" + "="*60)


if __name__ == "__main__":
    main()
