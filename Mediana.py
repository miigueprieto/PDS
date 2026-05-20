
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

# Configuración de matplotlib
%matplotlib inline
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



img_org = io.imread("lena.bmp", as_gray=True)

# Añadimos ruido "Sal y Pimienta" para simular la degradación
img_ruidosa = util.random_noise(img_org, mode='s&p', amount=0.05)

resultado = filtro_mediana(img_ruidosa, K=3)

# Visualización gráfica
fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

ax1.imshow(img_org, cmap='gray')
ax1.set_title('1. Imagen Original')
ax1.axis('off')

ax2.imshow(img_ruidosa, cmap='gray')
ax2.set_title('2. Degradación: Ruido S&P')
ax2.axis('off')

ax3.imshow(resultado, cmap='gray')
ax3.set_title('3. Restauración: Filtro Mediana')
ax3.axis('off')

plt.tight_layout()
plt.show()

 