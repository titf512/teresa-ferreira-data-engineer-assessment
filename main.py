"""Main entry point for the FIRDS ETL pipeline."""

import logging

from src.firds.extractor import Extractor
from src.firds.parser import Parser

logging.basicConfig(
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_pipeline():
    """Execute the complete process."""
    URL = "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100"
    DATA_DIR = "data/raw.xml"

    # 1. Download the xml
    logger.info("--- Starting XML Extraction ---\n")
    extractor = Extractor()
    extractor.download(URL, DATA_DIR)

    # 2. Find the DLTINS Link inside the XML and download the zip
    logger.info("--- Starting to fetch the second download "
                "link whose file_type is DLTINS ---\n")
    parser = Parser()
    xml_name = DATA_DIR
    dltins_url = parser.get_target_link(xml_name)

    # 3. Extract the xml from the zip
    logger.info("--- Starting ZIP Extraction ---\n")
    zip_path = "data/firds_data.zip"
    extractor.download(dltins_url, zip_path)
    xml_path = extractor.extract_zip(zip_path, "data/")
    logger.info(f"--- File unzipped: {xml_path} ---\n")

    # 4: Convert XML to CSV
    logger.info("--- Converting XML to CSV ---\n")
    output_csv = "data/firds_instruments.csv"
    parser.xml_to_csv(xml_path, output_csv)
    logger.info(f"--- CSV generated: {output_csv} ---\n")

    # 5: Add column a_count to csv
    # This column contains the number of times the lower-case character “a” is present in the column `FinInstrmGnlAttrbts.FullNm`
    logger.info("--- Adding a_count column to CSV ---\n")
    parser.add_a_count_column(output_csv)


if __name__ == "__main__":
    run_pipeline()