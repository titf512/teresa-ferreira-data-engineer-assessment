"""Test the parsor module."""

import csv
import os

from src.firds.parser import Parser


def test_csv_creation(tmp_path):
    """Test if the CSV file is created."""
    output_file = tmp_path / "firds_instruments_test.csv"

    sample_xml = "tests/resources/firds_instruments_test.xml"

    if os.path.exists(sample_xml):
        Parser().xml_to_csv(sample_xml, str(output_file))
        assert output_file.exists()


def test_csv_headers(tmp_path):
    """Test if the CSV has the correct headers."""
    output_file = tmp_path / "headers_check.csv"
    sample_xml = "data/raw/index.xml"

    expected_headers = [
        "FinInstrmGnlAttrbts.Id", "FinInstrmGnlAttrbts.FullNm",
        "FinInstrmGnlAttrbts.ClssfctnTp", "FinInstrmGnlAttrbts.CmmdtyDerivInd",
        "FinInstrmGnlAttrbts.NtnlCcy", "Issr"
    ]

    if os.path.exists(sample_xml):
        Parser().xml_to_csv(sample_xml, str(output_file))

        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            actual_headers = next(reader)

        assert actual_headers == expected_headers


def test_second_link_extraction():
    """Test if the parser correctly finds the download link."""
    sample_xml = "data/raw/index.xml"
    if os.path.exists(sample_xml):
        link = Parser().get_second_dltins_link(sample_xml)
        assert link is not None
        assert link.startswith("http")