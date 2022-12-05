import sqlite3

def db_setup():
    """Setup main.db by deleting and recreating tables"""
    # Define connection and cursor
    connection = sqlite3.connect('main.db')
    cursor = connection.cursor()

    results = get_all_table_names(cursor)
    
    for result in results:
        (table_name, ) = result
        cursor.execute("DROP TABLE IF EXISTS " + table_name)

    # Setup schema 
    setup_questions_table(cursor)
    setup_answers_table(cursor)
    setup_chapters_table(cursor)
    setup_scores_table(cursor)

    connection.commit()
    cursor.close()
    connection.close()

class Question:
    """Stores data in each row from questions table

    Attributes:
        id: Unique identifier
        chap_num: The chapter where the question is from
        name: Question name
    """
    def __init__(self, id, chap_num, name):
        """Inits Question with id, chap_num, name."""
        self._id = id
        self._chap_num = chap_num
        self._name = name
    
    #Compare attribute values of two Question objects
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__

class Answer:
    """Stores data in each row from answers table

    Attributes:
        id: Unique identifier
        qn_id: Foreign key. Linked to id in questions table
        name: Answer name
    """
    def __init__(self, id, qn_id, name):
        """Inits Answer with id, qn_id, name."""
        self._id = id
        self._qn_id = qn_id
        self._name = name

    #Compare attribute values of two Answer objects
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__

class Chapter:
    """Stores data in each row from chapter table

    Attributes:
        id: Unique identifier
        chap_num: The chapter number
        high_score: highest score of the chapter ever attained
        unlocked: boolean variable. True if unlocked, False if still locked.
    """
    def __init__(self, id, chap_num, high_score, unlocked):
        """Inits Answer with id, qn_id, name."""
        self._id = id
        self._chap_num = chap_num
        self._high_score = high_score
        self._unlocked = unlocked

    #Compare attribute values of two Chapter objects
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__

class Score:
    """Stores data in each row from scores table

    Attributes:
        id: Unique identifier
        name: User's name
        score: Value of score
    """
    def __init__(self, id, name, score):
        """Inits Score with id, name, score."""
        self._id = id
        self._name = name
        self._score = score

    #Compare attribute values of two Score objects
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__   

