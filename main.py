from fastapi import FastAPI, Request
from pydantic import BaseModel

class Document(BaseModel):
    doc_xml: str

app = FastAPI()

def auth(api_key):
    pass

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
async def post_print_jobs():
    pass