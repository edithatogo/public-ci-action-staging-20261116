"""Exercise the selected interpreter and isolated fixture environment."""

import importlib.metadata
import importlib.util
import sys
import unittest


class RuntimeSmokeTest(unittest.TestCase):
    def test_qualified_cpython(self):
        self.assertEqual(sys.implementation.name, "cpython")
        self.assertEqual(sys.version_info[:3], (3, 15, 1))

    def test_virtual_environment_and_excluded_packages(self):
        self.assertNotEqual(sys.prefix, sys.base_prefix)
        for name in ("pandas", "xarray"):
            with self.subTest(package=name):
                self.assertIsNone(importlib.util.find_spec(name))

    def test_fixture_dependency_is_installed(self):
        self.assertEqual(importlib.metadata.version("packaging"), "26.3")


if __name__ == "__main__":
    unittest.main()
