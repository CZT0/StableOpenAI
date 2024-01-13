import random
import time
import unittest

from stable_openai.key import KeyManager


class TestKeyManager(unittest.TestCase):
    def setUp(self):
        # Initialize 100 keys for testing
        self.keys = ["key" + str(i) for i in range(100)]
        self.manager = KeyManager(self.keys)

        # Set random TTLs for some of the keys
        lower_ttl_range = (1, 5)  # Lower range for TTL
        higher_ttl_range = (10, 15)  # Higher range for TTL

        for key in self.keys:
            if random.random() < 0.5:
                # Set a lower TTL for half of the keys
                ttl = random.uniform(*lower_ttl_range)
            else:
                # Set a higher TTL for the other half
                ttl = random.uniform(*higher_ttl_range)
            self.manager.set_ttl(key, ttl)

    def test_concurrent_get_and_validity(self):
        # Wait for some time to let the TTL of some keys to expire
        time.sleep(7)  # Waiting time is between the two TTL ranges

        get_results = []
        for _ in range(100):
            # Attempt to get a key from the manager
            get_results.append(self.manager.get_key())

        # Verify that obtained keys should not include those with non-zero TTL
        for key in get_results:
            if key is not None:
                # Assert that the key's TTL must be zero
                self.assertTrue(self.manager.data[key] == 0,
                                f"Key {key} should not have been returned as its TTL is not yet 0")


if __name__ == "__main__":
    unittest.main()
