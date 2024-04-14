#!/bin/env python

import sys
import datetime
import sqlite3
import concurrent.futures
import random
from rich.progress import Progress, TaskID
from rich.console import Console

console = Console()

def find_or_create_user_table(cur: sqlite3.Cursor) -> None:
    res = cur.execute("SELECT name FROM sqlite_master")
    result = res.fetchall()
    for i in result:
        table_name = "".join(i)
        if table_name == "user":
            console.log(f"user table found")
            return
    cur.execute("CREATE TABLE user(email, username, created_at, updated_at)")
    console.log("user table created")


def find_or_create_db_and_table(name: str) -> None:
    con = sqlite3.connect(name)
    cur = con.cursor()
    console.log(f"db {name} created")
    find_or_create_user_table(cur)
    con.close()


def generate_word(length: int) -> str:
    consonants = "bcdfghjklmnpqrstvwxyz"
    vowels = "aeiou"
    return "".join(random.choice((consonants, vowels)[i%2]) for i in range(length))


def create_task(db_name: str, progress: Progress, task_id: TaskID) -> None:
    con = sqlite3.connect(db_name)
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
    progress.update(task_id, advance=1)


def run_tasks(db_name: str, workers: int, num_tasks: int) -> None:
    console.log(f"Running {workers} tasks at a time, with a total of {num_tasks} to run")
    with Progress(transient=True) as progress:
        creating_users = progress.add_task(f"[green]Adding {num_tasks} users to the db...", 
                                           total=num_tasks)
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            for _ in range(1, num_tasks+1):
                executor.submit(create_task, db_name, progress, creating_users)

        if progress.finished:
            progress.console.print(f"[bright_green]{num_tasks} users were added to the database!")
            progress.console.print(f"All tasks completed.")


if __name__ == "__main__":
    workers = 10
    num_tasks = 1000

    # Optional arguments to run the script
    if sys.argv[1:]:
        args = sys.argv[1:]
        args_dict = {}
        for i in range(len(args)):
            if args[i] == '-h' or args[i] == '--help':
                args_dict[args[i]] = None
            if i%2 == 1:
                args_dict[args[i-1]] = args[i]

        if '-h' in args_dict or '--help' in args_dict:
            console.rule("[bold cyan]Help")
            console.print("[bold magenta]-h[/] or [bold magenta]--help[/] - Print this help")
            console.print("[bold magenta]-w[/] or [bold magenta]--workers[/] - [bold yellow][TYPE] integer[/] - [bold blue][DEFAULT] 10[/] - Define the ammount of workers (how many threads will be assigned).")
            console.print("[bold magenta]-t[/] or [bold magenta]--tasks[/] - [bold yellow][TYPE] integer[/] - [bold blue][DEFAULT] 1000[/] - Define the ammount of tasks that will run (how many users will be added to the db).")
            sys.exit(0)

        if '-w' in args_dict and '--workers' in args_dict:
            console.print("[bold red][ERROR] Duplicated parameters:[/] [bold magenta]'--workers'[/] and [bold magenta]'-w'[/] can't be used at the same time.")
            sys.exit(2)
        if '-t' in args_dict and '--tasks' in args_dict:
            console.print("[bold red][ERROR] Duplicated parameters:[/] [bold magenta]'--tasks'[/] and [bold magenta]'-t'[/] can't be used at the same time.")
            sys.exit(2)

        if '-w' in args_dict or '--workers' in args_dict:
            try:
                if '-w' in args_dict:
                    workers = int(args_dict['-w'])
                else:
                    workers = int(args_dict['--workers'])
            except ValueError as e:
                console.print(f"[bold red][ERROR] workers should be an integer and not [/]")
                sys.exit(2)
        if '-t' in args_dict or '--tasks' in args_dict:
            try:
                if '-t' in args_dict:
                    num_tasks = int(args_dict['-t'])
                else:
                    num_tasks = int(args_dict['--tasks'])
            except ValueError as e:
                console.print("[bold red][ERROR] tasks should be an integer.[/]")
                sys.exit(2)

    else:
        console.print(f"Default number of workers and tasks set to run.\nWorkers: {workers}\nTasks: {num_tasks}")

    find_or_create_db_and_table("example.db")
    run_tasks("example.db", workers, num_tasks)

