from pymavlink import mavutil
import time

# Função auxiliar para enviar comandos de movimento
def send_ned_velocity(the_connection, north, east, down):
    """Envia um comando de movimento NED relativo ao drone."""
    the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(
        10, #tempo do sistema em mls
        the_connection.target_system, 
        the_connection.target_component, 
        mavutil.mavlink.MAV_FRAME_LOCAL_OFFSET_NED, #sistema de referencia
        int(0b110111111000),  # Máscara dir>esq: x, y, z, vx, vy, vz, ax, ay, az, ignorar, yaw, yaw rate
        north, east, down,    # Movimentos NED
        0, 0, 0,  # Não alteramos velocidades
        0, 0, 0,  # Não alteramos acelerações
        0, 0      # Não alteramos yaw
    ))

# Função auxiliar para esperar até que o waypoint seja atingido
def wait_for_waypoint_reached(the_connection):
    """Espera até que o waypoint seja atingido, verificando se a distância está abaixo de um limiar."""
    waypoint = 0
    
    # Ignorar as primeiras leituras de waypoint até que recebamos um valor válido
    while waypoint == 0:
        msg = the_connection.recv_match(type='NAV_CONTROLLER_OUTPUT', blocking=True)
        if msg:
            waypoint = msg.wp_dist
            print(f"Primeira leitura - distância ao waypoint: {waypoint} metros")
    
    # Agora que temos um valor válido, podemos esperar até que o waypoint seja atingido
    while True:
        msg = the_connection.recv_match(type='NAV_CONTROLLER_OUTPUT', blocking=True)
        if msg:
            waypoint = msg.wp_dist
            print(f"Distância ao waypoint: {waypoint} metros")
            if waypoint == 0:  # Tolerância ?
                print("Waypoint atingido.")
                return

# Start a connection listening on a UDP port
the_connection = mavutil.mavlink_connection('tcp:127.0.0.1:5763')

# Wait for the first heartbeat
the_connection.wait_heartbeat()
print(f"Heartbeat recebido do sistema {the_connection.target_system} componente {the_connection.target_component}")

# Definimos os movimentos em uma lista (Norte, Leste, Sul, Oeste)
movimentos = [
    (5, 0, 0),  # Movimento 1: 5 metros para o norte
    (0, 5, 0),  # Movimento 2: 5 metros para o leste
    (-5, 0, 0),   # Movimento 3: 5 metros para o sul
    (0, -5, 0)    # Movimento 4: 5 metros para o oeste
]

# Loop pelos movimentos
for i, movimento in enumerate(movimentos):
    print(f"Movimento {i+1}: {movimento}")
    send_ned_velocity(the_connection, *movimento)
    
    # Espera até que o waypoint seja atingido antes de passar para o próximo movimento
    wait_for_waypoint_reached(the_connection)

print("Padrão quadrado completo!")