
from edinet.facade import APIFacade


api = APIFacade()


def read(path, taxonomy="edinet"):
    if taxonomy == "edinet":
        from edinet.reader.edinet.xbrl_reader import XBRLReader
        return XBRLReader(path)
    else:
        raise Exception(f"{taxonomy} is not supported.")
