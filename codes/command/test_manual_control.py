from pymavlink import mavutil

# Start a connection listening on a UDP port
the_connection = mavutil.mavlink_connection('udp:localhost:14445')

# Esperar pelo primeiro heartbeat até que o sistema correto responda
while True:
    the_connection.wait_heartbeat()
    if the_connection.target_system != 0:
        break
    print("Esperando o sistema correto...")

print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))


the_connection.mav.send(mavutil.mavlink.MAVLink_manual_control_message(the_connection.target_system, 10, 0, 10, 0, 0))
