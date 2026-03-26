"""Module responsible for parsing files."""
import csv
import logging

import pandas as pd
from lxml import etree

logger = logging.getLogger(__name__)


class Parser:
    """Handles parsing ESMA index and data files."""

    def get_target_link(self,xml_path: str):
        """Get the download link from the second DLTINS file."""
        # I decided to use lxml.etree.iterparse for memory-efficiency reasons
        # The xml file is quite heavy.
        # However, I could have used something more simple like pandas read_xml()
        tree = etree.parse(xml_path)

        # Selects the 'download_link' text of the SECOND 'doc'
        # where the 'file_type' is 'DLTINS'
        xpath = ("(//doc[str[@name='file_type']='DLTINS'])[2]/"
                 "str[@name='download_link']/text()")
        result = tree.xpath(xpath)

        return result[0] if result else ""

    def xml_to_csv(self, xml_path: str, output_path: str):
        """Parse the xml to csv file."""
        headers = [
            "FinInstrmGnlAttrbts.Id", "FinInstrmGnlAttrbts.FullNm",
            "FinInstrmGnlAttrbts.ClssfctnTp", "FinInstrmGnlAttrbts.CmmdtyDerivInd",
            "FinInstrmGnlAttrbts.NtnlCcy", "Issr"
        ]

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            context = etree.iterparse(xml_path, events=('end',),
                                      tag='{*}FinInstrmGnlAttrbts')
            for _, elem in context:
                row = [
                    elem.findtext('{*}Id'),
                    elem.findtext('{*}FullNm'),
                    elem.findtext('{*}ClssfctnTp'),
                    elem.findtext('{*}CmmdtyDerivInd'),
                    elem.findtext('{*}NtnlCcy'),
                ]
                issr_list = elem.xpath('..//*[local-name()="Issr"]/text()')
                row.append(issr_list[0] if issr_list else "")

                writer.writerow(row)

                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]


    def add_a_count_column(self, csv_path: str):
        """Add the 'a_count' column to the csv file."""
        #Using Pandas for simplicity and standard data manipulation.
        df = pd.read_csv(csv_path)

        column_name = "FinInstrmGnlAttrbts.FullNm"
        df['a_count'] = df[column_name].astype(str).str.count('a')

        df.to_csv(csv_path, index=False)