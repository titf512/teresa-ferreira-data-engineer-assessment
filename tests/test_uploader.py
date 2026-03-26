"""Test the uploader module."""
import fsspec

from src.firds.uploader import Uploader


def test_upload_file_to_memory(tmp_path):
    """Test that the uploader can move a file to a virtual memory space.

    This simulates S3/Azure.
    """
    local_file = "tests/resources/firds_instruments_with_contains_a.csv"

    # Upload to a 'memory://' URI
    uploader = Uploader()
    memory_uri = "memory://unit-test/firds_export.csv"

    success = uploader.upload(local_file, memory_uri)

    assert success is True

    # Verify the file actually exists in the virtual memory
    with fsspec.open(memory_uri, 'rt') as f:
        content = f.read()
        assert "AT0000A2B3D9" in content


def test_upload_failure_handles_exception(caplog):
    """Test that the uploader catches errors."""
    uploader = Uploader()

    # Try to upload a file that doesn't exist
    success = uploader.upload("non_existent_file.csv", "memory://error-test.csv")

    assert success is False
