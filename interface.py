import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import redactor
import os

# Função para selecionar arquivo
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        process_file(file_path)

# Função para processar arquivo após drop
def drop(event):
    file_path = event.data.strip("{}")
    if file_path:
        process_file(file_path)

# Função para processar arquivo
def process_file(file_path):
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if output_path:
        try:
            names_to_redact = get_names_to_redact()
            redactor.redact_info_in_pdf(file_path, output_path, names_to_redact=names_to_redact)
            messagebox.showinfo("Sucesso", "As informações foram devidamente anonimizadas.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Função auxiliar para coletar nomes a serem redigidos
def get_names_to_redact():
    names = names_entry.get("1.0", tk.END).strip()
    return [name.strip() for name in names.split(",") if name.strip()]

# Função para criar a interface gráfica
def create_gui():
    root = TkinterDnD.Tk()
    root.title("Anonimizador de PDF - Gabinete Des Saboia")
    root.geometry("600x400")
    root.configure(bg="#f3f3f3")
    root.resizable(False, False)

    # Definir o ícone da janela
    icon_path = os.path.join(os.path.dirname(__file__), "images", "icon.ico")
    if not os.path.exists(icon_path):
        messagebox.showerror("Erro", f"Ícone não encontrado: {icon_path}")
        return
    root.iconbitmap(icon_path)

    frame = tk.Frame(root, bg="#f3f3f3", padx=20, pady=20)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Adicionar a logo
    logo_path = os.path.join(os.path.dirname(__file__), "images", "logo.png")
    if not os.path.exists(logo_path):
        messagebox.showerror("Erro", f"Logo não encontrada: {logo_path}")
        return
    try:
        logo_img = Image.open(logo_path)
        logo = ImageTk.PhotoImage(logo_img)
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao carregar a logo: {e}")
        return

    logo_label = tk.Label(frame, image=logo, bg="#f3f3f3")
    logo_label.image = logo
    logo_label.pack(pady=10)

    label = tk.Label(frame, text="Selecione ou arraste um arquivo PDF para anonimizar:", font=("Helvetica", 16), fg="#333333", bg="#f3f3f3")
    label.pack(pady=10)

    select_button = tk.Button(frame, text="Selecionar PDF", command=select_file, font=("Helvetica", 14), bg="#0056a6", fg="white", relief=tk.FLAT)
    select_button.pack(pady=10, ipadx=10, ipady=5)

    # Adicionar um campo de entrada de texto para nomes a serem redigidos
    names_label = tk.Label(frame, text="Nomes adicionais para anonimizar (separados por vírgulas):", font=("Helvetica", 12), fg="#333333", bg="#f3f3f3")
    names_label.pack(pady=10)
    global names_entry
    names_entry = tk.Text(frame, height=4, width=50, font=("Helvetica", 12))
    names_entry.pack(pady=10)

    drop_label = tk.Label(frame, text="Arraste o arquivo PDF aqui", font=("Helvetica", 14), fg="#333333", bg="#d9d9d9", width=40, height=5, relief=tk.RIDGE)
    drop_label.pack(pady=10, fill=tk.BOTH, expand=True)
    drop_label.drop_target_register(DND_FILES)
    drop_label.dnd_bind('<<Drop>>', drop)

    exit_button = tk.Button(frame, text="Sair", command=root.quit, font=("Helvetica", 14), bg="#ff3333", fg="white", relief=tk.FLAT)
    exit_button.pack(pady=10, ipadx=20, ipady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
