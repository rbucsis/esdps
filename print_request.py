import functions_framework
import datetime

test_payload = '''<?xml version="1.0" encoding="utf-8"?>
<PrintRequestInfo Version="2.00">
  <ePOSPrint>
<Parameter>
  <devid>local_printer</devid>
  <timeout>10000</timeout>
  <printjobid>ABC123</printjobid>
</Parameter>
<PrintData>
<epos-print xmlns="http://www.epson-pos.com/schemas/2011/03/epos-print">
     <text lang="en" /> 
     <text smooth="true" /> 
     <text align="center" /> 
     <text font="font_b" /> 
     <text width="2" height="2" /> 
     <text reverse="false" ul="false" em="true" color="color_1" /> 
     <text>DELIVERY TICKET</text> 
     <feed unit="12" /> 
     <text></text> 
     <text align="left" /> 
     <text font="font_a" /> 
     <text width="1" height="1" /> 
     <text reverse="false" ul="false" em="false" color="color_1" /> 
     <text>Order 0001</text> 
     <text width="1" height="1" /> 
     <text reverse="false" ul="false" em="false" color="color_1" /> 
     <text>Time Mar 19 2013 13:53:15</text> 
     <text>Seat A-3</text> 
     <text></text> 
     <text width="1" height="1" /> 
     <text reverse="false" ul="false" em="false" color="color_1" /> 
     <text>Alt Beer</text> 
     <text>$6.00 x 2</text> 
     <text x="384" /> 
     <text>$12.00</text> 
     <text></text> 
     <text reverse="false" ul="false" em="true" /> 
     <text width="2" height="1" /> 
     <text>TOTAL</text> 
     <text x="264" /> 
     <text>$12.00</text> 
     <text reverse="false" ul="false" em="false" /> 
     <text width="1" height="1" /> 
     <feed unit="12" /> 
     <text align="center" /> 
     <barcode type="code39" hri="none" font="font_a" width="2" height="60">0001</barcode> 
     <feed line="3" /> 
     <cut type="feed" /> 
     </epos-print>
</PrintData>
  </ePOSPrint>
  <ePOSPrint>
<Parameter>
  <devid>local_printer</devid>
  <timeout>10000</timeout>
  <printjobid>ABC123</printjobid>
</Parameter>
<PrintData>
<epos-print xmlns="http://www.epson-pos.com/schemas/2011/03/epos-print">
     <text lang="en" /> 
     <text smooth="true" /> 
     <text align="center" /> 
     <text font="font_b" /> 
     <text width="2" height="2" /> 
     <text reverse="false" ul="false" em="true" color="color_1" /> 
     <text>DELIVERY TICKET 2</text> 
     <feed unit="12" /> 
     <text></text> 
     <text align="left" /> 
     <text font="font_a" /> 
     <text width="1" height="1" /> 
     <text reverse="false" ul="false" em="false" color="color_1" /> 
     <text>Order 0001</text> 
     <text width="1" height="1" /> 
     <text reverse="false" ul="false" em="false" color="color_1" /> 
     <text>Time Mar 19 2013 13:53:15</text> 
     <text>Seat A-3</text> 
     <text></text> 
     <text width="1" height="1" /> 
     <text reverse="false" ul="false" em="false" color="color_1" /> 
     <text>Alt Beer</text> 
     <text>$6.00 x 2</text> 
     <text x="384" /> 
     <text>$12.00</text> 
     <text></text> 
     <text reverse="false" ul="false" em="true" /> 
     <text width="2" height="1" /> 
     <text>TOTAL</text> 
     <text x="264" /> 
     <text>$12.00</text> 
     <text reverse="false" ul="false" em="false" /> 
     <text width="1" height="1" /> 
     <feed unit="12" /> 
     <text align="center" /> 
     <barcode type="code39" hri="none" font="font_a" width="2" height="60">0001</barcode> 
     <feed line="3" /> 
     <cut type="feed" /> 
     </epos-print>
</PrintData>
  </ePOSPrint>
</PrintRequestInfo>'''

@functions_framework.http
def handler(req):
    print(str(datetime.datetime.now()), str(req))
    body = req.get_json(silent=True)
    headers = req.headers
    query = req.params
    if body:
        print(body)
    print(headers)
    print(query)
    return ""