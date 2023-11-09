from jose import jwt

secret = "8b6f544bbe19aacbd5590760926f7d3ed2347da2403e861f61aae82a5e6fa871"

payload = {
    "sub": "example@test.com",
    "username": "vadim",
    "role": "moderator",
}

token = jwt.encode(payload, secret, algorithm=jwt.ALGORITHMS.HS512)
print(token)
