import json
from pathlib import Path
from typing import Optional

DATA_PATH = Path(__file__).parent.parent / "data" / "cars.json"

_cars_cache: list[dict] | None = None


def _load_cars() -> list[dict]:
    global _cars_cache
    if _cars_cache is None:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            _cars_cache = json.load(f)
    return _cars_cache


def search_cars(
    min_budget: Optional[float] = None,
    max_budget: Optional[float] = None,
    body_type: Optional[str] = None,
    fuel_type: Optional[str] = None,
    transmission: Optional[str] = None,
    seating_capacity: Optional[int] = None,
    min_safety_rating: Optional[int] = None,
    use_case: Optional[list[str]] = None,
) -> list[dict]:
    """Filter cars based on buyer criteria and return matching results."""
    cars = _load_cars()
    results = []

    for car in cars:
        if min_budget is not None and car["price_lakhs"] < min_budget:
            continue
        if max_budget is not None and car["price_lakhs"] > max_budget:
            continue
        if body_type is not None and car["body_type"].lower() != body_type.lower():
            continue
        if fuel_type is not None and car["fuel_type"].lower() != fuel_type.lower():
            continue
        if transmission is not None and car["transmission"].lower() != transmission.lower():
            continue
        if seating_capacity is not None and car["seating_capacity"] < seating_capacity:
            continue
        if min_safety_rating is not None and car["safety_rating_ncap"] < min_safety_rating:
            continue
        if use_case is not None:
            car_tags = set(car.get("best_for", []))
            if not any(tag in car_tags for tag in use_case):
                continue
        results.append(car)

    return results


def get_car_details(car_id: str) -> Optional[dict]:
    """Get full details for a specific car by ID."""
    cars = _load_cars()
    for car in cars:
        if car["id"] == car_id:
            return car
    return None


def compare_cars(car_ids: list[str]) -> dict:
    """Compare multiple cars side-by-side on key specs."""
    cars = _load_cars()
    selected = [car for car in cars if car["id"] in car_ids]

    if not selected:
        return {"error": "No matching cars found for the given IDs."}

    comparison_fields = [
        "make", "model", "variant", "price_lakhs", "body_type", "fuel_type",
        "engine_cc", "power_hp", "torque_nm", "transmission", "mileage_kmpl",
        "safety_rating_ncap", "seating_capacity", "key_features", "pros", "cons",
        "user_rating", "review_summary",
    ]

    comparison = {}
    for car in selected:
        comparison[car["id"]] = {k: car.get(k) for k in comparison_fields}

    return comparison


def get_all_makes() -> list[str]:
    """Return all unique car makes in the dataset."""
    cars = _load_cars()
    return sorted(set(car["make"] for car in cars))


def get_budget_ranges() -> dict:
    """Return min and max prices in the dataset."""
    cars = _load_cars()
    prices = [car["price_lakhs"] for car in cars]
    return {"min_lakhs": min(prices), "max_lakhs": max(prices)}
