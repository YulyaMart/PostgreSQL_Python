import psycopg2

# Функция, создающая структуру БД (таблицы).
def create_db(conn):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client_mandatory_info(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(40) NOT NULL,
        last_name VARCHAR(40) NOT NULL,
        email VARCHAR(40) UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS client_phone_info(
        id SERIAL PRIMARY KEY,
        phone_number VARCHAR(10) UNIQUE,
        client_id INTEGER NOT NULL REFERENCES client_mandatory_info(id)
    );
    """)
    return conn.commit()

# Функция, позволяющая добавить нового клиента.
def add_client(conn, first_name, last_name, email, phones=None):
    cur.execute("""
    INSERT INTO client_mandatory_info(first_name, last_name, email) VALUES(%s, %s, %s) RETURNING id;
    """, (first_name, last_name, email))
    client_id = cur.fetchone()[0]
    if phones is not None:
        for phone in phones:
            cur.execute("""
            INSERT INTO client_phone_info(client_id, phone_number) VALUES(%s, %s);
            """, (client_id, phone))
    return conn.commit()

# Функция, позволяющая добавить телефон для существующего клиента.
def add_phone(conn, client_id, phone):
    cur.execute("""
    INSERT INTO client_phone_info(client_id, phone_number) VALUES(%s, %s);
    """, (client_id, phone))
    return conn.commit()

# Функция, позволяющая изменить данные о клиенте.
def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    if first_name is not None:
        cur.execute("""
        UPDATE client_mandatory_info SET first_name=%s WHERE id=%s;
        """, (first_name, client_id))
    if last_name is not None:
        cur.execute("""
        UPDATE client_mandatory_info SET last_name=%s WHERE id=%s;
        """, (last_name, client_id))
    if email is not None:
        cur.execute("""
        UPDATE client_mandatory_info SET email=%s WHERE id=%s;
        """, (email, client_id))
    if phones is not None:
        cur.execute("""
        SELECT * FROM client_mandatory_info cmi
        LEFT JOIN client_phone_info cpi ON cmi.id = cpi.client_id
        WHERE cmi.id =%s
        """, (client_id,))
        phone_list = cur.fetchall()
        print(phone_list)
        phone_to_change = input('Введите номер телефона, наобходимый заменить: ')
        cur.execute("""
        UPDATE client_phone_info SET phone_number=%s WHERE phone_number=%s;
        """, (phones, phone_to_change))
    return conn.commit()

# # Функция, позволяющая удалить телефон для существующего клиента.
def delete_phone(conn, client_id, phone):
    cur.execute("""
    DELETE FROM client_phone_info WHERE client_id=%s AND phone_number=%s;
    """, (client_id, phone))
    return conn.commit()

# # Функция, позволяющая удалить существующего клиента.
def delete_client(conn, client_id):
    cur.execute("""
    DELETE FROM client_phone_info WHERE client_id=%s;
    """, (client_id))
    cur.execute("""
    DELETE FROM client_mandatory_info WHERE client_id=%s;
    """, (client_id))
    return conn.commit()

# # Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    cur.execute('''
    SELECT * FROM client_mandatory_info cmi
    LEFT JOIN client_phone_info cpi ON cmi.id = cpi.client_id 
    WHERE first_name=%s
    OR last_name=%s
    OR email=%s
    OR phone_number=%s;
    ''', (first_name, last_name, email, phone))
    print(cur.fetchall())

with psycopg2.connect(database="clients", user="postgres", password="postgres") as conn:
    with conn.cursor() as cur:
        # create_db(conn)
        # add_client(conn, 'Bart', 'Simpson', 'elbarto@sim.com')
        # add_phone(conn, 1, '9999999999')
        # change_client(conn, 1, first_name=None, last_name=None, email=None, phones='8888888888')
        # delete_phone(conn, 1, '9999999999')
        # delete_client(conn, client_id)
        find_client(conn, first_name=None, last_name='Simpson', email=None, phone='9999999999')
conn.close()