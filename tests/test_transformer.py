"""Test the transformer module."""

import shutil

import pandas as pd

from firds.transformer import Transformer


def test_add_a_count_logic(tmp_path):
    """Test the creation of the 'a_count' column."""
    csv_file = "tests/resources/firds_instruments.csv"

    #This is going to be a copy of the previous csv so the original isn't changed.
    csv_file_test = "tests/resources/firds_instruments_test.csv"

    shutil.copy2(csv_file, csv_file_test)

    Transformer(csv_file_test).add_a_count_column()

    df = pd.read_csv(csv_file_test)

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


def test_contains_a_logic():
    """Test the creation of the 'contains_a' column."""
    csv_file = "tests/resources/firds_instruments_with_a_count.csv"

    # This is going to be a copy of the previous csv so the original isn't changed.
    csv_file_test = "tests/resources/firds_instruments_with_a_count_test.csv"

    shutil.copy2(csv_file, csv_file_test)

    Transformer(csv_file_test).add_contains_a_column()

    df = pd.read_csv(csv_file_test)

    # Assertions
    assert df.iloc[0]['contains_a'] == "NO"
    assert df.iloc[1]['contains_a'] == "YES"
    assert df.iloc[2]['contains_a'] == "YES"
    assert df.iloc[3]['contains_a'] == "NO"