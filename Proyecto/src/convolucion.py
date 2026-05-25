import numpy as np

def convolucion_manual(imagen, kernel):
    # Obtenemos el alto y el ancho de la imagen
    alto_img, ancho_img = imagen.shape
    alto_k, ancho_k = kernel.shape
    
    # Calculamos un borde para que pueda aplicar el filtro en las esquinas de la imagen
    pad_h = alto_k // 2
    pad_w = ancho_k // 2
   
    # Su tamaño será el de la imagen original + los bordes necesarios
    imagen_pad = np.zeros((alto_img + 2 * pad_h, ancho_img + 2 * pad_w))
    
    # Insertar la imagen original en el centro exacto de esta nueva matriz de ceros
    imagen_pad[pad_h : pad_h + alto_img, pad_w : pad_w + ancho_img] = imagen
    
    # Crear una matriz vacía para guardar el resultado 
    resultado = np.zeros((alto_img, ancho_img), dtype=float)
    
    # Metodo de convolucion
    for i in range(alto_img):
        for j in range(ancho_img):
            ventana = imagen_pad[i : i + alto_k, j : j + ancho_k]
            valor_pixel = np.sum(ventana * kernel)
            resultado[i, j] = valor_pixel

    # Si el valor es menor que 0 o mayor que 255 lo aproximamos al limite
    resultado = np.clip(resultado, 0, 255)
    return resultado