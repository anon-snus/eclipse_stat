from aiohttp_proxy import ProxyConnector
from data import exceptions
import aiohttp

async def async_get(
        url: str,
        proxy: str | None = None,
        headers: dict | None = None,
        response_type: str = 'json',
        **kwargs
) -> dict | str | None:

    connector = ProxyConnector.from_url(
        url=proxy
    ) if proxy else None

    async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
        async with session.get(url=url, **kwargs) as response:
            status_code = response.status
            if response_type == "json":
                response = await response.json()
            elif response_type == "text":
                response = await response.text()
            if status_code <= 201:
                return response

            raise exceptions.HTTPException(response=response, status_code=status_code)