import numpy as np
import skimage

def filtro_homomorfico(imagen, frec_corte=30, a=0.5, b=1.5):
    # Leemos imagen, pasamos a YUV si tiene 3 canales, y normalizamos para optimizar
    if len(imagen.shape) == 3:
        img_yuv = skimage.color.rgb2yuv(imagen)
        # Nos quedamos solo con el canal Y de luminancia
        img = img_yuv[:, :, 0]
    else:
        img = np.copy(imagen)
    img = img/np.max(img)

    # Aplicamos logaritmo para poder operar los componentes de iluminación y reflectancia por separado
    img_log = np.log1p(img)

    # Hacemos la Transformada discreta de Fourier para calcular las frecuencias de la imagen
    dft = np.fft.fft2(img_log)
    # Reorganizamos las frecuencias para agrupar las frecuencias bajas en el centro y aplicar el filtro
    dft_shift = np.fft.fftshift(dft)

    # Creamos un sistema de coordenadas nuevo para calcular las distancias poniendo como centro el 0,0
    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2
    y, x = np.ogrid[-crow:rows-crow, -ccol:cols-ccol]
    dist2 = x**2 + y**2
    # Aplicamos la fórmula del filtro homomórfico
    filtro = (b - a) * (1 - np.exp(-dist2 / (2 * frec_corte**2))) + a

    # Revertimos la Transformada discreta de Fourier
    dft_filtrado = dft_shift * filtro
    img_back = np.fft.ifftshift(dft_filtrado)
    img_back = np.fft.ifft2(img_back)

    # Revertimos el logaritmo con la exponencial y nos quedamos con la imagen final modificada
    img_exp = np.expm1(np.real(img_back))

    # Si tenía 3 canales reinvertimos la conversión a YUV para tener el RGB
    if len(imagen.shape) == 3:
        img_yuv_final = img_yuv
        img_yuv_final[:, :, 0] = img_exp
        img_final = skimage.color.yuv2rgb(img_yuv_final)
    # Si era en escala de grises, no hay que hacer nada más
    else:
        img_final = img_exp

    return img_final