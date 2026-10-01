HOTEL_ROOMS = {
    "standard": {
        "available": 5,
        "price_per_night": 80
    },
    "deluxe": {
        "available": 3,
        "price_per_night": 120
    },
    "suite": {
        "available": 2,
        "price_per_night": 200
    }
}


def check_room_availability(room_type: str) -> dict:
    """
    Check the number of available rooms for a room type.
    """

    room_type = room_type.lower().strip()

    if room_type not in HOTEL_ROOMS:
        return {
            "success": False,
            "message": "Invalid room type."
        }

    room = HOTEL_ROOMS[room_type]

    return {
        "success": True,
        "room_type": room_type,
        "available_rooms": room["available"]
    }


def calculate_booking_price(room_type: str, nights: int) -> dict:
    """
    Calculate the estimated booking price.
    """

    room_type = room_type.lower().strip()

    if room_type not in HOTEL_ROOMS:
        return {
            "success": False,
            "message": "Invalid room type."
        }

    if nights <= 0 or nights > 30:
        return {
            "success": False,
            "message": "Number of nights must be between 1 and 30."
        }

    price_per_night = HOTEL_ROOMS[room_type]["price_per_night"]

    total_price = price_per_night * nights

    return {
        "success": True,
        "room_type": room_type,
        "nights": nights,
        "price_per_night": price_per_night,
        "total_price": total_price
    }