def setup_questions_table(cursor):
    """Create and populate questions table
    
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
    question_list = [
                    #Chapter 1 Questions
                    (1, "x = 7 / 2\n\nWhat is the value of x?"),
                    (1,  "y = 11 // 2\n\nWhat is the value of y?"),
                    (1,  "z = 8 % 3\n\nWhat is the value of z?"),
                    (1, "a = 1, b = 2\nx = a >= b\n\nWhat is the value of x?"),
                    (1, "a = 4.0, b = 4\nx = a == b\n\nWhat is the value of x?"),
                    (1, """x = 'England'\ny = 'France'\nprint(x+y)
                    \n\nWhat is displayed on the screen when the code is run?
                    \n\n1) France England\n2) EnglandFrance\n3) FranceEngland\n4) England France
                    \n\nPlease input the option number as the answer e.g. 1, 2, 3 etc."""),
                    (1, """x = 'Germany'\ny = 'Japan'\nz = 'Spain'\nprint(y,z,x)
                    \n\nWhat is displayed on the screen when the code is run?
                    \n\n1) Japan Spain Germany\n2) Spain Japan Germany\n3) SpainJapanGermany\n4) JapanSpainGermany
                    \n\nPlease input the option number as the answer e.g. 1, 2, 3 etc."""),

                    #Chapter 2 Questions
                    (2, """In Python, which of the below is the correct way to print "Hello"?
                    \n\n1) Print "Hello"\n2) print "Hello"\n3) Print("Hello")\n4) print("Hello")
                    \n\nPlease input the option number as the answer e.g. 1, 2, 3 etc."""),
                    (2, """Which of the following is an invalid variable name?
                    \n\n1) bl_nk\n2) print bl1nk\n3) blink-1\n4) BLINK1
                    \n\nPlease input the option number as the answer e.g. 1, 2, 3 etc."""),
                    (2, """Which of the following is a valid function header?
                    \n\n1) def func(x):\n2) func(x):\n3) def func@(x):\n4) def func-(x):
                    \n\nPlease input the option number as the answer e.g. 1, 2, 3 etc."""),
                    (2, """Consider the description below.
                    \n\n1. The string '7' is passed to the float function.\n2. The value returned by the float function is passed to the integer function.\n3. The value returned by the integer function is assigned to the variable x.
                    \n\nWhich of the following python statements match this description?
                    \n\n1) x = int(float(7))\n2) x = float(int(7))\n3) x = float(int('7'))\n4) x = int(float('7'))
                    \n\nPlease input the option number as the answer e.g. 1, 2, 3 etc."""),
                    (2, """In the following code, the programmer wants to calculate the sin of pi / 3
                    \n\n1 import math
                    \n2 rad = math.pi / 3
                    \n3 value = 
                    \n4 print(value)
                    \n\nWhat should be the expression that is assigned to value at Line 3?
                    \nThe expression must include the variable value, and a suitable function from the math library"""),
                    (2, """Analyse the following code.
                    \n\n1
                    \n2 val = sin(3) / 3
                    \n3 print(value)
                    \n\nWhat import statement should be put at line 1, so that the code runs without error?
                    \n\n1) from math import *\n2) from math import asin\n3) import math"""),

                    #Chapter 3 Questions
                    (3, """Complete the blank x with the range function so that the following is displayed on the screen:
                    \n[3, 4, 5, 6, 7, 8, 9, 10]
                    \n\n1 ls = list(x) 
                    \n2 print(ls)"""),
                    (3, """After the code is executed, the following is displayed on the screen:
                    \n[8, 9, 10, 11, 12]
                    \n\n1 a = list(range(2,17))
                    \n2 b = 
                    \n3 print(b)
                    \n\n What should be assigned to b? b contains an expression involving a list slice, using only positive indices."""),
                    (3, """What is displayed by the following statements?
                    \n1 x = [4, 6, 7]
                    \n2 y = [1, 5, 9]
                    \n3 print(x+y)
                    \n\n1) [(4, 6, 7), (1, 5, 9)]\n2) [4, 6, 7, 1, 5, 9]\n3) [1, 5, 9, 4, 6, 7]\n4) x = [(1, 5, 9), (4, 6, 7)])
                    \n\nPlease input the option number as the answer e.g. 1, 2, 3 etc."""),
                    (3, """Consider the following code
                    \n1 count = 2
                    \n2 while z : 
                    \n3     print("apple")
                    \n4     count = count + 1
                    \n\nWhen executed, it displays \napple\napple\napple\napple
                    \n\nWhat is expression z? Any possible answer is accepted"""),
                    (3, """Consider the following code.
                    \n\n1 ls = ['apple', 'banana', 'chestnut']
                    \n2 print("The last element of ls is", A) 
                    \n\nWhat is Blank A?. It is an expression that accesses the last element of ls using a negative index."""),
                    (3, """Complete Line 2 so that the following is displayed on the screen:
                    \n['Adam', 'Bob', 'Candy', 'Debbie'] 
                    \n\n1 ls = ['Adam', 'Bob', 'Candy'] 
                    \n2
                    \n3 print(ls)"""),

                    #Chapter 4 Questions


                    #Chapter 5 Questions


                    #Chapter 6 Questions


                    #Chapter 7 Questions


                    ]

    cursor.executemany("INSERT INTO questions (chap_num, name) VALUES(?, ?)", question_list)

def setup_answers_table(cursor):
    """Create and populate answers table
    
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
    answer_list = [
                  #Chapter 1 Answers
                  (1, "3.5"),
                  (2, "5"),
                  (3, "2"),
                  (4, "False"),
                  (5, "True"),
                  (6, "2"),
                  (7, "1"),

                  #Chapter 2 Answers
                  (8, "4"),
                  (9, "3"),
                  (10, "1"),
                  (11, "4"),
                  (12, "math.sin(rad)"),
                  (13, "1"),

                  #Chapter 3 Answers
                  (14, "range(3,11,1)"),
                  (14, "range(3, 11, 1)"),
                  (14, "range(3,11)"),
                  (14, "range(3, 11)"),
                  (15, "a[6:11]"),
                  (16, "2"),
                  (17, "count<=5"),
                  (17, "count <= 5"),
                  (17, "count=6"),
                  (17, "count = 6"),
                  (17, "count!=6"),
                  (17, "count != 6"),
                  (18, "ls[-1]"),
                  (19, "ls.append('Debbie')"),
                  (19, 'ls.append("Debbie")'),

                  #Chapter 4 Answers


                  #Chapter 5 Answers


                  #Chapter 6 Answers


                  #Chapter 7 Answers
                  
                  ]

    cursor.executemany("INSERT INTO answers (qn_id, name) VALUES(?, ?)", answer_list)

