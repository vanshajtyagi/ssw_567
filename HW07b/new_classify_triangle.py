"""
Triangle Classification Program 

Author: Vanshaj Tyagi
Date: October 27, 2025

This module contains an enhanced function to classify triangles based on side lengths.
All edge cases and potential bugs have been addressed per comprehensive testing.

Fixes Applied:
- Added type validation for non-numeric inputs
- Added NaN and infinity checks
- Added adaptive tolerance for floating point comparisons
- Enhanced input validation with clear error messages
- Added maximum size constraint
- Improved floating point equality checking
"""

import math

def classify_triangle(a, b, c):
    """
    Classify a triangle based on the lengths of its three sides.
    
    Args:
        a, b, c: The lengths of the three sides of the triangle (int or float)
    
    Returns:
        A string describing the triangle classification:
        - "Equilateral" for triangles with all sides equal
        - "Isosceles" for triangles with two sides equal
        - "Scalene" for triangles with all sides different
        - Appends " Right" if it's also a right triangle
        - "Invalid input: All sides must be positive" for non-positive input
        - "Invalid input: Sides must be numeric" for non-numeric input
        - "Invalid input: Sides cannot be infinite" for infinity values
        - "Invalid input: Side lengths too large" for extremely large values
        - "Not a triangle" if sides don't satisfy triangle inequality
    
    Edge Cases Handled:
        - String inputs, None, non-numeric types
        - NaN and infinity values
        - Very small positive numbers (0.0001)
        - Very large numbers (with upper limit)
        - Degenerate triangles (a + b = c)
        - Floating point precision issues
    """
    
    # Type validation - ensure all inputs are numeric
    try:
        a = float(a)
        b = float(b)
        c = float(c)
    except (TypeError, ValueError):
        return "Invalid input: Sides must be numeric"
    
    # Check for NaN or infinity
    if math.isnan(a) or math.isnan(b) or math.isnan(c):
        return "Invalid input: Sides must be numeric"
    
    if math.isinf(a) or math.isinf(b) or math.isinf(c):
        return "Invalid input: Sides cannot be infinite"
    
    # Input validation - all sides must be positive
    if a <= 0 or b <= 0 or c <= 0:
        return "Invalid input: All sides must be positive"
    
    # Check for reasonable maximum value (optional constraint)
    MAX_SIDE_LENGTH = 1e10
    if a > MAX_SIDE_LENGTH or b > MAX_SIDE_LENGTH or c > MAX_SIDE_LENGTH:
        return "Invalid input: Side lengths too large"
    
    # Check triangle inequality theorem
    # Using strict inequality to reject degenerate triangles
    if a + b <= c or a + c <= b or b + c <= a:
        return "Not a triangle"
    
    # Sort the sides to make right triangle checking easier
    sides = sorted([a, b, c])
    side1, side2, side3 = sides[0], sides[1], sides[2]
    
    # Check for right triangle using Pythagorean theorem
    # Using adaptive tolerance for floating point comparison
    # Tolerance scales with the magnitude of the numbers
    tolerance = max(1e-10, 1e-10 * side3**2)
    is_right = abs(side1**2 + side2**2 - side3**2) < tolerance
    
    # Use a more robust equality check for floating point numbers
    epsilon = 1e-10
    
    def almost_equal(x, y):
        """Check if two numbers are almost equal within tolerance."""
        return abs(x - y) < epsilon
    
    # Classify by side lengths
    if almost_equal(a, b) and almost_equal(b, c):
        triangle_type = "Equilateral"
    elif almost_equal(a, b) or almost_equal(b, c) or almost_equal(a, c):
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
    Main function to demonstrate the enhanced triangle classifier
    """
    
    # Test various cases including all edge cases
    test_cases = [
        # Valid triangles
        ("Equilateral", (5, 5, 5)),
        ("Equilateral Small", (0.5, 0.5, 0.5)),
        ("Equilateral Large", (1000, 1000, 1000)),
        
        ("Isosceles", (5, 5, 8)),
        ("Isosceles Permutation 1", (5, 8, 5)),
        ("Isosceles Permutation 2", (8, 5, 5)),
        
        ("Scalene", (6, 7, 8)),
        ("Scalene Small", (2, 3, 4)),
        
        # Right triangles
        ("Scalene Right (3-4-5)", (3, 4, 5)),
        ("Scalene Right (5-12-13)", (5, 12, 13)),
        ("Scalene Right (8-15-17)", (8, 15, 17)),
        ("Scalene Right Permutation", (4, 5, 3)),
        ("Isosceles Right", (1, 1, math.sqrt(2))),
        ("Isosceles Right (5-5-√50)", (5, 5, math.sqrt(50))),
        ("Right Large", (300, 400, 500)),
        
        # Invalid inputs - negative
        ("Invalid Negative", (-1, 2, 3)),
        ("Invalid All Negative", (-1, -2, -3)),
        ("Invalid Mixed Negative", (5, -5, 8)),
        
        # Invalid inputs - zero
        ("Invalid Zero", (0, 5, 5)),
        ("Invalid All Zero", (0, 0, 0)),
        
        # Not a triangle (violates triangle inequality)
        ("Not Triangle (1,2,10)", (1, 2, 10)),
        ("Not Triangle (1,1,3)", (1, 1, 3)),
        
        # Degenerate triangles (boundary case: a + b = c)
        ("Degenerate Triangle", (1, 2, 3)),
        ("Degenerate Triangle 2", (5, 5, 10)),
        
        # Floating point numbers
        ("Float Equilateral", (3.5, 3.5, 3.5)),
        ("Float Scalene", (2.3, 4.7, 5.9)),
        
        # Very small positive numbers
        ("Very Small", (0.001, 0.001, 0.001)),
    ]
    
    print("\n" + "="*80)
    print("TRIANGLE CLASSIFIER - COMPREHENSIVE TEST RESULTS")
    print("="*80 + "\n")
    
    for description, (a, b, c) in test_cases:
        result = classify_triangle(a, b, c)
        print(f"{description:30}: ({a:>5}, {b:>5}, {c:>5}) -> {result}")
    
    # Additional edge case tests
    print("\n" + "="*80)
    print("ADDITIONAL EDGE CASE TESTS")
    print("="*80 + "\n")
    
    edge_cases = [
        ("String Input", ("a", "b", "c")),
        ("None Input", (None, 5, 5)),
        ("Mixed Types", (5, "6", 7)),
        ("Infinity Input", (float('inf'), 5, 5)),
        ("NaN Input", (float('nan'), 5, 5)),
    ]
    
    for description, (a, b, c) in edge_cases:
        result = classify_triangle(a, b, c)
        print(f"{description:30}: ({a}, {b}, {c}) -> {result}")


if __name__ == "__main__":
    main()
