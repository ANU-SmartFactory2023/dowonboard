
from enum import Enum
import time
from models import Process
from sensor import Sensor
from server_communication import ServerComm
from wafer_maker import WaferMaker

class Step( Enum ) :
    start=0
    check_sensor=1
    wait_server_state=5
    make_wafer=11
    end=99

currnet_step = Step.start
running = True

exist_sensor = Sensor()
server_comm = ServerComm()
wafer_maker = WaferMaker()

while running:
    print( "running : " + str( running ) )
    time.sleep( 0.1 )
    match currnet_step :
        case Step.start: 
            print( Step.start )
            
            currnet_step = Step.check_sensor
        
        case Step.check_sensor:
            print( Step.check_sensor )
            if( exist_sensor.get_sensor_state() ):
                currnet_step = Step.wait_server_state
            
        case Step.wait_server_state:
            print( Step.wait_server_state )
            result = server_comm.ready()
            
            currnet_step = Step.make_wafer
            
        case Step.make_wafer:
            print( Step.make_wafer )
            result = wafer_maker.making()
            
            p = Process()
            p.name = "Wafer make"
            p.value = result
            server_comm.send_data( p )
            
            currnet_step = Step.end
                
        case Step.end:
            print( Step.end )
            running = False
           