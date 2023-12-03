class Operation:
    def __init__(self, name: str,
                 arity: int):
        self._name = name

        if arity != 1 and arity != 2:
            raise ValueError("Only unary and binary operations are supported")
        self._arity = arity

    @property
    def arity(self):
        return self._arity

    @property
    def name(self):
        return self._name

    def __eq__(self, other):
        return self.name == other.name and self.arity == other.arity
