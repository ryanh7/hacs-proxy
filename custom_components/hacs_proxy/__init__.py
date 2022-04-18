from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from aiohttp.client import ClientSession
from aiohttp.typedefs import StrOrURL

from .const import CONF_ENABLE, CONF_PROXY, DOMAIN, HACS_DOMAIN

class Proxy:
    def __init__(self, origin, proxy=None):
        self._origin = origin
        self._proxy_info = proxy
    
    async def get(self, url: StrOrURL, **kwargs: Any):
        args = {**kwargs, 'proxy': self._proxy_info}
        return await self._origin.get(url, **args)
    
    def __getattr__(self, name):
        return getattr(self._origin, name)

async def async_initialize_integration(
    hass: HomeAssistant,
    config_entry: ConfigEntry | None = None,
) -> bool:
    """Initialize the integration"""
    hacs = hass.data.get(HACS_DOMAIN)
    if hacs is None:
        return False
    
    config = config_entry.data
    if not config.get(CONF_ENABLE):
        return True

    session = hacs.session
    if not isinstance(session, ClientSession):
        return True

    proxy = Proxy(session, config.get(CONF_PROXY))
    hacs.session = proxy
    hacs.github._session = proxy
    hacs.githubapi._session = proxy

    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    config_entry.add_update_listener(async_reload_entry)
    return await async_initialize_integration(hass=hass, config_entry=config_entry)


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    hacs = hass.data[HACS_DOMAIN]
    if hacs is None:
        return True

    session = hacs.session
    if not isinstance(session, Proxy):
        return True

    origin = session._origin
    hacs.session = origin
    hacs.github._session = origin
    hacs.githubapi._session = origin

    return True


async def async_reload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Reload the HACS config entry."""
    await async_unload_entry(hass, config_entry)
    await async_setup_entry(hass, config_entry)
