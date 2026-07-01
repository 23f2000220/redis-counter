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
def hit_key(key: str):
    try:
        # INCR automatically creates the key if it doesn't exist and increments it atomically
        new_count = redis_client.incr(key)
        return {"key": key, "count": new_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")

@app.get("/count/{key}")
def get_count(key: str):
    try:
        count = redis_client.get(key)
        # If the key is unseen, return 0 as required
        if count is None:
            return {"key": key, "count": 0}
        return {"key": key, "count": int(count)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")

@app.get("/healthz")
def health_check():
    try:
        # Actively ping Redis to verify the connection is up
        if redis_client.ping():
            return {"status": "ok", "redis": "up"}
        raise Exception("Ping failed")
    except Exception:
        raise HTTPException(status_code=500, detail={"status": "error", "redis": "down"})


# @app.post("/hit/{key}")
# def hit(key: str):
#     count = r.incr(key)
#     return {"key": key, "count": count}

# @app.get("/count/{key}")
# def count(key: str):
#     value = r.get(key)
#     return {
#         "key": key,
#         "count": int(value) if value else 0
#     }

# @app.get("/healthz")
# def health():
#     try:
#         r.ping()
#         return {"status":"ok","redis":"up"}
#     except:
#         return {"status":"error","redis":"down"}
