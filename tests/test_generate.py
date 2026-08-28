import unittest

from generate import is_covered, parse_domains, remove_redundant


class GenerateTests(unittest.TestCase):
    def test_parses_supported_dns_syntax(self):
        text = "example.com\n||ads.example.net^$third-party\n0.0.0.0 track.example.org\n"
        self.assertEqual(parse_domains(text), {"example.com", "ads.example.net", "track.example.org"})

    def test_ignores_exceptions_and_url_filters(self):
        self.assertEqual(parse_domains("@@||good.example^\n/banner.js\n! comment\n"), set())

    def test_parent_covers_child(self):
        self.assertTrue(is_covered("a.ads.example.com", {"ads.example.com"}))
        self.assertFalse(is_covered("notexample.com", {"example.com"}))

    def test_only_explicit_parent_collapses(self):
        domains = {"ads.example.com", "a.ads.example.com", "b.example.com"}
        self.assertEqual(remove_redundant(domains), {"ads.example.com", "b.example.com"})


if __name__ == "__main__":
    unittest.main()
