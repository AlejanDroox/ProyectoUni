import tkinter as tk
from tkinter import messagebox
from db.crud_usuarios import ControlUsuarios
from db_connector import DBConnector


class RegistroUsuarioApp:
    def __init__(self, root, control_usuarios):
        self.root = root
        self.root.title("Registro de Usuario")

        self.control_usuarios = control_usuarios

        self.label_nombre = tk.Label(root, text="Nombre de Usuario:")
        self.label_nombre.pack()
        self.entry_nombre = tk.Entry(root)
        self.entry_nombre.pack()

        self.label_contraseña = tk.Label(root, text="Contraseña:")
        self.label_contraseña.pack()
        self.entry_contraseña = tk.Entry(root, show="*")
        self.entry_contraseña.pack()

        self.btn_registrar = tk.Button(
            root, text="Registrar Usuario", command=self.registrar_usuario)
        self.btn_registrar.pack()

    def registrar_usuario(self):
        username = self.entry_nombre.get()
        password = self.entry_contraseña.get()

        if not username or not password:
            messagebox.showerror(
                "Error", "Por favor ingrese un nombre de usuario y una contraseña")
            return

        if len(password) < 6:
            messagebox.showerror(
                "Error", "La contraseña debe tener al menos 6 caracteres")
            return

        if self.control_usuarios.create_user(username, password):
            messagebox.showinfo("Registro Exitoso",
                                "Usuario registrado exitosamente")
        else:
            messagebox.showerror(
                "Error", "El nombre de usuario ya está en uso")

        self.entry_nombre.delete(0, tk.END)
        self.entry_contraseña.delete(0, tk.END)


if __name__ == "__main__":
    # Configuración de la base de datos
    config = 'mysql://root:root123@127.0.0.1:3306/otravez'
    db_connector = DBConnector(config)

    # Crear instancia de ControlUsuarios
    control_usuarios = ControlUsuarios(db_connector)

    # Crear ventana de Tkinter
    root = tk.Tk()
    app = RegistroUsuarioApp(root, control_usuarios)
    root.mainloop()
