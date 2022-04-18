"""Provide info to system health."""
from homeassistant.components import system_health
from homeassistant.core import HomeAssistant, callback

from . import Proxy
from .const import HACS_DOMAIN

@callback
def async_register(hass: HomeAssistant, register: system_health.SystemHealthRegistration) -> None:
    """Register system health callbacks."""
    register.async_register_info(system_health_info)


async def system_health_info(hass):
    """Get info for the info page."""
    hacs = hass.data.get(HACS_DOMAIN)

    data = {
        "proxied": hacs is not None and isinstance(hacs.session, Proxy)
    }

    return data
