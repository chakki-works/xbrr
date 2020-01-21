from xbrr.base.reader.base_element_schema import BaseElementSchema


class ElementSchema(BaseElementSchema):

    def __init__(self,
                 name="", reference="", label="", alias="",
                 abstract="", data_type="",
                 period_type="", balance=""):
        super().__init__()
        self.name = name
        self.reference = reference
        self.label = label
        self.alias = alias
        self.abstract = abstract
        self.data_type = data_type
        self.period_type = period_type
        self.balance = balance

    def set_alias(self, alias):
        self.alias = alias
        return self

    @classmethod
    def create_from_reference(cls, reader, reference,
                              label_kind="", label_verbose=False):

        name = reference.split("#")[-1]
        label = ""
        abstract = ""
        data_type = ""
        period_type = ""
        balance = ""

        if reader.xbrl_dir:
            _def = reader.read_by_link(reference)
            label = _def.label(label_kind, label_verbose)
            xsd = _def.xsd
            abstract = xsd["abstract"]
            data_type = xsd["type"]
            if "xbrli:periodType" in xsd.attrs:
                period_type = xsd["xbrli:periodType"]

            if "xbrli:balance" in xsd.attrs:
                balance = xsd["xbrli:balance"]

        instance = cls(name=name, reference=reference, label=label,
                       abstract=abstract, data_type=data_type,
                       period_type=period_type, balance=balance)
        return instance

    def to_dict(self):
        return {
            "name": self.name,
            "reference": self.reference,
            "label": self.label,
            "abstract": self.abstract,
            "data_type": self.data_type,
            "period_type": self.period_type,
            "balance": self.balance
        }
