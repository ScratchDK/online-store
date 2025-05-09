class ZeroQuantityError(ValueError):
    def __init__(self, message="Количество товара не может быть нулевым!"):
        super().__init__(message)
