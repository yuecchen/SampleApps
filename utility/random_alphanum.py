#!/usr/bin/env python3

import random

def random_alphanum():
	return ''.join(random.choice('0123456789abcded') for i in range(6))


print(random_alphanum())
