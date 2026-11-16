"""Exercise large Git inventories using fictional temporary files."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import privacy_scan


class InventoryBatchingTest(unittest.TestCase):
    def test_git_errors_and_incomplete_metadata_fail_closed(self):
        blob = privacy_scan.Blob("fixture.txt", "a" * 64, "100644")
        cases = (
            (1, b"", "git_read_failed"),
            (0, b"malformed\n", "invalid_blob_metadata"),
            (0, b"", "incomplete_blob_metadata"),
        )
        for returncode, stdout, error in cases:
            with self.subTest(error=error), patch.object(
                privacy_scan.subprocess,
                "run",
                return_value=subprocess.CompletedProcess([], returncode, stdout),
            ):
                with self.assertRaisesRegex(privacy_scan.ScanError, error):
                    privacy_scan.blob_sizes(Path("."), [blob])

    def test_large_inventory_has_all_blob_sizes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            for number in range(1800):
                (root / f"item-{number:04d}.txt").write_text(
                    f"fictional{number:04d}\n", encoding="utf-8"
                )
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            scripts = Path(__file__).resolve().parents[1] / "scripts"
            program = """
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import privacy_scan
root = Path(sys.argv[2])
blobs = privacy_scan.selected_blobs(root, None, 'HEAD', True)
sizes = privacy_scan.blob_sizes(root, blobs)
assert len(blobs) == len(sizes) == 1800
assert set(sizes.values()) == {14}
"""
            subprocess.run(
                [sys.executable, "-I", "-c", program, str(scripts), str(root)],
                check=True,
                timeout=25,
            )


if __name__ == "__main__":
    unittest.main()
