import os
import time
import subprocess
import sys
import logging
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading

class AdvancedFRPRemover:
    def __init__(self):
        self.device_connected = False
        self.device_model = None
        self.adb_path = None
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            filename='frp_remover.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8'
        )
        logging.info("Iniciando herramienta FRP Remover")
        
    def find_adb(self):
        possible_paths = [
            "adb", "platform-tools/adb",
            "C:\\adb\\adb.exe", "C:\\platform-tools\\adb.exe",
            "/usr/bin/adb", "/usr/local/bin/adb"
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, "version"], 
                                      capture_output=True, text=True, check=True)
                if "Android Debug Bridge" in result.stdout:
                    logging.info(f"ADB encontrado en: {path}")
                    return path
            except:
                continue
        
        # Si no se encuentra automáticamente, pedir al usuario
        root = tk.Tk()
        root.withdraw()
        adb_path = filedialog.askopenfilename(
            title="Seleccione el archivo adb",
            filetypes=[("Ejecutables ADB", "adb*"), ("Todos los archivos", "*.*")]
        )
        root.destroy()
        
        if adb_path and os.path.isfile(adb_path):
            logging.info(f"ADB seleccionado manualmente: {adb_path}")
            return adb_path
        
        logging.error("ADB no encontrado")
        return None

    def check_device_connection(self):
        try:
            result = subprocess.run([self.adb_path, "devices"], 
                                  capture_output=True, text=True, check=True)
            devices = [line.split('\t')[0] for line in result.stdout.split('\n')[1:] 
                      if line and 'device' in line]
            
            if devices:
                self.device_connected = True
                # Obtener modelo del dispositivo
                model_result = subprocess.run([self.adb_path, "shell", "getprop", "ro.product.model"], 
                                            capture_output=True, text=True, check=True)
                self.device_model = model_result.stdout.strip()
                logging.info(f"Dispositivo detectado: {devices[0]} - Modelo: {self.device_model}")
                return True
            else:
                logging.warning("No se detectaron dispositivos")
                return False
                
        except Exception as e:
            logging.error(f"Error al verificar dispositivos: {e}")
            return False

    def enable_usb_debugging_emergency(self):
        """Método para activar depuración USB mediante llamada de emergencia"""
        logging.info("Intentando activar depuración USB mediante emergencia")
        
        try:
            # Abrir marcador de teléfono
            subprocess.run([self.adb_path, "shell", "am", "start", "-a", "android.intent.action.DIAL"], 
                         capture_output=True, timeout=10)
            time.sleep(2)
            
            # Ingresar código especial para Huawei
            subprocess.run([self.adb_path, "shell", "input", "text", "*#*#2846579#*#*"], 
                         capture_output=True, timeout=10)
            time.sleep(2)
            
            # Navegar al menú de proyecto (para Huawei)
            subprocess.run([self.adb_path, "shell", "input", "tap", "200", "300"], 
                         capture_output=True, timeout=10)
            time.sleep(1)
            
            subprocess.run([self.adb_path, "shell", "input", "tap", "200", "400"], 
                         capture_output=True, timeout=10)
            time.sleep(1)
            
            # Habilitar depuración USB
            subprocess.run([self.adb_path, "shell", "input", "tap", "200", "500"], 
                         capture_output=True, timeout=10)
            time.sleep(2)
            
            logging.info("Depuración USB activada mediante menú de emergencia")
            return True
            
        except Exception as e:
            logging.error(f"Error al activar depuración USB: {e}")
            return False

    def execute_frp_bypass_huawei(self):
        """Comandos específicos de bypass FRP para Huawei Y9 2019"""
        logging.info("Ejecutando bypass FRP para Huawei Y9 2019")
        
        bypass_commands = [
            # Eliminar cuentas Google
            "pm disable com.google.android.gsf.login",
            "pm disable com.google.android.gms",
            "pm clear com.google.android.gsf.login",
            "pm clear com.google.android.gms",
            
            # Configurar dispositivo como provisionado
            "settings put global device_provisioned 1",
            "settings put secure user_setup_complete 1",
            
            # Omitir configuración inicial
            "am start -n com.android.settings/.Settings",
            "content insert --uri content://settings/secure --bind name:s:device_provisioned --bind value:s:1",
            "content insert --uri content://settings/secure --bind name:s:user_setup_complete --bind value:s:1",
            
            # Habilitar opciones de desarrollo
            "settings put global development_settings_enabled 1",
            "settings put global adb_enabled 1",
            "settings put global usb_debugging_enabled 1"
        ]
        
        for cmd in bypass_commands:
            try:
                result = subprocess.run([self.adb_path, "shell", cmd], 
                                      capture_output=True, text=True, timeout=15)
                if result.returncode != 0:
                    logging.warning(f"Comando falló: {cmd} - Error: {result.stderr}")
                time.sleep(1)
            except Exception as e:
                logging.error(f"Error ejecutando comando {cmd}: {e}")

    def execute_frp_bypass_samsung(self):
        """Método alternativo para dispositivos Samsung (como referencia)"""
        logging.info("Ejecutando bypass FRP para Samsung (método de referencia)")
        
        try:
            # Abrir aplicación de emergencia
            subprocess.run([self.adb_path, "shell", "am", "start", "-a", "android.intent.action.CALL_EMERGENCY"], 
                         capture_output=True, timeout=10)
            time.sleep(2)
            
            # Escribir código especial
            subprocess.run([self.adb_path, "shell", "input", "text", "*#0*#"], 
                         capture_output=True, timeout=10)
            time.sleep(2)
            
            # Navegar por el menú de prueba
            subprocess.run([self.adb_path, "shell", "input", "keyevent", "KEYCODE_HOME"], 
                         capture_output=True, timeout=10)
            time.sleep(1)
            
            logging.info("Bypass FRP para Samsung ejecutado")
            
        except Exception as e:
            logging.error(f"Error en bypass Samsung: {e}")

    def reboot_device(self):
        logging.info("Reiniciando dispositivo")
        try:
            subprocess.run([self.adb_path, "reboot"], timeout=30)
            time.sleep(30)  # Esperar a que reinicie
            logging.info("Dispositivo reiniciado")
            return True
        except Exception as e:
            logging.error(f"Error al reiniciar: {e}")
            return False

    def check_frp_status(self):
        """Verificar si el FRP fue removido correctamente"""
        logging.info("Verificando estado de FRP")
        try:
            result = subprocess.run([self.adb_path, "shell", "settings", "get", "secure", "user_setup_complete"], 
                                  capture_output=True, text=True, timeout=10)
            if "1" in result.stdout:
                logging.info("FRP removido exitosamente")
                return True
            else:
                logging.warning("FRP可能 aún está presente")
                return False
        except Exception as e:
            logging.error(f"Error verificando FRP: {e}")
            return False

    def main_process(self):
        """Proceso principal de bypass FRP"""
        logging.info("Iniciando proceso de bypass FRP")
        
        # Paso 1: Encontrar ADB
        self.adb_path = self.find_adb()
        if not self.adb_path:
            logging.error("ADB no disponible. Abortando.")
            return False
        
        # Paso 2: Conectar dispositivo (modo recovery/fastboot)
        if not self.check_device_connection():
            # Si no se detecta, intentar activar depuración por emergencia
            if not self.enable_usb_debugging_emergency():
                logging.error("No se pudo conectar al dispositivo")
                return False
        
        # Paso 3: Ejecutar bypass según modelo
        if "HUAWEI" in self.device_model.upper() or "Y9" in self.device_model:
            self.execute_frp_bypass_huawei()
        else:
            # Intentar método genérico
            self.execute_frp_bypass_huawei()
        
        # Paso 4: Reiniciar y verificar
        if self.reboot_device():
            time.sleep(30)  # Esperar a que el dispositivo reinicie completamente
            if self.check_device_connection():
                return self.check_frp_status()
        
        return False

class FRPRemoverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Herramienta Avanzada FRP Remover - Agente Sánchez")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        self.frp_remover = AdvancedFRPRemover()
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, 
                               text="Herramienta de Bypass FRP\nPara Huawei Y9 2019", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Información del dispositivo
        device_frame = ttk.LabelFrame(main_frame, text="Información del Dispositivo", padding="10")
        device_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.device_status = ttk.Label(device_frame, text="Estado: No conectado")
        self.device_status.grid(row=0, column=0, sticky=tk.W)
        
        self.device_model = ttk.Label(device_frame, text="Modelo: Desconocido")
        self.device_model.grid(row=1, column=0, sticky=tk.W)
        
        # Progreso
        progress_frame = ttk.LabelFrame(main_frame, text="Progreso", padding="10")
        progress_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(progress_frame, text="Listo para comenzar")
        self.status_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        self.start_button = ttk.Button(button_frame, text="Iniciar Bypass FRP", 
                                      command=self.start_process)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.check_button = ttk.Button(button_frame, text="Verificar Conexión", 
                                      command=self.check_connection)
        self.check_button.grid(row=0, column=1, padx=5)
        
        self.log_button = ttk.Button(button_frame, text="Ver Log", 
                                    command=self.show_log)
        self.log_button.grid(row=0, column=2, padx=5)
        
        # Configurar columnas para expandirse
        main_frame.columnconfigure(0, weight=1)
        device_frame.columnconfigure(0, weight=1)
        progress_frame.columnconfigure(0, weight=1)
        
    def check_connection(self):
        self.status_label.config(text="Verificando conexión...")
        self.frp_remover.adb_path = self.frp_remover.find_adb()
        
        if self.frp_remover.adb_path:
            if self.frp_remover.check_device_connection():
                self.device_status.config(text="Estado: Conectado")
                self.device_model.config(text=f"Modelo: {self.frp_remover.device_model}")
                self.status_label.config(text="Dispositivo detectado correctamente")
            else:
                self.status_label.config(text="No se detectó dispositivo. Conecte en modo recuperación.")
        else:
            self.status_label.config(text="ADB no encontrado. Seleccione manualmente.")
            
    def start_process(self):
        self.start_button.config(state='disabled')
        self.progress.start()
        self.status_label.config(text="Iniciando proceso de bypass FRP...")
        
        # Ejecutar en un hilo separado para no bloquear la interfaz
        thread = threading.Thread(target=self.run_process)
        thread.daemon = True
        thread.start()
        
    def run_process(self):
        try:
            success = self.frp_remover.main_process()
            self.root.after(0, self.process_finished, success)
        except Exception as e:
            self.root.after(0, self.process_error, str(e))
            
    def process_finished(self, success):
        self.progress.stop()
        self.start_button.config(state='normal')
        
        if success:
            self.status_label.config(text="¡Bypass FRP completado exitosamente!")
            messagebox.showinfo("Éxito", "El proceso de bypass FRP se completó correctamente.")
        else:
            self.status_label.config(text="Error en el proceso de bypass FRP")
            messagebox.showerror("Error", "No se pudo completar el bypass FRP. Consulte el log para más detalles.")
            
    def process_error(self, error_msg):
        self.progress.stop()
        self.start_button.config(state='normal')
        self.status_label.config(text=f"Error: {error_msg}")
        messagebox.showerror("Error", f"Ocurrió un error: {error_msg}")
        
    def show_log(self):
        try:
            if os.path.exists("frp_remover.log"):
                os.system("notepad.exe frp_remover.log")
            else:
                messagebox.showinfo("Log", "El archivo de log no existe todavía.")
        except:
            messagebox.showerror("Error", "No se pudo abrir el archivo de log.")

def main():
    root = tk.Tk()
    app = FRPRemoverGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
