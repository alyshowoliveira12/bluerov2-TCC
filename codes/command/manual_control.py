import argparse
from pymavlink import mavutil

def main():
    # Configurar o parser de argumentos
    parser = argparse.ArgumentParser(description="Controle manual do BlueROV2 via MAVLink.")
    parser.add_argument("--x", type=int, required=True, help="Comando para o eixo X (exemplo: velocidade longitudinal).")
    parser.add_argument("--y", type=int, required=True, help="Comando para o eixo Y (exemplo: velocidade lateral).")
    parser.add_argument("--z", type=int, required=True, help="Comando para o eixo Z (thruster: positivo = subir, negativo = descer).")
    parser.add_argument("--r", type=int, required=True, help="Comando para o eixo de rotação (yaw).")
    parser.add_argument("--buttons", type=int, default=0, help="Comando para botões (opcional).")

    args = parser.parse_args()

    # Iniciar conexão ouvindo em uma porta UDP
    the_connection = mavutil.mavlink_connection('udp:localhost:14445')

    # Esperar pelo primeiro heartbeat até que o sistema correto responda
    while True:
        the_connection.wait_heartbeat()
        if the_connection.target_system != 0:
            break
        print("Esperando o sistema correto...")

    print(f"Heartbeat recebido do sistema {the_connection.target_system}, componente {the_connection.target_component}")

    # Enviar comando manual com os argumentos fornecidos
    the_connection.mav.send(
        mavutil.mavlink.MAVLink_manual_control_message(
            the_connection.target_system,  # ID do sistema alvo
            args.x,  # Comando para o eixo X (frente/trás)
            args.y,  # Comando para o eixo Y (esquerda/direita)
            args.z,  # Comando para o eixo Z (thruster: positivo = subir, negativo = descer)
            args.r,  # Comando para o eixo de rotação (yaw)
            args.buttons  # Comando para botões (padrão: 0)
        )
    )
    print(f"Comando enviado: x={args.x}, y={args.y}, z={args.z}, r={args.r}, buttons={args.buttons}")

if __name__ == "__main__":
    main()
