#!/usr/bin/env python3
"""
Tests for configuration manager
"""

import pytest
import sys
import os
import json
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.config_manager import ConfigManager


class TestConfigManager:
    """Test configuration manager"""

    @pytest.fixture
    def temp_config_dir(self):
        """Create temporary config directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def manager(self, temp_config_dir):
        """Create config manager with temp directory"""
        return ConfigManager(config_dir=temp_config_dir)

    def test_save_and_load_config(self, manager):
        """Test saving and loading configuration"""
        config = {
            "business_type": "Dentists",
            "outreach_type": "general_help",
            "automation_focus": None,
            "data_source": "manual",
            "total_businesses": 5
        }

        # Save
        result = manager.save_config(config)
        assert result is True

        # Load
        loaded = manager.load_config()
        assert loaded["business_type"] == "Dentists"
        assert loaded["outreach_type"] == "general_help"
        assert loaded["total_businesses"] == 5
        assert "created_at" in loaded
        assert "updated_at" in loaded

    def test_load_nonexistent_config(self, manager):
        """Test loading config that doesn't exist"""
        with pytest.raises(FileNotFoundError):
            manager.load_config()

    def test_update_config(self, manager):
        """Test updating configuration"""
        # First save
        config = {
            "business_type": "Dentists",
            "outreach_type": "general_help",
            "total_businesses": 5
        }
        manager.save_config(config)

        # Then update
        manager.update_config({"total_businesses": 10})

        # Verify
        loaded = manager.load_config()
        assert loaded["total_businesses"] == 10
        assert loaded["business_type"] == "Dentists"  # Unchanged

    def test_get_outreach_type(self, manager):
        """Test getting outreach type"""
        config = {
            "business_type": "Dentists",
            "outreach_type": "specific_automation"
        }
        manager.save_config(config)

        assert manager.get_outreach_type() == "specific_automation"

    def test_get_automation_focus(self, manager):
        """Test getting automation focus"""
        config = {
            "business_type": "Dentists",
            "outreach_type": "specific_automation",
            "automation_focus": "Appointment Reminders"
        }
        manager.save_config(config)

        assert manager.get_automation_focus() == "Appointment Reminders"

    def test_get_business_type(self, manager):
        """Test getting business type"""
        config = {
            "business_type": "Restaurants",
            "outreach_type": "general_help"
        }
        manager.save_config(config)

        assert manager.get_business_type() == "Restaurants"

    def test_config_exists(self, manager):
        """Test checking if config exists"""
        assert manager.config_exists() is False

        config = {"business_type": "Dentists", "outreach_type": "general_help"}
        manager.save_config(config)

        assert manager.config_exists() is True

    def test_delete_config(self, manager):
        """Test deleting configuration"""
        config = {"business_type": "Dentists", "outreach_type": "general_help"}
        manager.save_config(config)

        assert manager.config_exists() is True

        manager.delete_config()

        assert manager.config_exists() is False

    def test_save_with_sheet_id_from_env(self, manager):
        """Test that sheet_id is added from environment"""
        with patch.dict(os.environ, {"GOOGLE_SPREADSHEET_ID": "test-sheet-123"}):
            config = {
                "business_type": "Dentists",
                "outreach_type": "general_help"
            }
            manager.save_config(config)

            loaded = manager.load_config()
            assert loaded.get("sheet_id") == "test-sheet-123"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
