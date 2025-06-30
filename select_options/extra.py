def calc_ideal_columns(total_items: int, min_columns: int = 2, max_columns: int = 5, max_items: int | None = None) -> int:
    # sourcery skip: use-assigned-variable
    """
    Calculate the ideal number of columns for displaying a given number of items.

    Args:
        total_items (int): Total number of items to display.
        min_columns (int, optional): Minimum number of columns. Defaults to 2.
        max_columns (int, optional): Maximum number of columns. Defaults to 6.

    Returns:
        int: The ideal number of columns to use for displaying the items.
    """
    if max_items is not None and total_items > max_items:
        return max_columns
    
    best_columns: int = min_columns
    best_score: float = 1.0
    perfect_col: int | None = None

    for cols in range(min_columns, max_columns + 1):
        remainder = total_items % cols
        if remainder == 0:
            perfect_col = cols
            continue

        score = abs(remainder-cols) / cols
        if score < best_score:
            best_score = score
            best_columns = cols

    return perfect_col or best_columns