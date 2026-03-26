"""Test the parsor module."""

import csv
import os
import shutil

import pandas as pd

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
    sample_xml = "tests/resources/raw.xml"
    if os.path.exists(sample_xml):
        link = Parser().get_target_link(sample_xml)
        assert link is not None
        assert link.startswith("http")


def test_add_a_count_logic(tmp_path):
    """Test the creation of the 'a_count' column."""
    csv_file = "tests/resources/firds_instruments.csv"

    #This is going to be a copy of the previous csv so the original isn't changed.
    csv_file_test = "tests/resources/firds_instruments_test.csv"

    shutil.copy2(csv_file, csv_file_test)

    Parser().add_a_count_column(csv_file)

    df = pd.read_csv(csv_file)

    # 'EGB OE TL.Z./SARTORIUS V' -> 0
    # (All 'A's are uppercase)
    assert df.iloc[0]['a_count'] == 0

    # 'Raiffeisen Centrobank AG TurboL O.End SAP' -> 2
    # ('a' in Raiffeisen, 'a' in Centrobank)
    assert df.iloc[1]['a_count'] == 2

    # 'Turbo Long Open End Zertifikat auf SAP SE' -> 2 (
    # 'a' in Zertifikat, 'a' in auf)
    assert df.iloc[2]['a_count'] == 2

    # 'RCB OE TL.Z./SAP' -> 0 (No lowercase 'a')
    assert df.iloc[3]['a_count'] == 0