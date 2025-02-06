from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from .const import DOMAIN

class ShiftTrackerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handles initial setup flow for HA Shift Tracker."""

    async def async_step_user(self, user_input=None):
        """Skip configuration at setup and just create an entry."""
        return self.async_create_entry(title="HA Shift Tracker", data={})