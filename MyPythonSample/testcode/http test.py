
import http.client, urllib.parse
import json

form_data = dict(name='test',password='1234')

class TestModel :
    name:str
    password:str
    
testModel = TestModel()
testModel.name = "test"
testModel.password = "1234"


conn = http.client.HTTPConnection( 'localhost', 5294 )

params = json.dumps( testModel.__dict__ )
headers = {"Content-type": "application/json",
           "Accept": "*/*"}

conn.request( 'POST', '/api/values/value3', params, headers  )
print( "value3 : " + conn.getresponse().read().decode() )







"""
r = requests.post( host_url + "/api/values/value3", json=form_data ).text #ok
print( "value3 : " + r )


print( "=============================================" )


r = requests.post( host_url + "/api/values/value1", json='{"name":"test","password":"1234"}' ).text #ok
print( "value1 : " + r )


print( "=============================================" )


class TestModel :
    name:str
    password:str
    
testModel = TestModel()
testModel.name = "test"
testModel.password = "1234"

r = requests.post( host_url + "/api/values/value3", json=testModel.__dict__ ).text #ok
print( "value3 : " + r )

"""