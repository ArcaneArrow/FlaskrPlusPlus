import os
import app as flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    def test_messages(self):
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            category='A category'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data
        assert b'A category' in rv.data

    def delete_entry(self, id_num):
        return self.app.post("/delete", data=dict(id=id_num), follow_redirects=True)

    def edit_entry(self, id_num):
        return self.app.post("/edit", data=dict(id=id_num))

    def update_entry(self, id_num, title_text, category_text, text_text):
        return self.app.post("/update", data=dict(
            id=id_num,
            title=title_text,
            category=category_text,
            text=text_text
        ), follow_redirects=True)

if __name__ == '__main__':
    unittest.main()