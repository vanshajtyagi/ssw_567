"""
Triangle Classification Program
Author: Vanshaj Tyagi
Date: 17th September 2025

This module contains a function to classify triangles based on side lengths.
"""
import math

def classify_triangle(a, b, c):
    """
    Classify a triangle based on the lengths of its three sides.

    Args:
        a, b, c: The lengths of the three sides of the triangle

    Returns:
        A string describing the triangle classification:
        - "Equilateral" for triangles with all sides equal
        - "Isosceles" for triangles with two sides equal  
        - "Scalene" for triangles with all sides different
        - Appends "Right" if it's also a right triangle
        - "Invalid input: All sides must be positive" for invalid input
        - "Not a triangle" if sides don't satisfy triangle inequality
    """
    # Input validation - all sides must be positive
    if a <= 0 or b <= 0 or c <= 0:
        return "Invalid input: All sides must be positive"

    # Check triangle inequality theorem
    if a + b <= c or a + c <= b or b + c <= a:
        return "Not a triangle"

    # Sort the sides to make right triangle checking easier
    sides = sorted([a, b, c])
    side1, side2, side3 = sides[0], sides[1], sides[2]

    # Check for right triangle using Pythagorean theorem
    # Using small tolerance for floating point comparison
    is_right = abs(side1**2 + side2**2 - side3**2) < 1e-10

    # Classify by side lengths
    if a == b == c:
        triangle_type = "Equilateral"
    elif a == b or b == c or a == c:
        triangle_type = "Isosceles"
    else:
        triangle_type = "Scalene"

    # Combine classifications
    if is_right:
        return f"{triangle_type} Right"
    else:
        return triangle_type

def main():
    """
    Main function to demonstrate the triangle classifier
    """
    #  Test various cases
test_cases = [
    ("Equilateral", (5, 5, 5)),
    ("Isosceles", (5, 5, 8)), 
    ("Scalene", (6, 7, 8)),
    ("Right Scalene", (3, 4, 5)),
    ("Right Isosceles", (1, 1, 1.4142135623730951)),  # sqrt(2)
    ("Invalid negative", (-1, 2, 3)),
    ("Invalid zero", (0, 5, 5)),
    ("Not a triangle", (1, 2, 10)),
    ("Large numbers", (300, 400, 500)),
]

print("\nManual Test Results:")
print("-" * 40)
for description, (a, b, c) in test_cases:
    result = classify_triangle(a, b, c)
    print(f"{description:15}: ({a}, {b}, {c}) -> {result}")

if __name__ == "__main__":
    main()