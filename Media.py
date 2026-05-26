# Cálculo numérico y convolución
import numpy as np
from scipy.signal import convolve2d

# Visualización
import matplotlib.pyplot as plt

# Manejo básico de imágenes y ruido
import skimage
import skimage.io as io
from skimage import util

plt.rcParams["figure.figsize"] = (16, 5)

def calcular_mse(original, procesada):
    return np.mean((original - procesada) ** 2)

def calcular_psnr(original, procesada, max_pixel=1.0):
    mse = calcular_mse(original, procesada)
    if mse == 0:
        return float('inf') 
    return 10 * np.log10((max_pixel ** 2) / mse)


img_org = io.imread("lena.bmp", as_gray=True)

# Añadimos ruido "Gaussiano" para simular la degradación
img_ruidosa = util.random_noise(img_org, mode='gaussian', var=0.015)

# Definimos y creamos una matriz de 3x3 llena de unos y la dividimos por 9 (K^2)
K = 3
media = np.ones((K, K)) / (K ** 2)

# mode='same' mantiene el tamaño de la matriz y utilizamos boundary='symm' para simular los bordes con el efecto espejo
resultado = convolve2d(img_ruidosa, media, mode='same', boundary='symm')

mse_ruido = calcular_mse(img_org, img_ruidosa)
psnr_ruido = calcular_psnr(img_org, img_ruidosa, max_pixel=1.0)

mse_filtro = calcular_mse(img_org, resultado)
psnr_filtro = calcular_psnr(img_org, resultado, max_pixel=1.0)

print("FILTRO DE MEDIA")
print(f"Imagen Ruidosa -> (MSE: {mse_ruido:.4f} | PSNR: {psnr_ruido:.2f} dB)")
print(f"Imagen Filtrada -> (MSE: {mse_filtro:.4f} | PSNR: {psnr_filtro:.2f} dB)")

# Visualización gráfica
fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

ax1.imshow(img_org, cmap='gray')
ax1.set_title('1. Imagen Original')
ax1.axis('off')

ax2.imshow(img_ruidosa, cmap='gray')
ax2.set_title('2. Ruido S&P')
ax2.axis('off')

ax3.imshow(resultado, cmap='gray')
ax3.set_title('3. Restauración por Media')
ax3.axis('off')

plt.tight_layout()
