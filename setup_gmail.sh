#!/bin/bash
# Gmail App Password Setup Helper

echo ""
echo "============================================================"
echo "📧 GMAIL APP PASSWORD SETUP"
echo "============================================================"
echo ""
echo "First, generate your App Password:"
echo "1. Go to: https://myaccount.google.com/apppasswords"
echo "2. Create an app password for 'Mail'"
echo "3. Copy the 16-character password (remove spaces)"
echo ""
echo "============================================================"
echo ""

# Ask for the app password
read -p "Paste your Gmail App Password here: " APP_PASSWORD

# Remove spaces from password
APP_PASSWORD="${APP_PASSWORD// /}"

# Validate length
if [ ${#APP_PASSWORD} -ne 16 ]; then
    echo ""
    echo "⚠️  Warning: Password should be 16 characters (you entered ${#APP_PASSWORD})"
    echo "   Make sure you removed all spaces!"
    echo ""
    read -p "Continue anyway? (yes/no): " CONTINUE
    if [ "$CONTINUE" != "yes" ]; then
        echo "Cancelled."
        exit 1
    fi
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo ""
    echo "❌ .env file not found!"
    echo "   Creating from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file"
fi

# Check if GMAIL_APP_PASSWORD already exists
if grep -q "^GMAIL_APP_PASSWORD=" .env; then
    echo ""
    echo "⚠️  GMAIL_APP_PASSWORD already exists in .env"
    read -p "Overwrite it? (yes/no): " OVERWRITE
    if [ "$OVERWRITE" = "yes" ]; then
        # Replace existing line
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s|^GMAIL_APP_PASSWORD=.*|GMAIL_APP_PASSWORD=$APP_PASSWORD|" .env
        else
            # Linux
            sed -i "s|^GMAIL_APP_PASSWORD=.*|GMAIL_APP_PASSWORD=$APP_PASSWORD|" .env
        fi
        echo "✅ Updated GMAIL_APP_PASSWORD in .env"
    else
        echo "Cancelled."
        exit 1
    fi
else
    # Add new line
    echo "GMAIL_APP_PASSWORD=$APP_PASSWORD" >> .env
    echo "✅ Added GMAIL_APP_PASSWORD to .env"
fi

echo ""
echo "============================================================"
echo "✅ GMAIL APP PASSWORD CONFIGURED!"
echo "============================================================"
echo ""
echo "Running validation..."
echo ""

# Run validation
python3 validate_env.py

echo ""
echo "============================================================"
echo ""
echo "Next steps:"
echo "  make run      # Start the system"
echo "  make test     # Run tests"
echo ""
