import cv2
import numpy as np

# Definindo o dicionário ArUco e carregando a imagem
# O dicionário contém os padrões das marcas ArUco
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
image_path = "captured_frame.png"  # Caminho para a imagem capturada
image = cv2.imread(image_path)

# Verificar se a imagem foi carregada corretamente
if image is None:
    print("[ERROR] Imagem não encontrada!")
    exit(1)

print("[INFO] Detectando marcas ArUco...")

# Configuração dos parâmetros do detector ArUco
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

# Configuração da matriz da câmera e coeficientes de distorção
# A matriz define os parâmetros intrínsecos da câmera
cameraMatrix = np.array([
    [800, 0, 320],  # fx, 0, cx
    [0, 800, 240],  # 0, fy, cy
    [0, 0, 1]       # 0, 0, 1
], dtype="float32")
distCoeffs = np.zeros((4, 1))  # Sem distorção da lente

# Definir o tamanho real da marca (em centímetros)
markerSizeInCM = 10

# Detectar marcas ArUco na imagem
markerCorners, markerIds, _ = detector.detectMarkers(image)

# Verificar se foram detectadas marcas ArUco
if markerIds is not None:
    markerIds = markerIds.flatten()  # Achatar a lista de IDs para iteração
    for (markerCorner, markerID) in zip(markerCorners, markerIds):
        # Estimar a pose da marca (rotação e translação)
        rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
            markerCorner, markerSizeInCM, cameraMatrix, distCoeffs
        )

        # Obter os cantos da marca e convertê-los para coordenadas inteiras
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

        # Obter a distância da marca em relação à câmera
        distance = tvec[0][0][2]
        cv2.putText(image, f"ID: {markerID} Dist: {distance:.2f}cm",
                    (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 2)

        # Exibir informações no console
        print(f"[INFO] Marca ID {markerID} está a {distance:.2f} cm de distância.")
else:
    print("[INFO] Nenhuma marca detectada.")

# Exibir a imagem com as marcas destacadas
cv2.imshow("Detecção de Marcas ArUco", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
