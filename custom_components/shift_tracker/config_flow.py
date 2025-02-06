from homeassistant import config_entries
from .const import DOMAIN
from .options_flow import ShiftTrackerOptionsFlowHandler

class ShiftTrackerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the initial config flow."""

    async def async_step_user(self, user_input=None):
        """Skip configuration at setup and just create an entry."""
        return self.async_create_entry(title="HA Shift Tracker", data={})

    @staticmethod
    def async_get_options_flow(entry):
        """Return the options flow handler for Home Assistant."""
        return ShiftTrackerOptionsFlowHandler(entry)
