"""Module responsible for parsing files."""
import logging

from lxml import etree

logger = logging.getLogger(__name__)


class Parser:
    """Handles parsing ESMA index and data files."""

    def get_target_link(self,xml_path: str):
        """Get the download link from the second DLTINS file."""
        tree = etree.parse(xml_path)

        # Selects the 'download_link' text of the SECOND 'doc'
        # where the 'file_type' is 'DLTINS'
        xpath = ("(//doc[str[@name='file_type']='DLTINS'])[2]/"
                 "str[@name='download_link']/text()")
        result = tree.xpath(xpath)

        return result[0] if result else ""