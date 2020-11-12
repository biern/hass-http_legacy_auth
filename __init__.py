import asyncio
from aiohttp.web import middleware
from aiohttp.frozenlist import FrozenList
import logging

from homeassistant.components.http import HomeAssistantHTTP
from homeassistant.components.http.const import KEY_AUTHENTICATED

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "http_legacy_auth"
_LOGGER = logging.getLogger(__name__)

KEY_API_PASSWORD = 'api_password'

@asyncio.coroutine
def async_setup(hass, config):
    api_password = config[DOMAIN][KEY_API_PASSWORD]

    @middleware
    async def auth_middleware(request, handler):
        if KEY_API_PASSWORD in request.query and \
               request.query[KEY_API_PASSWORD] == api_password:

            auth_type = 'api_password'
            _LOGGER.debug(
                "Authenticated %s for %s using %s",
                request,
                request.path,
                auth_type,
            )

            request[KEY_AUTHENTICATED] = True

        return await handler(request)

    # NOTE: This hack is an accident waiting to happen, however HASS
    # doesn't seem to offer a way to add a middleware to the http
    # component. aiohttp "freezes" app state after start so it's
    # impossible to use public API to add a middleware there directly.
    hass.http.app._middlewares = FrozenList([*hass.http.app.middlewares, auth_middleware])
    hass.http.app._middlewares_handlers = tuple(hass.http.app._prepare_middleware())
    return True
