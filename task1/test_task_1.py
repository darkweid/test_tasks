import unittest
from solution import strict

# Example function decorated with @strict
@strict
def sum_two(a: int, b: int) -> int:
    return a + b

class TestStrictDecorator(unittest.TestCase):
    def test_correct_types(self):
        """Test with correct argument types."""
        self.assertEqual(sum_two(1, 2), 3)

    def test_incorrect_types(self):
        """Test with incorrect argument types."""
        with self.assertRaises(TypeError):
            sum_two(1, 2.4)  # The second argument is float, expected int

    def test_multiple_incorrect_types(self):
        """Test with multiple incorrect arguments."""
        with self.assertRaises(TypeError):
            sum_two("1", "2")  # Both arguments are str, expected int

    def test_empty_arguments(self):
        """Test with no arguments passed."""
        with self.assertRaises(TypeError):
            sum_two()  # Missing required arguments

    def test_none_value(self):
        """Test with None value (should raise TypeError)."""
        with self.assertRaises(TypeError):
            sum_two(None, 2)  # None is not a valid argument for int

    def test_multiple_arguments(self):
        """Test a function with more than two arguments."""
        @strict
        def add_three(a: int, b: int, c: int) -> int:
            return a + b + c

        self.assertEqual(add_three(1, 2, 3), 6)

        with self.assertRaises(TypeError):
            add_three(1, "2", 3)  # Second argument is a string, expected int

    def test_return_type_annotation(self):
        """Test function with return type annotation."""
        @strict
        def multiply(a: int, b: int) -> float:
            return float(a * b)

        self.assertEqual(multiply(2, 3), 6.0)

        with self.assertRaises(TypeError):
            multiply(2, "3")  # Second argument is a string, expected int

    def test_bool_type(self):
        """Test with boolean argument."""
        @strict
        def and_operation(a: bool, b: bool) -> bool:
            return a and b

        self.assertEqual(and_operation(True, False), False)
        with self.assertRaises(TypeError):
            and_operation(True, 1)  # Second argument is int, expected bool

    def test_float_type(self):
        """Test with float argument."""
        @strict
        def divide(a: float, b: float) -> float:
            return a / b

        self.assertEqual(divide(6.0, 2.0), 3.0)
        with self.assertRaises(TypeError):
            divide(6.0, "2.0")  # Second argument is string, expected float

    def test_str_type(self):
        """Test with string argument."""
        @strict
        def concat(a: str, b: str) -> str:
            return a + b

        self.assertEqual(concat("Hello, ", "world!"), "Hello, world!")
        with self.assertRaises(TypeError):
            concat("Hello, ", 1)  # Second argument is an int, expected str

if __name__ == "__main__":
    unittest.main()
