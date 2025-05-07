import logging
from datetime import timedelta, datetime

import async_timeout
import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.config_entries import ConfigEntry
from homeassistant.util.dt import now

from .const import DOMAIN, LOGIN_URL, POLLENS_URL, DEFAULT_ZONE

_LOGGER = logging.getLogger(__name__)


class PollensCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry | None):
        self.username = entry.data["username"]
        self.password = entry.data["password"]
        self.zone = entry.data.get("zone", DEFAULT_ZONE)

        def next_15h():
            """Retourne le prochain datetime à 15h00 (aujourd’hui ou demain)."""
            today_15h = now().replace(hour=15, minute=0, second=0, microsecond=0)
            return today_15h if now() < today_15h else today_15h + timedelta(days=1)

        super().__init__(
            hass,
            _LOGGER,
            name="Pollens France",
            update_interval=timedelta(days=1),
            update_method=self._async_update_data,
            next_interval=next_15h(),
        )

    async def _async_update_data(self):
        try:
            async with async_timeout.timeout(15):
                async with aiohttp.ClientSession() as session:
                    token = await self._get_token(session)
                    return await self._get_pollens(session, token)
        except Exception as err:
            raise UpdateFailed(f"Erreur lors de la récupération des données pollens: {err}") from err

    async def _get_token(self, session):
        async with session.post(
            LOGIN_URL,
            json={"username": self.username, "password": self.password},
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return data["token"]

    async def _get_pollens(self, session, token):
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        async with session.get(POLLENS_URL, headers=headers, params=self.zone) as resp:
            resp.raise_for_status()
            return await resp.json()
