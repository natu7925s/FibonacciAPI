import sqlite3
import time
import os

import sys
sys.set_int_max_str_digits(100000) 

DB_PATH = "./fibonacci.db"
SLEEP_SEC = 0.01

# DBの初期化関数
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fibonacci (
            n INTEGER PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# 最後に保存されたnの取得
def get_last_n():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT MAX(n) FROM fibonacci")
    row = cur.fetchone()
    conn.close()
    return row[0] if row and row[0] is not None else -1

# 値の保存
def save_fib(n, value):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO fibonacci (n, value) VALUES (?, ?)", (n, str(value)))
    conn.commit()
    conn.close()

# メイン処理（ループ型、メモ化DB方式）
def background_calc():
    init_db()
    memo = {}

    # DBからデータを読み込みつつ、最大nを確認
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT n, value FROM fibonacci ORDER BY n")
    rows = cur.fetchall()
    for n, value in rows:
        memo[n] = int(value)
    conn.close()

    last_n = max(memo.keys(), default=-1)

    # 初期値セット
    if 0 not in memo:
        memo[0] = 0
        save_fib(0, 0)
    if 1 not in memo:
        memo[1] = 1
        save_fib(1, 1)

    # 継続して計算
    n = last_n + 1
    while True:
        memo[n] = memo[n - 1] + memo[n - 2]
        save_fib(n, memo[n])
        n += 1
        time.sleep(SLEEP_SEC)

if __name__ == "__main__":
    background_calc()
