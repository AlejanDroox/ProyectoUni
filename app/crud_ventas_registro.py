from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, DateTime, Enum, Text, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime

# Configura la cadena de conexión utilizando pymysql
DATABASE_URL = "mysql+pymysql://root:root123@localhost:3306/dbferreteria"

# Crea el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

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
    Valor_Producto = Column(Numeric(10, 2), nullable=False)

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

    venta = relationship("Venta", back_populates="productos_relacion")
    producto = relationship("Producto", back_populates="ventas_relacion")
    user = relationship("User", back_populates="ventas_relacion")

# Crea las tablas en la base de datos si no existen
Base.metadata.create_all(engine)

# Clase para manejar la conexión a la base de datos
class DbConnector:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        return self.SessionLocal()

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

    def crear_venta(self, ventas, usuario_id, metodo_pago):
        """Crea una venta para productos existentes"""
        try:
            # Verificar existencia de productos
            for venta in ventas:
                producto = self.encontrar_producto(venta['nombre'])
                if not producto or producto.Existencia < venta['cantidad']:
                    raise Exception(f"No hay suficiente existencia del producto {venta['nombre']}")

            # Crear nueva venta
            monto_total = sum([venta['cantidad'] * venta['precio'] for venta in ventas])
            nueva_venta = Venta(
                Monto_venta=monto_total,
                Desc_compra=', '.join([venta['nombre'] for venta in ventas]),
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
                    Users_idUsers=usuario_id
                )
                self.db_session.add(venta_producto)

                producto.Existencia -= venta['cantidad']
                self.db_session.commit()

            return nueva_venta, "Venta creada exitosamente"
        except Exception as e:
            self.db_session.rollback()
            return None, f"Error al crear la venta: {e}"

    def obtener_ventas(self):
        """Obtiene todas las ventas"""
        registros = (
            self.db_session.query(Venta, User, VentaProducto)
            .join(VentaProducto, Venta.idVentas == VentaProducto.ventas_idventas1)
            .join(User, User.idUsers == VentaProducto.Users_idUsers)
            .all()
        )
        ventas = []
        for venta, user, _ in registros:
            ventas.append({
                "fecha": venta.Fecha_Venta,
                "cliente": user.username,
                "Descripcion": venta.Desc_compra,
                "Monto": venta.Monto_venta,
                "Metodo": venta.Metodo
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

    def crear_ventas_multiples(self, ventas, username, metodo_pago):
        """Crea múltiples ventas a la vez"""
        usuario = self.encontrar_usuario(username)
        if not usuario:
            return [f"Usuario {username} no encontrado"]

        mensajes = []
        for nombre, cantidad, precio in ventas:
            nueva_venta, mensaje = self.crear_venta([{'nombre': nombre, 'cantidad': cantidad, 'precio': precio}], usuario.idUsers, metodo_pago)
            if nueva_venta:
                mensajes.append(f"Venta de {cantidad} {nombre} realizada: Total {nueva_venta.Monto_venta}")
            else:
                mensajes.append(f"Error al realizar venta de {cantidad} {nombre}: {mensaje}")

        return mensajes

# Ejemplo de uso
if __name__ == '__main__':
    conexion = DbConnector(DATABASE_URL)

    # Crea una instancia de sesión
    db_session = conexion.get_session()

    # Instancia el CRUD de ventas
    crud_ventas = CRUDVentas(db_session)

    # Ejemplo de crear múltiples ventas
    ventas = [("Tornillos", 2, 10.0), ("Clavos", 5, 5.0)]
    resultados = crud_ventas.crear_ventas_multiples(ventas, "yosnel", "USD")
    
    for resultado in resultados:
        print(resultado)

    # Obtener y mostrar todas las ventas
    ventas_registradas = crud_ventas.obtener_ventas()
    print(ventas_registradas)

    # Cierra la sesión de la base de datos
    db_session.close()