from pymavlink import mavutil

# Start a connection listening on a UDP port
the_connection = mavutil.mavlink_connection('udp:localhost:14445')

# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
# Esperar pelo primeiro heartbeat até que o sistema correto responda
while True:
    the_connection.wait_heartbeat()
    if the_connection.target_system != 0:
        break
    print("Esperando o sistema correto...")
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)