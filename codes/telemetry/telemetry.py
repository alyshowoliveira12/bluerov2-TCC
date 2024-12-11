import argparse
from pymavlink import mavutil

def main():
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(description="Coleta de dados de telemetria do BlueROV2.")
    parser.add_argument("--conexao", type=str, required=True, help="Tipo de conexão. Exemplo: 'udpin:localhost:14445'")
    parser.add_argument("--tipo", type=str, required=True, choices=["SYS_STATUS", "ATTITUDE", "SCALED_PRESSURE"],
                        help="Tipo de mensagem de telemetria a ser coletada: SYS_STATUS, ATTITUDE ou SCALED_PRESSURE")
    args = parser.parse_args()

    # Conexão com o veículo
    the_connection = mavutil.mavlink_connection(args.conexao)

    # Aguarda o primeiro heartbeat para sincronizar o sistema e o componente
    the_connection.wait_heartbeat()
    print(f"Conexão estabelecida com o sistema {the_connection.target_system}, componente {the_connection.target_component}")

    # Receber mensagem do tipo especificado
    msg = the_connection.recv_match(type=args.tipo, blocking=True, timeout=5)
    if not msg:
        print("Nenhuma mensagem recebida no intervalo de tempo.")
        return

    # Processar e exibir dados da mensagem recebida
    if args.tipo == "SYS_STATUS":
        print(f"Voltage Battery: {msg.voltage_battery / 1000.0} V")
        print(f"Current Battery: {msg.current_battery / 100} A")

    elif args.tipo == "ATTITUDE":
        print(f"Roll: {msg.roll} rad")
        print(f"Pitch: {msg.pitch} rad")
        print(f"Yaw: {msg.yaw} rad")

    elif args.tipo == "SCALED_PRESSURE":
        print(f"Absolute Pressure: {msg.press_abs} hPa")
        print(f"Differential Pressure: {msg.press_diff} hPa")

if __name__ == "__main__":
    main()
