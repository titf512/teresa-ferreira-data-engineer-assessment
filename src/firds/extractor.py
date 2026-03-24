"""Module responsible for downloading files from ESMA."""
import logging
import os
import zipfile

import requests

logger = logging.getLogger(__name__)


class Extractor:
    """Handles downloading the DLTINS file from the link."""

    def download(self, url: str, target_path: str):
        """Downloads the file to the specified path."""
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        logger.info(f"Initiating download from: {url}")

        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(target_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        logger.info(f"File successfully saved to: {target_path}")



    def extract_zip(self, zip_path: str, extract_to: str):
        """Unzips the file and returns the path to the extracted XML."""
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            xml_filename = zip_ref.namelist()[0]
            return os.path.join(extract_to, xml_filename)

