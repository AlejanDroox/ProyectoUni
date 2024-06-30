from db.db_connector import DbConnector
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from utils.errores import ValuesExist
from utils.globals import CONFIG


# Crea el motor de SQLAlchemy
engine = create_engine(CONFIG)

# Crea una instancia de automap_base
Base = automap_base()

# Refleja las tablas de la base de datos en los modelos de SQLAlchemy
Base.prepare(engine)

# Accede a la clase de modelo correspondiente a la tabla 'Productos'

Producto = Base.classes.productos

class ControlProductos():
    """clase que maneja las operaciones de los productos"""

    def __init__(self, db_connector):
        self.db_connector = db_connector

    def encontrar_producto(self, nombre, descripcion=None):
        """Busca producto por nombre y descripción"""
        query = self.db_connector.session.query(Producto).filter_by(nom_producto=nombre)
        if descripcion:
            query = query.filter_by(Desc_Producto=descripcion)
        return query.first()


        
    
    def devolver_productor(self,Producto):
        devolver2= list(self.db_connector.session.query(Producto).all())
        if devolver2:
            for Producto in devolver2 :
                    break
                    print(f"Nombre_Producto: {Producto.nom_Producto}")
                    print(f"existencia: {Producto.Existencia}")
                    print(f"valor_producto: {Producto.Valor_Producto}")
                    print("-" * 20)   
                    
                    # no se que tiene este codigo no agarra
        return devolver2                    
        
 

    def create_product(self, nom_Producto, existencia, descripcion, valor_v,valor_c,
                    id_usuarios, image):
        """crea un producto"""
        producto = self.encontrar_producto(nom_Producto)
        if not producto:
            producto = Producto(
                nom_producto=nom_Producto, 
                Existencia=existencia,
                Desc_Producto=descripcion,
                Valor_Producto_C=valor_c,
                Valor_Producto_V=valor_v,
                Image=image,
                #Users_idUsers=id_usuarios
                )
            self.db_connector.session.add(producto)
            self.db_connector.session.commit()
            msg = f"El producto {nom_Producto} fue creado exitosamente."
            return msg
        raise ValuesExist(msg=f'Ya se encuentra almacenado un producto con el {nom_Producto} y la descripcion ingresada, intente con otros datos')

    def update_products(self, nom_Producto, **kwargs):
        #print(Producto)
        """actualizaz los datos de un producto"""
        producto = self.encontrar_producto(nom_Producto)
        if producto:
            for key, value in kwargs.items():
                setattr(producto, key, value)
            self.db_connector.session.commit()
            print(f"los datos del producto {nom_Producto} se han actualizado")
            return True
        else:
            print(f"El producto {nom_Producto} no se encuentra en existencia")
            return False





            # Configuración de la base de datos
            

if __name__ =='__main__':

    conexion = DbConnector(CONFIG)

    Base.metadata.create_all(conexion.engine)

    control_productos = ControlProductos(conexion)

    #control_productos.update_products(
        #"Tornillos4", Valor_Producto=20, Existencia=100)
    
    
    control_productos.devolver_productor(Producto)
