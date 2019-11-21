class XBRLValue():

    def __init__(self, value, data_type, ground=""):
        self.value = value
        self.data_type = data_type
        self.ground = ground

    @classmethod
    def integer(cls, value, ground=""):
        return cls(value, "INT", ground)

    @classmethod
    def float(cls, value, ground=""):
        return cls(value, "FLT", ground)

    @classmethod
    def category(cls, value, ground=""):
        return cls(value, "CAT", ground)

    @classmethod
    def string(cls, value, ground=""):
        return cls(value, "STR", ground)

    @classmethod
    def text(cls, value, ground=""):
        return cls(value, "TXT", ground)

    @classmethod
    def date(cls, value, ground=""):
        return cls(value, "DAT", ground)

    @classmethod
    def timestamp(cls, value, ground=""):
        return cls(value, "TIM", ground)

    def __str__(self):
        return f"(Value: {self.value}, Unit: {self.unit}, Ground: {self.ground})"
