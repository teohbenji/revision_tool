import sqlite3
import unittest
import db

def test_db_setup():
    """Setup test.db by deleting and recreating tables"""
    # Define connection and cursor
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()

    results = db.get_all_table_names(cursor)
    
    for result in results:
        (table_name, ) = result
        cursor.execute("DROP TABLE IF EXISTS " + table_name)

    # Setup schema 
    test_setup_questions_table(cursor)
    test_setup_answers_table(cursor)
    test_setup_chapters_table(cursor)
    test_setup_scores_table(cursor)

    connection.commit()
    cursor.close()
    connection.close()

def test_setup_questions_table(cursor):
    """Create and populate questions table in test.db
    
    Args:
        cursor: cursor object for executing SQLite queries

    Returns:
        None
    """
    create_table_query = """CREATE TABLE IF NOT EXISTS questions (
                            id INTEGER PRIMARY KEY,
                            chap_num INTEGER,
                            name TEXT)"""

    cursor.execute(create_table_query)

    # Populates table with question list
    question_list = [(1, "Chap 1 Q1"),
                     (1, "Chap 1 Q2"),
                     (2, "Chap 2 Q1"),
                     (3, "Chap 3 Q1")]

    cursor.executemany("INSERT INTO questions (chap_num, name) VALUES(?, ?)", question_list)

def test_setup_answers_table(cursor):
    """Create and populate answers table in test.db
    
    Args:
        cursor: cursor object for executing SQLite queries

    Returns:
        None
    """
    create_table_query = """CREATE TABLE IF NOT EXISTS answers (
                            id INTEGER PRIMARY KEY,
                            qn_id INTEGER,
                            name TEXT,
                            FOREIGN KEY (qn_id)
                                REFERENCES questions (id)
                            )"""

    cursor.execute(create_table_query)

    # Populates table with answer list
    answer_list = [(1, "Chap 1 Q1 A1"),
                   (1, "Chap 1 Q1 A2"),
                   (2, "Chap 1 Q2 A1"),
                   (3, "Chap 2 Q1 A1"),
                   (4, "Chap 3 Q1 A1")]

    cursor.executemany("INSERT INTO answers (qn_id, name) VALUES(?, ?)", answer_list)

def test_setup_chapters_table(cursor):
    """Create and populate chapters table in test.db
    
    Args:
        cursor: cursor object for executing SQLite queries

    Returns:
        None
    """
    create_table_query = """CREATE TABLE IF NOT EXISTS chapters (
                            id INTEGER PRIMARY KEY,
                            chap_num INTEGER,
                            high_score INTEGER,
                            unlocked BOOLEAN
                            )"""

    cursor.execute(create_table_query)

    # Populates table with chapter list
    chapter_list = [(1, 5, True),
                  (2, 4, True),
                  (3, 0, False)]

    cursor.executemany("INSERT INTO chapters (chap_num, high_score, unlocked) VALUES(?, ?, ?)", chapter_list)  

def test_setup_scores_table(cursor):
    """Creates and populates scores table
    
    Args:
        cursor: cursor object for executing SQLite queries

    Returns:
        None
    """
    create_table_query = """CREATE TABLE IF NOT EXISTS scores (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            score INTEGER
                            )"""

    cursor.execute(create_table_query)

    # Populates table with scores list
    scores_list = [("Alice", 1),
                   ("Bob", 2),
                   ("Jordan", 23),
                   ("Ronaldo", 7),
                   ("Messi", 10),
                   ("Lebron", 6),
                   ("Kobe", 24)
                  ]

    cursor.executemany("INSERT INTO scores (name, score) VALUES(?, ?)", scores_list)

class Testdb(unittest.TestCase):
    #Resets test.db whenever every test case is run
    def setUp(self):
        test_db_setup()

    def test_get_all_chapters(self):
        self.assertEqual(db.get_all_chapters("test"), [db.Chapter(1, 1, 5, 1), db.Chapter(2, 2, 4, 1), db.Chapter(3, 3, 0, 0)])
    
    def test_get_unlocked_chap_nums(self):
        self.assertEqual(db.get_unlocked_chap_nums("test"), [1, 2])

    def test_get_locked_chap_nums(self):
        self.assertEqual(db.get_locked_chap_nums("test"), [3])

    def test_get_chapter_high_score(self):
        self.assertEqual(db.get_chapter_high_score(1, "test"), 5)
        self.assertEqual(db.get_chapter_high_score(2, "test"), 4)
        self.assertEqual(db.get_chapter_high_score(3, "test"), 0)

    def test_update_chapter_high_score(self):
        db.update_chapter_high_score(3, 4, "test")
        self.assertEqual(db.get_chapter_high_score(3, "test"), 4)

    def test_update_chapter_unlocked(self):
        db.update_chapter_unlocked(3, "test")
        self.assertTrue(3 in db.get_unlocked_chap_nums("test"))

    def test_get_all_questions(self):
        self.assertEqual(db.get_all_questions("test"), [db.Question(1, 1, "Chap 1 Q1"), db.Question(2, 1, "Chap 1 Q2"), 
                                                        db.Question(3, 2, "Chap 2 Q1"), db.Question(4, 3, "Chap 3 Q1")])

    def test_get_question_by_id(self):
        self.assertEqual(db.get_question_by_id(1, "test"), db.Question(1, 1, "Chap 1 Q1"))

    def test_get_questions_by_chap_num(self):
        self.assertEqual(db.get_questions_by_chap_num(1, "test"), [db.Question(1, 1, "Chap 1 Q1"), db.Question(2, 1, "Chap 1 Q2")])
        self.assertEqual(db.get_questions_by_chap_num(3, "test"), [db.Question(4, 3, "Chap 3 Q1")])

    def test_get_answers_by_question_id(self):
        self.assertEqual(db.get_answers_by_question_id(1, "test"), [db.Answer(1, 1, "Chap 1 Q1 A1"), db.Answer(2, 1, "Chap 1 Q1 A2")])
        self.assertEqual(db.get_answers_by_question_id(2, "test"), [db.Answer(3, 2, "Chap 1 Q2 A1")])

    def test_get_newest_question_id(self):
        self.assertEqual(db.get_newest_question_id("test"), 4)
    
    def test_add_question(self):
        db.add_question(db.Question("", 4, "Chap 4 Q1"), "test")
        self.assertEqual(db.get_newest_question_id("test"), 5)
    
    def test_get_highscores(self):
        self.assertEqual(db.get_highscores("test"), [db.Score(7, "Kobe", 24), db.Score(3, "Jordan", 23), db.Score(5, "Messi", 10),
                                                     db.Score(4, "Ronaldo", 7), db.Score(6, "Lebron", 6)])

    def test_add_score(self):
        db.add_score(db.Score("", "Trent", 66), "test")
        self.assertEqual(db.get_highscores("test"), [db.Score(8, "Trent", 66), db.Score(7, "Kobe", 24), db.Score(3, "Jordan", 23), 
                                                     db.Score(5, "Messi", 10), db.Score(4, "Ronaldo", 7)])

    def test_get_all_question_ids(self):
        self.assertEqual(db.get_all_question_ids("test"), ['1', '2', '3', '4'])

    def test_remove_question_by_id(self):
        db.remove_question_by_id(4, "test")
        self.assertEqual(db.get_newest_question_id("test"), 3)

    def test_remove_answer_by_question_id(self):
        db.remove_answer_by_question_id(4, "test")
        self.assertEqual(db.get_answers_by_question_id(4, "test"), [])

if __name__ == '__main__':
    unittest.main()

