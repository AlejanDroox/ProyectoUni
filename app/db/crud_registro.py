from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, DateTime, Enum, Text, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime
from utils.globals import CONFIG



# Crea el motor de SQLAlchemy
engine = create_engine(CONFIG)

# Crea una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea una instancia de Base declarativa
Base = declarative_base()

# Definición del modelo de Producto
class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, index=True)
    nom_producto = Column(String(255), unique=True, index=True)
    Existencia = Column(Integer, nullable=False)
    Desc_Producto = Column(Text)
    Valor_Producto_C = Column(Numeric(10, 2), nullable=False)
    Valor_Producto_V = Column(Numeric(10, 2), nullable=False)
    Image = Column(Text)
    ventas_relacion = relationship("VentaProducto", back_populates="producto")

# Definición del modelo de Usuario
class User(Base):
    __tablename__ = "users"

    idUsers = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)

    ventas_relacion = relationship("VentaProducto", back_populates="user")

# Definición del modelo de Venta
class Venta(Base):
    __tablename__ = "ventas"

    idVentas = Column(Integer, primary_key=True, index=True)
    Fecha_Venta = Column(DateTime, default=func.now())
    Monto_venta = Column(Numeric(10, 2), nullable=False)
    Desc_compra = Column(Text)
    cantidad = Column(Integer, nullable=False)
    Metodo = Column(Enum('BS', 'COP', 'USD'), nullable=False)

    productos_relacion = relationship("VentaProducto", back_populates="venta")

# Definición del modelo de VentaProducto
class VentaProducto(Base):
    __tablename__ = "ventas_productos"

    id = Column(Integer, primary_key=True, index=True)
    ventas_idventas1 = Column(Integer, ForeignKey('ventas.idVentas'))
    productos_idproductos1 = Column(Integer, ForeignKey('productos.id_producto'))
    Users_idUsers = Column(Integer, ForeignKey('users.idUsers'))
    cantidad = Column(Integer, nullable=False)
    grupo = Column(Integer, nullable=False)  # Nueva columna para agrupar las ventas

    venta = relationship("Venta", back_populates="productos_relacion")
    producto = relationship("Producto", back_populates="ventas_relacion")
    user = relationship("User", back_populates="ventas_relacion")


class DatosCliente(Base):
    __tablename__ = "datos_clientes"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre_cliente = Column(String(255), nullable=False)
    numero_identificacion = Column(String(50), nullable=False)

    ventas_relacion = relationship("VentaProducto", back_populates="cliente")

# Agregar relación de cliente en VentaProducto
VentaProducto.cliente_id = Column(Integer, ForeignKey('datos_clientes.id_cliente'))
VentaProducto.cliente = relationship("DatosCliente", back_populates="ventas_relacion")


# Crea las tablas en la base de datos si no existen
Base.metadata.create_all(engine)

# Clase para manejar la conexión a la base de datos
class DbConnector:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        return self.SessionLocal()


# Clase para los Clientes

