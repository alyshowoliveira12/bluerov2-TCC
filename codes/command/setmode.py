from pymavlink import mavutil

# Estabelecer a conexão com o BlueROV2
the_connection = mavutil.mavlink_connection('udp:localhost:14445')

# Esperar o heartbeat
the_connection.wait_heartbeat()
print(f"Conectado ao sistema (system {the_connection.target_system} component {the_connection.target_component})")

# Definir o modo desejado (exemplo: STABILIZE)
MODE = 'GUIDED'

# Função para definir o modo
def set_mode(mode):
    # Obter o número do modo a partir do nome
    mode_id = the_connection.mode_mapping()[mode]
    the_connection.mav.set_mode_send(
        the_connection.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_GUIDED_ENABLED,
        mode_id
    )
    print(f"Modo definido para: {mode}")

# Alterar para o modo STABILIZE
set_mode(MODE)
