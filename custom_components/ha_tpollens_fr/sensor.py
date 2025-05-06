from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_UNKNOWN
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
from .utils import parse_pollens_api_response

ATTRIBUTION = "Données Atmo France via admindata.atmo-france.org"

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    username = config.get("username")
    password = config.get("password")
    zone = config.get("zone")

    # Pour simplifier : on appelle directement ton script ici si pas de config_entry
    from .coordinator import PollensCoordinator
    class DummyEntry:
        data = {"username": username, "password": password, "zone": zone}

    coordinator = PollensCoordinator(hass, DummyEntry())
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([PollensFRSensor(coordinator)], True)

class PollensFRSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Pollens France"
        self._attr_unique_id = "pollens_fr"
        self._state = STATE_UNKNOWN
        self._attributes = {}

    @property
    def name(self):
        return "Pollens France"

    @property
    def unique_id(self):
        return "pollens_fr"

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
