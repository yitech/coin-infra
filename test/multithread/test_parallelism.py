import unittest
import time
from general.mutithread import Parallelism


class TestParallelism(unittest.TestCase):
    def test_add_function(self):
        results = []

        # Job to add two numbers and append the result to the results list
        def add_and_store(a, b):
            result = a + b
            results.append(result)

        # Initialize thread pool with 4 workers
        pool = Parallelism(4)

        # Data for testing
        test_data = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
                     (6, 7), (7, 8), (8, 9), (9, 10), (10, 11)]

        # Add jobs to the thread pool using the test data
        for data in test_data:
            pool.add_job(add_and_store, data)

        # Wait for all jobs to complete
        pool.wait_completion()

        # Check that all jobs were executed
        self.assertEqual(len(results), 10)

        # Validate the results of the addition
        expected_results = [sum(data) for data in test_data]
        self.assertEqual(sorted(results), expected_results)


if __name__ == "__main__":
    unittest.main()