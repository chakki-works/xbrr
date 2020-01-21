import unicodedata


class BaseElementValue():

    def __init__(self):
        pass

    def normalize(self, text):
        if text is None:
            return ""
        _text = text.strip()
        _text = unicodedata.normalize("NFKC", _text)
        return _text

    def to_dict(self):
        raise NotImplementedError(
            "You have to implement to_dict in subclass.")
