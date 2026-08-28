from backend.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

password = "PredictGuard123"

hashed = hash_password(password)

print("Hashed Password:")
print(hashed)

print()

print("Password Valid:")
print(verify_password(password, hashed))

print()

token = create_access_token(
    {"sub": "admin@predictguard.com"}
)

print("JWT Token:")
print(token)
