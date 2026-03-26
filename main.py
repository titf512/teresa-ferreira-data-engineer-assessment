"""Main entry point for the FIRDS ETL pipeline."""

import logging

from src.firds.extractor import Extractor
from src.firds.parser import Parser
from src.firds.transformer import Transformer
from src.firds.uploader import Uploader

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

    # csv transformer
    transformer = Transformer(output_csv)

    # 5: Add column a_count to csv
    # This column contains the number of times the lower-case character “a”
    # is present in the column `FinInstrmGnlAttrbts.FullNm`
    logger.info("--- Adding a_count column to CSV ---\n")
    transformer.add_a_count_column()

    # 6: Add column contains_a to csv
    # value “YES” if `a_count` is greater than 0, “NO” otherwise.
    logger.info("--- Adding contains_a column to CSV ---\n")
    transformer.add_contains_a_column()

    # 7+8: Store the csv
    # Code below how I would handle AWS S3 and Microsoft Azure
    # Since I don't have real AWS or Azure credentials, I'm going to use Local Mocking
    # for demonstration by using the file:// protocol with fsspec

    '''
    # --- For AWS S3---
    # I didn't put storage_options for AWS S3 because fsspec Looks for ~/.aws/credentials
    # In a real production environment I would just have to make sure that I had that file
    aws_uploader = Uploader()
    aws_s3_url = "PLACEHOLDER_FOR_URL"
    aws_uploader.upload(output_csv, aws_s3_url)

    # --- For Microsoft Azure ---
    azure_options = {
        "account_name": "my_azure_account",
        "account_key": "my_secret_key"
    }
    azure_uploader = Uploader(azure_options)
    azure_url = "PLACEHOLDER_FOR_URL"
    azure_uploader.upload(output_csv, azure_url)
    '''

    mock_cloud_path = "file://data/mock_s3_bucket/firds_export.csv"

    uploader = Uploader()
    uploader.upload(output_csv, mock_cloud_path)


if __name__ == "__main__":
    run_pipeline()