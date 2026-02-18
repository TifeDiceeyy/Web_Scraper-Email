#!/usr/bin/env python3
"""
Simple Telegram Chat ID Finder
Uses bot token from .env file
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_telegram_chat_id():
    """Get your Telegram Chat ID from bot updates"""

    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

    if not bot_token or bot_token == 'your-telegram-bot-token-here':
        print("❌ TELEGRAM_BOT_TOKEN not set in .env file")
        return

    print("="*60)
    print("📱 TELEGRAM CHAT ID FINDER")
    print("="*60)
    print(f"\n✅ Bot Token: {bot_token[:20]}...")
    print("\n📝 INSTRUCTIONS:")
    print("1. Open Telegram on your phone/computer")
    print("2. Search for your bot (or start a chat with it)")
    print("3. Send ANY message to your bot (e.g., 'hello', 'hi', or '/start')")
    print("4. Press Enter here after you've sent the message...\n")

    input("Press Enter after sending a message to your bot: ")

    print("\n🔍 Fetching updates from Telegram...\n")

    # Call Telegram API to get updates
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if not data.get('ok'):
            print(f"❌ Error from Telegram API: {data.get('description', 'Unknown error')}")
            return

        updates = data.get('result', [])

        if not updates:
            print("❌ No messages found!")
            print("\n💡 Make sure you:")
            print("   1. Started a chat with your bot")
            print("   2. Sent at least one message")
            print("   3. The message was sent recently")
            print("\n🔗 You can also check manually:")
            print(f"   Visit: {url}")
            return

        # Get the most recent chat ID
        latest_update = updates[-1]
        chat_id = latest_update['message']['chat']['id']
        chat_type = latest_update['message']['chat']['type']

        if 'username' in latest_update['message']['chat']:
            username = latest_update['message']['chat']['username']
        else:
            username = latest_update['message']['chat'].get('first_name', 'Unknown')

        print("="*60)
        print("✅ SUCCESS! Found your Chat ID:")
        print("="*60)
        print(f"\n📱 Chat ID: {chat_id}")
        print(f"👤 Username: {username}")
        print(f"💬 Chat Type: {chat_type}")
        print("\n" + "="*60)
        print("\n💾 Add this to your .env file:")
        print(f"TELEGRAM_CHAT_ID={chat_id}")
        print("\n" + "="*60)

        # Show all recent messages for verification
        print("\n📝 Recent messages from your bot:")
        for i, update in enumerate(updates[-5:], 1):  # Last 5 messages
            msg = update['message']
            text = msg.get('text', '[No text]')
            from_user = msg['from'].get('username', msg['from'].get('first_name', 'Unknown'))
            print(f"   {i}. From @{from_user}: {text}")

        return chat_id

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        print("\n🔗 Try visiting this URL in your browser:")
        print(f"   {url}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("\n🔗 Try visiting this URL in your browser:")
        print(f"   {url}")

if __name__ == "__main__":
    chat_id = get_telegram_chat_id()

    if chat_id:
        print("\n🎉 Next Step:")
        print("   Copy the Chat ID above and share it with me, or")
        print("   add it manually to your .env file")
