import logging
import pytest
import time
from app.calculator import Calculator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestCalculator:
    def setup_method(self):
        self.calc = Calculator()

    def log_and_assert(self, test_name, operation_str, result, expected):
        logger.info(f"{test_name} Result: {result}")
        if result == expected:
            logger.info(f"✅ {test_name} test passed!")
        else:
            logger.error(f"❌ {test_name} test failed! Expected {expected}, but got {result}")
            assert result == expected, f"{test_name} failed: Expected {expected}, got {result}"

    def test_add(self):
        a, b = 1, 3
        test_name = "Addition"
        logger.info(f"Testing addition: {a} + {b}")
        start_time = time.time()
        result = self.calc.add(a, b)
        end_time = time.time()
        logger.info(f"Addition took {end_time - start_time:.4f} seconds")
        self.log_and_assert(test_name, f"{a} + {b}", result, 3)

    def test_subtract(self):
        a, b = 5, 2
        test_name = "Subtraction"
        logger.info(f"Testing subtraction: {a} - {b}")
        start_time = time.time()
        result = self.calc.subtract(a, b)
        end_time = time.time()
        logger.info(f"Subtraction took {end_time - start_time:.4f} seconds")
        self.log_and_assert(test_name, f"{a} - {b}", result, 3)

    def test_multiply(self):
        a, b = 2, 3
        test_name = "Multiplication"
        logger.info(f"Testing multiplication: {a} * {b}")
        start_time = time.time()
        result = self.calc.multiply(a, b)
        end_time = time.time()
        logger.info(f"Multiplication took {end_time - start_time:.4f} seconds")
        self.log_and_assert(test_name, f"{a} * {b}", result, 6)

    def test_divide(self):
        a, b = 10, 2
        test_name = "Division"
        logger.info(f"Testing division: {a} / {b}")
        start_time = time.time()
        result = self.calc.divide(a, b)
        end_time = time.time()
        logger.info(f"Division took {end_time - start_time:.4f} seconds")
        self.log_and_assert(test_name, f"{a} / {b}", result, 5)

    def test_divide_by_zero(self):
        a, b = 1, 0
        test_name = "Divide by Zero"
        logger.info(f"Testing divide by zero: {a} / {b}")
        start_time = time.time()
        try:
            self.calc.divide(a, b)
            logger.error("❌ Divide by zero did not raise ValueError as expected.")
            assert False, "Expected ValueError for divide by zero"
        except ValueError as e:
            end_time = time.time()
            logger.info(f"Divide by zero test took {end_time - start_time:.4f} seconds")
            logger.info(f"Expected error: {str(e)}")
            logger.info(f"✅ {test_name} test passed!")
