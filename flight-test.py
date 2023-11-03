# Import Packages
from dronekit import connect, VehicleMode, LocationGlobalRelative,APIException
import time
import socket
import exceptions
import mathimport 
import argparse



def ConnectMyCopter():
    parser = argparse.ArgumentParser(description="commands")
    parser.add_argument(--connect)
    args = parser.parse_args()

    connection_string = args.connect
    baud_rate = 57600

    vehicle = connect(connection_string,
                      baud=baud_rate,
                      wait_ready=True)
    
    return vehicle


def Arm():

    while vehicle.is_armable == False:
        print("Waiting for vehicle to become armable...")
        time.sleep(1)
    print("Vehicle is now armable")
    print("\n")

    vehicle.armed = True

    while vehicle.armed == False:
        print("Waiting for drone to arm...")
        time.sleep(1)
    
    
        print("Vehicle is now armed.")
        print("PROPS ARE SPINNING!")  

        return None
    

vehicle = ConnectMyCopter()

Arm()

print("End of Script")
    
 
