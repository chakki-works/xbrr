import os
import pyfbi
from xbrr.client.document_client import DocumentClient
from xbrr.reader.edinet.xbrl_reader import XBRLReader
from xbrr.reader.edinet.aspects.finance import Finance


@pyfbi.target
def check():
    _dir = os.path.join(os.path.dirname(__file__), "./tests/data")
    client = DocumentClient()
    file_path = client.get_xbrl("S100G2KL", save_dir=_dir,
                                expand_level="dir")
    reader = XBRLReader(file_path)
    bs = reader.extract(Finance).bs()
    bs.to_csv("bs.csv", index=False, encoding="shift_jis")


with pyfbi.watch():
    check()

pyfbi.dump("result")
pyfbi.show()
