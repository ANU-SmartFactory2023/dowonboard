#wafer_maker.py

import random
import time

class WaferMaker:

    def making( self ):
        for i in range( 0, 5 ):
            time.sleep(1)
            print(".")
            
        print( "complete" )

        return (int)(random.random()*100)