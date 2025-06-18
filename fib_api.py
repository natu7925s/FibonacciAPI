from fastapi import FastAPI, HTTPException
import sqlite3

DB_PATH = "./fibonacci.db"

app = FastAPI()

def get_fib(n: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT value FROM fibonacci WHERE n=?", (n,))
    row = cur.fetchone()
    conn.close()
    if row:
        return row[0]
    else:
        return None

def get_max_n():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT MAX(n) FROM fibonacci")
    max_n = cur.fetchone()[0]
    conn.close()
    return max_n if max_n is not None else 0

@app.get("/")
def read_root():
    return {"message": "フィボナッチAPIです"}

@app.get("/fib/{n}")
def get_fibonacci(n: int):
    result = get_fib(n)
    if result is None:
        raise HTTPException(status_code=404, detail="まだその値は計算されていません")
    return {"n": n, "value": result}

@app.get("/max")
def get_latest():
    return {"max_n": get_max_n()}
