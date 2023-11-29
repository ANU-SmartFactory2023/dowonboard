#server_communication.py
import http.client
import json
from models import Process

class ServerComm :
    conn:http.client.HTTPConnection
    headers = {"Content-type": "application/json", "Accept": "*/*"}
    
    def __init__( self ) :
        self.conn = http.client.HTTPConnection( 'localhost', 5294 )
    
    def ready(self) :
        self.conn.request( 'GET', '/api/state' )
        result = self.conn.getresponse().read().decode()
        json_object = json.loads( result )
        msg = json_object[ 'msg' ]
        statusCode = json_object[ 'statusCode' ]
        print( "ready : " + result )
        
        return result
    
    def send_data(self, p:Process) :
        self.conn.request( 'POST', '/api/process', json.dumps( p.__dict__ ), self.headers )
        result = self.conn.getresponse().read().decode()
        
        print( "recvdata : " + result )
        
