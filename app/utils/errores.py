class NullValues(Exception):
    def __init__(self, sin_values):
        super().__init__()
        self.sin_values = sin_values
class ValuesInvalid(Exception):
   pass
class ValuesExist(Exception):
    def __init__(self, msg:str = 'Ha ocurrido un error inesperado intentelo nuevamente \n si el error persiste llamar al servicio tecnico'):
        super().__init__()
        self.msg = msg
