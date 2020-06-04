import mysql.connector
from os import environ

VALIDATION_RESULT_NOT_DONE = 0
VALIDATION_RESULT_CORRECT = 1
VALIDATION_RESULT_INCORRECT = 2

__db__ = mysql.connector.connect(
    user=environ.get('MYSQL_USER'),
    passwd=environ.get('MYSQL_PASSWORD'),
    db=environ.get('MYSQL_DATABASE')
)
__db__.autocommit = True

__tables__ = ["""
    CREATE TABLE IF NOT EXISTS Recordings(
        filepath NVARCHAR(255) PRIMARY KEY,
        authorId NVARCHAR(255),
        label NVARCHAR(30)
    );
""",
              """
    CREATE TABLE IF NOT EXISTS Validations(
        validationId NVARCHAR(255) PRIMARY KEY,
        filepath NVARCHAR(255),
        result INT
    );
"""]

__insert_recording_command__ = """
    INSERT INTO Recordings VALUES (%s, %s, %s);
"""

__insert_validation_command__ = """
    INSERT INTO Validations VALUES (%s, %s, %s);
"""

__get_filepaths_command__ = """
    SELECT Recordings.filepath AS filepath, Recordings.label AS label, COUNT(*) AS cnt
    FROM (Recordings LEFT JOIN Validations ON Recordings.filepath = Validations.filepath)
    WHERE
        Recordings.authorId <> %s
    GROUP BY filepath, label
    ORDER BY cnt
    LIMIT 10;
"""

__get_validation_command__ = """
    SELECT * FROM Validations WHERE validationId = %s;
"""

__update_validation_command__ = """
    UPDATE Validations SET result = IF(result = 0, %s, result) WHERE validationId = %s;
"""


def __create_table__(cursor, table_description):
    try:
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        print("Failed creating table: {}".format(err))


def init_database():
    cursor = __db__.cursor()
    for item in __tables__:
        __create_table__(cursor, item)
    cursor.close()


def insert_recordings(recordings):
    try:
        cursor = __db__.cursor()
        cursor.executemany(__insert_recording_command__, recordings)
        cursor.close()
    except mysql.connector.Error as err:
        print("Failed inserting recordings: {}".format(err))
        raise err


def insert_validations(validations):
    try:
        cursor = __db__.cursor()
        cursor.executemany(__insert_validation_command__, validations)
        cursor.close()
    except mysql.connector.Error as err:
        print("Failed inserting validations: {}".format(err))
        raise err


def get_recordings_from_different_user(userId):
    results = []
    try:
        cursor = __db__.cursor()
        cursor.execute(__get_filepaths_command__, (userId,))
        for (filepath, label, cnt) in cursor:
            results.append((filepath, label))
        cursor.close()
    except mysql.connector.Error as err:
        print("Failed getting recordings: {}".format(err))
        raise err
    return results


def get_validation(validation_id):
    result = None
    try:
        cursor = __db__.cursor()
        cursor.execute(__get_validation_command__, (validation_id,))
        result = cursor.fetchone()
        cursor.close()
    except mysql.connector.Error as err:
        print("Failed getting validation: {}".format(err))
        raise err
    return result


def update_validations(validations):
    try:
        cursor = __db__.cursor()
        cursor.executemany(__update_validation_command__, validations)
        cursor.close()
    except mysql.connector.Error as err:
        print("Failed updating validations: {}".format(err))
        raise err
