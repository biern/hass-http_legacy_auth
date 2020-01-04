import asyncio
from aiohttp.web import middleware
import logging

from homeassistant.components.http.const import KEY_AUTHENTICATED, KEY_REAL_IP

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
                request[KEY_REAL_IP],
                request.path,
                auth_type,
            )

            request[KEY_AUTHENTICATED] = True

        return await handler(request)

    hass.http.app.middlewares.append(auth_middleware);

    return True
