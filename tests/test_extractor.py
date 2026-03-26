"""Test the extractor."""

from unittest.mock import MagicMock, patch

from firds.extractor import Extractor


def test_extractor_mock(tmp_path):
    """Test if the extractor handles the stream properly with mocks."""
    extractor = Extractor()
    target_file = tmp_path / "firds.xml"

    with patch('requests.get') as mock_get:
        mock_response = mock_get.return_value.__enter__.return_value
        mock_response.iter_content = lambda chunk_size: [b"data"]
        mock_response.raise_for_status = MagicMock()

        extractor.download("http://fakeurl.com", str(target_file))

    assert target_file.exists()

    assert target_file.parent.exists()
    assert target_file.exists()