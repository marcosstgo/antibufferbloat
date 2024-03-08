![anti-bufferbloat-2-1](https://github.com/marcosstgo/antibufferbloat/assets/50328367/c1e8705f-ced3-4b04-b5ce-27074e0bc39a)


1. Interfaz gráfica de usuario (GUI):
   - Diseñada con PySide6 para crear una interfaz amigable.
   - Presenta botones para activar/desactivar Auto-Tuning y RSS, ejecutar pruebas de velocidad, abrir sitios web de pruebas, mostrar información y verificar actualizaciones.
   - Muestra el estado actual de Auto-Tuning y RSS, el ping en tiempo real y el progreso de las pruebas de velocidad.

2. Funciones de red:
   - Utiliza el comando `netsh` de Windows para modificar la configuración de red, como Auto-Tuning y RSS.
   - Ejecuta pruebas de velocidad utilizando la biblioteca Speedtest.
   - Actualiza periódicamente el ping a través de un hilo (thread) separado.
   - Comprueba actualizaciones a través de una API online.

3. Funcionalidades esenciales:
   - **Activar/Desactivar Auto-Tuning:** Permite ajustar la gestión del buffer de recepción TCP para optimizar el rendimiento de la red.
   - **Activar/Desactivar RSS:** Habilita la distribución del procesamiento de paquetes de red en múltiples procesadores, mejorando la eficiencia.
   - **Pruebas de velocidad:** Ofrece opciones para realizar pruebas de velocidad a través de speedtest.net, speedtest-cli, Waveform.com y Fast.com.
   - **Información sobre Auto-Tuning y RSS:** Ofrece una ventana de diálogo con información detallada sobre estas funciones.
   - **Actualizaciones:** Verifica automáticamente la disponibilidad de actualizaciones y permite descargarlas.

Puntos a destacar:

- **Diseño visual:** La aplicación presenta un diseño oscuro con botones azules y texto blanco, proporcionando una estética visual agradable.
- **Funcionalidad para RSS:** Incluye la capacidad de activar o desactivar RSS, una función que puede mejorar el rendimiento de la red en sistemas con múltiples procesadores.
- **Actualizaciones automáticas:** Incorpora un mecanismo para verificar y descargar actualizaciones automáticamente, asegurando que la aplicación se mantenga al día con las mejoras.

Recuerda que:

- La modificación de la configuración de red a través de esta aplicación podría impactar en el rendimiento de tu conexión. Se recomienda utilizar la aplicación con precaución y entender los efectos de los cambios realizados.
- Si experimentas problemas de red, es recomendable consultar con un experto en redes o tu proveedor de servicios de internet.

