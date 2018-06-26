from app import app, User, Message
import unittest


class UserZapIntegrationTestCase(unittest.TestCase):
    def test_users_index(self):
        """check for h1 in / route"""
        client = app.test_client()
        result = client.get('/')
        self.assertEqual(result.status_code, 302)

        result = client.get('/', follow_redirects=True)
        self.assertIn(b'<h2>Current user ZAP users:</h2>', result.data)

    def test_users_new(self):
        """tests for new"""
        client = app.test_client()
        result = client.get('/users/new')
        self.assertIn(b'<h2>Create New User</h2>', result.data)

    def test_users_create(self):
        """tests new user form handling"""
        client = app.test_client()
        result = client.post(
            '/users',
            data={
                'username': 'Jane',
                'password': 'Smith',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'img_url': 'http://some-image.com/'
            },
            follow_redirects=True)
        self.assertIn(b'<h2>Current user ZAP users:</h2>', result.data)

    def test_users_update(self):
        """test edit form and handling"""
        client = app.test_client()
        result = client.patch(
            "/users/9",
            data={
                'first_name': 'June',
                'last_name': 'Doe',
                'img_url': 'http://some-image.com/'
            },
            follow_redirects=True)
        self.assertIn(b'<h3>User info for June</h3>', result.data)

    def test_users_destroy(self):
        """test delete user"""
        client = app.test_client()
        # delete only works because user id was hard coded
        result = client.delete("/users/33", follow_redirects=True)
        self.assertEqual(result.status_code, 404)

        deleted_user = User.query.filter(User.id == 33).first()
        self.assertEqual(deleted_user, None)

    def test_messages_index(self):
        """test list of all messages for given user"""
        client = app.test_client()
        result = client.get('/users/1/messages')
        self.assertIn(b"<h2>Harry's Messages:</h2>", result.data)

    def test_messages_create(self):
        """test new message form handler"""
        client = app.test_client()
        result = client.post(
            'users/1/messages',
            data={'message_content': 'expelliarmus!'},
            follow_redirects=True)
        self.assertIn(b"<h2>Harry's Messages:</h2>", result.data)

    def test_messages_update(self):
        """test message update"""
        client = app.test_client()
        result = client.patch(
            '/messages/13?user_id=1',
            data={'message_content': 'EXPELLIARMUS!'},
            follow_redirects=True)
        self.assertIn(b"<h2>Harry's Messages:</h2>", result.data)

    def test_messages_destroy(self):
        """test delete message"""
        client = app.test_client()
        result = client.delete('/messages/14?user_id=1', follow_redirects=True)
        self.assertEqual(result.status_code, 404)
        deleted_message = Message.query.filter(Message.id == 14).first()
        self.assertEqual(deleted_message, None)

    def test_page_not_found(self):
        """tests 404 page"""
        client = app.test_client()
        result = client.get('/nevergoingtobearealroute')
        self.assertEqual(result.status_code, 404)

    def test_users_update_prepop(self):
        """ensure that edit message form is prepopulated"""
        client = app.test_client()
        # hard coded message id
        result = client.get('messages/26/edit')
        self.assertIn(b'value="testing for form prepop"', result.data)

    def test_user_create_notempty(self):
        """ensure a new user first/last is not null"""
        client = app.test_client()
        result = client.post(
            '/users/new',
            data={
                'first_name': '',
                'last_name': '',
                'img_url': 'http://www.image.com'
            },
            follow_redirects=True)
        self.assertRaises(ValueError, client.post, '/users/new', result.data)


if __name__ == '__main__':
    unittest.main()