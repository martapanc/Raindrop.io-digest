import sqlite3


def create_database():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE raindrop_code (auth_code text)''')
    c.execute('''CREATE TABLE raindrop_token (access_token text, refresh_token text)''')
    conn.commit()
    conn.close()


def drop_database():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''DROP TABLE raindrop_code''')
    c.execute('''DROP TABLE raindrop_token''')
    conn.commit()
    conn.close()


def save_auth_code(code):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''DELETE FROM raindrop_code''')
    c.execute('''REPLACE INTO raindrop_code VALUES ('{}')'''.format(code))
    conn.commit()
    conn.close()


def save_token(access_token, refresh_token):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''DELETE FROM raindrop_token''')
    c.execute('''REPLACE INTO raindrop_token VALUES ('{}', '{}')'''.format(access_token, refresh_token))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_database()
