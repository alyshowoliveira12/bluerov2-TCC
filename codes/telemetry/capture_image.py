import vlc
import time
import os

# Caminho para o arquivo SDP
# O arquivo SDP contém informações do stream que será capturado
sdp_path = "stream.sdp"

# Configuração do VLC
# Instância do VLC com a opção "--quiet" para minimizar mensagens no console
instance = vlc.Instance("--quiet")
player = instance.media_player_new()

# Configura o stream a partir do arquivo SDP
media = instance.media_new(sdp_path)
media.add_option("network-caching=300")  # Configura o cache da rede para reduzir a latência
player.set_media(media)

# Inicia a reprodução do stream
player.play()

# Aguarda o carregamento do stream antes de capturar o frame
print("Carregando o stream...")
time.sleep(2)

# Caminho para salvar o frame capturado
snapshot_path = "captured_frame.png"

# Captura um frame do stream e salva no caminho especificado
print("\nCapturando o frame...")
result = player.video_take_snapshot(0, snapshot_path, 0, 0)

# Verifica se a captura foi bem-sucedida e se o arquivo foi criado
if result == 0 and os.path.exists(snapshot_path):
    print(f"Frame capturado e salvo como: {snapshot_path}")
else:
    print("Erro ao salvar o frame.")

# Para o player e libera os recursos
player.stop()
print("Player fechado.")
