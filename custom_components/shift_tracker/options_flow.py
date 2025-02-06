import voluptuous as vol
import os
import json
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from .const import DOMAIN

SCHEDULES_PATH = os.path.join(os.path.dirname(__file__), "schedules")

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from .const import DOMAIN

class ShiftTrackerOptionsFlowHandler(config_entries.OptionsFlow):
    """Handles options for HA Shift Tracker."""

    def __init__(self, entry: config_entries.ConfigEntry):
        """Initialize options flow."""
        self.entry = entry
        self.data = entry.options.copy()

    async def async_step_init(self, user_input=None):
        """Step 1: Basic settings."""
        if user_input is not None:
            self.data["start_date"] = user_input["start_date"]
            self.data["shift_count"] = user_input["shift_count"]
            return await self.async_step_shifts()

        data_schema = vol.Schema({
            vol.Required("start_date", default=self.data.get("start_date", "")): cv.string,
            vol.Required("shift_count", default=self.data.get("shift_count", 1)): vol.All(vol.Coerce(int), vol.Range(min=1, max=10))
        })

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            title="config.step.init.title",
            description="config.step.init.description"
        )

    async def async_step_shifts(self, user_input=None):
        """Step 2: Configure shifts."""
        shift_count = int(self.data["shift_count"])
        shift_schema = {}

        for i in range(shift_count):
            shift_schema[vol.Required(f"shift_{i}_name", default=self.data.get(f"shift_{i}_name", ""))] = cv.string
            shift_schema[vol.Optional(f"shift_{i}_start", default=self.data.get(f"shift_{i}_start", ""))] = cv.string
            shift_schema[vol.Optional(f"shift_{i}_end", default=self.data.get(f"shift_{i}_end", ""))] = cv.string

        if user_input is not None:
            self.data.update(user_input)
            return await self.async_step_schedule()

        return self.async_show_form(
            step_id="shifts",
            data_schema=vol.Schema(shift_schema),
            description_placeholders={},
            title="config.step.shifts.title",
            description="config.step.shifts.description"
        )

    async def async_step_schedule(self, user_input=None):
        """Step 3: Shift cycle setup."""
        if user_input is not None:
            self.data["shift_pattern"] = user_input["shift_pattern"]
            return self.async_create_entry(title="", data=self.data)

        cycle_length = len(self.data.get("shift_pattern", "").split("\n")) if self.data.get("shift_pattern") else 0

        data_schema = vol.Schema({
            vol.Required("shift_pattern", default=self.data.get("shift_pattern", "")): cv.string,
        })

        return self.async_show_form(
            step_id="schedule",
            data_schema=data_schema,
            description_placeholders={"cycle_length": f"{cycle_length}"},
            title="config.step.schedule.title",
            description="config.step.schedule.description"
        )
