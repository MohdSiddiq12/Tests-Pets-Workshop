def validate_dog_age(age: int) -> None:
    """
    Validates that the dog's age is between 0 and 20 (inclusive).
    Raises ValueError if age is outside this range.
    """
    if not (0 <= age <= 20):
        raise ValueError("Dog age must be between 0 and 20.")
