import logging
import sqlite3
import os
from other import db_dir, db_name

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file_sqlite3.txt",
    filemode="w",
)
def insert_row(db_name, values, columns):
    columns = '(' + ', '.join(columns) + ')'
    sql_query = f"INSERT INTO {db_name}, {columns} VALUES({', '.join(['?'] * len(values))})"
    execute_query(sql_query, values)

def create_table(db_name, table_columns):
    columns_str = ', '.join([f'{column} {data_type}' for column, data_type in table_columns.items()])
    query = f'CREATE TABLE IF NOT EXISTS {db_name} ({columns_str})'
    execute_query(query)

def create_db(directory_db=db_dir, database_name=db_name):
    if not os.path.exists(directory_db):
        os.makedirs(directory_db)
    db_path = f'{directory_db}/{database_name}'
    with sqlite3.connect(db_path) as connection:
        connection.cursor()

    logging.info(f'Database succsesfuly created')

def add_record_to_table(user_id, role, content, date, tokens, session_id):
    insert_row(db_name, [user_id, role, content, date, tokens, session_id],
               columns=['user_id', 'role', 'content', 'date', 'tokens', 'session_id'])

def prepare_db(clean_if_exists):
    create_db()
    create_table(db_name=db_name,
                 table_columns={
                     'id': 'INTEGER PRIMARY KEY',
                     'user_id': 'INTEGER',
                     'role': 'TEXT',
                     'content': 'TEXT',
                     'date': 'DATETIME',
                     'tokens': 'INTEGER',
                     'session_id': 'INTEGER'
                 })
    # debug
    # if clean_if_exists:
    #   delete_user(db_name)


def execute_query(sql_query, data=None, db_path=f'{db_dir}/{db_name}'):
    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            if data:
                cur.execute(sql_query, data)
            else:
                cur.execute(sql_query)

            conn.commit()
    except Exception as e:
        logging.error(f'Error! this exception - {e}')


def execute_selection_query(sql_query, data=None, db_path=f'{db_dir}/{db_name}'):
    try:
        logging.info(f'Database execute query {sql_query}')

        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            if data:
                cur.execute(sql_query, data)
            else:
                cur.execute(sql_query)
            rows = cur.fetchall()
            conn.commit()
            return rows
    except Exception as e:
        logging.error(f'Error! this exception - {e}')
        return []


def get_value_from_table(value, user_id, DB_TABLE_NAME):
    sql_query = (f'SELECT {value}'
                 f'FROM {DB_TABLE_NAME}'
                 f'WHERE user_id = ? ORDER BY date desc')

    rows = execute_selection_query(sql_query, [user_id])

    return rows[0]

def is_value_in_table(db_name, column_name, value):
    sql_query = f'SELECT {column_name} FROM {db_name} WHERE {column_name} = ? ORDER BY date decs'
    rows = execute_selection_query(sql_query, [value])
    return rows

def count_all_tokens_from_db(db_name):
    sql_query = f'SELECT tokens FROM {db_name} WHERE user_id = ?'
    total_tokens = execute_selection_query(sql_query)
    return total_tokens

def get_users_amount(db_name):
    sql_query = f'SELECT users FROM {db_name} WHERE user_id is not null'
    total_users = execute_selection_query(sql_query)
    return total_users

def get_dialogue_for_user(user_id, session_id):
    sql_query = (f'SELECT * FROM {db_name}'
                 f'WHERE user_id = ? AND tokens IS NOT NULL AND session_id = ?'
                 f'ORDER BY date asc')
    rows = execute_selection_query(sql_query, [user_id, session_id])
    return rows


def delete_user(db_name):
    query = """
        DELETE 
        FROM users
    """

    execute_query(db_name, query)
    logging.info("Successfully deleted userdata")


if __name__ == "__main__":
    db_file = 'user_of_bot.db'

    # add_user(db_file, '199912331', 'math')

    # update_user_level(db_file, '199912331', 'beginner')
    # update_user_level(db_file, '199912331', 'advanced')
