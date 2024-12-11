import argparse
from pymavlink import mavutil

# Função auxiliar para enviar comandos de movimento
def send_ned_velocity(the_connection, north, east, down):
    """Envia um comando de movimento NED relativo ao drone."""
    the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(
        10,  # Tempo do sistema em ms
        the_connection.target_system, 
        the_connection.target_component, 
        mavutil.mavlink.MAV_FRAME_LOCAL_OFFSET_NED,  # Sistema de referência
        int(0b110111111000),  # Máscara dir>esq: x, y, z, vx, vy, vz, ax, ay, az, ignorar, yaw, yaw rate
        north, east, down,  # Movimentos NED
        0, 0, 0,  # Não alteramos velocidades
        0, 0, 0,  # Não alteramos acelerações
        0, 0      # Não alteramos yaw
    ))

# Função auxiliar para esperar até que o waypoint seja atingido
def wait_for_waypoint_reached(the_connection):
    """Espera até que o waypoint seja atingido, verificando se a distância está abaixo de um limiar."""
    while True:
        msg = the_connection.recv_match(type='NAV_CONTROLLER_OUTPUT', blocking=True)
        if msg:
            waypoint = msg.wp_dist
            print(f"Distância ao waypoint: {waypoint} metros")
            if waypoint == 0:  # Tolerância atingida
                print("Waypoint atingido.")
                return

def main():
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(description="Envia um comando de movimento NED ao BlueROV2.")
    parser.add_argument("--conexao", type=str, required=True, help="Tipo de conexão com o veículo. Ex.: 'tcp:127.0.0.1:5763'")
    parser.add_argument("--north", type=float, required=True, help="Movimento no eixo norte (metros).")
    parser.add_argument("--east", type=float, required=True, help="Movimento no eixo leste (metros).")
    parser.add_argument("--down", type=float, required=True, help="Movimento no eixo vertical (metros, positivo para baixo).")
    args = parser.parse_args()

    # Conectar ao drone
    the_connection = mavutil.mavlink_connection(args.conexao)

    # Esperar pelo primeiro heartbeat
    the_connection.wait_heartbeat()
    print(f"Heartbeat recebido do sistema {the_connection.target_system}, componente {the_connection.target_component}")

    # Enviar o comando com os argumentos fornecidos
    print(f"Enviando comando: North={args.north}, East={args.east}, Down={args.down}")
    send_ned_velocity(the_connection, args.north, args.east, args.down)

    # Esperar até que o waypoint seja atingido
    wait_for_waypoint_reached(the_connection)

if __name__ == "__main__":
    main()
