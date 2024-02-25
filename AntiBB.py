import tkinter as tk
from tkinter import messagebox
import subprocess
import webbrowser
import threading
import re
import customtkinter as ctk

# Colores relacionados con gaming - Tema Azul
gaming_bg_color = "#0a0f0d"  # Azul muy oscuro/verde azulado para el fondo
gaming_button_color = "#007acc"  # Azul brillante para botones
gaming_text_color = "#d0e0f0"  # Azul claro para texto

def run_command(command, process_output=False):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if process_output:
            return process_output(result.stdout)
        else:
            messagebox.showinfo("Resultado", result.stdout)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error al ejecutar el comando: {e}")

def process_tcp_show_output(output):
    for line in output.splitlines():
        if "Receive Window Auto-Tuning Level" in line:
            return line
    return "Información no encontrada."

def activate_antibufferbloat():
    run_command("netsh int tcp set global autotuninglevel=disabled")

def deactivate_antibufferbloat():
    run_command("netsh int tcp set global autotuninglevel=normal")

def show_status():
    output = run_command("netsh interface tcp show global", process_output=process_tcp_show_output)
    messagebox.showinfo("Estado Actual", output)

def open_bufferbloat_test():
    webbrowser.open("https://www.waveform.com/tools/bufferbloat")

def open_speedtest():
    webbrowser.open("https://www.speedtest.net")

def open_fast():
    webbrowser.open("https://www.fast.com")

def start_ping():
    def ping():
        process = subprocess.Popen(['ping', 'google.com', '-t'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        while True:
            output = process.stdout.readline().decode('utf-8')
            ping_time = re.search(r'time=(\d+)', output)
            if ping_time:
                ping_label.config(text=f"Ping: {ping_time.group(1)}ms")
    
    threading.Thread(target=ping, daemon=True).start()

def change_color():
    rgb = (255, 0, 0)  # Color inicial rojo

    def animate():
        nonlocal rgb
        r, g, b = rgb
        if r == 255 and g < 255 and b == 0:
            g += 15
        elif g == 255 and r > 0 and b == 0:
            r -= 15
        elif g == 255 and b < 255 and r == 0:
            b += 15
        elif b == 255 and g > 0 and r == 0:
            g -= 15
        elif b == 255 and r < 255 and g == 0:
            r += 15
        elif r == 255 and b > 0 and g == 0:
            b -= 15
        rgb = (r, g, b)
        header_label.config(fg="#%02x%02x%02x" % rgb)
        root.after(100, animate)

    animate()

root = tk.Tk()
root.title("AntiBufferBloat")
root.configure(bg=gaming_bg_color)

# Establecer tamaño de la ventana
root.geometry("450x415")

# Header del título Anti BB 1.2 en RGB animado
header_label = tk.Label(root, text="Anti BB 1.2", font=("Helvetica", 24), bg=gaming_bg_color)
header_label.pack(pady=(10, 20))
change_color()

# Botones con tamaño aumentado, colores personalizados y espacios entre bordes
button_font = ("Helvetica", 12)

activate_button = ctk.CTkButton(root, text="Activar Anti-BufferBloat", command=activate_antibufferbloat, font=button_font)
deactivate_button = ctk.CTkButton(root, text="Desactivar Anti-BufferBloat", command=deactivate_antibufferbloat, font=button_font)
show_button = ctk.CTkButton(root, text="Mostrar Estado BufferBloat", command=show_status, font=button_font)
bufferbloat_button = ctk.CTkButton(root, text="BufferBloat Test", command=open_bufferbloat_test, font=button_font)
speedtest_button = ctk.CTkButton(root, text="Speedtest.net", command=open_speedtest, font=button_font)
fast_button = ctk.CTkButton(root, text="Fast.com", command=open_fast, font=button_font)
exit_button = ctk.CTkButton(root, text="Salir", command=root.destroy, font=button_font)

# Organizando los botones en la ventana
activate_button.pack(fill=tk.X, pady=(0, 10), padx=15)
deactivate_button.pack(fill=tk.X, pady=(0, 10), padx=15)
show_button.pack(fill=tk.X, pady=(0, 10), padx=15)
bufferbloat_button.pack(fill=tk.X, pady=(0, 10), padx=15)
speedtest_button.pack(fill=tk.X, pady=(0, 10), padx=15)
fast_button.pack(fill=tk.X, pady=(0, 10), padx=15)
exit_button.pack(fill=tk.X, pady=(0, 10), padx=15)

# Etiqueta para mostrar el ping en tiempo real
ping_label = tk.Label(root, text="", font=("Helvetica", 12), bg=gaming_bg_color, fg=gaming_text_color)
ping_label.pack(side=tk.BOTTOM, pady=(0, 10))

# Iniciar el ping al inicio
start_ping()

# Etiqueta para mostrar el copyright
copyright_label = tk.Label(root, text="Creado por Katat0nia", font=("Helvetica", 10), bg=gaming_bg_color, fg=gaming_text_color)
copyright_label.pack(side=tk.BOTTOM, pady=(0, 10))

root.mainloop()
