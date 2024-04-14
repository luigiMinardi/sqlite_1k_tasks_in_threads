import sqlite3
import unittest
import os

from rich.progress import Progress

from main import find_or_create_db_and_table, find_or_create_user_table, generate_word, run_tasks, create_task

class TestScript(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = "test.db"
        find_or_create_db_and_table(cls.db)
        cls.con = sqlite3.connect(cls.db)
        cls.cur = cls.con.cursor()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.con.close()
        if os.path.isfile(cls.db):
            os.remove(cls.db)

    def test_find_or_create_db_and_table(self):
        res = self.cur.execute("SELECT name FROM sqlite_master")
        usr_table = res.fetchone()

        self.assertEqual(("user",), usr_table)
        self.assertTrue(os.path.isfile(self.db))

        find_or_create_user_table(self.cur)
        res = self.cur.execute("SELECT name FROM sqlite_master")
        tables = res.fetchall()

        self.assertEqual([("user",)], tables)

    def test_generate_word(self):
        word = generate_word(5)
        self.assertRegex(word, '[a-z]{5}')

    def test_create_task(self):
        with Progress(transient=True) as progress:
            creating_user = progress.add_task(f"[green]Adding a user to the db...", total=1)
            create_task(self.db, progress, creating_user)

            res = self.cur.execute("SELECT COUNT(*) AS rows FROM user")
            
            self.assertEqual((1,),res.fetchone())

    def test_run_tasks(self):
        run_tasks(self.db, 10, 1000)

        res = self.cur.execute("SELECT COUNT(*) AS rows from user")

        self.assertEqual((1001,), res.fetchone())

