import numpy as np
import skimage

def filtro_semitono(imagen, tamano_bloque=8):
    # Pasamos la imagen a flotante y si es en color pasamos a escala de grises
    img = skimage.img_as_float(imagen)
    if len(img.shape) == 3:
        img = skimage.color.rgb2gray(img)
    
    rows, cols = img.shape

    # Creamos una matriz en blanco del mismo tamaño que la imagen
    lienzo = np.ones((rows, cols))

    # Creamos los ejes para hacer las operaciones de los bloques
    y, x = np.ogrid[0:tamano_bloque, 0:tamano_bloque]
    # Calculamos el centro del círculo a dibujar
    centro = (tamano_bloque - 1) / 2
    # Y las distancias de cada pixel que conforma el bloque respecto al centro
    distancia_al_centro = (x - centro)**2 + (y - centro)**2
    # Calculamos el radio máximo que puede tener el bloque
    radio_maximo = tamano_bloque / 2

    for r in range(0, rows, tamano_bloque):
        for c in range(0, cols, tamano_bloque):
            # Extraemos el bloque
            bloque = img[r : r + tamano_bloque, c : c + tamano_bloque]
            h, w = bloque.shape

            # Comprobamos que el tamaño sea el correcto
            if h == tamano_bloque and w == tamano_bloque:
                # Se calcula la media del valor del bloque
                brillo = np.mean(bloque)
                # Si la zona es muy blanca, el brillo será cercano a 1 y el circulo será pequeño o no habrá círculo
                radio_circulo = radio_maximo * (1.0 - brillo)
                # Se crea la máscara para saber los pixeles del bloque donde afectará el círculo
                mascara_circulo = distancia_al_centro <= radio_circulo**2
                # Se pinta en el lienzo creado el círculo usando la máscara
                lienzo[r : r + tamano_bloque, c : c + tamano_bloque][mascara_circulo] = 0.0
                
    return lienzo