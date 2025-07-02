import os
import asyncio
import json
import random
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types


USER_ID = "Chris"
MEMORY_FILE = "travel_agent_memory.json"

# Load environment variables from .env file
load_dotenv()


class SimpleMemory:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.memory_store = self._load_from_file()
        print(f"[Memory System] Initialized and loaded data from '{self.filepath}'")

    def _load_from_file(self) -> dict:
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _save_to_file(self):
        with open(self.filepath, "w") as f:
            json.dump(self.memory_store, f, indent=4)

    def add(self, user_id: str, category: str, data: str):
        self.memory_store.setdefault(user_id, {}).setdefault(category, [])
        if data not in self.memory_store[user_id][category]:
            self.memory_store[user_id][category].append(data)
            self._save_to_file()
            print(
                f"[Memory System] Saved data for user '{user_id}' in category '{category}': '{data}'"
            )
        return True

    def search_by_category(self, user_id: str, category: str) -> list:
        user_memory = self.memory_store.get(user_id, {})
        results = user_memory.get(category, [])
        print(
            f"[Memory System] Retrieved {len(results)} items from category '{category}' for user '{user_id}'."
        )
        return results


persistent_data = SimpleMemory(filepath=MEMORY_FILE)


def save_user_preference(category: str, preference: str) -> dict:
    user_id = getattr(save_user_preference, "user_id", USER_ID)
    persistent_data.add(user_id=user_id, category=category, data=preference)
    return {
        "status": "success",
        "message": f"Preference saved in category '{category}'.",
    }


def retrieve_user_preferences(category: str) -> dict:
    user_id = getattr(retrieve_user_preferences, "user_id", USER_ID)
    results = persistent_data.search_by_category(user_id=user_id, category=category)
    return {"status": "success", "preferences": results, "count": len(results)}


def find_flights(
    destination: str, departure_date: str, preferences: Optional[list[str]] = None
) -> dict:
    print(
        f"INFO: Dummy tool 'find_flights' called for {destination} on {departure_date} with preferences: {preferences}"
    )

    all_airlines = [
        "Delta",
        "Qatar Airways",
        "Singapore Airlines",
        "Ryanair",
        "Lufthansa",
        "Emirates",
    ]
    preferred_airline = None

    if preferences:
        for pref in preferences:
            for airline in all_airlines:
                if airline.lower() in pref.lower():
                    preferred_airline = airline
                    break
            if preferred_airline:
                break

    flights_found = []
    if preferred_airline:
        flights_found.append(
            {
                "airline": preferred_airline,
                "flight_number": f"{preferred_airline[:2].upper()}{random.randint(100, 999)}",
                "departure_time": (
                    datetime.now() + timedelta(hours=random.randint(2, 5))
                ).strftime("%H:%M"),
                "arrival_time": (
                    datetime.now() + timedelta(hours=random.randint(10, 14))
                ).strftime("%H:%M"),
                "price": f"{random.randint(800, 1800)} EUR",
                "notes": "Matches your preferred airline",
            }
        )

    for _ in range(random.randint(1, 2)):
        airline = random.choice([a for a in all_airlines if a != preferred_airline])
        flights_found.append(
            {
                "airline": airline,
                "flight_number": f"{airline[:2].upper()}{random.randint(100, 999)}",
                "departure_time": (
                    datetime.now() + timedelta(hours=random.randint(2, 12))
                ).strftime("%H:%M"),
                "arrival_time": (
                    datetime.now() + timedelta(hours=random.randint(14, 20))
                ).strftime("%H:%M"),
                "price": f"{random.randint(400, 1500)} EUR",
                "notes": "Standard option",
            }
        )

    return {"status": "success", "flights": flights_found}


travel_agent = Agent(
    name="travel_assistant",
    model="gemini-2.5-flash",
    description="A helpful travel assistant that remembers user preferences to provide personalized recommendations.",
    instruction="""
You are a friendly and efficient Travel Assistant. Your goal is to make booking travel as easy as possible by remembering user preferences. When user says Hi, you greet them warmly and ask how you can assist with their travel plans. If they mention a destination, you offer to find flights and ask for their preferences. You should save user preferences for future reference.

Core Workflow for Flight Searches:
1. Check Memory First: Use `retrieve_user_preferences` with the category 'travel_preferences'.
2. Call Flight Search: Then call `find_flights`, passing in the retrieved preferences.
3. Present Results: Show the details of each flight clearly to the user.
4. Save Preferences: If the user shares a new preference, use `save_user_preference`.
""",
    tools=[save_user_preference, retrieve_user_preferences, find_flights],
)


session_service = InMemorySessionService()
APP_NAME = "travel_assistant_app"
SESSION_ID = "session_001"

runner = Runner(
    agent=travel_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


async def call_agent_async(query: str, user_id: str, session_id: str):
    print(f"\n>>> User ({user_id}): {query}")
    content = types.Content(role="user", parts=[types.Part(text=query)])
    setattr(save_user_preference, "user_id", user_id)
    setattr(retrieve_user_preferences, "user_id", user_id)

    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text
            print(f"<<< Assistant: {final_response}")
            return final_response

    return "No response received."


async def interactive_chat():
    print("--- Starting Interactive Travel Assistant ---")
    print("Type 'quit' to end the session.")
    while True:
        user_query = input("\n> ")
        if user_query.lower() in ["quit", "exit"]:
            print("Ending session. Goodbye!")
            break
        await call_agent_async(query=user_query, user_id=USER_ID, session_id=SESSION_ID)


async def create_session():
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )


if __name__ == "__main__":
    if (
        not os.getenv("GOOGLE_API_KEY")
        or os.getenv("GOOGLE_API_KEY") == "YOUR_GOOGLE_API_KEY_HERE"
    ):
        print(
            "ERROR: Please set your GOOGLE_API_KEY environment variable to run this script."
        )
    else:
        asyncio.run(create_session())
        asyncio.run(interactive_chat())
