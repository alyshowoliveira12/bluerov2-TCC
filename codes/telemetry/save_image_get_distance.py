import vlc
import time
import os
import cv2
import numpy as np

# Configurações da stream de vídeo
sdp_path = "stream.sdp"  # Caminho para o arquivo SDP
snapshot_path = "frame.png"  # Caminho para salvar o frame capturado

# Configuração do VLC
print("[INFO] Iniciando stream de vídeo...")
instance = vlc.Instance("--quiet")
player = instance.media_player_new()
media = instance.media_new(sdp_path)
media.add_option("network-caching=300")  # Reduzir latência
player.set_media(media)
player.play()

# Aguarda o carregamento da stream
time.sleep(2)

# Captura o frame do vídeo
print("[INFO] Capturando frame...")
result = player.video_take_snapshot(0, snapshot_path, 0, 0)

# Verificar se o frame foi salvo com sucesso
if result == 0 and os.path.exists(snapshot_path):
    print(f"[INFO] Frame capturado e salvo como: {snapshot_path}")
else:
    print("[ERROR] Falha ao capturar o frame.")
    player.stop()
    exit(1)

# Parar o player e liberar recursos
player.stop()
print("[INFO] Player de vídeo fechado.")

# Adicionar um timer antes de iniciar a detecção (opcional)
print("[INFO] Iniciando detecção de marcas ArUco em 3 segundos...")
time.sleep(3)

# Parte 2: Detecção de marcas ArUco
print("[INFO] Carregando imagem capturada...")
image = cv2.imread(snapshot_path)

# Verificar se a imagem foi carregada corretamente
if image is None:
    print("[ERROR] Imagem não encontrada!")
    exit(1)

print("[INFO] Detectando marcas ArUco...")
# Configuração do dicionário ArUco e parâmetros do detector
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

# Configuração da matriz da câmera e coeficientes de distorção
cameraMatrix = np.array([
    [800, 0, 320],  # fx, 0, cx
    [0, 800, 240],  # 0, fy, cy
    [0, 0, 1]       # 0, 0, 1
], dtype="float32")
distCoeffs = np.zeros((4, 1))  # Sem distorção da lente

# Tamanho real da marca em centímetros
markerSizeInCM = 10

# Detectar marcas ArUco na imagem
markerCorners, markerIds, _ = detector.detectMarkers(image)

# Verificar se foram detectadas marcas ArUco
if markerIds is not None:
    markerIds = markerIds.flatten()  # Achatar IDs para iteração
    for (markerCorner, markerID) in zip(markerCorners, markerIds):
        # Estimar pose da marca (rotação e translação)
        rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
            markerCorner, markerSizeInCM, cameraMatrix, distCoeffs
        )

        # Obter os cantos da marca e converter para inteiros
        corners = markerCorner.reshape((4, 2))
        topLeft, topRight, bottomRight, bottomLeft = map(lambda pt: (int(pt[0]), int(pt[1])), corners)

        # Desenhar as bordas da marca na imagem
        cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
        cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
        cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
        cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)

        # Calcular o centro da marca
        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)
        cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)

        # Obter a distância da marca (z do vetor de translação)
        distance = tvec[0][0][2]
        cv2.putText(image, f"ID: {markerID} Dist: {distance:.2f}cm",
                    (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 2)

        # Exibir informações no console
        print(f"[INFO] Marca ID {markerID} está a {distance:.2f} cm de distância.")
else:
    print("[INFO] Nenhuma marca detectada.")

# Exibir a imagem resultante
cv2.imshow("Detecção de Marcas ArUco", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
