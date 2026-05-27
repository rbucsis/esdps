from typing import Annotated
from fastapi import FastAPI, Request, Header, HTTPException, Response
from pydantic import BaseModel
import pg
import auth

class Document(BaseModel):
    doc_xml: str

app = FastAPI()

@app.post("/request_jobs")
async def get_print_jobs(req: Request):
    body = await req.form()
    client_ip = req.client.host
    data = dict(body)
    connection_type = data["ConnectionType"] if "ConnectionType" in data else None
    api_key = data['ID'] if "ID" in data else None
    name = data["Name"] if "Name" in data else None
    if not api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if connection_type == "GetRequest":
        user = auth.authorize(api_key)
        if user:
            response = ""
            conn = pg.connect()
            cur = conn.cursor()
            cur.execute("INSERT INTO esdp.requests (device_ip, user_id) VALUES (%s, %s) RETURNING id, created_utc", (client_ip, user,))
            job = cur.fetchone()
            job_id = job[0]
            timestamp = job[1]
            print(timestamp.strftime("%Y-%m-%d %H:%M:%S"),"-",client_ip)
            cur.execute("UPDATE esdp.pending_jobs_v1 SET record_status = 'Complete' WHERE created_utc <= %s AND created_by = %s RETURNING id, doc_xml", (timestamp,user,))
            docs = cur.fetchall()
            if docs:
                response = '''<?xml version="1.0" encoding="utf-8"?>
<PrintRequestInfo Version="2.00">'''
                for doc in docs:
                    id = doc[0]
                    data = doc[1]
                    tmp = f'''<ePOSPrint>
<Parameter>
<devid>local_printer</devid>
<timeout>10000</timeout>
<printjobid>{id[:23]}</printjobid>
</Parameter>
<PrintData>
{data}
</PrintData>
</ePOSPrint>'''
                    response = response + tmp
                
                response = response + "</PrintRequestInfo>"

            conn.commit()
            cur.close()
            conn.close()
            return Response(content=response, media_type="text/xml")
        
        raise HTTPException(status_code=401, detail="Unauthorized")
    elif connection_type == "SetResponse":
        print(body)

    return ""

@app.post("/print_jobs")
async def post_print_jobs(Authorization: Annotated[str, Header()], req: Document):
    api_key = Authorization.split(" ")[1] if "Bearer " in Authorization else None
    if not api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user = auth.authorize(api_key)

    if user:
        doc = req.doc_xml
        conn = pg.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO esdp.print_jobs (created_by, doc_xml) VALUES (%s, %s)", (user, doc,))
        conn.commit()
        cur.close()
        conn.close()
        return "OK"
    
    raise HTTPException(status_code=401, detail="Unauthorized")