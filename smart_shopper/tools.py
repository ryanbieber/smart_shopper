"""Random tools used by this."""
import time
import random

def jitter(max_time: int = 5):
    time.sleep(random.randint(0, max_time))
