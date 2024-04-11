import datetime
import sqlite3
import logging
import concurrent.futures
import random

def find_or_create_user_table(cur):
    res = cur.execute("SELECT name FROM sqlite_master")
    result = res.fetchall()
    for i in result:
        table_name = "".join(i)
        if table_name == "user":
            logging.info("table found")
            return
    cur.execute("CREATE TABLE user(email, username, created_at, updated_at)")
    logging.info("table created")

def find_or_create_db():
    con = sqlite3.connect("example.db")
    cur = con.cursor()
    logging.info("db created")
    find_or_create_user_table(cur)
    con.close()

def generate_word(length):
    consonants = "bcdfghjklmnpqrstvwxyz"
    vowels = "aeiou"
    return "".join(random.choice((consonants, vowels)[i%2]) for i in range(length))

def create_task(task_counter):
    logging.info("Thread %s: starting", task_counter)
    con = sqlite3.connect("example.db")
    cur = con.cursor()
    name = generate_word(random.randint(5,10))
    data = {
            "email": f"{name}@foo.bar",
            "username": f"{name}",
            "created_at": str(datetime.datetime.now()),
            "updated_at": str(datetime.datetime.now())
            }
    cur.execute("INSERT INTO user VALUES(:email, :username, :created_at, :updated_at)", data)
    con.commit()
    con.close()
    logging.info("Thread %s: finishing", task_counter)

def run_tasks(workers, num_tasks):
    logging.info(f"Running {workers} tasks at a time, with a total of {num_tasks} to run")
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(create_task, range(1, num_tasks+1))

if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO,
                        datefmt="%H:%M:%S")
    find_or_create_db()
    workers = 10
    num_tasks = 1000
    run_tasks(workers, num_tasks)

