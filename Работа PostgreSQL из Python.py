import psycopg2

# 1. Функция, создающая структуру БД (таблицы).
def create_db(cursor):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client(
        client_id SERIAL PRIMARY KEY, 
        name TEXT,
        surname TEXT,
        e_mail TEXT);
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phone(
        phone VARCHAR(12) PRIMARY KEY, 
        client_id INTEGER REFERENCES client(client_id));
    """)

# 2. Функция, позволяющая добавить нового клиента.
def add_client(cursor, name, surname, e_mail):
    cursor.execute("""INSERT INTO client(name, surname, e_mail)
    VALUES(%s, %s, %s);
    """, (name, surname, e_mail))

# 3. Функция, позволяющая добавить телефон для существующего клиента.
def add_phone(cursor, phone, client_id):
    cursor.execute("""INSERT INTO phone(phone, client_id)
    VALUES(%s, %s);
    """, (phone, client_id))

# 4. Функция, позволяющая изменить данные о клиенте.
def change_client(cursor, client_id, name=None, surname=None, e_mail=None):
    if surname == None and e_mail == None:
        cursor.execute("""UPDATE client
        SET name=%s WHERE client_id=%s;
        """, (name, client_id))
    elif e_mail == None:
        cursor.execute("""UPDATE client 
        SET name=%s, surname=%s WHERE client_id=%s;
        """, (name, surname, client_id))
    else:
        cursor.execute("""UPDATE client
        SET name=%s, surname=%s, e_mail=%s WHERE client_id=%s;
        """, (name, surname, e_mail, client_id))

# 5. Функция, позволяющая удалить телефон для существующего клиента.
def delete_phone(cursor, phone):
    cursor.execute("""DELETE FROM phone
    WHERE phone=%s;
    """, (phone,))

# 6. Функция, позволяющая удалить существующего клиента.
def delete_client(cursor, client_id):
    cursor.execute("""DELETE FROM client
    WHERE client_id=%s;
    """, (client_id,))

# 7. Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
def find_client(cursor, name=None, surname=None, e_mail=None, phone=None):
    if surname == None and e_mail == None and phone == None:
        cursor.execute("""SELECT * FROM client c
        JOIN phone p ON c.client_id = p.client_id 
        WHERE name=%s;
        """, (name,))
        print (cur.fetchone())
    elif e_mail == None and phone == None:
        cursor.execute("""SELECT * FROM client c
        JOIN phone p ON c.client_id = p.client_id 
        WHERE name=%s and surname=%s;
        """, (name, surname))
        print (cur.fetchone())
    elif phone == None:
        cursor.execute("""SELECT * FROM client c
        JOIN phone p ON c.client_id = p.client_id 
        WHERE name=%s and surname=%s and e_mail=%s;
        """, (name, surname, e_mail))
        print (cur.fetchone())
    else:
        cursor.execute("""SELECT * FROM client c
        JOIN phone p ON c.client_id = p.client_id 
        WHERE name=%s and surname=%s and e_mail=%s and phone=%s;
        """, (name, surname, e_mail, phone))
        print (cur.fetchone())


if __name__ == '__main__':   
    with psycopg2.connect(database="PostgreSQL_from_Python", user="postgres", password="Danil367173") as conn:
        with conn.cursor() as cur:
            # tables = create_db(cur)
            # new_client = add_client(cur, 'IVAN', 'IVANOV', 'ivan@ya.ru')
            # new_phone = add_phone(cur, 89992221213, 1)
            # new_data = change_client(cur, 1, 'SERGEY')
            # del_phone = delete_phone(cur, '89992221213')
            # del_client = delete_client(cur, 1)
            # find = find_client(cur, 'SERGEY', 'IVANOV')
    conn.close()
