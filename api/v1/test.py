#!/usr/bin/env python3
import hashlib

def grav(email, size=100):
    email_hash = hashlib.md5(email.encode()).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?s={size}"

print(grav('lekanmojibola@gmail.com'))