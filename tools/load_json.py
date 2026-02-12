#!/usr/bin/env python3
"""
Load businesses from JSON file
"""

import json
from pathlib import Path


def load_businesses_from_json(file_path):
    """
    Load businesses from a JSON file

    Expected JSON format:
    [
        {
            "name": "Business Name",
            "email": "email@business.com",
            "phone": "(555) 123-4567",
            "website": "https://business.com",
            "location": "City, State"
        },
        ...
    ]

    Args:
        file_path: Path to JSON file

    Returns:
        list: List of business dictionaries
    """

    try:
        path = Path(file_path)

        if not path.exists():
            print(f"❌ File not found: {file_path}")
            return []

        with open(path, 'r') as f:
            data = json.load(f)

        # Validate structure
        if not isinstance(data, list):
            print("❌ JSON file must contain a list of businesses")
            return []

        # Normalize keys
        businesses = []
        for item in data:
            business = {
                'name': item.get('name', ''),
                'email': item.get('email', ''),
                'phone': item.get('phone', ''),
                'website': item.get('website', ''),
                'location': item.get('location', ''),
                'contact_person': item.get('contact_person', '')
            }
            businesses.append(business)

        return businesses

    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return []
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")
        return []


def create_sample_json():
    """Create a sample JSON file for testing"""

    sample_data = [
        {
            "name": "Smile Dental Care",
            "email": "info@smiledental.com",
            "phone": "(555) 123-4567",
            "website": "https://smiledental.com",
            "location": "123 Main St, San Francisco, CA"
        },
        {
            "name": "Healthy Teeth Dentistry",
            "email": "contact@healthyteeth.com",
            "phone": "(555) 234-5678",
            "website": "https://healthyteeth.com",
            "location": "456 Oak Ave, San Francisco, CA"
        },
        {
            "name": "Family Dental Group",
            "email": "hello@familydental.com",
            "phone": "(555) 345-6789",
            "website": "https://familydental.com",
            "location": "789 Elm St, San Francisco, CA"
        }
    ]

    sample_path = Path(__file__).parent.parent / ".tmp" / "sample_businesses.json"
    sample_path.parent.mkdir(exist_ok=True)

    with open(sample_path, 'w') as f:
        json.dump(sample_data, f, indent=2)

    print(f"✅ Sample JSON created at: {sample_path}")
    return sample_path


if __name__ == "__main__":
    # Create sample file
    sample_path = create_sample_json()

    # Test loading
    businesses = load_businesses_from_json(sample_path)
    print(f"\nLoaded {len(businesses)} businesses:")
    for b in businesses:
        print(f"  - {b['name']}")
