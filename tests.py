import unittest
from unittest.mock import patch
import datetime

from peewee import*
from playhouse.test_utils import test_database

from functions import selected_entry, border_finder, edit_delete
from functions import get_name, get_time, get_notes, get_date, table_or_page
from functions import new_database_entry, view_table, page_through
from run import Entry, menuloop

test_db = SqliteDatabase(':memory:')
now = datetime.datetime.now()
class TestMyFunctions(unittest.TestCase):
    def test_get_date(self):
        with unittest.mock.patch('builtins.input', side_effect=['asdfasdf',
                                                                '',
                                                                '5/23/2017'
                                                               ]):
            self.assertIsInstance(get_date("Text"), datetime.date)

    def test_get_time(self):
        with unittest.mock.patch('builtins.input', side_effect=['asdfasdf',
                                                                '',
                                                                '5:5:5'
                                                               ]):
            self.assertIsInstance(get_time("Text"), datetime.time)

    def test_get_name(self):
        with unittest.mock.patch('builtins.input', side_effect=[('g' * 323),
                                                                '',
                                                                '',
                                                                '',
                                                                'Jeeno'
                                                               ]):
            self.assertLessEqual(len(get_name("Text")), 255)

    def test_get_notes(self):
        with unittest.mock.patch('builtins.input', side_effect=['blah blah']):
            self.assertGreater(len(get_notes()), 0)

    def test_border_finder(self):
        self.assertGreater(border_finder(5, 10), -1)

class TestEntryDatabase(unittest.TestCase):
    def test_database_related_functions(self):
        with test_database(test_db, [Entry]):
            with unittest.mock.patch('builtins.input',
                    side_effect=['05/23/2017',
                                 'Joe Swanson',
                                 'Testing1',
                                 '05:05:05',
                                 'More generic words.',
                                 'Y'
                                ]):
                new_database_entry(Entry)
            with unittest.mock.patch('builtins.input',
                    side_effect=['05/23/2017',
                                 'Joe Swanson',
                                 'Testing1',
                                 '05:05:05',
                                 'More generic words.',
                                 'Y'
                                ]):
                new_database_entry(Entry)
            with unittest.mock.patch('builtins.input',
                    side_effect=['05/23/2017',
                                 'Joe Swanson',
                                 'Testing1',
                                 '05:05:05',
                                 'More generic words.',
                                 'Y'
                                ]):
                new_database_entry(Entry)
                self.assertTrue(Entry.select())
            with unittest.mock.patch('builtins.input',
                    side_effect=['1',
                                 ''
                                ]):
                table_or_page(Entry.select()) # also tests table
            with unittest.mock.patch('builtins.input',
                    side_effect=['2',
                                 '1',
                                 '2',
                                 '4'
                                ]):
                table_or_page(Entry.select()) # also tests page through
            with unittest.mock.patch('builtins.input',
                    side_effect=['1',
                                 '3',
                                 '2',
                                 'Y',
                                 ''
                                ]):
                table_or_page(Entry.select()) # deleting an entry
            with unittest.mock.patch('builtins.input',
                    side_effect=['1',
                                 '1',
                                 '05/23/2017',
                                 '6'
                                ]):
                edit_delete(Entry.select().get()) # edit
            with unittest.mock.patch('builtins.input',
                    side_effect=['asfd',
                                 '',
                                 '3'
                                ]):
                edit_delete(Entry.select().get()) # test edit error
            with unittest.mock.patch('builtins.input',
                    side_effect=['asfd',
                                 '',
                                 '7'
                                ]):
                menuloop() # menuloop test error and quit
            with unittest.mock.patch('builtins.input',
                    side_effect=['6',
                                 'safasdf',
                                 '',
                                 '7'
                                ]):
                menuloop() # menuloop tests search by term
            with unittest.mock.patch('builtins.input',
                    side_effect=['3',
                                 '1',
                                 '05/23/1993',
                                 '',
                                 '7'
                                ]):
                menuloop() # menuloop tests search by specific date
            with unittest.mock.patch('builtins.input',
                    side_effect=['3',
                                 '2',
                                 '05/23/1993',
                                 '05/24/1993',
                                 '',
                                 '7'
                                ]):
                menuloop() # menuloop tests search by date range
            with unittest.mock.patch('builtins.input',
                    side_effect=['4',
                                 'robert',
                                 '',
                                 '7'
                                ]):
                menuloop() # menuloop tests search by username
            with unittest.mock.patch('builtins.input',
                    side_effect=['5',
                                 '01:01:01',
                                 '',
                                 '7'
                                ]):
                menuloop() # menuloop tests search by time spent





if __name__ == '__main__':
    unittest.main()
