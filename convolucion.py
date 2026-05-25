import numpy as np
import matplotlib.pyplot as plt
import cv2

def convolucion_manual(imagen, kernel):
    
    #Obtenemos el alto y el ancho de la imagen
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
    # Recorremos cada píxel de la imagen original
    for i in range(alto_img):
        for j in range(ancho_img):
            #Obtenmos la matriz desde i a i+ alto_k lo mismo para las columnas en este caso son los valores vecinos al pixel i,j
            ventana = imagen_pad[i : i + alto_k, j : j + ancho_k]
            
            # Multiplicar la ventana por el kernel elemento a elemento y sumar todo
            valor_pixel = np.sum(ventana * kernel)
            
            # Guardar el cálculo en el píxel correspondiente 
            resultado[i, j] = valor_pixel

    #Si el valor es menor que 0 o mayor que 255 lo aproximamos al limite que toque por ejemplo si da 2555 se aproxima a 255 blanco
    resultado = np.clip(resultado, 0, 255)
    return resultado

def main():
    ruta_imagen = 'tigre.jpeg' 
    
    # cv2.IMREAD_GRAYSCALE carga la foto directamente en blanco y negro 
    imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
    
    # Comprobamos que exista
    if imagen is None:
        print(f"Error: No se pudo cargar la imagen '{ruta_imagen}'. Revisa el nombre y la carpeta.")
        return

    # Redimensionamos
    imagen = cv2.resize(imagen, (300, 200))
    # Definir el Kernel 
    kernel_bordes = np.array([
        [-1, -1, -1],
        [-1,  8, -1],
        [-1, -1, -1]
    ])
    
    #  Aplicar nuestra función 
    print("Calculando convolución:")
    resultado = convolucion_manual(imagen, kernel_bordes)  

    # Mostrar los resultados
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    
    axs[0].imshow(imagen, cmap='gray')
    axs[0].set_title('Imagen Original')
    axs[0].axis('off')
    
    axs[1].imshow(resultado, cmap='gray')
    axs[1].set_title('Convolución')
    axs[1].axis('off')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()