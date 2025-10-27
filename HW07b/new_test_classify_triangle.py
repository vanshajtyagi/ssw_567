"""
Comprehensive Test Suite for Triangle Classification 

Author: Vanshaj Tyagi
Date: October 27, 2025

This test suite covers all edge cases and boundary conditions including:
- All triangle types (Equilateral, Isosceles, Scalene)
- Right triangles (all combinations and Pythagorean triples)
- Invalid inputs (negative, zero, non-numeric, NaN, infinity)
- Boundary conditions (degenerate triangles, very small/large numbers)
- Floating point precision
- Input permutations
- Type validation

Total Tests: 50+ comprehensive test cases
"""

import pytest
import math
from new_classify_triangle import classify_triangle


class TestTriangleClassification:
    """Comprehensive test class for triangle classification functionality"""
   
    def test_equilateral_triangles(self):
        """Test equilateral triangles (all sides equal)"""
        assert classify_triangle(1, 1, 1) == "Equilateral"  # T01
        assert classify_triangle(5, 5, 5) == "Equilateral"  # T02
        assert classify_triangle(10, 10, 10) == "Equilateral"  # T03
        assert classify_triangle(0.5, 0.5, 0.5) == "Equilateral"  # T04
        assert classify_triangle(1000, 1000, 1000) == "Equilateral"  # T05
        assert classify_triangle(7, 7, 7) == "Equilateral"
        assert classify_triangle(45, 45, 45) == "Equilateral"
        assert classify_triangle(100, 100, 100) == "Equilateral"
    
    def test_equilateral_very_small(self):
        """Test equilateral with very small values (T35)"""
        assert classify_triangle(0.001, 0.001, 0.001) == "Equilateral"  # T35
        assert classify_triangle(0.0001, 0.0001, 0.0001) == "Equilateral"
    
    def test_equilateral_floating_point(self):
        """Test equilateral with floating point numbers"""
        assert classify_triangle(3.333, 3.333, 3.333) == "Equilateral"
        assert classify_triangle(7.5, 7.5, 7.5) == "Equilateral"
    
    def test_isosceles_triangles(self):
        """Test isosceles triangles (two sides equal)"""
        # Test all permutations of equal sides
        assert classify_triangle(5, 5, 8) == "Isosceles"  # T06
        assert classify_triangle(5, 8, 5) == "Isosceles"  # T07
        assert classify_triangle(8, 5, 5) == "Isosceles"  # T08
        assert classify_triangle(3, 3, 4) == "Isosceles"  # T09
        assert classify_triangle(10, 6, 10) == "Isosceles"  # T10
        assert classify_triangle(7, 10, 7) == "Isosceles"
    
    def test_isosceles_various_sizes(self):
        """Test isosceles with various sizes"""
        assert classify_triangle(2, 2, 3) == "Isosceles"
        assert classify_triangle(50, 50, 60) == "Isosceles"
        assert classify_triangle(100, 100, 150) == "Isosceles"
    
    def test_isosceles_boundary(self):
        """Test isosceles near triangle inequality boundary (T49)"""
        assert classify_triangle(5, 5, 9.99) == "Isosceles"  # T49
        assert classify_triangle(10, 10, 19.9) == "Isosceles"
    
    def test_scalene_triangles(self):
        """Test scalene triangles (all sides different)"""
        assert classify_triangle(3, 7, 5) == "Scalene"  # T11
        assert classify_triangle(4, 6, 8) == "Scalene"  # T12
        assert classify_triangle(2, 3, 4) == "Scalene"  # T13
        assert classify_triangle(6, 10, 14) == "Scalene"
        assert classify_triangle(5, 9, 7) == "Scalene"
    
    def test_scalene_various_sizes(self):
        """Test scalene with various sizes"""
        assert classify_triangle(6, 7, 8) == "Scalene"
        assert classify_triangle(10, 11, 12) == "Scalene"
        assert classify_triangle(100, 150, 200) == "Scalene"
    
    def test_scalene_very_small(self):
        """Test scalene with very small values (T50)"""
        assert classify_triangle(0.0001, 0.0002, 0.00025) == "Scalene"  # T50
    
    def test_right_triangles_classic(self):
        """Test classic Pythagorean triples (scalene right)"""
        # 3-4-5 triple (all permutations)
        assert classify_triangle(3, 4, 5) == "Scalene Right"  # T14
        assert classify_triangle(4, 3, 5) == "Scalene Right"  # T15
        assert classify_triangle(5, 3, 4) == "Scalene Right"  # T16
        assert classify_triangle(3, 5, 4) == "Scalene Right"
        assert classify_triangle(4, 5, 3) == "Scalene Right"
        assert classify_triangle(5, 4, 3) == "Scalene Right"
    
    def test_right_triangles_pythagorean_triples(self):
        """Test various Pythagorean triples"""
        # 5-12-13 triple
        assert classify_triangle(5, 12, 13) == "Scalene Right"  # T17
        assert classify_triangle(12, 5, 13) == "Scalene Right"
        
        # 8-15-17 triple
        assert classify_triangle(8, 15, 17) == "Scalene Right"  # T18
        assert classify_triangle(15, 8, 17) == "Scalene Right"
        
        # 7-24-25 triple
        assert classify_triangle(7, 24, 25) == "Scalene Right"  # T19
        
        # 20-21-29 triple
        assert classify_triangle(20, 21, 29) == "Scalene Right"  # T46
    
    def test_right_triangles_scaled(self):
        """Test scaled Pythagorean triples"""
        # 3-4-5 scaled by 2 = 6-8-10
        assert classify_triangle(6, 8, 10) == "Scalene Right"  # T36
        
        # 3-4-5 scaled by 10 = 30-40-50
        assert classify_triangle(30, 40, 50) == "Scalene Right"  # T37
        
        # 3-4-5 scaled by 100 = 300-400-500
        assert classify_triangle(300, 400, 500) == "Scalene Right"  # T22
    
    def test_right_triangles_floating_point(self):
        """Test right triangles with floating point"""
        # 1.5-2-2.5 (scaled 3-4-5)
        assert classify_triangle(1.5, 2, 2.5) == "Scalene Right"  # T47
        
        # 0.3-0.4-0.5 (scaled 3-4-5)
        assert classify_triangle(0.3, 0.4, 0.5) == "Scalene Right"  # T48
    
    def test_isosceles_right_triangles(self):
        """Test isosceles right triangles (45-45-90)"""
        # 1-1-√2
        assert classify_triangle(1, 1, math.sqrt(2)) == "Isosceles Right"  # T20
        assert classify_triangle(1, math.sqrt(2), 1) == "Isosceles Right"
        assert classify_triangle(math.sqrt(2), 1, 1) == "Isosceles Right"
        
        # 5-5-√50
        assert classify_triangle(5, 5, math.sqrt(50)) == "Isosceles Right"  # T21
        assert classify_triangle(5, math.sqrt(50), 5) == "Isosceles Right"
        
        # 2-2-√8
        assert classify_triangle(2, 2, math.sqrt(8)) == "Isosceles Right"  # T38
        
        # 3-3-√18
        assert classify_triangle(3, 3, math.sqrt(18)) == "Isosceles Right"  # T39
    
    def test_isosceles_right_additional(self):
        """Test additional isosceles right triangles"""
        # 10-10-√200
        assert classify_triangle(10, 10, math.sqrt(200)) == "Isosceles Right"
        
        # 7-7-√98
        assert classify_triangle(7, 7, math.sqrt(98)) == "Isosceles Right"
    
    def test_invalid_negative_single(self):
        """Test triangles with one negative side"""
        assert classify_triangle(-1, 2, 2) == "Invalid input: All sides must be positive"  # T23
        assert classify_triangle(2, -1, 2) == "Invalid input: All sides must be positive"
        assert classify_triangle(2, 2, -1) == "Invalid input: All sides must be positive"
    
    def test_invalid_negative_multiple(self):
        """Test triangles with multiple negative sides"""
        assert classify_triangle(5, -5, 8) == "Invalid input: All sides must be positive"  # T24
        assert classify_triangle(-1, 2, -3) == "Invalid input: All sides must be positive"
        assert classify_triangle(1, -2, -3) == "Invalid input: All sides must be positive"
    
    def test_invalid_all_negative(self):
        """Test all negative sides"""
        assert classify_triangle(-1, -2, -3) == "Invalid input: All sides must be positive"  # T25
        assert classify_triangle(-5, -5, -5) == "Invalid input: All sides must be positive"
    
    def test_invalid_zero_single(self):
        """Test triangles with one zero side"""
        assert classify_triangle(0, 5, 5) == "Invalid input: All sides must be positive"  # T26
        assert classify_triangle(5, 0, 5) == "Invalid input: All sides must be positive"  # T28
        assert classify_triangle(5, 5, 0) == "Invalid input: All sides must be positive"
    
    def test_invalid_all_zero(self):
        """Test all zero sides"""
        assert classify_triangle(0, 0, 0) == "Invalid input: All sides must be positive"  # T27
    
    def test_invalid_zero_multiple(self):
        """Test multiple zero sides"""
        assert classify_triangle(0, 0, 5) == "Invalid input: All sides must be positive"
        assert classify_triangle(0, 5, 0) == "Invalid input: All sides must be positive"
    
    def test_invalid_string_input(self):
        """Test non-numeric string inputs"""
        assert classify_triangle("a", "b", "c") == "Invalid input: Sides must be numeric"  # T40
        assert classify_triangle("five", "six", "seven") == "Invalid input: Sides must be numeric"
    
    def test_invalid_mixed_type_input(self):
        """Test mixed type inputs"""
        # Should convert string "6" to float
        assert classify_triangle(5, "6", 7) == "Scalene"  # T42
        assert classify_triangle("5", 6, 7) == "Scalene"
        assert classify_triangle(5, 6, "7") == "Scalene"
    
    def test_invalid_none_input(self):
        """Test None inputs"""
        assert classify_triangle(None, 5, 5) == "Invalid input: Sides must be numeric"  # T41
        assert classify_triangle(5, None, 5) == "Invalid input: Sides must be numeric"
        assert classify_triangle(5, 5, None) == "Invalid input: Sides must be numeric"
    
    def test_invalid_nan_input(self):
        """Test NaN inputs"""
        assert classify_triangle(float('nan'), 5, 5) == "Invalid input: Sides must be numeric"  # T44
        assert classify_triangle(5, float('nan'), 5) == "Invalid input: Sides must be numeric"
    
    def test_invalid_infinity_input(self):
        """Test infinity inputs"""
        assert classify_triangle(float('inf'), 5, 5) == "Invalid input: Sides cannot be infinite"  # T43
        assert classify_triangle(5, float('inf'), 5) == "Invalid input: Sides cannot be infinite"
        assert classify_triangle(5, 5, float('inf')) == "Invalid input: Sides cannot be infinite"
    
    def test_not_triangle_one_side_too_long(self):
        """Test where one side is too long"""
        assert classify_triangle(1, 2, 10) == "Not a triangle"  # T29
        assert classify_triangle(1, 10, 2) == "Not a triangle"  # T30
        assert classify_triangle(10, 1, 2) == "Not a triangle"  # T31
        assert classify_triangle(1, 1, 3) == "Not a triangle"  # T32
    
    def test_not_triangle_degenerate(self):
        """Test degenerate triangles (a + b = c)"""
        assert classify_triangle(1, 2, 3) == "Not a triangle"  # T33
        assert classify_triangle(2, 3, 5) == "Not a triangle"
        assert classify_triangle(5, 5, 10) == "Not a triangle"  # T34
        assert classify_triangle(10, 5, 5) == "Not a triangle"
    
    def test_not_triangle_large_gap(self):
        """Test triangles with large gaps"""
        assert classify_triangle(5, 5, 20) == "Not a triangle"
        assert classify_triangle(1, 100, 2) == "Not a triangle"
    
    def test_boundary_very_large_numbers(self):
        """Test very large numbers"""
        assert classify_triangle(10000, 10000, 10000) == "Equilateral"
        assert classify_triangle(100000, 100000, 150000) == "Isosceles"
        assert classify_triangle(3000, 4000, 5000) == "Scalene Right"
        assert classify_triangle(1e10, 1e10, 1e10) == "Equilateral"  # T45
    
    def test_floating_point_precision(self):
        """Test floating point precision"""
        # Test that small differences are handled correctly
        assert classify_triangle(3.0, 3.0, 3.0) == "Equilateral"
        assert classify_triangle(5.0, 5.0, 8.0) == "Isosceles"
        
        # Test calculated hypotenuse
        a, b = 3.0, 4.0
        c = math.sqrt(a**2 + b**2)
        assert classify_triangle(a, b, c) == "Scalene Right"


# Standalone test for quick sanity check
def test_quick_sanity_check():
    """Quick sanity check for basic functionality"""
    assert classify_triangle(3, 4, 5) == "Scalene Right"
    assert classify_triangle(5, 5, 5) == "Equilateral"
    assert classify_triangle(5, 5, 8) == "Isosceles"
    assert classify_triangle(-1, 2, 3) == "Invalid input: All sides must be positive"
    assert classify_triangle(1, 2, 10) == "Not a triangle"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
