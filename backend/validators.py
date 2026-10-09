MAX_ACTIVE_BOOKINGS = 3


def has_reached_booking_limit(active_booking_count: int) -> bool:
    """Return True if the member already has the maximum active bookings."""
    return active_booking_count >= MAX_ACTIVE_BOOKINGS