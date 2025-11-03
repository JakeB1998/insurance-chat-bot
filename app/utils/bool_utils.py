def to_bool(value):
    """
    Convert any primitive to a boolean.

    Strings are interpreted case-insensitively:
      - True values: 'true', '1', 'yes', 'y', 't'
      - False values: 'false', '0', 'no', 'n', 'f', '', None
    Numbers: 0 is False, everything else True
    Booleans: returned as-is
    Other objects: use Python's default truthiness
    """
    if isinstance(value, bool):
        return value

    if value is None:
        return False

    if isinstance(value, (int, float)):
        return value != 0

    if isinstance(value, str):
        val = value.strip().lower()
        if val in ("true", "1", "yes", "y", "t"):
            return True
        elif val in ("false", "0", "no", "n", "f", ""):
            return False
        else:
            # Any other non-empty string -> True
            return True

    # fallback to Python's truthiness
    return bool(value)
