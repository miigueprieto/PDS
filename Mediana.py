
# Cálculo numérico y manejo de arrays
import numpy as np

# Visualización
import matplotlib.pyplot as plt

# Manejo básico de imágenes
import skimage
import skimage.io as io
from skimage import util

# Librería de señales para comparar
import scipy.signal as signal

plt.rcParams["figure.figsize"] = (16, 5)

def filtro_mediana(imagen, K=3):
    # Calculamos los píxeles extra necesarios para que la ventana del filtro quepa en los bordes
    margen = K // 2
    
    # Creamos una matriz extendida (padding) que simula vecinos en los bordes mediante reflexión (espejo).
    # Esto permite que no se salga de la matriz.
    img_borde = np.pad(imagen, margen, mode='reflect')
    
    img_salida = np.zeros_like(imagen)
    
    # Recorremos la imagen píxel a píxel
    filas, columnas = imagen.shape
    for i in range(filas):
        for j in range(columnas):
            # Recortamos la vecindad de tamaño KxK que rodea al píxel actual
            ventana = img_borde[i : i+K, j : j+K]
            
            # Asignamos la mediana al píxel central
            img_salida[i, j] = np.median(ventana)
            
    return img_salida



def calcular_mse(original, procesada):
    # El Error Cuadrático Medio es la media de las diferencias al cuadrado, cuanto más cerca de 0 mejor
    return np.mean((original - procesada) ** 2)

def calcular_psnr(original, procesada, max_pixel=1.0):
    mse = calcular_mse(original, procesada)
    if mse == 0:
        return float('inf') # Si no hay error, el PSNR es infinito
    
    # Fórmula del PSNR, cuantos menos dB más ruido en la imagen
    return 10 * np.log10((max_pixel ** 2) / mse)

img_org = io.imread("lena.bmp", as_gray=True)

# Añadimos ruido "Sal y Pimienta" para simular la degradación
img_ruidosa = util.random_noise(img_org, mode='s&p', amount=0.05)

resultado = filtro_mediana(img_ruidosa, K=3)

mse_ruido = calcular_mse(img_org, img_ruidosa)
psnr_ruido = calcular_psnr(img_org, img_ruidosa, max_pixel=1.0)

mse_filtro = calcular_mse(img_org, resultado)
psnr_filtro = calcular_psnr(img_org, resultado, max_pixel=1.0)

print(" FILTRO MEDIANA ")
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
ax3.set_title('3. Restauración Mediana')
ax3.axis('off')

plt.tight_layout()
plt.show()
 
