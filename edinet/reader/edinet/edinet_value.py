from edinet.reader.base_value import BaseValue


class EDINETValue(BaseValue):

    def __init__(self, name="", reference="",
                 value="", unit="",
                 consolidated=True,
                 period=None, period_start=None,
                 label="", ground=""):
        super().__init__()
        self.name = name
        self.reference = reference
        self.value = value
        self.unit = unit
        self.consolidated = consolidated
        self.period = period
        self.period_start = period_start
        self.label = label
        self.ground = ground

    @property
    def normalized_text(self):
        return self.normalize(self.value)

    @classmethod
    def create_from_element(cls, reader, element,
                            label_kind="", label_verbose=False):
        name = element.name
        reference = f"{element.namespace}#{element.name}"
        value = element.text
        unit = ""
        if "unitRef" in element.attrs:
            unit = element["unitRef"]

        label = ""
        if reader.xbrl_dir:
            label = reader\
                    .read_by_link(reference)\
                    .label(label_kind, label_verbose)

        consolidated = True
        period = None
        period_start = None

        if "contextRef" in element.attrs:
            context_id = element["contextRef"]
            if context_id.endswith("NonConsolidatedMember"):
                consolidated = False

            context = reader.xbrl.find("xbrli:context", {"id": context_id})
            if context.find("xbrli:instant"):
                period = context.find("xbrli:instant").text
            elif context.find("xbrli:endDate"):
                period = context.find("xbrli:endDate").text
                period_start = context.find("xbrli:startDate").text

        instance = cls(
            name=name, reference=reference,
            value=value, unit=unit,
            consolidated=consolidated,
            period=period, period_start=period_start,
            label=label,
            ground=""
        )

        return instance

    def to_dict(self):
        return {
            "name": self.name,
            "reference": self.reference,
            "value": self.value,
            "unit": self.unit,
            "consolidated": self.consolidated,
            "period": self.period,
            "period_start": self.period_start,
            "label": self.label,
        }


class EDINETElementSchema():

    def __init__(self,
                 name="", reference="", label="", alias="",
                 abstract="", data_type="",
                 period_type="", balance=""):
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
        if reader.xbrl_dir:
            _def = reader.read_by_link(reference)
            label = _def.label(label_kind, label_verbose)
            xsd = _def.xsd
            abstract = xsd["abstract"]
            data_type = xsd["type"]

        period_type = ""
        if "xbrli:periodType" in xsd.attrs:
            period_type = xsd["xbrli:periodType"]

        balance = ""
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
