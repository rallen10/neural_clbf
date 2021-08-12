import rospy
import battery_status
import message_creator
from math import pi


def execute_command(command_publisher, move_command, move_command_translational,
                    move_command_angular, position, rotation):
    """
    
    Sends movement command created by a control script to a turtlebot.
    Also pushes information to message_creator.py to output a message
    to the console.

    Arguments:
        command_publisher: publisher node on which to send commands

        move_command: empty twist object; not a command in and of itself.
        the angular and linear properties of move_command are set to
        move_command_angular and move_command_translational, respectively,
        within this function.

        move_command_translational: command to make the turtlebot
        move either forward or backwards

        move_command_angular: command to make the turtlebot rotate

        position: turtlebot's current position

        rotation: turtlebot's current attitude
    
    """
    max_command_translational = 0.3
    max_command_rotational = 1

    if move_command_translational > max_command_translational:
        move_command_translational = max_command_translational

    move_command.linear.x = move_command_translational

    if move_command_angular > max_command_rotational:
        move_command_angular = max_command_rotational

    move_command.angular.z = move_command_angular

    # send the command to the turtlebot
    command_publisher.publish(move_command)
    
    # publish turtlebot status to console
    message_creator.create_message(
        move_command, battery_status.batteryLevel, position, rotation*360/(2*pi)
    )

    # briefly pause to avoid overloading turtlebot with commands, which will
    # cause sync issues
    rospy.sleep(.001)