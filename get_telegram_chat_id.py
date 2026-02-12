#!/usr/bin/env python3
"""
Get Telegram Chat ID Helper
Run this after messaging your bot to get your chat ID
"""

import sys
import requests

def get_chat_id(bot_token):
    """Get chat ID from Telegram bot"""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return None

        data = response.json()

        if not data.get('ok'):
            print(f"❌ Error: {data.get('description', 'Unknown error')}")
            return None

        results = data.get('result', [])

        if not results:
            print("❌ No messages found!")
            print("")
            print("Make sure you:")
            print("  1. Opened your bot in Telegram")
            print("  2. Clicked 'Start' or sent a message")
            print("  3. Then run this script again")
            return None

        # Get the most recent message
        latest_message = results[-1]
        chat_id = latest_message.get('message', {}).get('chat', {}).get('id')

        if chat_id:
            print("✅ SUCCESS!")
            print("")
            print(f"Your Chat ID: {chat_id}")
            print("")
            print("Copy this number and add it to your .env file:")
            print(f"TELEGRAM_CHAT_ID={chat_id}")
            return chat_id
        else:
            print("❌ Could not find chat ID in response")
            print(f"Response: {data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    print("")
    print("="*60)
    print("📱 TELEGRAM CHAT ID FINDER")
    print("="*60)
    print("")

    if len(sys.argv) > 1:
        bot_token = sys.argv[1]
    else:
        bot_token = input("Paste your Bot Token: ").strip()

    if not bot_token:
        print("❌ No token provided!")
        sys.exit(1)

    print("")
    print("Fetching chat ID...")
    print("")

    chat_id = get_chat_id(bot_token)

    if chat_id:
        print("")
        print("="*60)
        print("")
        sys.exit(0)
    else:
        sys.exit(1)
