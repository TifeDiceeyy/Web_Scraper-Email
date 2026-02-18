#!/usr/bin/env python3
"""
Automatic Telegram Chat ID Finder
No interaction needed - just fetches your chat ID
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_telegram_chat_id_auto():
    """Automatically get your Telegram Chat ID"""

    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

    if not bot_token or bot_token == 'your-telegram-bot-token-here':
        print("❌ TELEGRAM_BOT_TOKEN not set in .env file")
        return None

    print("="*60)
    print("📱 TELEGRAM CHAT ID FINDER (AUTO MODE)")
    print("="*60)
    print(f"\n✅ Using bot token: {bot_token[:20]}...\n")

    # Call Telegram API to get updates
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"

    print("🔍 Fetching updates from Telegram API...")
    print(f"🔗 URL: {url}\n")

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if not data.get('ok'):
            print(f"❌ Error from Telegram API: {data.get('description', 'Unknown error')}")
            print("\n💡 Common issues:")
            print("   - Invalid bot token")
            print("   - Bot was deleted or deactivated")
            return None

        updates = data.get('result', [])

        if not updates:
            print("❌ No messages found in bot history!")
            print("\n📝 TO FIX THIS:")
            print("   1. Open Telegram on your phone/computer")
            print("   2. Search for your bot")
            print("   3. Send ANY message (e.g., 'hi' or '/start')")
            print("   4. Run this script again\n")
            print("🔗 Or visit this URL in your browser:")
            print(f"   {url}\n")
            return None

        # Get the most recent chat ID
        print(f"✅ Found {len(updates)} message(s) in bot history\n")

        latest_update = updates[-1]
        chat = latest_update['message']['chat']
        chat_id = chat['id']
        chat_type = chat['type']

        username = chat.get('username', chat.get('first_name', chat.get('title', 'Unknown')))

        print("="*60)
        print("✅ SUCCESS! Found your Chat ID:")
        print("="*60)
        print(f"\n📱 Chat ID: {chat_id}")
        print(f"👤 Name/Username: {username}")
        print(f"💬 Chat Type: {chat_type}")
        print("\n" + "="*60)

        # Show recent messages
        print("\n📝 Recent messages (last 5):")
        for i, update in enumerate(updates[-5:], 1):
            msg = update['message']
            text = msg.get('text', msg.get('caption', '[Media/Sticker]'))
            from_user = msg['from'].get('username') or msg['from'].get('first_name', 'Unknown')
            msg_chat_id = msg['chat']['id']
            print(f"   {i}. [{msg_chat_id}] @{from_user}: {text[:50]}")

        print("\n" + "="*60)
        print("\n💾 Your Chat ID is:")
        print(f"\n   TELEGRAM_CHAT_ID={chat_id}")
        print("\n" + "="*60)

        return chat_id

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        print("\n🔗 Try visiting this URL in your browser:")
        print(f"   {url}")
        return None
    except KeyError as e:
        print(f"❌ Unexpected response format: {e}")
        print("\n📊 Raw response:")
        print(data)
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

if __name__ == "__main__":
    chat_id = get_telegram_chat_id_auto()

    if chat_id:
        print("\n✅ NEXT STEP:")
        print(f"\n   Share this Chat ID with me: {chat_id}")
        print("   Or add it manually to your .env file")
        print("\n🎉 Once added, Telegram notifications will work!")
    else:
        print("\n❌ Could not retrieve Chat ID")
        print("   Please follow the instructions above and try again")
