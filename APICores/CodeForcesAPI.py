import asyncio
import httpx

from GlobalVariable import (
    logger
)

jsessionid = ""


async def get_max_rate(handle: str) -> int:
    url = f"https://codeforces.com/api/user.rating?handle={handle}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()

        if data.get("status") == "OK":
            rating_changes = data.get("result", [])
            if not rating_changes:
                return 0

            max_rating = max(change["newRating"] for change in rating_changes)
            return max_rating

    except Exception as e:
        logger.error(e)

    return -1


async def check_code_on_codeforces(handle: str, code: str) -> bool:
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "OK":
                    first_name = data["result"][0].get("firstName", "")
                    logger.info("Current firstName: %s", first_name)
                    if first_name == code:
                        return True
        except Exception as e:
            logger.error("Error checking Codeforces API: %s", e)

    return False