# Clase CRUDVentas
class CRUDVentas:
    def __init__(self, db_session):
        self.db_session = db_session

    def encontrar_producto(self, nombre):
        """Busca producto por nombre"""
        return self.db_session.query(Producto).filter_by(nom_producto=nombre).first()

    def encontrar_usuario(self, username):
        """Busca usuario por nombre"""
        return self.db_session.query(User).filter_by(username=username).first()

    def encontrar_cliente(self, nombre_cliente, numero_identificacion):
        """Busca cliente por nombre e identificación"""
        return self.db_session.query(DatosCliente).filter_by(nombre_cliente=nombre_cliente, numero_identificacion=numero_identificacion).first()

    def crear_cliente(self, nombre_cliente, numero_identificacion):
        """Crea un nuevo cliente si no existe"""
        cliente = self.encontrar_cliente(nombre_cliente, numero_identificacion)
        if not cliente:
            cliente = DatosCliente(nombre_cliente=nombre_cliente, numero_identificacion=numero_identificacion)
            self.db_session.add(cliente)
            self.db_session.commit()
        return cliente

    def obtener_nuevo_grupo(self):
        """Obtiene el nuevo número de grupo para las ventas"""
        ultimo_grupo = self.db_session.query(func.max(VentaProducto.grupo)).scalar()
        return (ultimo_grupo or 0) + 1

    def crear_venta(self, ventas, usuario_id, metodo_pago, fecha_venta, grupo, cliente_id):
        """Crea una venta para productos existentes"""
        try:
            # Verificar existencia de productos
            for venta in ventas:
                producto = self.encontrar_producto(venta['nombre'])
                if not producto or producto.Existencia < venta['cantidad']:
                    raise Exception(f"No hay suficiente existencia del producto {venta['nombre']}")

            # Crear nueva venta
            monto_total = sum([venta['cantidad'] * venta['precio'] for venta in ventas])
            descripcion = ', '.join([venta['nombre'] for venta in ventas])
            nueva_venta = Venta(
                Fecha_Venta=fecha_venta,
                Monto_venta=monto_total,
                Desc_compra=descripcion,
                cantidad=sum([venta['cantidad'] for venta in ventas]),
                Metodo=metodo_pago
            )
            self.db_session.add(nueva_venta)
            self.db_session.commit()

            # Insertar en ventas_productos y actualizar stock
            for venta in ventas:
                producto = self.encontrar_producto(venta['nombre'])
                venta_producto = VentaProducto(
                    ventas_idventas1=nueva_venta.idVentas,
                    productos_idproductos1=producto.id_producto,
                    Users_idUsers=usuario_id,
                    cantidad=venta['cantidad'],
                    grupo=grupo,
                    cliente_id=cliente_id
                )
                self.db_session.add(venta_producto)

                producto.Existencia -= venta['cantidad']
                self.db_session.commit()

            return nueva_venta, "Venta creada exitosamente"
        except Exception as e:
            self.db_session.rollback()
            return None, f"Error al crear la venta: {e}"

    def obtener_ventas(self):
        """Obtiene todas las ventas agrupadas por el grupo"""
        registros = self.db_session.query(VentaProducto.grupo, Venta, DatosCliente).join(Venta, Venta.idVentas == VentaProducto.ventas_idventas1).join(DatosCliente, DatosCliente.id_cliente == VentaProducto.cliente_id).group_by(VentaProducto.grupo, Venta.idVentas, DatosCliente.id_cliente).all()
        ventas = []

        for grupo, venta, cliente in registros:
            productos = self.db_session.query(VentaProducto, Producto).filter(VentaProducto.grupo == grupo).join(Producto, Producto.id_producto == VentaProducto.productos_idproductos1).all()
            descripcion_venta = {producto.nom_producto: venta_producto.cantidad for venta_producto, producto in productos}
            ventas.append({
                "fecha": venta.Fecha_Venta.strftime("%Y-%m-%d"),
                "cliente": cliente.nombre_cliente,
                "Cedula": cliente.numero_identificacion,
                "Descripcion_Venta": descripcion_venta,
                "monto_total": venta.Monto_venta,
                "metodo": venta.Metodo
            })
        return ventas

    def eliminar_venta(self, venta_id):
        """Elimina una venta y actualiza la cantidad del producto"""
        try:
            venta = self.db_session.query(Venta).get(venta_id)
            if not venta:
                return False, "Venta no encontrada"

            productos_venta = self.db_session.query(VentaProducto).filter_by(ventas_idventas1=venta_id).all()
            for pv in productos_venta:
                producto = self.db_session.query(Producto).get(pv.productos_idproductos1)
                producto.Existencia += pv.cantidad
                self.db_session.delete(pv)

            self.db_session.delete(venta)
            self.db_session.commit()

            return True, "Venta eliminada exitosamente"
        except Exception as e:
            self.db_session.rollback()
            return False, f"Error al eliminar la venta: {e}"

    def crear_ventas_multiples(self, ventas, username, nombre_cliente, numero_identificacion, metodo_pago, fecha_venta):
        """Crea múltiples ventas a la vez en un solo registro"""
        usuario = self.encontrar_usuario(username)
        if not usuario:
            return [f"Usuario {username} no encontrado"]

        # Crear o encontrar el cliente
        cliente = self.crear_cliente(nombre_cliente, numero_identificacion)

        # Obtener nuevo grupo
        nuevo_grupo = self.obtener_nuevo_grupo()

        # Agrupar todas las ventas en un solo registro
        productos = [{"nombre": nombre, "cantidad": cantidad, "precio": precio} for nombre, cantidad, precio in ventas]

        # Crear un solo registro de venta
        nueva_venta, mensaje = self.crear_venta(productos, usuario.idUsers, metodo_pago, fecha_venta, nuevo_grupo, cliente.id_cliente)
        
        if nueva_venta:
            return [f"Venta creada: Fecha {nueva_venta.Fecha_Venta}, Cliente {nombre_cliente}, Descripción {nueva_venta.Desc_compra}, Monto {nueva_venta.Monto_venta}, Método {nueva_venta.Metodo}"]
        else:
            return [f"Error al crear la venta: {mensaje}"]

# Ejemplo de uso
if __name__ == '__main__':
    conexion = DbConnector(DATABASE_URL)

    # Crea una instancia de sesión
    db_session = conexion.get_session()

    # Instancia el CRUD de ventas
    crud_ventas = CRUDVentas(db_session)

    # Ejemplo de crear múltiples ventas
    ventas = [("Martillo", 4, 25.0), ("Clavos", 2, 10.0), ("Lijas", 6, 5.0)]
    resultados = crud_ventas.crear_ventas_multiples(ventas, "John Doe", "Jane Doe", "123456789", "USD", "2024-06-23")
    
    for resultado in resultados:
        print(resultado)

    # Obtener y mostrar todas las ventas
    ventas_registradas = crud_ventas.obtener_ventas()
    for registro in ventas_registradas:
        print(registro)

    # Cierra la sesión de la base de datos
    db_session.close()