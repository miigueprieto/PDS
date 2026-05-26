import numpy as np
from scipy.signal import convolve2d

def filtro_media(imagen, K=3):
    
    # Definimos el kernel 
    kernel_media = np.ones((K, K)) / (K ** 2)
    
    resultado = convolve2d(imagen, kernel_media, mode='same', boundary='symm')
    
    return resultado