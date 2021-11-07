import unittest

from main import find_all_info, add_new_person, remove_doc_from_shelf

class unitTest(unittest.TestCase):
    def test_find_all_info(self):
        self.assertEqual(find_all_info([{"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"}]),
                         [["passport", "2207 876234", "Василий Гупкин"]])

    def test_add_new_person(self):
        docs = [{"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"}]
        direct = {'1': ['2207 876234']}
        doc = {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"}
        shelf_number = "1"
        self.assertEqual(add_new_person(docs, direct, doc, shelf_number), {'1': ['2207 876234', '11-2']})

    def test_remove_doc_from_shelf(self):
        self.assertEqual(remove_doc_from_shelf("11-2"), 'yes')

if __name__ == '__main__':
    unittest.main()