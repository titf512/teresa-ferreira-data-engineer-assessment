from src.firds.extractor import Extractor
from unittest.mock import patch, MagicMock

def test_extractor_creates_directory(tmp_path):
    """Test if the extractor creates the target directory."""
    extractor = Extractor()
    target_file = tmp_path / "raw" / "firds.xml"

    # Mock the request so it doesn't actually go to the internet
    with patch('requests.get') as mock_get:
        mock_get.return_value.__enter__.return_value.iter_content = lambda chunk_size: [b"data"]
        mock_get.return_value.__enter__.return_value.raise_for_status = MagicMock()

        extractor.download("http://fakeurl.com", str(target_file))

    assert target_file.parent.exists()
    assert target_file.exists()