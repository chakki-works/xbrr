class Value():

    def __init__(self, value, unit, ground):
        self.value = value
        self.unit = unit
        self.ground = ground

    def __str__(self):
        return f"(Value: {self.value}, Unit: {self.unit}, Ground: {self.ground})"


class BaseFeature():

    def __init__(self, xbrl_file):
        self.xbrl_file = xbrl_file

    def get(self, name):
        property = getattr(self, name, None)
        if property is None:
            raise Exception("{} does not exist as property.".format(name))
        else:
            return property
