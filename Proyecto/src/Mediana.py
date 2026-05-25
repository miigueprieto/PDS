import numpy as np

def filtro_mediana(imagen, K=3):
    # Calculamos los píxeles extra necesarios para que la ventana del filtro quepa en los bordes
    margen = K // 2
    
    # Creamos una matriz extendida (padding) que simula vecinos en los bordes mediante reflexión (espejo).
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