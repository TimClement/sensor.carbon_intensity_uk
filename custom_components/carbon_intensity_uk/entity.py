"""CarbonIntensityEntity and FuelMixEntity classes."""

from homeassistant.helpers import entity

from .const import DOMAIN, NAME, VERSION


class CarbonIntensityEntity(entity.Entity):
    """Basis for carbon intensity sensor."""

    def __init__(self, coordinator, config_entry) -> None:
        """Set coordinator and configuration."""
        self.coordinator = coordinator
        self.config_entry = config_entry

    @property
    def should_poll(self):
        """No need to poll. Coordinator notifies entity of updates."""
        return False

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.last_update_success

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id + "_forecast"

    @property
    def device_info(self):
        """Standard device information."""
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": NAME + "_forecast",
            "model": VERSION,
            "manufacturer": NAME,
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        data = {}
        now = self.coordinator.data.get("now")
        data["current_period_index"] = now.get("current_period_index")
        data["current_period_forecast"] = now.get("current_period_forecast")
        data["forecast"] = self.coordinator.data.get("forecast")
        return data

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update Carbon Intensity UK entity."""
        await self.coordinator.async_request_refresh()


class FuelMixEntity(entity.Entity):
    """Basis for fuel mix sensor."""

    def __init__(self, coordinator, config_entry) -> None:
        """Set coordinator and configuration."""
        self.coordinator = coordinator
        self.config_entry = config_entry

    @property
    def should_poll(self):
        """No need to poll. Coordinator notifies entity of updates."""
        return False

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.last_update_success

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id + "_fuel_mix"

    @property
    def device_info(self):
        """Standard device information."""
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": NAME + "_fuel_mix",
            "model": VERSION,
            "manufacturer": NAME,
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        data = self.coordinator.data.get("now")
        return data

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update Carbon Intensity UK entity."""
        await self.coordinator.async_request_refresh()
