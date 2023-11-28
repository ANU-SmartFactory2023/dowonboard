
from enum import Enum
import time
from motor import Motor, GuideMotorStep
from sensor import Sensor
from server_communication import ServerComm


class Step( Enum ) :
    start=0    
    input_part_sensor_check = 10   
    wait_server_state= 20 
    go_rail= 30        
    photo_part_detect_sensor_check = 50
    stop_rail = 100
    photo_process = 150
    servo_motor_drive =300  
    sonic_part_detect_sensor_check= 400
    
    

   

currnet_step = Step.start
running = True

sensor = Sensor()
server_comm = ServerComm()

pass_or_fail:bool = False

INPUT_PART_SENSOR_PIN_NO = 17
PHOTO_PART_SENSOR_PIN_NO = 18
SONIC_PART_SENSOR_PIN_NO1 = 19
SONIC_PART_SENSOR_PIN_NO2 = 20

while running:
    print( "running : " + str( running ) )# 디버깅확인용
    time.sleep( 0.1 )
    match currnet_step :
        case Step.start: 
            print( Step.start )
            motor.doGuideMotor( GuideMotorStep.stop )
            #시작하기전에 검사할것들: 통신확인여부, 모터정렬, 센서 검수
            currnet_step = Step.input_part_sensor_check
        
        case Step.input_part_sensor_check:
            print( Step.input_part_sensor_check )
            if( sensor.get_sensor_state( INPUT_PART_SENSOR_PIN_NO ) ):
                #1번핀의 감지상태
                # 서버에게 센서 감지상태를 포스트로 전달한다.
                # server_comm.setSensorState( True )
                currnet_step = Step.wait_server_state
            
        case Step.wait_server_state:
            print( Step.wait_server_state )
            result = server_comm.ready()#get으로 물어보는 함수
            if( result == "ok" ):
                currnet_step = Step.go_rail
            
        case Step.go_rail:
            print( Step.go_rail )
            result = motor.#DC모터 구동            
            currnet_step = Step.end

        case Step.photo_part_detect_sensor_check:
            print( Step.photo_part_detect_sensor_check )
            if( sensor.get_sensor_state(PHOTO_PART_SENSOR_PIN_NO) ):                
                currnet_step = Step.stop_rail

        case Step.stop_rail:
            print( Step.stop_rail )
            result = motor.#DC모터 정지            
            currnet_step = Step.photo_process
        
        case Step.photo_process:
            print( Step.photo_process)
            result = sensor.#이미지 처리 값
            pass_or_fail = server_comm.#서버에값을 전달( result )

            currnet_step = Step.servo_motor_drive
                
        case Step.servo_motor_drive:
            motor_step = GuideMotorStep.stop
            if( pass_or_fail ):
                motor_step = GuideMotorStep.good
            else :
                motor_step = GuideMotorStep.fail

            motor.doGuideMotor( motor_step )

        case Step.go_rail_next:
            print( Step.go_rail )
            result = motor.#DC모터 구동            
            currnet_step = Step.end
            
        case Step.sonic_part_detect_sensor_check:
            print( Step.sonic_part_detect_sensor_check )
            if( sensor.get_sensor_state(SONIC_PART_SENSOR_PIN_NO) ):                
                currnet_step = Step.stop_rail

        case Step.stop_rail:
            print( Step.stop_rail )
            result = motor.#DC모터 정지            
            currnet_step = Step.start





        case Step.measure_start_check:

            if( sensor.get_sensor_state(SONIC_PART_SENSOR_PIN_NO1) ):                
                currnet_step = Step.measure



        case Step.measure:
            value = sensor.getSonicValue()
            measure.add( value )

            if( sensor.get_sensor_state(SONIC_PART_SENSOR_PIN_NO2) ):                
                currnet_step = Step.clac
        
        case Step.clac:
            resutl = measure.clac()
            server_comm.sendData( result )