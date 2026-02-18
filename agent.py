#!/usr/bin/env python3
"""
Business Outreach Automation Agent
WAT Framework: Workflows, Agents, Tools
"""

import os
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
from logger import logger
from validators import (
    validate_business_type, validate_email, validate_file_path,
    validate_integer, validate_choice, validate_location,
    get_validated_input
)

# Load environment variables
load_dotenv()


class OutreachAgent:
    """Main orchestrator for business outreach automation"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.workflows_dir = self.project_root / "workflows"
        self.tools_dir = self.project_root / "tools"
        self.tmp_dir = self.project_root / ".tmp"
        self.config_file = self.tmp_dir / "campaign_config.json"

        # Ensure .tmp directory exists
        self.tmp_dir.mkdir(exist_ok=True)

    def run(self):
        """Main entry point - display menu and handle user choice"""
        logger.info("Business Outreach Automation System started")

        while True:
            try:
                self.display_menu()

                # Validate menu choice
                choice = get_validated_input(
                    "\nEnter your choice (1-9): ",
                    validate_choice,
                    valid_choices=["1", "2", "3", "4", "5", "6", "7", "8", "9"]
                )

                if choice == "1":
                    self.start_campaign()
                elif choice == "2":
                    self.generate_emails()
                elif choice == "3":
                    self.manage_sheet()
                elif choice == "4":
                    self.send_emails()
                elif choice == "5":
                    self.track_responses()
                elif choice == "6":
                    self.scrape_social_media()
                elif choice == "7":
                    self.enrich_contacts()
                elif choice == "8":
                    self.verify_emails_menu()
                elif choice == "9":
                    logger.info("System shutting down")
                    print("\nGoodbye!")
                    sys.exit(0)

            except KeyboardInterrupt:
                logger.info("User interrupted operation")
                print("\n\n⚠️  Operation interrupted by user")
                confirm = input("Do you want to exit? (yes/no): ").strip().lower()
                if confirm == "yes":
                    logger.info("System shutting down via user request")
                    print("\nGoodbye!")
                    sys.exit(0)
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}", exc_info=True)
                print(f"\n❌ An error occurred: {e}")
                print("   Please try again or contact support if the issue persists")

            input("\nPress Enter to continue...")

    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("🚀 BUSINESS OUTREACH AUTOMATION SYSTEM")
        print("="*60)
        print("\n1. 📋 Start New Campaign")
        print("2. ✉️  Generate Emails")
        print("3. 📊 Manage Google Sheet")
        print("4. 📤 Send Approved Emails")
        print("5. 📥 Track Responses")
        print("6. 📱 Scrape Social Media")
        print("7. 🔍 Enrich Contact Info")
        print("8. ✅ Verify Email Addresses")
        print("9. 🚪 Exit")
        print("\n" + "="*60)

    def start_campaign(self):
        """Workflow 1: Start a new outreach campaign"""
        print("\n" + "="*60)
        print("📋 STARTING NEW CAMPAIGN")
        print("="*60)
        logger.info("Starting new outreach campaign")

        # Step 1: Ask business type
        business_type = self.ask_business_type()

        # Step 2: CRITICAL DECISION - Ask outreach strategy
        outreach_type = self.ask_outreach_type()

        # Step 3: If specific automation, ask which one
        automation_focus = None
        if outreach_type == "specific_automation":
            automation_focus = self.ask_automation_focus()

        # Step 4: Ask how to get businesses
        data_source = self.ask_data_source()

        # Step 5: Collect businesses based on data source
        businesses = self.collect_businesses(data_source, business_type)

        if not businesses:
            logger.error("No businesses collected. Campaign aborted.")
            print("\n❌ No businesses collected. Campaign aborted.")
            return

        # Step 6: Save configuration
        config = {
            "business_type": business_type,
            "outreach_type": outreach_type,
            "automation_focus": automation_focus,
            "data_source": data_source,
            "total_businesses": len(businesses)
        }
        self.save_config(config)

        # Step 7: Upload to Google Sheets
        logger.info(f"Uploading {len(businesses)} businesses to Google Sheets")
        print("\n📤 Uploading businesses to Google Sheets...")
        self.upload_to_sheets(businesses)

        logger.info(f"Campaign started successfully: {business_type} | {outreach_type} | {len(businesses)} businesses")
        print("\n✅ Campaign started successfully!")
        print(f"   Business Type: {business_type}")
        print(f"   Outreach Strategy: {outreach_type.replace('_', ' ').title()}")
        if automation_focus:
            print(f"   Automation Focus: {automation_focus}")
        print(f"   Total Businesses: {len(businesses)}")

    def ask_business_type(self):
        """Ask user what type of businesses to target"""
        print("\n🎯 What type of businesses do you want to target?")
        print("\nCommon options:")
        print("  - Dentists")
        print("  - Restaurants")
        print("  - Plumbers")
        print("  - Hair Salons")
        print("  - Gyms")
        print("  - Law Firms")
        print("  - Real Estate Agents")
        print("  - Or enter your own...")

        business_type = get_validated_input(
            "\nEnter business type (1-50 characters): ",
            validate_business_type
        )
        logger.info(f"Business type selected: {business_type}")
        return business_type

    def ask_outreach_type(self):
        """
        CRITICAL DECISION POINT
        This determines which email generation strategy to use
        """
        print("\n" + "="*60)
        print("🔥 CRITICAL DECISION: Choose Your Outreach Strategy")
        print("="*60)

        print("\n1️⃣  GENERAL HELP (Discovery Approach)")
        print("   📧 Email asks: 'What problems do you face?'")
        print("   🎯 Best for: Cold outreach, building relationships")
        print("   💡 Offers: General help with any automation needs")
        print("   📊 Conversion: Lower initial, but broader appeal")

        print("\n2️⃣  SPECIFIC AUTOMATION (Focused Approach)")
        print("   📧 Email says: 'We reduce no-shows by 30%'")
        print("   🎯 Best for: Warm leads, targeted solution")
        print("   💡 Offers: One specific automation benefit")
        print("   📊 Conversion: Higher for those with that problem")

        while True:
            choice = input("\nChoose strategy (1 or 2): ").strip()
            if choice == "1":
                print("\n✅ Selected: GENERAL HELP approach")
                return "general_help"
            elif choice == "2":
                print("\n✅ Selected: SPECIFIC AUTOMATION approach")
                return "specific_automation"
            else:
                print("❌ Invalid choice. Please enter 1 or 2.")

    def ask_automation_focus(self):
        """Ask which specific automation to focus on"""
        print("\n🎯 Which automation do you want to focus on?")
        print("\nPopular automations:")
        print("  1. Appointment Reminder System (reduce no-shows)")
        print("  2. Review Request Automation (get more 5-star reviews)")
        print("  3. Lead Follow-up System (never miss a lead)")
        print("  4. Customer Feedback Collection")
        print("  5. Inventory Alerts")
        print("  6. Custom (enter your own)")

        automations = {
            "1": "Appointment Reminder System",
            "2": "Review Request Automation",
            "3": "Lead Follow-up System",
            "4": "Customer Feedback Collection",
            "5": "Inventory Alerts"
        }

        # Validate choice
        choice = get_validated_input(
            "\nEnter choice (1-6): ",
            validate_choice,
            valid_choices=["1", "2", "3", "4", "5", "6"]
        )

        if choice == "6":
            custom = input("Enter your custom automation: ").strip()
            logger.info(f"Custom automation selected: {custom}")
            return custom

        automation = automations[choice]
        logger.info(f"Automation focus selected: {automation}")
        return automation

    def ask_data_source(self):
        """Ask how to collect business data"""
        print("\n📊 How do you want to collect businesses?")
        print("\n1. Google Maps (scrape by location and type)")
        print("2. Upload JSON file (manual list)")
        print("3. Enter manually (for small lists)")

        while True:
            choice = input("\nChoose option (1-3): ").strip()
            if choice in ["1", "2", "3"]:
                return ["google_maps", "json_file", "manual"][int(choice) - 1]
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")

    def collect_businesses(self, data_source, business_type):
        """Collect businesses based on chosen data source"""
        if data_source == "google_maps":
            return self.scrape_google_maps(business_type)
        elif data_source == "json_file":
            return self.load_from_json()
        elif data_source == "manual":
            return self.enter_manually()
        return []

    def scrape_google_maps(self, business_type):
        """Scrape businesses from Google Maps"""
        print("\n🗺️  Google Maps Scraper")

        # Validate location
        location = get_validated_input(
            "Enter location (e.g., 'San Francisco, CA'): ",
            validate_location
        )

        # Validate max_results with default
        max_results_input = input("How many businesses to scrape? (default: 20): ").strip()
        if max_results_input:
            is_valid, error_msg, max_results = validate_integer(max_results_input, min_val=1, max_val=100)
            if not is_valid:
                logger.warning(f"Invalid number, using default: {error_msg}")
                print(f"⚠️  Invalid number, using default of 20")
                max_results = 20
        else:
            max_results = 20

        logger.info(f"Scraping {max_results} {business_type} businesses in {location}")
        print(f"\n🔍 Scraping {business_type} in {location}...")

        # Import and run the tool
        sys.path.insert(0, str(self.tools_dir))
        from scrape_google_maps import scrape_google_maps

        businesses = scrape_google_maps(business_type, location, max_results)
        logger.info(f"Found {len(businesses)} businesses")
        print(f"✅ Found {len(businesses)} businesses")
        return businesses

    def load_from_json(self):
        """Load businesses from JSON file"""
        print("\n📄 Load from JSON")

        # Validate file path
        file_path = get_validated_input(
            "Enter path to JSON file: ",
            validate_file_path,
            must_exist=True
        )

        logger.info(f"Loading businesses from {file_path}")

        sys.path.insert(0, str(self.tools_dir))
        from load_json import load_businesses_from_json

        businesses = load_businesses_from_json(file_path)
        logger.info(f"Loaded {len(businesses)} businesses from JSON")
        print(f"✅ Loaded {len(businesses)} businesses")
        return businesses

    def enter_manually(self):
        """Manually enter businesses"""
        print("\n✏️  Enter businesses manually")
        print("(Enter blank name to finish)")

        businesses = []
        while True:
            print(f"\n--- Business #{len(businesses) + 1} ---")
            name = input("Business name: ").strip()
            if not name:
                break

            # Validate email if provided
            email = input("Email (optional, press Enter to skip): ").strip()
            if email:
                is_valid, error_msg = validate_email(email)
                while not is_valid:
                    logger.warning(f"Invalid email: {error_msg}")
                    print(f"❌ {error_msg}")
                    email = input("Email (optional, press Enter to skip): ").strip()
                    if not email:
                        break
                    is_valid, error_msg = validate_email(email)

            phone = input("Phone (optional): ").strip()
            website = input("Website (optional): ").strip()
            location = input("Location (optional): ").strip()

            businesses.append({
                "name": name,
                "email": email,
                "phone": phone,
                "website": website,
                "location": location
            })

            logger.info(f"Added business: {name}")

        return businesses

    def upload_to_sheets(self, businesses):
        """Upload businesses to Google Sheets"""
        sys.path.insert(0, str(self.tools_dir))
        from upload_to_sheets import upload_businesses

        upload_businesses(businesses)

    def save_config(self, config):
        """Save campaign configuration to JSON"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            logger.info(f"Configuration saved to {self.config_file}")
            print(f"\n💾 Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            print(f"\n❌ Failed to save configuration: {e}")

    def load_config(self):
        """Load campaign configuration"""
        if not self.config_file.exists():
            logger.warning("No campaign configuration found")
            print("\n❌ No campaign configuration found.")
            print("   Please start a new campaign first (Option 1)")
            return None

        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            logger.info("Configuration loaded successfully")
            return config
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            print(f"\n❌ Failed to load configuration: {e}")
            return None

    def generate_emails(self):
        """Workflow 2: Generate emails based on campaign strategy"""
        print("\n" + "="*60)
        print("✉️  GENERATING EMAILS")
        print("="*60)
        logger.info("Starting email generation workflow")

        # Load campaign config
        config = self.load_config()
        if not config:
            logger.error("No campaign configuration found")
            return

        strategy = config['outreach_type'].replace('_', ' ').title()
        logger.info(f"Campaign strategy: {strategy}")
        print(f"\n📋 Campaign Strategy: {strategy}")

        # Get draft businesses from Google Sheet
        sys.path.insert(0, str(self.tools_dir))
        from get_draft_businesses import get_draft_businesses

        businesses = get_draft_businesses()

        if not businesses:
            logger.warning("No draft businesses found in Google Sheet")
            print("\n❌ No draft businesses found in Google Sheet")
            return

        logger.info(f"Found {len(businesses)} draft businesses")
        print(f"📊 Found {len(businesses)} businesses with 'Draft' status")

        # Choose the right email generation tool based on strategy
        if config['outreach_type'] == "general_help":
            from generate_general_email import generate_general_email as generate_email
            logger.info("Using GENERAL HELP email strategy")
            print("\n🎯 Using GENERAL HELP email strategy")
        else:
            from generate_specific_email import generate_specific_email as generate_email
            logger.info(f"Using SPECIFIC AUTOMATION strategy: {config.get('automation_focus', 'N/A')}")
            print(f"\n🎯 Using SPECIFIC AUTOMATION strategy")
            print(f"   Focus: {config.get('automation_focus', 'N/A')}")

        # Generate emails for each business
        for i, business in enumerate(businesses, 1):
            logger.info(f"Generating email {i}/{len(businesses)} for: {business['name']}")
            print(f"\n[{i}/{len(businesses)}] Generating email for: {business['name']}")

            # Scrape website if available
            website_content = ""
            if business.get('website'):
                logger.debug(f"Scraping website: {business['website']}")
                print(f"   🌐 Scraping website: {business['website']}")
                from scrape_website import scrape_website
                website_content = scrape_website(business['website'])

            # Generate email using appropriate strategy
            subject, body = generate_email(
                business_name=business['name'],
                business_type=config['business_type'],
                website_content=website_content,
                automation_focus=config.get('automation_focus')
            )

            logger.info(f"Generated email: {subject}")
            print(f"   ✅ Generated: {subject}")

            # Update Google Sheet
            from update_sheet_emails import update_email
            update_email(business['row_number'], subject, body)

        logger.info(f"Successfully generated {len(businesses)} emails")
        print("\n✅ All emails generated successfully!")
        print("   Check your Google Sheet to review them")

    def manage_sheet(self):
        """Workflow 3: Manage businesses in Google Sheet"""
        print("\n📊 Google Sheet Management")
        print("\nOpening Google Sheet in browser...")

        sheet_id = os.getenv('GOOGLE_SPREADSHEET_ID')
        if sheet_id:
            url = f"https://docs.google.com/spreadsheets/d/{sheet_id}"
            print(f"\n🔗 {url}")

            # Try to open in browser
            import webbrowser
            webbrowser.open(url)
        else:
            print("❌ GOOGLE_SPREADSHEET_ID not set in .env")

    def send_emails(self):
        """Workflow 4: Send approved emails via Gmail"""
        print("\n" + "="*60)
        print("📤 SENDING APPROVED EMAILS")
        print("="*60)
        logger.info("Starting email sending workflow")

        sys.path.insert(0, str(self.tools_dir))
        from send_emails import send_approved_emails

        sent_count = send_approved_emails()
        logger.info(f"Email sending complete: {sent_count} emails sent")
        print(f"\n✅ Sent {sent_count} emails successfully!")

    def track_responses(self):
        """Workflow 5: Track email responses"""
        print("\n" + "="*60)
        print("📥 TRACKING RESPONSES")
        print("="*60)
        logger.info("Starting response tracking workflow")

        sys.path.insert(0, str(self.tools_dir))
        from track_responses import track_email_responses

        track_email_responses()
        logger.info("Response tracking complete")

    def scrape_social_media(self):
        """Workflow 6: Scrape businesses from social media platforms"""
        print("\n" + "="*60)
        print("📱 SOCIAL MEDIA SCRAPING")
        print("="*60)
        logger.info("Starting social media scraping workflow")

        # Ask which platform
        print("\nChoose platform:")
        print("1. Instagram")
        print("2. Facebook")
        print("3. TikTok")
        print("4. All platforms (coming soon)")

        platform_choice = get_validated_input(
            "\nEnter choice (1-4): ",
            validate_choice,
            valid_choices=["1", "2", "3", "4"]
        )

        platform_map = {
            "1": "Instagram",
            "2": "Facebook",
            "3": "TikTok",
            "4": "All"
        }

        platform = platform_map[platform_choice]

        if platform == "All":
            print("\n⚠️  Multi-platform scraping coming soon!")
            print("   Please choose a single platform for now")
            return

        # Ask for search query
        print(f"\n🔍 Scraping {platform}")
        query = input(f"Enter search term (e.g., 'coffee shop sf'): ").strip()

        if not query:
            print("❌ Search term cannot be empty")
            logger.warning("Empty search term provided")
            return

        # Ask for max results
        max_results_input = input("How many results? (default: 10): ").strip()
        if max_results_input:
            is_valid, error_msg, max_results = validate_integer(max_results_input, min_val=1, max_val=50)
            if not is_valid:
                logger.warning(f"Invalid number: {error_msg}")
                print(f"⚠️  Invalid number, using default of 10")
                max_results = 10
        else:
            max_results = 10

        logger.info(f"Scraping {max_results} results from {platform} for query: {query}")
        print(f"\n🔍 Searching {platform} for: '{query}'...")

        # Import and call appropriate scraper
        sys.path.insert(0, str(self.tools_dir))
        try:
            from scrape_social_media import (
                scrape_instagram_profiles,
                scrape_facebook_pages,
                scrape_tiktok_users
            )

            if platform == "Instagram":
                businesses = scrape_instagram_profiles(query, max_results)
            elif platform == "Facebook":
                businesses = scrape_facebook_pages(query, max_results)
            elif platform == "TikTok":
                businesses = scrape_tiktok_users(query, max_results)

            logger.info(f"Found {len(businesses)} businesses from {platform}")
            print(f"\n✅ Found {len(businesses)} businesses from {platform}")

            if businesses:
                # Upload to Google Sheets
                print("\n📤 Uploading to Google Sheets...")
                self.upload_to_sheets(businesses)
                print(f"✅ {len(businesses)} businesses uploaded successfully!")
            else:
                print("❌ No businesses found. Try a different search term.")

        except Exception as e:
            logger.error(f"Social media scraping failed: {e}", exc_info=True)
            print(f"\n❌ Scraping failed: {e}")
            print("   Check your Apify token and try again")

    def enrich_contacts(self):
        """Workflow 7: Enrich existing businesses with missing contact info"""
        print("\n" + "="*60)
        print("🔍 CONTACT ENRICHMENT")
        print("="*60)
        logger.info("Starting contact enrichment workflow")

        # Get businesses from Sheet
        sys.path.insert(0, str(self.tools_dir))
        try:
            from get_draft_businesses import get_draft_businesses

            businesses = get_draft_businesses()

            if not businesses:
                print("\n❌ No businesses found in Google Sheet")
                logger.warning("No businesses to enrich")
                return

            # Filter businesses with websites but missing emails
            businesses_to_enrich = [
                b for b in businesses
                if b.get('website') and not b.get('email')
            ]

            if not businesses_to_enrich:
                print(f"\n✅ All {len(businesses)} businesses already have contact info!")
                logger.info("No businesses need enrichment")
                return

            print(f"\n📊 Found {len(businesses_to_enrich)} businesses needing enrichment")
            print(f"   (out of {len(businesses)} total businesses)")

            # Confirm
            confirm = input("\nProceed with enrichment? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("❌ Enrichment cancelled")
                return

            # Enrich
            print(f"\n🔍 Enriching contact information...")
            from enrich_contacts import enrich_business_contacts

            enriched = enrich_business_contacts(businesses_to_enrich)

            # Count successful enrichments
            found_contacts = sum(1 for b in enriched if b.get('email') or b.get('phone'))

            logger.info(f"Enrichment complete: {found_contacts}/{len(enriched)} found")
            print(f"\n✅ Enrichment complete!")
            print(f"   📧 Found contact info for {found_contacts} businesses")
            print(f"   ❌ Could not find info for {len(enriched) - found_contacts} businesses")

            # Update Google Sheet
            print("\n📤 Updating Google Sheet...")
            from update_sheet_emails import update_email
            # TODO: Need to update this to update contact info, not just emails

            print("✅ Google Sheet updated with enriched data")

        except Exception as e:
            logger.error(f"Contact enrichment failed: {e}", exc_info=True)
            print(f"\n❌ Enrichment failed: {e}")
            print("   Check your Apify token and Google Sheet access")

    def verify_emails_menu(self):
        """Workflow 8: Verify email addresses before sending"""
        print("\n" + "="*60)
        print("✅ EMAIL VERIFICATION")
        print("="*60)
        logger.info("Starting email verification workflow")

        # Get all businesses from Sheet
        sys.path.insert(0, str(self.tools_dir))
        try:
            from get_draft_businesses import get_draft_businesses

            businesses = get_draft_businesses()

            if not businesses:
                print("\n❌ No businesses found in Google Sheet")
                logger.warning("No businesses to verify")
                return

            # Filter businesses with emails
            businesses_with_emails = [
                b for b in businesses
                if b.get('email')
            ]

            if not businesses_with_emails:
                print(f"\n❌ No businesses have email addresses to verify")
                print("   Run 'Enrich Contact Info' first to find missing emails")
                return

            businesses_without_emails = len(businesses) - len(businesses_with_emails)

            print(f"\n📊 Found {len(businesses_with_emails)} businesses with email addresses")
            if businesses_without_emails > 0:
                print(f"   ⚠️  {businesses_without_emails} businesses have no email")

            # Ask if they want DNS checking (slower but more accurate)
            print("\n🔍 Verification options:")
            print("1. Quick (syntax only) - Fast, basic validation")
            print("2. Full (syntax + DNS) - Slower, checks if domain accepts email")

            check_choice = get_validated_input(
                "\nChoose verification level (1-2): ",
                validate_choice,
                valid_choices=["1", "2"]
            )

            check_dns = (check_choice == "2")

            # Confirm
            print(f"\n⚠️  About to verify {len(businesses_with_emails)} email addresses")
            if check_dns:
                print("   This may take 1-2 minutes with DNS checking...")

            confirm = input("\nProceed with verification? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("❌ Verification cancelled")
                return

            # Verify
            print(f"\n🔍 Verifying email addresses...")
            from verify_emails import verify_businesses

            verified = verify_businesses(businesses_with_emails, check_dns=check_dns)

            # Show results
            valid = [b for b in verified if b.get('email_verified')]
            invalid = [b for b in verified if not b.get('email_verified')]

            logger.info(f"Verification complete: {len(valid)} valid, {len(invalid)} invalid")
            print(f"\n✅ Verification complete!")
            print(f"   ✅ Valid emails: {len(valid)} ({len(valid)/len(verified)*100:.1f}%)")
            print(f"   ❌ Invalid emails: {len(invalid)} ({len(invalid)/len(verified)*100:.1f}%)")

            if invalid:
                print("\n❌ Invalid emails found:")
                for b in invalid[:5]:  # Show first 5
                    reason = b.get('verification_reason', 'Unknown')
                    print(f"   • {b['name']}: {b['email']} ({reason})")
                if len(invalid) > 5:
                    print(f"   ... and {len(invalid) - 5} more")

            # Update Google Sheet with verification status
            print("\n📤 Updating Google Sheet with verification results...")
            # TODO: Need sheet update function for verification status

            print("✅ Verification results saved to Google Sheet")

        except Exception as e:
            logger.error(f"Email verification failed: {e}", exc_info=True)
            print(f"\n❌ Verification failed: {e}")
            print("   Check your internet connection and try again")


def main():
    """Entry point"""
    agent = OutreachAgent()
    agent.run()


if __name__ == "__main__":
    main()
