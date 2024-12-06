from unittest import TestCase
from app import app
from flask import session

app.config['TESTING'] = True

class Sign_up_TestCase(TestCase):
    """Examples of integration tests: testing Flask app."""

    def test_signup_form(self):
        with app.test_client() as client:
            # can now make requests to flask via `client`
            resp = client.get('/signup')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            # self.assertIn('<h1>Color Form</h1>', html)

    def test_signup_post_form(self):
        with app.test_client() as client:
    # Test valid input
            resp = client.post('/signup',
                                data = {
                                    'first_name': 'John',
                                    'last_name': 'Doe',
                                    'email': 'john@example.com',
                                    'username': 'johndoe',
                                    'password': 'password123'
                                })
    
            assert resp.status_code == 200


class Lyrics_SearchTestCase(TestCase):
    def test_lyrics_search_form(self):
        with app.test_client() as client:
            # can now make requests to flask via `client`
            resp = client.get('/profile/1')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)


class InboxTestCase(TestCase):
    def test_inbox_redirect(self):
        with app.test_client() as client:
            res = client.get('/harleyquin2024/inbox')

            self.assertEqual(res.status_code, 302)
            
       

