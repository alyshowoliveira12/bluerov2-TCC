import argparse
from pymavlink import mavutil

def main():
    # Configurar o parser de argumentos
    parser = argparse.ArgumentParser(description="Conexão e controle do BlueROV2 via MAVLink.")
    parser.add_argument(
        "--conexao",
        type=str,
        required=True,
        help="Tipo de conexão com o sistema. Exemplos: 'udp:localhost:14445' ou 'tcp:127.0.0.1:5763'"
    )
    args = parser.parse_args()

    # Iniciar a conexão com base no tipo fornecido
    the_connection = mavutil.mavlink_connection(args.conexao)

    # Esperar pelo primeiro heartbeat até que o sistema correto responda
    while True:
        the_connection.wait_heartbeat()
        if the_connection.target_system != 0:  # Certifique-se de que a resposta não seja de um sistema nulo
            break
        print("Esperando o sistema correto...")  # Informa que o sistema ainda não respondeu
    print(f"Heartbeat recebido do sistema {the_connection.target_system}, componente {the_connection.target_component}")

    # Enviar o comando para armar o veículo
    # Parâmetros: 
    # 1 - Arm/Disarm (1 para armar, 0 para desarmar)
    # 2 - 0: Armar/desarmar, sujeito a verificações de segurança 
    #     21196: Forçar armar/desarmar, ignorando verificações de segurança
    # 3 a 7 - Parâmetros adicionais, geralmente não usados para este comando
    the_connection.mav.command_long_send(
        the_connection.target_system,  # ID do sistema alvo
        the_connection.target_component,  # ID do componente alvo
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,  # Comando de armar/desarmar
        0,  # Confirmar comando
        1,  # Parâmetro para armar (1)
        0,  # 0: sujeito a verificações de segurança, 21196: força armar/desarmar
        0, 0, 0, 0, 0  # Outros parâmetros não utilizados aqui
    )

    # Receber a resposta do comando
    msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
    print("Resposta ao comando:", msg)

if __name__ == "__main__":
    main()
