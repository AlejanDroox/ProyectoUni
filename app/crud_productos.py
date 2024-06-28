from db.db_connector import DbConnector
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from db.crud_usuarios import ControlUsuarios
from utils.globals import CONFIG


# Crea el motor de SQLAlchemy
engine = create_engine(CONFIG)

# Crea una instancia de automap_base
Base = automap_base()

# Refleja las tablas de la base de datos en los modelos de SQLAlchemy
Base.prepare(engine)

# Accede a la clase de modelo correspondiente a la tabla 'Productos'

Producto = Base.classes.productos
Proveedor=Base.classes.proveedor

class ControlProductos():
    """clase que maneja las operaciones de los productos"""

    def __init__(self, db_connector):
        self.db_connector = db_connector

    def encontrar_producto(self, nom_Producto):
        """busca producto por nom_Producto"""
        return self.db_connector.session.query(Producto).filter_by(nom_Producto=nom_Producto).first()
        
    def encontrar_id_by_name(self,Nom_proveedor):
        #devuelve el id por elnombre del proveedor
        devolver_id=self.db_connector.session.query(Proveedor.Id_provedor).filter_by(Nom_proveedor=Nom_proveedor).first()
        if devolver_id:
            return devolver_id [0]
        else:
            return None
    

        
    
    def devolver_productos(self,Producto):
        devolver2=list(self.db_connector.session.query(Producto).all())
        if  devolver2: #si no les arroja nada es por que no tienen nada en la db
            print(1)
            print(f"Nombre_productos: {Producto.nom_Producto}")
            for Producto in devolver2 :
                
                print(f"Nombre_productos: {Producto.nom_Producto}")
                print(f"existencia: {Producto.Existencia}")
                print(f"valor_productos: {Producto.Valor_Producto}")
                print("-" * 20)   

                    
        
 

    def create_product(self, nom_Producto, existencia, descripcion, valor,nombre_proveedor, id_usuarios):
        """crea un producto"""
        
        nombre_proveedor=self.encontrar_id_by_name(nombre_proveedor)
       
        
        producto = self.encontrar_producto(nom_Producto)
        if not producto:
            producto = Producto(nom_Producto=nom_Producto, Existencia=existencia,
                                Desc_Producto=descripcion, Valor_Producto=valor, 
                                Proveedor_Id_provedor=nombre_proveedor, Users_idUsers=id_usuarios)
            
            self.db_connector.session.add(producto)
            self.db_connector.session.commit()
            print(f"El producto {nom_Producto} fue creado exitosamente.")
            return True
        else:
            print(f"El producto {nom_Producto} ya existe.")
            return False

    def update_products(self, nom_Producto, **kwargs):
        print(Producto)
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
    ctrl = ControlUsuarios(conexion)
    ctrl.create_user('admin', 'admin2', '1234', 'administrador')
    #control_productos.devolver_productos(Producto)
    
    #control_productos.create_product("caraota",1,"wuw",25,"jonathan",1)

    