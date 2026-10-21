import os

import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

PLACES_URL = "https://places.googleapis.com/v1/places:searchText"


def search_restaurant(name: str):
    if not API_KEY:
        raise RuntimeError("GOOGLE_MAPS_API_KEY is missing from .env")

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": (
            "places.id,"
            "places.displayName,"
            "places.formattedAddress,"
            "places.websiteUri"
        ),
    }

    payload = {
        "textQuery": name,
        "includedType": "restaurant",
        "maxResultCount": 5,
    }

    response = httpx.post(
        PLACES_URL,
        headers=headers,
        json=payload,
        timeout=20,
    )
    response.raise_for_status()

    return response.json().get("places", [])


if __name__ == "__main__":
    restaurant_name = input("Enter restaurant name: ").strip()

    results = search_restaurant(restaurant_name)

    if not results:
        print("No restaurants found.")

    for restaurant in results:
        print("\nRestaurant:", restaurant.get("displayName", {}).get("text"))
        print("Address:", restaurant.get("formattedAddress", "Unavailable"))
        print("Website:", restaurant.get("websiteUri", "Unavailable"))