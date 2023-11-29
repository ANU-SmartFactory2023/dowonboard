
from enum import Enum
import time
from motor import Motor, GuideMotorStep
from sensor import Sensor
from server_communication import ServerComm


class Step( Enum ) :    #각 스텝별 이름, 동사형으로 지을것, 무엇을 하는 스텝인지 알 수 있는 네이밍
    start=0    
    process_start = 10   
    sonic_part_sensor_check = 100
    measure_start_check = 200
    measure_start = 300
    measure_section_pass_check = 400
    stop_rail = 500
    calculated_values_send = 600
    servo_motor_drive = 700
    go_rail_next = 800

currnet_step = Step.start   #기본설정
running = True  

sensor = Sensor()   #센서 참조
server_comm = ServerComm()  #서버참조

pass_or_fail:bool = False

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
            currnet_step = Step.sonic_part_sensor_check #다음스텝으로 이동

        case Step.sonic_part_sensor_check:  #1번 초음파 센서에 감지
            print( Step.sonic_part_sensor_check )
            if( sensor.get_sensor_state( SONIC_PART_SENSOR_PIN_NO1 ) ):
                # 감지상태
                # 서버에게 센서 감지상태를 포스트로 전달한다.
                server_comm.setSensorState( True )
                currnet_step = Step.measure_start_check

        case Step.measure_start_check:  #계산함수 시작조건 - 센서감지
            print( Step.measure_start_check )          
            if( sensor.get_sensor_state(SONIC_PART_SENSOR_PIN_NO1) ):   
                #계산함수 시작전 적외선 센서 감지             
                currnet_step = Step.measure_start

        case Step.measure_start:
            print( Step.measure_start )
            value = sensor.getSonicValue()  # 초음파센서값
            measure.add( value ) # measure에 값 삽입                           
            currnet_step = Step.measure_section_pass_check

        case Step.measure_section_pass_check:   #구간종료
            print( Step.measure_section_pass_check )
            if( sensor.get_sensor_state(SONIC_PART_SENSOR_PIN_NO2) ): #2번 적외선센서 도달
                measure.stop(value) #값 삽입 중단                          
                currnet_step = Step.stop_rail

        case Step.stop_rail:
            print( Step.stop_rail )
            result = motor.#DC모터 정지            
            currnet_step = Step.calculated_values_send

        case Step.calculated_values_send:
            resutl = measure.clac()     # 값계산
            pass_or_fail = server_comm.sendData( result )  #서버에 값송신
            currnet_step = Step.servo_motor_drive
                
        case Step.servo_motor_drive:
            motor_step = GuideMotorStep.stop    #기본 stop
            if( pass_or_fail ):                 #서버에서 받은 불량기준
                motor_step = GuideMotorStep.good
            else :
                motor_step = GuideMotorStep.fail

            motor.doGuideMotor( motor_step )    #위에 따라서 모터구동 
            currnet_step = Step.go_rail_next
            
        case Step.go_rail_next:
            print( Step.go_rail )
            result = motor.#DC모터 구동            
            currnet_step = Step.start


        
        
        