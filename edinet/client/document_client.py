import re
from pathlib import Path
import tempfile
from zipfile import ZipFile
import requests
from edinet.client.base_client import BaseClient
from edinet.models.error_response import ErrorResponse


class DocumentClient(BaseClient):
    """Client to get file."""

    def __init__(self):
        super().__init__(target="documents/{}")

    def get(self, document_id: str, response_type: str,
            save_dir: str = "", file_name: str = "") -> str:
        """Get file of document_id and save it to save_dir/file_name.

        Arguments:
            document_id {str} -- Document id of EDINET.
            response_type {str} -- Response type of document get API.
                                   "1": Submitted document & audit report (ZIP)
                                   "2": Submitted document (PDF)
                                   "3": Attachment documents (ZIP)
                                   "4": English file (ZIP)

        Keyword Arguments:
            save_dir {str} -- Directory to save file (default: {""}).
            file_name {str} -- Filename of the document (default: {""}).

        Returns:
            str -- Path to saved file.
        """
        url = self.endpoint.format(document_id)
        params = {
            "type": response_type
        }

        # Caution
        r = requests.get(url, params=params, stream=True, verify=False)

        if not r.ok:
            r.raise_for_status()
        elif r.headers["content-type"].startswith("application/json"):
            error = ErrorResponse.create(r.json())
            error.raise_for_status(r)
        else:
            _file_name = file_name
            if not _file_name:
                if "content-disposition" in r.headers:
                    d = r.headers["content-disposition"]
                    file_names = re.findall("filename=\"(.+)\"", d)
                    if len(file_names) > 0:
                        _file_name = file_names[0]

                if not _file_name:
                    ext = ".pdf" if response_type == "2" else ".zip"
                    _file_name = document_id + ext

            chunk_size = 1024
            if save_dir:
                save_path = Path(save_dir).joinpath(_file_name)
            else:
                tmpf = tempfile.NamedTemporaryFile(
                        suffix="__" + _file_name, delete=False)
                save_path = Path(tmpf.name)

            with save_path.open(mode="wb") as f:
                for chunk in r.iter_content(chunk_size):
                    f.write(chunk)

            return save_path

    def get_pdf(self, document_id: str,
                save_dir: str = "", file_name: str = "") -> str:
        """Get PDF file.

        Arguments:
            document_id {str} -- Document id of EDINET.

        Keyword Arguments:
            save_dir {str} -- Directory to save file (default: {""}).
            file_name {str} -- Filename of the document (default: {""}).

        Returns:
            str -- Saved file path.
        """
        response_type = "2"
        path = self.get(document_id, response_type, save_dir, file_name)
        return path

    def get_xbrl(self, document_id: str,
                 lang: str = "ja", save_dir: str = "", file_name: str = ""):
        """Get XBRL file.

        Arguments:
            document_id {str} -- Document id of EDINET.

        Keyword Arguments:
            lang {str} -- Language of document (default: {"ja"})
            save_dir {str} -- Directory to save file (default: {""}).
            file_name {str} -- Filename of the document (default: {""}).

        Returns:
            str -- Saved file path.
        """
        response_type = -1
        xbrl_path = ""
        if lang == "ja":
            response_type = "1"
            xbrl_path = "XBRL/PublicDoc/"
        elif lang == "en":
            response_type = "4"
            xbrl_path = "XBRL/EnglishDoc/"
        else:
            raise Exception(f"Language {lang} is not supported on EDINET.")

        path = self.get(document_id, response_type, save_dir, file_name)

        with ZipFile(path, "r") as zip:
            files = zip.namelist()
            xbrl_file = ""
            for file_name in files:
                if file_name.startswith(xbrl_path) and \
                   file_name.endswith(".xbrl"):
                    xbrl_file = file_name
                    break

            if xbrl_file:
                xbrl_path = path.with_suffix(".xbrl")
                with xbrl_path.open("wb") as f:
                    f.write(zip.read(xbrl_file))
                path.unlink()
                path = xbrl_path

        return path
