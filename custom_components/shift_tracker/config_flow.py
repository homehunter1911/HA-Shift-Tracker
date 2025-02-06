import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from .const import DOMAIN

DATA_SCHEMA = vol.Schema({
    vol.Required("start_date"): str,
    vol.Required("repeat_every"): str,
    vol.Required("shift_pattern"): str,
})

class ShiftTrackerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HA Shift Tracker."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="HA Shift Tracker", data=user_input)
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)