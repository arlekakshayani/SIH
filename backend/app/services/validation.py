class ValidationService:
    """
    Custom validation logic and helpers for flight data hygiene.
    """

    @staticmethod
    def validate_route_code(route: str) -> bool:
        parts = route.split("-")
        return len(parts) == 2 and len(parts[0]) == 3 and len(parts[1]) == 3
