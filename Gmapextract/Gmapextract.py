
import time
import pandas as pd
import googlemaps

# 1. Replace with your own API key
API_KEY = "YOUR_GOOGLE_CLOUD_API_KEY"
gmaps = googlemaps.Client(key=API_KEY)

# 2. Define your search parameters
location = (40.7128, -74.0060)     # e.g., New York City lat/lng
radius_m = 1000                    # search within 1 km
place_type = "restaurant"          # e.g., "restaurant", "cafe", "store", etc.

# 3. Fetch initial page of results
response = gmaps.places_nearby(location=location,
                               radius=radius_m,
                               type=place_type)

all_places = response.get("results", [])

# 4. Handle pagination (if more than 20 results)
while "next_page_token" in response:
    time.sleep(2)  # token needs a short delay before it becomes valid
    response = gmaps.places_nearby(page_token=response["next_page_token"])
    all_places.extend(response.get("results", []))

# 5. For each place, get detailed fields
records = []
for p in all_places:
    detail = gmaps.place(place_id=p["place_id"],
                         fields=[
                             "name",
                             "formatted_address",
                             "formatted_phone_number",
                             "website",
                             "rating",
                             "user_ratings_total",
                             "geometry/location"
                         ])["result"]
    records.append({
        "Name": detail.get("name"),
        "Address": detail.get("formatted_address"),
        "Phone": detail.get("formatted_phone_number", ""),
        "Website": detail.get("website", ""),
        "Rating": detail.get("rating", ""),
        "Reviews": detail.get("user_ratings_total", ""),
        "Lat": detail["geometry"]["location"]["lat"],
        "Lng": detail["geometry"]["location"]["lng"]
    })

# 6. Convert to DataFrame and export
df = pd.DataFrame(records)
df.to_csv("google_maps_data.csv", index=False)
print(f"Extracted {len(df)} places → google_maps_data.csv")
