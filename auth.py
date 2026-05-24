import bcrypt

def hashData(data):
    data = data.encode("utf-8")
    salt = bcrypt.gensalt(12)
    hashed = bcrypt.hashpw(data, salt)
    return hashed.decode()

def checkData(data, hashed):
    return bcrypt.checkpw(data.encode("utf-8"), hashed.encode("utf-8"))