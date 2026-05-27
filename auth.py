import bcrypt
import pg
from psycopg2.extras import RealDictCursor

def hashData(data):
    data = data.encode("utf-8")
    salt = bcrypt.gensalt(10)
    hashed = bcrypt.hashpw(data, salt)
    return hashed.decode()

def checkData(data, hashed):
    return bcrypt.checkpw(data.encode("utf-8"), hashed.encode("utf-8"))

def authorize(api_key):
    conn = pg.connect()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM esdp.users_v1")
    users = cur.fetchall()
    cur.close()
    conn.close()
    for user in users:
        if (checkData(api_key, user['api_key'])):
            return user['id']
    return None

if __name__ == "__main__":
    import random as r

    key = ''
    hex = '0123456789abcdef'
    while len(key) < 30:
        rand = r.randint(0, 15)
        key += hex[rand:rand+1]

    print("API Key:", key)
    hashed = hashData(key)
    print("Hashed:", hashed)