import logging
import threading
import time
import random

from stable_openai.rw_lock import RWLock
from stable_openai.tools import singleton


# Singleton decorator ensures that only one instance of this class is created.
@singleton
class KeyManager:
    def __init__(self, api_keys: list):
        # Using a Read-Write lock to manage concurrent access to the keys.
        self.rw_lock = RWLock()
        # Initializing keys with a time-to-live (TTL) of 0.
        self.data = {key: 0 for key in api_keys}
        # Starting a thread to decrement TTL of keys over time.
        self.thread = threading.Thread(target=self.decrement_ttl)
        self.thread.start()

    def decrement_ttl(self):
        # Continuously decrements the TTL of keys.
        while True:
            with self.rw_lock.w_locked():  # Acquiring write lock.
                for key in self.data:
                    if self.data[key] > 0:
                        self.data[key] -= 1
            time.sleep(1)

    def get_key(self):
        # Retrieves a key with TTL of 0 (i.e., available for use).
        while True:
            with self.rw_lock.r_locked():  # Acquiring read lock.
                keys_with_ttl_zero = [key for key, ttl in self.data.items() if ttl == 0]
                if keys_with_ttl_zero:
                    return random.choice(keys_with_ttl_zero)
                elif not self.data:
                    raise ValueError("No available keys")

            min_ttl = self.get_min_ttl()
            logging.info(f"All keys have reached their limit, minimum waiting time is: {min_ttl} seconds")
            time.sleep(min_ttl)

    def set_ttl(self, key, ttl):
        # Sets the TTL for a given key.
        with self.rw_lock.w_locked():
            if key in self.data:
                self.data[key] = ttl

    def delete_key(self, key):
        # Deletes a key from the manager.
        with self.rw_lock.w_locked():
            if key in self.data:
                del self.data[key]

    def get_min_ttl(self):
        # Returns the minimum TTL among all keys.
        with self.rw_lock.r_locked():
            return min(self.data.values()) if self.data else 0
