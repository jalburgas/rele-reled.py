import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import threading
import time

class RelayController:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Relé - Arduino Pin 13")
        self.root.geometry("400x200")
        self.root.resizable(False, False)
        
        self.serial_port = None
        self.is_connected = False
        self.stop_reading = False
        
        self.setup_ui()
        self.update_ports_list()
        
    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="Control de Relé con Arduino", 
                                font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Frame de conexión
        connection_frame = ttk.LabelFrame(main_frame, text="Conexión Serial", padding="10")
        connection_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(connection_frame, text="Puerto COM:", font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, padx=5)
        self.port_combo = ttk.Combobox(connection_frame, width=15, font=('Arial', 10))
        self.port_combo.grid(row=0, column=1, padx=5)
        
        self.connect_btn = ttk.Button(connection_frame, text="Conectar", 
                                      command=self.toggle_connection, width=12)
        self.connect_btn.grid(row=0, column=2, padx=5)
        
        refresh_btn = ttk.Button(connection_frame, text="↻", width=3,
                                 command=self.update_ports_list)
        refresh_btn.grid(row=0, column=3, padx=5)
        
        self.status_label = ttk.Label(connection_frame, text="Estado: Desconectado",
                                      font=('Arial', 9))
        self.status_label.grid(row=1, column=0, columnspan=2, pady=5, sticky=tk.W)
        
        self.led_indicator = tk.Canvas(connection_frame, width=20, height=20)
        self.led_indicator.grid(row=1, column=2, columnspan=2, pady=5)
        self.update_led_indicator("red")
        
    def update_ports_list(self):
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports]
        
        if not port_list:
            port_list = ["No hay puertos disponibles"]
            self.port_combo.set("")
        else:
            self.port_combo.set(port_list[0] if port_list else "")
        
        self.port_combo['values'] = port_list
        
    def update_led_indicator(self, color):
        self.led_indicator.delete("all")
        self.led_indicator.create_oval(2, 2, 18, 18, fill=color, outline="")
        
    def toggle_connection(self):
        if not self.is_connected:
            self.connect_arduino()
        else:
            self.disconnect_arduino()
            
    def connect_arduino(self):
        port = self.port_combo.get()
        
        if not port or port == "No hay puertos disponibles":
            messagebox.showerror("Error", "No hay puertos disponibles")
            return
            
        try:
            self.serial_port = serial.Serial(port, 9600, timeout=1)
            time.sleep(2)
            
            self.is_connected = True
            self.stop_reading = False
            
            self.connect_btn.config(text="Desconectar")
            
            self.status_label.config(text="Estado: Conectado")
            self.update_led_indicator("green")
            self.port_combo.config(state=tk.DISABLED)
            
            self.serial_port.reset_input_buffer()
            
            self.read_thread = threading.Thread(target=self.read_serial, daemon=True)
            self.read_thread.start()
            
            # Eliminado el messagebox de éxito
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar: {str(e)}")
            
    def disconnect_arduino(self):
        self.stop_reading = True
        self.is_connected = False
        
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        
        self.connect_btn.config(text="Conectar")
        
        self.status_label.config(text="Estado: Desconectado")
        self.update_led_indicator("red")
        self.port_combo.config(state=tk.NORMAL)
        
    def read_serial(self):
        while self.is_connected and not self.stop_reading and self.serial_port and self.serial_port.is_open:
            try:
                if self.serial_port.in_waiting > 0:
                    line = self.serial_port.readline()
                    # Solo leer pero no mostrar nada
                time.sleep(0.05)
                
            except serial.SerialException as e:
                break
            except Exception as e:
                time.sleep(0.1)
            
    def on_closing(self):
        self.stop_reading = True
        self.is_connected = False
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RelayController(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
