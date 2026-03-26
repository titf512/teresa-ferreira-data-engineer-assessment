"""Module responsible for storing the csv file."""
import logging

import fsspec

logger = logging.getLogger(__name__)


class Uploader:
    """A cloud-agnostic uploader using fsspec."""
    def __init__(self, storage_options: dict = None):
        """Initializes the Uploader with the different credentials.

        e.g., {"key": "...", "secret": "..."} for S3
        or {"account_name": "...", "account_key": "..."} for Azure.
        """
        self.storage_options = storage_options or {}

    def upload(self, local_path: str, remote_url: str):
        """Uploads the csv file to a cloud path."""
        try:
            logger.info(f"--- Uploading {local_path} to {remote_url} ---\n")
            with fsspec.open(local_path, 'rb') as source:
                with fsspec.open(remote_url, 'wb', **self.storage_options) as target:
                    target.write(source.read())

            logger.info("--- Upload of csv was successful ---")
            return True

        except Exception as e:
            logger.error(f"--- Upload Failed: {str(e)} ---")
            return False