# import os
# import redis
# from fastapi import FastAPI

# app = FastAPI()

# REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
# REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

# r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


# @app.post("/hit/{key}")
# def hit(key: str):
#     count = r.incr(f"counter:{key}")
#     return {"key": key, "count": count}


# @app.get("/count/{key}")
# def count(key: str):
#     value = r.get(f"counter:{key}")
#     return {"key": key, "count": int(value) if value is not None else 0}


# @app.get("/healthz")
# def healthz():
#     try:
#         pong = r.ping()
#         return {"status": "ok", "redis": "up" if pong else "down"}
#     except Exception:
#         return {"status": "ok", "redis": "down"}


import os
from fastapi import FastAPI, HTTPException
from redis import Redis

app = FastAPI()

# Check if Render's full connection string is available, otherwise use host/port
REDIS_URL = os.getenv("REDIS_URL")

if REDIS_URL:
    redis_client = Redis.from_url(REDIS_URL, decode_responses=True)
else:
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    redis_client = Redis(host=REDIS_HOST, port=6379, decode_responses=True)

@app.post("/hit/{key}")
def hit(key: str):
    count = r.incr(key)
    return {"key": key, "count": count}

@app.get("/count/{key}")
def count(key: str):
    value = r.get(key)
    return {
        "key": key,
        "count": int(value) if value else 0
    }

@app.get("/healthz")
def health():
    try:
        r.ping()
        return {"status":"ok","redis":"up"}
    except:
        return {"status":"error","redis":"down"}
