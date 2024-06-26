class NullValues(Exception):
    def __init__(self, sin_values: list = []):
        super().__init__()
        self.sin_values = sin_values
class ValuesInvalid(Exception):
   pass