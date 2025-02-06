from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "shift_tracker"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the HA Shift Tracker from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Optionen sicherstellen
    if not entry.options:
        hass.config_entries.async_update_entry(entry, options={
            "start_date": "06.02.2025",
            "repeat_every": "7d",
            "shift_pattern": "Frei, Früh, Spät, Nacht",
        })

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])