PERMISOS = {
    'administrador': ['crear', 'leer', 'actualizar', 'eliminar'],
    'gerente': ['leer', 'actualizar'],
    'empleado': ['leer']
}


def verificar_permiso(rol_nombre, accion):
    return accion in PERMISOS.get(rol_nombre, [])

def encontrar_Rol(self, Rol):
    """busca usuario por nombre"""
    return self.db_connector.session.query("""usuario""").filter_by(Rol=Rol).first()

#crear_admin
def crear_admin(usuario_creador):
    verificar_permiso('administrador','crear')
# leer_admin
def leer_admin(usuario_creador):
    verificar_permiso('administrador','leer')
# actualizar_admin
def actualizar_admin(usuario_creador):
    verificar_permiso('administrador','actualizar')

def eliminar_admin(usuario_creador):
    verificar_permiso('administrador','eliminar')

# fin admin

def leer_gerente(usuario_creador):
    verificar_permiso('gerente','leer')
# actualizar_gerente
def actualizar_gerente(usuario_creador):
    verificar_permiso('gerente','actualizar')
#fin gerente    

def leer_empleado(usuario_creador):
    verificar_permiso('empleado','leer')
# fin empleado

# 
# # usuario_creador = control_usuarios.encontrar_usuario(username)

