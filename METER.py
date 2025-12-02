# AI Meter Prototype - Auto Fare Calculator
# Requires: geopy
# Install: pip install geopy

from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import json

# Initialize geolocator
geolocator = Nominatim(user_agent="ai_meter")

# Hardcoded fuel prices per city (₹ per litre)
fuel_prices = {
    "Chennai": 100.80,
    "Bangalore": 105.50,
    "Delhi": 101.20
}

# Function to get coordinates
def get_coordinates(place):
    location = geolocator.geocode(place)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

# Function to calculate fare
def calculate_fare(from_place, to_place):
    coords1 = get_coordinates(from_place)
    coords2 = get_coordinates(to_place)
    
    if not coords1 or not coords2:
        return None, None  # Invalid input
    
    # Calculate distance in km
    distance = geodesic(coords1, coords2).km
    
    # Get fuel price for the city (default to Chennai if city not found)
    city = from_place.split(",")[0]  # Simple city extraction
    fuel_price = fuel_prices.get(city, fuel_prices["Chennai"])
    
    # Fare calculation (example logic)
    base_fare = 36       # ₹ for first 2 km
    per_km_rate = 18     # ₹ per km after first 2 km
    fuel_efficiency = 15 # km per litre
    
    if distance <= 2:
        fare = base_fare
    else:
        fare = base_fare + (distance - 2) * per_km_rate
    
    # Adjust fare slightly based on fuel price
    fare += (fuel_price - 100) * (distance / fuel_efficiency)
    
    return distance, fare

# Main program
from_place = input("Enter starting place (From): ")
to_place = input("Enter destination (To): ")

distance, fare = calculate_fare(from_place, to_place)

if distance is None:
    print("Invalid location entered. Please check spelling or city name.")
else:
    print(f"\nDistance: {distance:.2f} km")
    print(f"Estimated Auto Fare: ₹{fare:.2f}")
    
    # Save result to JSON (optional)
    result = {
        "From": from_place,
        "To": to_place,
        "Distance_km": round(distance, 2),
        "Fare_Rs": round(fare, 2)
    }
    with open("fare_result.json", "w") as f:
        json.dump(result, f, indent=4)
    print("\nResult saved to fare_result.json")

