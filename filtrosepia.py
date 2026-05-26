import numpy as np
import matplotlib.pyplot as plt
import skimage

def filtro_sepia(imagen):

    # Pasamos a coma flotante para que el rango de valores no cuele de 255 al hacer las operaciones
    img_float = skimage.img_as_float(imagen)

    # Matriz que aplica a cada componente de color el filtro sepia estándar
    matriz_sepia = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])

    # Multiplicamos y sumamos cada componente de color para obtener el nuevo RGB
    img_sepia = np.dot(img_float[:, :, :3], matriz_sepia.T)

    # Comprobamos que los valores no se hayan salido del rango de 0 y 1
    img_sepia = np.clip(img_sepia, 0, 1)
    
    return img_sepia

imagen_original = skimage.data.astronaut()

imagen_sepia = filtro_sepia(imagen_original)

fig, axes = plt.subplots(1, 2)

axes[0].imshow(imagen_original)
axes[0].set_title("Imagen Original")
axes[0].axis("off")

axes[1].imshow(imagen_sepia)
axes[1].set_title("Filtro Sepia")
axes[1].axis("off")

plt.show()