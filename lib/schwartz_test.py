import unittest

from schwartz import is_valid_short_form, has_letter, has_capital, extract_pairs


class SchwartzTest(unittest.TestCase):

    def test_is_valid_short_form(self):
        self.assertTrue(is_valid_short_form("abc"))
        self.assertTrue(is_valid_short_form("1abc"))
        self.assertTrue(is_valid_short_form("(abc"))
        self.assertTrue(is_valid_short_form("abc"))
        self.assertFalse(is_valid_short_form("123"))
        self.assertFalse(is_valid_short_form("(123"))

    def test_has_letter(self):
        self.assertTrue(has_letter("abc"))
        self.assertTrue(has_letter("123a"))
        self.assertFalse(has_letter("123"))

    def test_has_capital(self):
        self.assertTrue(has_capital("Abc"))
        self.assertTrue(has_capital("ABC"))
        self.assertFalse(has_capital("abc"))
        self.assertFalse(has_capital("123"))

    def test_extract_pairs(self):
        sentence = """
            Three aspects of the involvement of tumor necrosis factor 
            in human immunodeficiency virus (HIV) pathogenesis were examined.
        """
        pairs = extract_pairs(sentence)
        self.assertListEqual(pairs, [{"acronym": "HIV", "definition": "human immunodeficiency virus"}])

    def test_best_long_form(self):
        self.assertTrue(True)

    def test_match_pair(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
