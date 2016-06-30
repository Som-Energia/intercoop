import unittest
from . import portal
from . import peerdatastorage

class Portal_Test(unittest.TestCase):
    index_html="""<html>
            <head></head>
            <body>Lista de peers</body>
            </html>
            """

    def setUp(self):
        app = portal.Portal("testportal").app
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index(self):
        self.assertEqual(self.index_html,self.client.get("/").data.decode('utf-8'))
