from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, DateTime, Enum, Text, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime
from utils.globals import CONFIG
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


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

# Clase CRUDVentas
class CRUDVentas:
    def __init__(self, db_session):
        self.db_session = db_session

    def encontrar_producto(self, nombre, descripcion=None):
        """Busca producto por nombre y descripción"""
        query = self.db_session.query(Producto).filter_by(nom_producto=nombre)
        if descripcion:
            query = query.filter_by(Desc_Producto=descripcion)
        return query.first()

    def encontrar_usuario(self, username):
        """Busca usuario por nombre"""
        return self.db_session.query(User).filter_by(username=username).first()

    def encontrar_cliente(self, numero_identificacion):
        """Busca cliente por nombre e identificación"""
        return self.db_session.query(DatosCliente).filter_by(numero_identificacion=numero_identificacion).first()

    def crear_cliente(self, nombre_cliente, numero_identificacion):
        """Crea un nuevo cliente si no existe"""
        cliente = self.encontrar_cliente(numero_identificacion)
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
        """Obtiene todas las ventas agrupadas por el grupo y ordenadas por índice descendente"""
        registros = self.db_session.query(VentaProducto.grupo, Venta, DatosCliente).join(Venta, Venta.idVentas == VentaProducto.ventas_idventas1).join(DatosCliente, DatosCliente.id_cliente == VentaProducto.cliente_id).group_by(VentaProducto.grupo, Venta.idVentas, DatosCliente.id_cliente).order_by(Venta.idVentas.desc()).all()
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

    def buscar_ventas_por_grupo(self, grupo):
        """Busca ventas mediante su agrupación"""
        registros = self.db_session.query(VentaProducto.grupo, Venta, DatosCliente).join(Venta, Venta.idVentas == VentaProducto.ventas_idventas1).join(DatosCliente, DatosCliente.id_cliente == VentaProducto.cliente_id).filter(VentaProducto.grupo == grupo).group_by(VentaProducto.grupo, Venta.idVentas, DatosCliente.id_cliente).order_by(Venta.idVentas.desc()).all()
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
                self.db_session.delete()

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

    def agregar_producto(self, nombre, descripcion, existencia, valor_c, valor_v, image=None):
        """Agrega un nuevo producto si no existe uno con el mismo nombre y descripción"""
        producto_existente = self.encontrar_producto(nombre, descripcion)
        if producto_existente:
            return None, "Producto con el mismo nombre y descripción ya existe"

        nuevo_producto = Producto(
            nom_producto=nombre,
            Desc_Producto=descripcion,
            Existencia=existencia,
            Valor_Producto_C=valor_c,
            Valor_Producto_V=valor_v,
            Image=image
        )
        self.db_session.add(nuevo_producto)
        self.db_session.commit()
        return nuevo_producto, "Producto agregado exitosamente"

    def generar_pdf_ventas(self, ventas, filename='ventas.pdf'):
        """Genera un PDF con todas las ventas registradas"""
        doc = SimpleDocTemplate(filename, pagesize=letter,
                                rightMargin=inch, leftMargin=inch,
                                topMargin=inch, bottomMargin=inch)
        elements = []
        
        # Definir estilos
        styles = getSampleStyleSheet()
        style_title = styles['Title']
        style_normal = styles['Normal']
        style_heading = styles['Heading2']
        
        # Título del documento
        elements.append(Paragraph("Registro de Ventas", style_title))
        elements.append(Spacer(1, 12))  # Espaciador
        
        # Encabezados de la tabla
        table_data = [['Fecha', 'Cliente', 'Identificación', 'Descripción', 'Monto Total', 'Método']]
        
        for venta in ventas:
            descripcion_venta = "<br/>".join([f"{producto}: {cantidad}" for producto, cantidad in venta['Descripcion_Venta'].items()])
            descripcion_venta_paragraph = Paragraph(descripcion_venta, style_normal)
            table_data.append([
                venta['fecha'],
                venta['cliente'],
                venta['Cedula'],
                descripcion_venta_paragraph,
                f"${venta['monto_total']:.2f} bs",
                venta['metodo']
            ])
        
        # Crear tabla
        table = Table(table_data, colWidths=[80, 100, 100, 200, 80, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(table)
        
        # Construir el documento PDF
        doc.build(elements)
        

        return filename

# Ejemplo de uso
if __name__ == '__main__':
    conexion = DbConnector(CONFIG)

    # Crea una instancia de sesión
    db_session = conexion.get_session()

    # Instancia el CRUD de ventas
    crud_ventas = CRUDVentas(db_session)

    # Ejemplo de crear múltiples ventas
    ventas = [("Martillo", 9, 25.0), ("Clavos", 9, 10.0)]
    resultados = crud_ventas.crear_ventas_multiples(ventas, "John Doe", "Jane Doe", "123456789", "USD", "2024-06-23")
    
    for resultado in resultados:
        print(resultado)

    # Obtener y mostrar todas las ventas ordenadas por índice descendente
    ventas_registradas = crud_ventas.obtener_ventas()
    for registro in ventas_registradas:
        print(registro)

    # Generar PDF de ventas
    pdf_filename = crud_ventas.generar_pdf_ventas(ventas_registradas)
    print(f"PDF generado: {pdf_filename}")

    # Cierra la sesión de la base de datos
    db_session.close()