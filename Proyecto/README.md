# Procesador de Filtros de Imagen

Una aplicación de escritorio ligera construida con Python y Tkinter para aplicar filtros de procesamiento de imagen en el dominio espacial y frecuencial.

## Características y Filtros
El programa permite cargar imágenes desde el equipo, aplicar diferentes técnicas y guardar el resultado. Incluye:
**Filtro Sepia**: Modificación del espacio de color.
**Filtro Mediana**: Reducción de ruido .
**Efecto Semitono**: Transformación artística en bloques.
**Convolución (Detección de Bordes)**: Aplicación de kernels personalizados.
**Filtro Homomórfico**: Mejora del contraste y normalización de la iluminación mediante la Transformada de Fourier.
**Filtro Notch**: Eliminación de ruidos periódicos en el dominio de la frecuencia.

## Instalación y Uso
1. Clona este repositorio.
2. Instala las dependencias necesarias:
   pip install -r requirements.txt
3. Ejecuta el proyecto dentro de la carpeta src:
    python3 app.py