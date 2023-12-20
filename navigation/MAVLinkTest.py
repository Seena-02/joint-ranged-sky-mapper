# Imports
import math
from pymavlink import mavutil

# Create class to format Mission Item.
class mission_item:
    def __init__(self, i, current, x, y, z):
        self.seq = i
        self.frame = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT # Yse Global Latitude and Longitude for position data
        self.command = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT # Move to the waypoint
        self.current = current
        self.auto = 1
        self.param1 = 0.0
        self.param2 = 2.0
        self.param3 = 20.00
        self.param4 = math.nan
        self.param5 = x
        self.param6 = y
        self.param7 = z
        self.mission_type = 0 # The MAV_MISION_TYPE value for MAV_TYPE_MISSION


# Arm the Drone.
def arm(the_connection):
    print("-- Arming")
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0 ,0 ,0 ,0)
    ack(the_connection, "COMMAND_ACK")


# Takeoff.
def takeoff(the_connection):
    print("-- Takeoff Initiated")
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, math.nan ,0 ,0 ,10)
    ack(the_connection, "COMMAND_ACK")


# Upload the mission items to drone.
def upload_mission(the_connection, mission_items):
    n = len(mission_items)
    print("-- Sending Message out")

    the_connection.mav.mission_count_send(the_connection.target_system, the_connection.target_component, n, 0)

    ack(the_connection, "MISSION_REQUEST")

    for waypoint in mission_items: # mission_items created based on MavLink message protocol
        print("-- Creating a waypoint")

        the_connection.mav.mission_item_send(the_connection.target_system,      # Target System
                                            the_connection.target_component,   # Target Comoponent
                                            waypoint.seq,                      # Sequence
                                            waypoint.frame,                    # Frame
                                            waypoint.command,                  # Command
                                            waypoint.current,                  # Current
                                            waypoint.auto,                     # AutoContinue
                                            waypoint.param1,                   # Hold Time
                                            waypoint.param2,                   # Accept Radius
                                            waypoint.param3,                   # Pass Radius
                                            waypoint.param4,                   # Yaw
                                            waypoint.param5,                   # Local X
                                            waypoint.param6,                   # Local Y
                                            waypoint.param7,                   # Local X
                                            waypoint.mission_type)             # Mission Type
        
    if waypoint != mission_items[n - 1]:
        ack(the_connection, "MISSION_REQUEST")
    ack(the_connection, "MISSION_ACK")

# Send message for the drone to return to the launch point
def set_return(the_connection):
    print("-- Set Return To launch")
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                         mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0 ,0 ,0 ,0)
    
    ack(the_connection, "COMMAND_ACK")


# Start Mission
def start_mission(the_connection):
    print("-- Mission Start")
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                         mavutil.mavlink.MAV_CMD_MISSION_START, 0, 0, 0, 0, 0 ,0 ,0 ,0)
    ack(the_connection, "COMMAND_ACK")

# Acknoledgement from the Drone
def ack(the_connection, keyword):
    print("-- Message Read " + str(the_connection.recv_match(type=keyword, blocking=True)))


# Main Function
if __name__ == "__main__":
    print("-- Program Started")
    the_connection = mavutil.mavlink_connection('udp:localhost:14540')

    while(the_connection.target_system == 0):
        print("-- Checking Hearbeat")
        the_connection.wait_heartbeat()
        print("-- Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

        mission_waypoints = []

        mission_waypoints.append(mission_item(0, 0, 42.434193622721835, -83.98698183753619, 10)) # Above takeoff point
        mission_waypoints.append(mission_item(1, 0, 42.43432724637685, -83.98613425948624, 10))  # Above Destination Point 
        mission_waypoints.append(mission_item (2, 0, 42.43432724637685, -83.98613425948624, 5))  # Destination Point

        upload_mission(the_connection, mission_waypoints)

        arm(the_connection)

        takeoff(the_connection)

        start_mission(the_connection)

        for mission_item in mission_waypoints:
            print("-- Message Read " + str(the_connection.recv_match(type="MISSION_ITEM_REACHED", condition="MISSION_ITEM_REACHED.seq == {0}".format(mission_item.seq) , blocking=True)))

        set_return(the_connection)


