from typing import Annotated
from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import psycopg2 as pg
from psycopg2.extras import RealDictCursor
import os
import auth

load_dotenv()

class Document(BaseModel):
    doc_xml: str

app = FastAPI()

def connect():
    return pg.connect(
        database=os.getenv("PG_NAME"),
        user=os.getenv("PG_USER"),
        host=os.getenv("PG_HOST"),
        password=os.getenv("PG_PASS")
    )

@app.post("/request_jobs")
async def get_print_jobs(req: Request):
    body = await req.form()
    client_ip = req.client.host
    data = dict(body)
    connection_type = data["ConnectionType"] if "ConnectionType" in data else None
    api_key = data['ID'] if "ID" in data else None
    name = data["Name"] if "Name" in data else "Unknown"
    if connection_type == "GetRequest":
        print(client_ip, "-",connection_type)
        return ""
    return ""

@app.post("/print_jobs")
async def post_print_jobs(Authorization: Annotated[str, Header()], req: Document):
    print(Authorization)
    api_key = Authorization.split(" ")[1] if "Bearer " in Authorization else None

    if not api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    conn = connect()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM esdp.users_v1")
    users = cur.fetchall()
    for user in users:
        if (auth.checkData(api_key, user['api_key'])):
            doc = req.doc_xml or None
            cur.execute("INSERT INTO esdp.print_jobs (created_by, doc_xml) VALUES (%s, %s)", (user['id'], doc,))
            conn.commit()
            cur.close()
            conn.close()
            return "OK"
    
    cur.close()
    conn.close()
    raise HTTPException(status_code=401, detail="Unauthorized")