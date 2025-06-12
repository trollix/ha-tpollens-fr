import logging
from datetime import timedelta, datetime

import async_timeout
import aiohttp
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_point_in_time
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.config_entries import ConfigEntry
from homeassistant.util.dt import now as ha_now

from .const import DOMAIN, LOGIN_URL, POLLENS_URL, DEFAULT_ZONE

_LOGGER = logging.getLogger(__name__)


class PollensCoordinator(DataUpdateCoordinator):
    """Coordonnateur des données pollens."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="Pollens France",
            update_interval=timedelta(days=1),   # mises à jour quotidiennes
        )

        self.username = entry.data["username"]
        self.password = entry.data["password"]
        self.zone = entry.data.get("zone", DEFAULT_ZONE)

        # Planifie la toute première mise à jour à 15h
        self._schedule_first_refresh()

    # ---------------------------------------------------------------------

    def _schedule_first_refresh(self) -> None:
        """Planifie la 1ʳᵉ mise à jour aujourd’hui (ou demain) à 15 h."""

        @callback
        async def _refresh_at_time(_now):
            await self.async_refresh()

        today_15h = ha_now().replace(hour=15, minute=0, second=0, microsecond=0)
        first_run = today_15h if ha_now() < today_15h else today_15h + timedelta(days=1)

        _LOGGER.debug("Première mise à jour pollens programmée pour %s", first_run)
        async_track_point_in_time(self.hass, _refresh_at_time, first_run)

    # ---------------------------------------------------------------------

    async def _async_update_data(self):
        """Récupère les données de l’API."""
        try:
            async with async_timeout.timeout(15):
                async with aiohttp.ClientSession() as session:
                    token = await self._fetch_token(session)
                    return await self._fetch_pollens(session, token)
        except Exception as err:
            raise UpdateFailed(f"Erreur de récupération des données pollens : {err}") from err

    # ---------------------------------------------------------------------

    async def _fetch_token(self, session: aiohttp.ClientSession) -> str:
        async with session.post(
            LOGIN_URL,
            json={"username": self.username, "password": self.password},
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        ) as resp:
            resp.raise_for_status()
            return (await resp.json())["token"]

    async def _fetch_pollens(self, session: aiohttp.ClientSession, token: str):
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
        async with session.get(POLLENS_URL, headers=headers, params=self.zone) as resp:
            resp.raise_for_status()
            return await resp.json()
