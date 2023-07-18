import time
import aiohttp
import asyncio
import more_itertools
from typing import Iterable
from create_db import create_db_session
from insert_db import insert_db_session

API_URL = "https://swapi.dev/api/people/"
MAX_COUNT = 10


async def get_person(person_id: int) -> dict:
    print(f"Получаю person_id {person_id}")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/{person_id}/") as response:
            response = await response.json(content_type=None)
            response["id"] = person_id
            print(f"Завершено person_id {person_id}")
            return response


async def get_people(id_range: Iterable[int]):
    for id_range_count in more_itertools.chunked(id_range, MAX_COUNT):
        yield await asyncio.gather(*[get_person(i) for i in id_range_count])


async def get_name(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = await response.json(content_type=None)
            if "title" in response:
                return response["title"]
            if "name" in response:
                return response["name"]


async def check_dict_fields(people):
    people_checked = []
    for person in people:
        if "detail" in person:
            people.remove(person)
        else:
            print(f'В работе person_id {person["id"]}')
            person.pop("created", None)
            person.pop("edited", None)
            person.pop("url", None)
            person["homeworld"] = await get_name(person["homeworld"])
            person["films"] = ", ".join([await get_name(i) for i in person["films"]])
            person["species"] = ", ".join(
                [await get_name(i) for i in person["species"]]
            )
            person["starships"] = ", ".join(
                [await get_name(i) for i in person["starships"]]
            )
            person["vehicles"] = ", ".join(
                [await get_name(i) for i in person["vehicles"]]
            )
            people_checked.append(tuple(person.values()))

    return people_checked


async def main():
    tasks = []
    async for people in get_people(range(1, 100)):
        task_1 = asyncio.create_task(check_dict_fields(people))
        tasks.append(task_1)
        task_2 = asyncio.create_task(insert_db_session(await task_1))
        tasks.append(task_2)
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_db_session())
    asyncio.run(main())
    print(time.time() - start)
