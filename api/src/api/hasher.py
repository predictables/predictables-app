from passlib.hash import pbkdf2_sha256

hashing_kwargs = {"salt_size": 10}

Hasher = pbkdf2_sha256.using(**hashing_kwargs)
