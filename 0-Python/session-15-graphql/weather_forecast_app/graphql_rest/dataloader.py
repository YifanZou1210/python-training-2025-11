from aiodataloader import DataLoader
import httpx

REST_URL = "http://localhost:8000"

class UserTasksLoader(DataLoader):
    # keys -> multiple user id , group total requests into batch to return tasks
    async def batch_load_fn(self, keys):
        async with httpx.AsyncClient() as client:
            results = []
            for user_id in keys:
                r = await client.get(f"{REST_URL}/tasks/", params={"user_id": user_id})
                results.append(r.json())
            return results