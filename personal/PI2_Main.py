from enum import Enum
import time
import os
import sys

# 현재 스크립트 파일의 디렉토리 경로
current_path = os.path.dirname(os.path.abspath(__file__))

# common 폴더의 경로 지정
common_folder_path = os.path.join(current_path, 'C:\\SFProject\\dowonboard\\common')

# sys.path에 common 폴더 경로 추가
sys.path.append(common_folder_path) 

# common 폴더 안에 있는 모듈들을 import 할 수 있음
from model import SensorModel, ProcessModel
from motor import Motor, GuideMotorStep
from sensor import Sensor
from server_communication import ServerComm


class Step( Enum ) :    #각 스텝별 이름, 동사형으로 지을것, 무엇을 하는 스텝인지 알 수 있는 네이밍
    start=0    
    process_start = 10   
    sonic_part_sensor_check = 100    
    measure_start = 300   
    stop_rail = 500
    calculated_values_send = 600
    servo_motor_drive = 700
    process_check = 750
    go_rail_next = 800

currnet_step = Step.start   #기본설정

running = True  
motor = Motor()  
sensor = Sensor()   #센서 참조
server_comm = ServerComm()  #서버참조

pass_or_fail = ''   #서버에서 주는 담아주는 값이 string 형태


SONIC_PART_ir_SENSOR_PIN_NO1 = 19
SONIC_PART_ir_SENSOR_PIN_NO2 = 20
RELAY_PART_ir_SENSOR_PIN = 21
while running:
    print( "running : " + str( running ) )# 디버깅확인용
    time.sleep( 0.1 )
    match currnet_step :

        case Step.start: 
            print( Step.start )
            motor.doGuideMotor( GuideMotorStep.stop )
            #시작하기전에 검사할것들: 통신확인여부, 모터정렬, 센서 검수
            currnet_step = Step.sonic_part_sensor_check #다음스텝으로 이동

        case Step.sonic_part_sensor_check:  #1번 초음파 센서에 감지
            print( Step.sonic_part_sensor_check )
            on_off = sensor.get_ir_sensor( SONIC_PART_ir_SENSOR_PIN_NO1 )
            if( on_off ):
                # 감지상태
                # 서버에게 센서 감지상태를 포스트로 전달한다.
                server_comm.confirmationObject(2,on_off)
                server_comm.etchingStart( True )
                currnet_step = Step.measure_start

        case Step.measure_start:
            print( Step.measure_start )
            value = sensor.get_sonic_sensor ()  # 초음파센서값
            measure.add( value ) # measure에 값 삽입     
            on_off = sensor.get_ir_sensor( SONIC_PART_ir_SENSOR_PIN_NO2 )
            if(on_off ): #2번 적외선센서 도달                
                server_comm.confirmationObject(3,on_off)
                currnet_step = Step.stop_rail

        case Step.stop_rail:
            print( Step.stop_rail )
            result = motor.stopConveyor#DC모터 정지            
            currnet_step = Step.calculated_values_send

        case Step.calculated_values_send:
            resutl = measure.clac()     # 값계산
            pass_or_fail = server_comm.etchingEnd( result )  #서버에 값송신
            currnet_step = Step.servo_motor_drive
                
        case Step.servo_motor_drive:
            motor_step = GuideMotorStep.stop    #기본 stop
            if( pass_or_fail == 'fail'):                 #서버에서 받은 불량기준
                motor_step = GuideMotorStep.fail
            else :
                motor_step = GuideMotorStep.good

            motor.doGuideMotor( motor_step )    #위에 따라서 모터구동 
            currnet_step = Step.process_check

        case Step.process_check:    #불량여부에 따라서 프로세스 수정
            result = motor.doConveyor#DC모터 구동 

            if(pass_or_fail == 'False'):
                time.sleep(5)       
                motor.stopConveyor()     
                currnet_step = Step.start
            else :
                currnet_step = Step.go_rail_next
            
        case Step.go_rail_next:
            print( Step.go_rail_next )
            if( sensor.get_ir_sensor(RELAY_PART_ir_SENSOR_PIN) ):
                motor.stopConveyor()         
                currnet_step = Step.start


        
        
        