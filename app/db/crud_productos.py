from db_connector import DBConnector
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base


# Crea el motor de SQLAlchemy
engine = create_engine(
    'mysql://root:1234@127.0.0.1:3306/dbferreteria')

# Crea una instancia de automap_base
Base = automap_base()

# Refleja las tablas de la base de datos en los modelos de SQLAlchemy
Base.prepare(engine, reflect=True)

# Accede a la clase de modelo correspondiente a la tabla 'Productos'
Producto = Base.classes.productos


class ControlProductos():
    """clase que maneja las operaciones de los productos"""

    def __init__(self, db_connector):
        self.db_connector = db_connector

    def encontrar_producto(self, nombre):
        """busca producto por nombre"""
        return self.db_connector.session.query(Producto).filter_by(nom_Producto=nombre).first()

    def create_product(self, nombre, existencia, descripcion, valor, marca,
                       id_categoria, id_proveedor, id_usuarios):
        """crea un producto"""
        producto = self.encontrar_producto(nombre)
        if not producto:
            producto = Producto(nom_Producto=nombre, Existencia=existencia,
                                Desc_Producto=descripcion, Valor_Producto=valor,
                                Marca=marca, Categoria_idCategoria=id_categoria,
                                Proveedor_Id_provedor=id_proveedor, Users_idUsers=id_usuarios)
            self.db_connector.session.add(producto)
            self.db_connector.session.commit()
            print(f"El producto {nombre} fue creado exitosamente.")
            return True
        else:
            print(f"El producto {nombre} ya existe.")
            return False

    def update_products(self, nombre, **kwargs):
        """actualizaz los datos de un producto"""
        producto = self.encontrar_producto(nombre)
        if producto:
            for key, value in kwargs.items():
                setattr(producto, key, value)
            self.db_connector.session.commit()
            print(f"los datos del producto {nombre} se han actualizado")
            return True
        else:
            print(f"El producto {nombre} no se encuentra en existencia")
            return False

            # Configuración de la base de datos
CONFIG = 'mysql://root:1234@127.0.0.1:3306/dbferreteria'
conexion = DBConnector(CONFIG)

Base.metadata.create_all(conexion.engine)

control_productos = ControlProductos(conexion)

control_productos.update_products(
    "Tornillos4", Valor_Producto=20, Existencia=100)
