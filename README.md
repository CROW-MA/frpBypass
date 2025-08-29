Una herramienta especializada para bypass de Factory Reset Protection (FRP) en dispositivos Android, con soporte especial para Huawei Y9 2019 y otros modelos.
⚠️ Advertencia Legal

IMPORTANTE: Esta herramienta está diseñada únicamente para:

    Recuperación de dispositivos de propiedad legítima

    Propósitos educativos e investigación autorizada

    Uso por técnicos profesionales con autorización

El uso de esta herramienta para acceder a dispositivos sin autorización explícita es ilegal en muchas jurisdicciones.
✨ Características

    Bypass FRP para Huawei Y9 2019: Solución especializada para este modelo

    Interfaz gráfica intuitiva: Fácil de usar con indicadores visuales

    Detección automática de ADB: Busca automáticamente las herramientas necesarias

    Múltiples métodos de bypass: Incluye técnicas para diferentes marcas

    Sistema de logging: Registro detallado de todas las operaciones

    Verificación de resultados: Confirma el éxito del proceso de bypass

📋 Requisitos del Sistema
Sistema Operativo

    Windows 7/8/10/11 (recomendado)

    Linux (con configuraciones adicionales)

    macOS (con configuraciones adicionales)

Pre-requisitos

    Python 3.8 o superior

    Drivers ADB instalados para su dispositivo

    Dispositivo Android con depuración USB habilitada (o capacidad para habilitarla)

Instalación de dependencias
bash

pip install tkinter

🛠 Instalación

    Descargar la herramienta:

bash

git clone https://github.com/CROWN-MA/frp-remover-tool.git
cd frp-remover-tool

    Conectar el dispositivo:

        Active la depuración USB en su dispositivo Android

        Conéctelo mediante un cable USB en buen estado

        Asegúrese de que el dispositivo esté en modo recuperación si es necesario

    Ejecutar la herramienta:

bash

python frp_remover.py

🚀 Uso
Interfaz Gráfica

    Verificar conexión: Haga clic en "Verificar Conexión" para confirmar que el dispositivo está detectado

    Iniciar bypass: Haga clic en "Iniciar Bypass FRP" para comenzar el proceso

    Seguir instrucciones: Espere a que el proceso termine (puede tomar varios minutos)

    Verificar resultados: La herramienta indicará si el proceso fue exitoso

Proceso Automático

La herramienta ejecuta automáticamente estos pasos:

    Detección de ADB y dispositivos conectados

    Activación de depuración USB (si es necesario)

    Ejecución de comandos específicos de bypass FRP

    Reinicio del dispositivo

    Verificación del estado de FRP

Modelos Compatibles

    Huawei Y9 2019 (compatible total)

    Otros modelos Huawei (compatibilidad parcial)

    Dispositivos Samsung (método de referencia)

    Otros dispositivos Android (métodos genéricos)

🔧 Comandos Especiales

La herramienta utiliza estos comandos ADB para el bypass:
bash

# Comandos específicos para Huawei
pm disable com.google.android.gsf.login
pm disable com.google.android.gms
settings put global device_provisioned 1
settings put secure user_setup_complete 1

# Códigos de emergencia
*#*#2846579#*#*  # Menú de proyecto Huawei
*#0*#             # Menú de prueba Samsung

📊 Estructura del Proyecto
text

frp-remover-tool/
├── frp_remover.py      # Script principal
├── frp_remover.log     # Archivo de registro (generado automáticamente)
└── README.md           # Este archivo

⚠️ Solución de Problemas
Error: "ADB no encontrado"

    Seleccione manualmente la ubicación de ADB cuando se le solicite

    Asegúrese de tener instalados los drivers ADB para su dispositivo

    Descargue platform-tools desde Google y extraígalos en una carpeta accesible

Error: "No se detectaron dispositivos"

    Verifique que la depuración USB esté habilitada en el dispositivo

    Pruebe con otro cable USB

    Reinicie el dispositivo y la herramienta

Error: "El proceso de bypass falló"

    Consulte el archivo frp_remover.log para detalles

    Verifique que el modelo sea compatible

    Intente reiniciar el dispositivo manualmente y vuelva a intentar

🔄 Flujo de Trabajo Recomendado

    Conecte el dispositivo en modo recuperación (si es posible)

    Ejecute la herramienta y verifique la conexión

    Inicie el proceso de bypass

    Espere a que el dispositivo se reinicie automáticamente

    Verifique que el bypass fue exitoso

    Si falla, consulte el log y repita el proceso

📝 Registro de Cambios
v1.0

    Versión inicial con soporte para Huawei Y9 2019

    Interfaz gráfica básica

    Sistema de logging integrado

v1.1

    Mejora en la detección de dispositivos

    Comandos adicionales para otros modelos

    Optimización del proceso de bypass

🤝 Soporte Técnico

Si encuentra problemas:

    Revise el archivo frp_remover.log para detalles del error

    Asegúrese de estar usando la versión más reciente

    Verifique la compatibilidad de su modelo de dispositivo

📜 Licencia

Este proyecto es para fines educativos y de investigación. El uso de esta herramienta para dispositivos que no le pertenecen puede ser ilegal.
🚨 Limitaciones Conocidas

    No funciona en todos los modelos de dispositivos

    Puede ser detectado y bloqueado por actualizaciones de seguridad

    Algunos métodos pueden requerir intervención manual

    Algunos fabricantes han parcheado estas vulnerabilidades

Nota: Esta herramienta se proporciona "tal cual" sin garantías. El usuario es responsable de su uso conforme a las leyes locales.