def setup_chapters_table(cursor):
    """Create and populate chapters table
    
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
    chapter_list = [(1, 0, True),
                  (2, 0, True),#TODO:For testing, set back to False when done
                  (3, 0, True),#TODO:For testing, set back to False when done
                  (4, 0, True),
                  (5, 0, True),
                  (6, 0, True),
                  (7, 0, True)]

    cursor.executemany("INSERT INTO chapters (chap_num, high_score, unlocked) VALUES(?, ?, ?)", chapter_list) 

def setup_scores_table(cursor):
    """Creates empty scores table
    
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

def get_all_table_names(cursor):
    """Gets all table names in schema

    Args:
        cursor: cursor object for executing SQLite queries
        
    Returns:
        results: A list of single variable tuples containing table names in schema.
        E.g. [(customers,), (orders,)]
    """
    cursor.execute("""SELECT name FROM sqlite_schema WHERE type ='table'""")
    results = cursor.fetchall()

    return results

def db_get_all_chapters(db='main'):
    """Gets list of all chapter data from chapters table

    Args:
        db: Default value is 'main' to access main.db, use 'test' instead to access test.db 

    Returns:
        chapters_list: A list of data for each chapter. Each row is represented as a Chapter object, and then appended into
        chapters_list.
    """
    connection = sqlite3.connect('test.db' if db == 'test' else 'main.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM chapters")
    results = cursor.fetchall()
    chapters_list = []
    
    # Save each result in Chapter object
    for result in results:
        chapter = Chapter(result[0], result[1], result[2], result[3])
        chapters_list.append(chapter)
    
    cursor.close()
    connection.close()

    return chapters_list

def db_get_unlocked_chap_nums(db='main'):
    """Gets unlocked chapter numbers from chapters table

    Args:
        db: Default value is 'main' to access main.db, use 'test' instead to access test.db 

    Returns:
        unlocked_chap_nums_list: A list of unlocked chapter numbers.
    """
    connection = sqlite3.connect('test.db' if db == 'test' else 'main.db')
    cursor = connection.cursor()

    cursor.execute("SELECT chap_num FROM chapters where unlocked = 1")
    results = cursor.fetchall()

    unlocked_chap_nums_list = []

    for result in results:
        (chap_num, ) = result
        unlocked_chap_nums_list.append(chap_num)
    
    cursor.close()
    connection.close()

    return unlocked_chap_nums_list

def db_get_locked_chap_nums(db='main'):
    """Gets locked chapter numbers from chapters table

    Args:
        db: Default value is 'main' to access main.db, use 'test' instead to access test.db 

    Returns:
        locked_chap_nums_list: A list of locked chapter numbers.
    """
    connection = sqlite3.connect('test.db' if db == 'test' else 'main.db')
    cursor = connection.cursor()

    cursor.execute("SELECT chap_num FROM chapters where unlocked = 0")
    results = cursor.fetchall()
    locked_chap_nums_list = []

    for result in results:
        (chap_num, ) = result
        locked_chap_nums_list.append(chap_num)
    
    cursor.close()
    connection.close()

    return locked_chap_nums_list

def db_get_chapter_high_score(chap_num, db='main'):
    """Gets high score of chapter from chapters table

    Args:
        chap_num: Chapter number
        db: Default value is 'main' to access main.db, use 'test' instead to access test.db 

    Returns:
        high_score: High score of chapter
    """
    connection = sqlite3.connect('test.db' if db == 'test' else 'main.db')
    cursor = connection.cursor()

    cursor.execute("SELECT high_score FROM chapters WHERE chap_num = ?", (chap_num,))

    (high_score,) = cursor.fetchone()

    cursor.close()
    connection.close()

    return high_score

def db_update_chapter_high_score(chap_num, new_high_score, db='main'):
    """Updates high score of chapter in chapters table

    Args:
        chap_num: Chapter number
        new_high_score: New high score that replaces old high score in table
        db: Default value is 'main' to access main.db, use 'test' instead to access test.db 

    Returns:
        None
    """
    
    connection = sqlite3.connect('test.db' if db == 'test' else 'main.db')
    cursor = connection.cursor()

    cursor.execute('''UPDATE chapters
                      SET high_score = ?
                      WHERE chap_num = ?''', (new_high_score, chap_num))

    connection.commit()
    cursor.close()
    connection.close()

def db_update_chapter_unlocked(chap_num, db='main'):
    """Updates unlocked status of chapter in chapters table

    Args:
        chap_num: Chapter number
        db: Default value is 'main' to access main.db, use 'test' instead to access test.db

    Returns:
        None
    """
    connection = sqlite3.connect('test.db' if db == 'test' else 'main.db')
    cursor = connection.cursor()

    cursor.execute('''UPDATE chapters
                      SET unlocked = ?
                      WHERE chap_num = ?''', (1, chap_num))

    connection.commit()
    cursor.close()
    connection.close()

def db_get_all_questions(db="main"):
    """Gets a list of all questions from questions table

    Args:
        db: Default value is 'main' to access main.db, use 'test' instead to access test.db
        
    Returns:
        questions_list: A list of question objects. Each row is represented as a Question object, and then appended into
        question_list.
    """
    connection = sqlite3.connect('test.db' if db == 'test' else 'main.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM questions")
    results = cursor.fetchall()
    questions_list =[]

    # Save each result in Question object
    for result in results:
        question = Question(result[0], result[1], result[2])
        questions_list.append(question)

    cursor.close()
    connection.close()

    return questions_list

def db_get_questions_by_chap_num(chap_num, db='main'):
    """Gets list of questions of specified chapter number from questions table

    Args:
        chap_num: chapter number
        db: Default value is 'main' to access main.db, use 'test' instead to access test.db

    Returns:
        questions_list: A list of questions. Each row is represented as a Question object, and then appended into
        question_list.
    """

    connection = sqlite3.connect('test.db' if db == 'test' else 'main.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM questions WHERE chap_num = ?", (chap_num,))

    questions_list = []
    results = cursor.fetchall()

    # Save each result in Question object
    for result in results:
        question = Question(result[0], result[1], result[2])
        questions_list.append(question)
    
    cursor.close()
    connection.close()

    return questions_list

def db_get_answers_by_question_id(qn_id, db='main'):
    """Gets list of answers of specified question id from answers table

    Args:
        qn_id: question id
        db: Default value is 'main' to access main.db, use 'test' instead to access test.db

    Returns:
        answers_list: A list of answers. Each row is represented as an Answer object, and then appended into
        answer_list.
    """

    connection = sqlite3.connect('test.db' if db == 'test' else 'main.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM answers WHERE qn_id = ?", (qn_id,))

    answers_list = []
    results = cursor.fetchall()

    # Save each result in Answer object
    for result in results:
        answer = Answer(result[0], result[1], result[2])
        answers_list.append(answer)
    
    cursor.close()
    connection.close()

    return answers_list

def db_add_question(question, db='main'):
    """Adds question into questions table

    question object has empty id value, only _chap_num and _name
    db: Default value is 'main' to access main.db, use 'test' instead to access test.db

    Args:
        question: Question object

    Returns:
        None
    """
    connection = sqlite3.connect('test.db' if db == 'test' else 'main.db')
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO questions (chap_num, name) VALUES(?, ?)", (question._chap_num, question._name))

    connection.commit()
    cursor.close()
    connection.close()

def db_get_newest_question_id(db = 'main'):
    """Gets id of newest question from questions table

    Args:
        db: Default value is 'main' to access main.db, use 'test' instead to access test.db

    Returns:
        newest_qn_id: id of newest question
    """
    connection = sqlite3.connect('test.db' if db == 'test' else 'main.db')
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM questions ORDER BY id DESC LIMIT 1")

    result = cursor.fetchall()
    (newest_qn_id,) = result[0]

    return newest_qn_id

def db_add_answer(answer, db = 'main'):
    """Adds answer into answers table

    answer object has empty id value, only _qn_id and _name

    Args:
        answer: Answer object
        db: Default value is 'main' to access main.db, use 'test' instead to access test.db

    Returns:
        None
    """
    connection = sqlite3.connect('test.db' if db == 'test' else 'main.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO answers (qn_id, name) VALUES(?, ?)", (answer._qn_id, answer._name))

    connection.commit()
    cursor.close()
    connection.close()


def db_get_highscores(db='main'):
    """Gets list of the 5 highest scores in sudden death

    Args:
        db: Default value is 'main' to access main.db, use 'test' instead to access test.db

    Returns:
        scores_list: A list of scores. Each row is represented as a score object, and then appended into
        scores_list.
    """
    connection = sqlite3.connect('test.db' if db == 'test' else 'main.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM scores ORDER BY score DESC LIMIT 5")

    results = cursor.fetchall()
    scores_list = []

    # Save each result in Score object
    for result in results:
        score = Score(result[0], result[1], result[2])
        scores_list.append(score)

    cursor.close()
    connection.close()

    return scores_list

def db_add_score(score, db='main'):
    """Add new score from sudden death mode
    Args:
        score: score object to be added
        db: Default value is 'main' to access main.db, use 'test' instead to access test.db

    Returns:
        None
    """
    connection = sqlite3.connect('test.db' if db == 'test' else 'main.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO scores (name, score) VALUES(?, ?)", (score._name, score._score))

    connection.commit()
    cursor.close()
    connection.close()

def db_get_questions_sorted_by_chapter(db='main'):
    """Gets questions from question table, and sorts them by chapter
    Args:
        db: Default value is 'main' to access main.db, use 'test' instead to access test.db

    Returns:
        chapter_question_list: List of lists, where each nested list contains questions of the same chapter
    """
    connection = sqlite3.connect('test.db' if db == 'test' else 'main.db')
    cursor = connection.cursor()
    
    cursor.execute("SELECT chap_num FROM questions" )
    chapter_set = set(cursor.fetchall())

    chapter_question_list = []

    for chap_tuple in chapter_set:
        (chap_num, ) = chap_tuple
        cursor.execute("SELECT * FROM questions WHERE chap_num = ?", (chap_num,))

        question_list = []
        results = cursor.fetchall()

        # Save each result in Question object
        for result in results:
            question = Question(result[0], result[1], result[2])
            question_list.append(question)

        chapter_question_list.append(question_list)

    cursor.close()
    connection.close()
    
    return chapter_question_list

def db_get_all_question_ids(db='main'):
    """Gets a list of all question ids from questions table

    Args:
        db: Default value is 'main' to access main.db, use 'test' instead to access test.db

    Returns:
        qn_id_list: List of qn_id strings
    """
    connection = sqlite3.connect('test.db' if db == 'test' else 'main.db')
    cursor = connection.cursor()
    
    cursor.execute("SELECT id FROM questions" )
    results = cursor.fetchall()
    
    qn_id_list = []
    for id_tuple in results:
        (id,) = id_tuple
        qn_id_list.append(str(id))

    cursor.close()
    connection.close()
    
    return qn_id_list

def db_remove_question_by_id(qn_id, db = 'main'):
    """Deletes question from questions table 

    Args:
        qn_id: Question id of question to be deleted
        db: Default value is 'main' to access main.db, use 'test' instead to access test.db

    Returns:
        None
    """
    connection = sqlite3.connect('test.db' if db == 'test' else 'main.db')
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM questions where id = ?" , (qn_id,))

    connection.commit()
    cursor.close()
    connection.close()

def db_remove_answer_by_question_id(qn_id, db = 'main'):
    """Deletes answer(s) from answers table using qn_id

    Args:
        qn_id: Question id of answers to be deleted
        db: Default value is 'main' to access main.db, use 'test' instead to access test.db

    Returns:
        None
    """
    connection = sqlite3.connect('test.db' if db == 'test' else 'main.db')
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM answers where qn_id = ?" , (qn_id,))

    connection.commit()
    cursor.close()
    connection.close()

