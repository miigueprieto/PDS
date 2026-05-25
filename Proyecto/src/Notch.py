import cv2
import numpy as np

def filtro_notch(imagen, centers=[(30, 30)]):
    # OpenCV usa BGR -> Nos aseguramos de tener la escala de grises
    if len(imagen.shape) == 3:
        img_gray = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
    else:
        img_gray = np.copy(imagen)

    # FFT
    f = np.fft.fft2(img_gray)
    fshift = np.fft.fftshift(f)

    # Crear máscara notch
    rows, cols = img_gray.shape
    mask = np.ones((rows, cols), np.float32)

    for (u, v) in centers:
        cv2.circle(mask, (cols//2 + u, rows//2 + v), 10, 0, -1)
        cv2.circle(mask, (cols//2 - u, rows//2 - v), 10, 0, -1)

    # Aplicar filtro
    filtered = fshift * mask

    # FFT inversa
    ishift = np.fft.ifftshift(filtered)
    img_back = np.fft.ifft2(ishift)
    img_back = np.abs(img_back)

    return img_back