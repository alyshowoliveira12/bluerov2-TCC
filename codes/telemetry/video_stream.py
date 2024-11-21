import cv2

cap = cv2.VideoCapture('udp://192.168.2.2:5600')

if not cap.isOpened():
    print("Erro ao abrir o stream de vídeo via FFMPEG")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Falha ao capturar o frame")
        break

    cv2.imshow('Video Stream', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
