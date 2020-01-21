from xbrr.base.reader.base_element_value import BaseElementValue


class ElementValue(BaseElementValue):

    def __init__(self, name="", reference="",
                 value="", unit="",
                 consolidated=True,
                 context="", member="",
                 period=None, period_start=None,
                 label="", ground=""):
        super().__init__()
        self.name = name
        self.reference = reference
        self.value = value
        self.unit = unit
        self.consolidated = consolidated
        self.context = context
        self.member = member
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

        _element = element.element
        name = _element.name
        reference = element.reference
        value = _element.text
        unit = ""
        if "unitRef" in _element.attrs:
            unit = _element["unitRef"]

        label = ""
        if reader.xbrl_dir:
            label = reader\
                    .read_by_link(reference)\
                    .label(label_kind, label_verbose)

        consolidated = True
        period = None
        period_start = None
        context_text = ""
        member = ""

        if "contextRef" in _element.attrs:
            context_id = _element["contextRef"]
            context_ids = context_id.split("_", 1)
            if len(context_ids) > 1:
                context_text = context_ids[0]
                member = context_ids[1]
            else:
                context_text = context_ids[0]

            if "NonConsolidatedMember" in context_id:
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
            context=context_text, member=member,
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
            "context": self.context,
            "member": self.member,
            "period": self.period,
            "period_start": self.period_start,
            "label": self.label,
        }
