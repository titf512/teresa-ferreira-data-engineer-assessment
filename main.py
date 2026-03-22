"""Main entry point for the FIRDS ETL pipeline."""

import logging

from src.firds.extractor import Extractor

logging.basicConfig(
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_pipeline():
    """Execute the complete process."""
    URL = "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100"
    DATA_DIR = "data/raw"

    # 1. Download the xml
    logger.info("--- Starting Extraction ---\n")
    extractor = Extractor()
    extractor.download(URL, DATA_DIR)

if __name__ == "__main__":
    run_pipeline()