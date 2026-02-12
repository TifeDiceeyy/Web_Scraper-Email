#!/usr/bin/env python3
"""
Demo: Apify Enhanced Lead Generation
Shows all three enhancements:
1. Contact enrichment (find emails from websites)
2. Multi-platform scraping (Instagram, Facebook, TikTok)
3. Email verification (validate before sending)
"""

from dotenv import load_dotenv
from tools.scrape_google_maps import scrape_with_apify
from tools.scrape_social_media import scrape_multi_platform
from tools.enrich_contacts import enrich_business_contacts
from tools.verify_emails import verify_businesses

load_dotenv()


def demo_complete_workflow():
    """
    Complete demo of enhanced lead generation workflow
    """

    print("\n" + "=" * 70)
    print("🚀 APIFY ENHANCED LEAD GENERATION DEMO")
    print("=" * 70)

    # Step 1: Scrape Google Maps
    print("\n📍 STEP 1: Scrape businesses from Google Maps")
    print("-" * 70)

    businesses = scrape_with_apify(
        business_type="Coffee Shop",
        location="San Francisco, CA",
        max_results=3
    )

    print(f"\n✅ Found {len(businesses)} businesses from Google Maps")

    # Step 2: Scrape Social Media (Optional)
    print("\n" + "=" * 70)
    print("\n📱 STEP 2: Scrape social media platforms")
    print("-" * 70)

    social_leads = scrape_multi_platform(
        business_type="Coffee Shop",
        location="San Francisco",
        platforms=['instagram'],  # Just Instagram for demo
        max_per_platform=2
    )

    print(f"\n✅ Found {len(social_leads)} leads from social media")

    # Combine all leads
    all_leads = businesses + social_leads

    # Step 3: Enrich contacts (find emails from websites)
    print("\n" + "=" * 70)
    print("\n🔍 STEP 3: Enrich contacts from websites")
    print("-" * 70)

    enriched_leads = enrich_business_contacts(all_leads)

    emails_found = len([l for l in enriched_leads if l.get('email')])
    print(f"\n✅ Enriched {emails_found} businesses with email addresses")

    # Step 4: Verify emails
    print("\n" + "=" * 70)
    print("\n✉️  STEP 4: Verify email addresses")
    print("-" * 70)

    verified_leads = verify_businesses(enriched_leads, check_dns=False)

    valid_emails = len([
        l for l in verified_leads
        if l.get('email_verified') and l.get('email_verified') == True
    ])

    # Final Summary
    print("\n" + "=" * 70)
    print("📊 FINAL SUMMARY")
    print("=" * 70)
    print(f"Total leads collected: {len(all_leads)}")
    print(f"  • Google Maps: {len(businesses)}")
    print(f"  • Social Media: {len(social_leads)}")
    print(f"\nContact enrichment:")
    print(f"  • Emails found: {emails_found}")
    print(f"  • Valid emails: {valid_emails}")

    print(f"\n✅ Ready-to-contact leads: {valid_emails}")

    # Show sample leads
    print("\n" + "=" * 70)
    print("📋 SAMPLE LEADS (Ready for outreach)")
    print("=" * 70)

    ready_leads = [
        l for l in verified_leads
        if l.get('email_verified') and l.get('email')
    ]

    for i, lead in enumerate(ready_leads[:3], 1):
        print(f"\n{i}. {lead.get('name', 'N/A')}")
        print(f"   📧 Email: {lead.get('email')}")
        print(f"   🌐 Website: {lead.get('website', 'N/A')}")
        print(f"   📍 Location: {lead.get('location', 'N/A')}")
        if lead.get('platform'):
            print(f"   📱 Platform: {lead.get('platform')}")
        print(f"   ✅ Email verified: Yes")

    print("\n" + "=" * 70)
    print("✨ Demo complete! These leads are ready for your email campaign.")
    print("=" * 70)

    return verified_leads


def demo_quick_test():
    """
    Quick test of email verification only (no API calls)
    """

    print("\n🧪 QUICK TEST: Email Verification\n")

    test_businesses = [
        {
            'name': 'Blue Bottle Coffee',
            'email': 'hello@bluebottlecoffee.com',
            'website': 'https://bluebottlecoffee.com'
        },
        {
            'name': 'Invalid Email Business',
            'email': 'not-a-valid-email',
            'website': 'https://example.com'
        },
        {
            'name': 'No Email Business',
            'email': '',
            'website': 'https://example.com'
        }
    ]

    verified = verify_businesses(test_businesses, check_dns=False)

    print("\n✅ Verification complete!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        # Quick test without API calls
        demo_quick_test()
    else:
        # Full demo with API calls
        print("\n⏳ This demo will use your Apify credits.")
        print("💡 To run a quick test without API calls, use: python demo_apify_enhancements.py quick")
        print("\nPress Enter to continue or Ctrl+C to cancel...")
        input()

        demo_complete_workflow()
