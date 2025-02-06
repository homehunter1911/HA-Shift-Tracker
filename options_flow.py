import os
import json
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from .const import DOMAIN

SCHEDULES_PATH = os.path.join(os.path.dirname(__file__), "schedules")

def get_available_schedules():
    """Lese die index.json und erhalte eine Liste der verfügbaren Modelle."""
    index_file = os.path.join(SCHEDULES_PATH, "index.json")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as file:
            return json.load(file).get("templates", [])
    return []

def load_schedule(template_name):
    """Lade ein Schichtmodell aus einer JSON-Datei."""
    schedule_file = os.path.join(SCHEDULES_PATH, f"{template_name}.json")
    if os.path.exists(schedule_file):
        with open(schedule_file, "r", encoding="utf-8") as file:
            return json.load(file).get("Schedule", [])
    return []

class ShiftTrackerOptionsFlowHandler(config_entries.OptionsFlow):
    """Handles options for HA Shift Tracker."""

    def __init__(self, entry: config_entries.ConfigEntry):
        """Initialize options flow."""
        self.entry = entry
        self.data = entry.options.copy()
        self.schedule_templates = get_available_schedules()

    async def async_step_schedule(self, user_input=None):
        """Step für Schichtplanung."""
        if user_input is not None:
            if user_input["template_name"] != "None":
                self.data["shift_pattern"] = "\n".join(load_schedule(user_input["template_name"]))
            else:
                self.data["shift_pattern"] = user_input["shift_pattern"]
            return self.async_create_entry(title="", data=self.data)

        cycle_length = len(self.data.get("shift_pattern", "").split("\n"))

        data_schema = vol.Schema({
            vol.Optional("template_name", default="None"): vol.In(["None"] + self.schedule_templates),
            vol.Required("shift_pattern", default=self.data.get("shift_pattern", "")): cv.string,
        })

        return self.async_show_form(
            step_id="schedule",
            data_schema=data_schema,
            description_placeholders={"cycle_length": f"Schichtzyklus: {cycle_length} Tage"}
        )