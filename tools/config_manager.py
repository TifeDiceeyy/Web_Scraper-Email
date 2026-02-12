#!/usr/bin/env python3
"""
Campaign Configuration Manager
Handles reading/writing campaign_config.json
"""

import json
import os
from pathlib import Path
from datetime import datetime


class ConfigManager:
    """Manages campaign configuration"""

    def __init__(self, config_dir=None):
        """
        Initialize config manager

        Args:
            config_dir: Path to .tmp directory (default: project_root/.tmp)
        """
        if config_dir is None:
            project_root = Path(__file__).parent.parent
            config_dir = project_root / ".tmp"

        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / "campaign_config.json"

        # Ensure .tmp directory exists
        self.config_dir.mkdir(exist_ok=True)

    def save_config(self, config):
        """
        Save campaign configuration

        Args:
            config: dict with campaign settings
                - business_type: str
                - outreach_type: str (general_help or specific_automation)
                - automation_focus: str (optional)
                - data_source: str
                - total_businesses: int (optional)

        Returns:
            bool - True if saved successfully
        """
        try:
            # Add timestamp
            config['created_at'] = datetime.now().isoformat()
            config['updated_at'] = datetime.now().isoformat()

            # Add sheet ID if in environment
            if 'sheet_id' not in config:
                sheet_id = os.getenv("GOOGLE_SPREADSHEET_ID")
                if sheet_id:
                    config['sheet_id'] = sheet_id

            # Write to file
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)

            print(f"✅ Configuration saved to {self.config_file}")
            return True

        except Exception as e:
            print(f"❌ Failed to save configuration: {e}")
            return False

    def load_config(self):
        """
        Load campaign configuration

        Returns:
            dict - Campaign configuration, or None if not found

        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file is invalid
        """
        if not self.config_file.exists():
            raise FileNotFoundError(
                f"No campaign configuration found at {self.config_file}. "
                "Please start a new campaign first."
            )

        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)

            return config

        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in configuration file: {e}",
                e.doc,
                e.pos
            )

    def update_config(self, updates):
        """
        Update specific fields in campaign configuration

        Args:
            updates: dict with fields to update

        Returns:
            bool - True if updated successfully
        """
        try:
            # Load existing config
            config = self.load_config()

            # Update fields
            config.update(updates)
            config['updated_at'] = datetime.now().isoformat()

            # Save
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)

            print(f"✅ Configuration updated")
            return True

        except Exception as e:
            print(f"❌ Failed to update configuration: {e}")
            return False

    def get_outreach_type(self):
        """
        Get the outreach strategy from config

        Returns:
            str - "general_help" or "specific_automation"

        Raises:
            FileNotFoundError: If no config exists
        """
        config = self.load_config()
        return config.get('outreach_type')

    def get_automation_focus(self):
        """
        Get the automation focus from config (if specific_automation)

        Returns:
            str or None - Automation focus name
        """
        config = self.load_config()
        return config.get('automation_focus')

    def get_business_type(self):
        """
        Get the business type from config

        Returns:
            str - Business type (e.g., "Dentists")
        """
        config = self.load_config()
        return config.get('business_type')

    def config_exists(self):
        """
        Check if campaign configuration exists

        Returns:
            bool - True if config file exists
        """
        return self.config_file.exists()

    def delete_config(self):
        """
        Delete campaign configuration

        Returns:
            bool - True if deleted successfully
        """
        try:
            if self.config_file.exists():
                self.config_file.unlink()
                print(f"✅ Configuration deleted")
                return True
            else:
                print(f"⚠️  No configuration to delete")
                return False

        except Exception as e:
            print(f"❌ Failed to delete configuration: {e}")
            return False

    def print_config(self):
        """Print current configuration in readable format"""
        try:
            config = self.load_config()

            print("\n" + "="*60)
            print("CURRENT CAMPAIGN CONFIGURATION")
            print("="*60)
            print(f"\nBusiness Type: {config.get('business_type', 'N/A')}")
            print(f"Outreach Strategy: {config.get('outreach_type', 'N/A').replace('_', ' ').title()}")

            if config.get('automation_focus'):
                print(f"Automation Focus: {config.get('automation_focus')}")

            print(f"Data Source: {config.get('data_source', 'N/A').replace('_', ' ').title()}")

            if config.get('total_businesses'):
                print(f"Total Businesses: {config.get('total_businesses')}")

            if config.get('created_at'):
                print(f"\nCreated: {config.get('created_at')}")

            if config.get('updated_at'):
                print(f"Last Updated: {config.get('updated_at')}")

            print("="*60 + "\n")

        except FileNotFoundError:
            print("\n⚠️  No active campaign found. Start a new campaign first.\n")
        except Exception as e:
            print(f"\n❌ Error reading configuration: {e}\n")


def test_config_manager():
    """Test the configuration manager"""
    print("="*60)
    print("CONFIG MANAGER TEST")
    print("="*60)

    manager = ConfigManager()

    # Test 1: Save config
    print("\n1️⃣  Testing save_config()...")
    test_config = {
        "business_type": "Dentists",
        "outreach_type": "general_help",
        "automation_focus": None,
        "data_source": "manual",
        "total_businesses": 5
    }
    manager.save_config(test_config)

    # Test 2: Load config
    print("\n2️⃣  Testing load_config()...")
    loaded = manager.load_config()
    print(f"Loaded: {json.dumps(loaded, indent=2)}")

    # Test 3: Update config
    print("\n3️⃣  Testing update_config()...")
    manager.update_config({"total_businesses": 10})

    # Test 4: Get specific fields
    print("\n4️⃣  Testing getter methods...")
    print(f"Outreach Type: {manager.get_outreach_type()}")
    print(f"Business Type: {manager.get_business_type()}")
    print(f"Automation Focus: {manager.get_automation_focus()}")

    # Test 5: Print config
    print("\n5️⃣  Testing print_config()...")
    manager.print_config()

    # Test 6: Config exists
    print("6️⃣  Testing config_exists()...")
    print(f"Config exists: {manager.config_exists()}")

    print("\n✅ All tests completed!")


if __name__ == "__main__":
    test_config_manager()
