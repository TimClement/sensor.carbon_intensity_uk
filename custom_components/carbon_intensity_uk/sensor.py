"""Sensor platform for carbon intensity UK."""
from .const import (
    DEFAULT_NAME,
    DOMAIN,
    HIGH_ICON,
    ICON,
    INTENSITY,
    LOW_ICON,
    MODERATE_ICON,
    SENSOR,
)

from .entity import CarbonIntensityEntity, FuelMixEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        [CarbonIntensitySensor(coordinator, entry), FuelMixSensor(coordinator, entry)]
    )


class CarbonIntensitySensor(CarbonIntensityEntity):
    """Carbon Intensity Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_intensity"

    @property
    def state(self):
        """Return the state of the sensor."""
        now = self.coordinator.data.get("now")
        return now.get("current_period_index")

    @property
    def icon(self):
        """Return the icon of the sensor."""
        now = self.coordinator.data.get("now")
        index = now.get("current_period_index")
        try:
            intensity = INTENSITY[index]
            if intensity >= INTENSITY["high"]:
                return HIGH_ICON
            elif intensity == INTENSITY["moderate"]:
                return MODERATE_ICON
            else:
                return LOW_ICON
        except KeyError:
            return ICON


class FuelMixSensor(FuelMixEntity):
    """Fuel Mix Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_mix"

    @property
    def state(self):
        """Return the state of the sensor."""
        now = self.coordinator.data.get("now")
        return now.get("current_period_forecast")

    @property
    def icon(self):
        """Return the icon of the sensor."""
        now = self.coordinator.data.get("now")
        index = now.get("current_period_index")
        try:
            intensity = INTENSITY[index]
            if intensity >= INTENSITY["high"]:
                return HIGH_ICON
            elif intensity == INTENSITY["moderate"]:
                return MODERATE_ICON
            else:
                return LOW_ICON
        except KeyError:
            return ICON
