from fastapi import Response,status
import json

def res(content, status_code):
    return Response(content=json.dumps(content), status_code=status_code)
    
