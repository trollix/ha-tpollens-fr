from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_UNKNOWN
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .utils import parse_pollens_api_response

ATTRIBUTION = "Données Atmo France via admindata.atmo-france.org"


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([AtmoPollensSensor(coordinator)], True)


class AtmoPollensSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator):
        super().__init__(coordinator)

        zone_name = coordinator.zone.get("nom", "inconnu").lower().replace(" ", "_")
        self._attr_name = f"Atmo {zone_name}"
        self._attr_unique_id = f"atmo_{zone_name}"
        self._state = STATE_UNKNOWN
        self._attributes = {}

    @property
    def name(self):
        return self._attr_name

    @property
    def unique_id(self):
        return self._attr_unique_id

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    async def async_update(self):
        await self.coordinator.async_request_refresh()

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.update_from_coordinator()

    def update_from_coordinator(self):
        data = self.coordinator.data
        if not data:
            self._state = STATE_UNKNOWN
            self._attributes = {}
            return

        state, attributes = parse_pollens_api_response(data)
        self._state = state
        self._attributes = attributes
        self._attributes["attribution"] = ATTRIBUTION
