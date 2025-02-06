from datetime import datetime, timedelta
import logging
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
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
        self._start_date = datetime.strptime(entry.data["start_date"], "%d.%m.%Y")
        self._repeat_every = self.parse_time_period(entry.data["repeat_every"])
        self._shift_pattern = entry.data["shift_pattern"].split(", ")
        self._state = None

    def parse_time_period(self, period: str):
        """Convert time period (e.g., '7d', '1m', '4w') into timedelta."""
        if period.endswith("d"):
            return timedelta(days=int(period[:-1]))
        elif period.endswith("w"):
            return timedelta(weeks=int(period[:-1]))
        elif period.endswith("m"):
            return timedelta(days=int(period[:-1]) * 30)
        return timedelta(days=1)  # Fallback: 1 Tag

    def update(self):
        """Update the sensor state based on the schedule."""
        days_since_start = (datetime.now() - self._start_date).days
        shift_index = (days_since_start // self._repeat_every.days) % len(self._shift_pattern)
        self._state = self._shift_pattern[shift_index]

    @property
    def state(self):
        """Return the current shift."""
        return self._state