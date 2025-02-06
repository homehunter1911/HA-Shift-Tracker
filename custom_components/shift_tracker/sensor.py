from datetime import datetime, timedelta
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up HA Shift Tracker sensor from a config entry."""
    async_add_entities([ShiftTrackerSensor(entry)])

class ShiftTrackerSensor(SensorEntity):
    """Representation of the shift tracker sensor."""

    def __init__(self, entry):
        """Initialize the sensor."""
        self._attr_name = "Current Shift"
        self._attr_unique_id = f"shift_tracker_{entry.entry_id}"
        self._start_date = datetime.strptime(entry.options["start_date"], "%d.%m.%Y")
        self._shift_count = int(entry.options["shift_count"])
        self._shifts = {
            entry.options[f"shift_{i}_name"]: {
                "start": entry.options[f"shift_{i}_start"],
                "end": entry.options[f"shift_{i}_end"]
            }
            for i in range(self._shift_count)
        }
        self._shift_pattern = entry.options["shift_pattern"].split("\n")
        self._state = None

    def update(self):
        """Update the sensor state based on the schedule."""
        days_since_start = (datetime.now() - self._start_date).days
        shift_index = days_since_start % len(self._shift_pattern)
        shift_name = self._shift_pattern[shift_index]
        shift_data = self._shifts.get(shift_name, {"start": "00:00", "end": "23:59"})

        self._state = f"{shift_name} ({shift_data['start']} - {shift_data['end']})"

    @property
    def state(self):
        """Return the current shift."""
        return self._state