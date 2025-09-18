import pytest
import math
from classify_triangle import classify_triangle

class TestTriangleClassification:
    """Test class for triangle classification functionality"""

    def test_equilateral_triangles(self):
        """Test equilateral triangles (all sides equal)"""
        assert classify_triangle(1, 1, 1) == "Equilateral"
        assert classify_triangle(5, 5, 5) == "Equilateral"
        assert classify_triangle(10, 10, 10) == "Equilateral"
        assert classify_triangle(0.5, 0.5, 0.5) == "Equilateral"
        assert classify_triangle(100, 100, 100) == "Equilateral"
        assert classify_triangle(7, 7, 7) == "Equilateral"

    def test_isosceles_triangles(self):
        """Test isosceles triangles (two sides equal)"""
        # Test all permutations of equal sides
        assert classify_triangle(5, 5, 8) == "Isosceles"
        assert classify_triangle(5, 8, 5) == "Isosceles"
        assert classify_triangle(8, 5, 5) == "Isosceles"
        assert classify_triangle(3, 3, 4) == "Isosceles"
        assert classify_triangle(10, 6, 10) == "Isosceles"
        assert classify_triangle(7, 10, 7) == "Isosceles"

    def test_scalene_triangles(self):
        """Test scalene triangles (all sides different)"""
        assert classify_triangle(3, 7, 5) == "Scalene"
        assert classify_triangle(4, 6, 8) == "Scalene"
        assert classify_triangle(2, 3, 4) == "Scalene"
        assert classify_triangle(6, 10, 14) == "Scalene"
        assert classify_triangle(5, 9, 7) == "Scalene"

    def test_right_triangles(self):
        """Test right triangles (satisfy Pythagorean theorem)"""
        # Classic Pythagorean triples
        assert classify_triangle(3, 4, 5) == "Scalene Right"
        assert classify_triangle(4, 3, 5) == "Scalene Right"
        assert classify_triangle(5, 3, 4) == "Scalene Right"
    
    def test_triangle_cases(self):
        """Test various triangle cases including edge cases"""
        assert classify_triangle(-1, 2, 2) == "Invalid input: All sides must be positive"
        assert classify_triangle(1, 2, 4) == "Not a triangle"
        assert classify_triangle(0, 0, 0) == "Invalid input: All sides must be positive"
        
