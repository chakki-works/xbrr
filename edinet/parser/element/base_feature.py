class BaseFeature():

    def __init__(self, xbrl_file):
        self.xbrl_file = xbrl_file

    def get(self, name):
        property = getattr(self, name, None)
        if property is None:
            raise Exception("{} does not exist as property.".format(name))
        else:
            value, ground = property
            result = {}
            result[name] = {
                "value": value,
                "ground": ground
            }
            return result
