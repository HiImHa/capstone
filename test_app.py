
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db
import requests

class BookPublisher(unittest.TestCase):

    def setUp(self):
        # DATABASE_URL= "postgresql://postgres_deployment_example_60m2_user:xq0knbOVJUe5gdKUy6xmMhWPYsWhJ20J@dpg-ctodvj52ng1s73biauk0-a.oregon-postgres.render.com/postgres_deployment_example_60m2"
        # ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCIsImtpZCI6Ilo5RG1oQWI1Qm10Zm9DcnB5d2ZRUyJ9.eyJpc3MiOiJodHRwczovL2Rldi12czd5em96ZW0yaXNva3VjLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzcxMzIwZjU1M2ExZDBkNGY2M2EzYjAiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTczNTQ4MTUxMywiZXhwIjoxNzM1NDg4NzEzLCJqdGkiOiJjUDhnWVZnZGRROGNoQ0VDYWh1Zk41IiwiY2xpZW50X2lkIjoid1MwOEdtcTRHWjcwZ21Vdm5uTmJnaGQxTklEOEhjOVciLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YXV0aG9ycyIsImdldDpib29rcyJdfQ.cLata2oUihwKu5hTafrxCIDnsX2lKaj-Zmn_FGrP1h9a2UhCQ0re-WC-DQWFM6TZoEL-HHMZLT-jSMQNfbtIrDPcMz2IicMrGo3LWdYPS0zl_Qy_dmCZZjI5c4FSIIaEvQmD6TJhz4ZzmUBH0w_wm0A1YRu7P4UVkE4VG4dg1xxQamlb7dOW_SKkUMOj0DC_qNnLidYkutIWcxMDD6nLeEQknGBWOphiW-eCFev7cUqmLm2S02HaPRky9s-wByT-dMBI_tDVtCBEN2hE9GSEKvwd1AjcwvG1CRQdUWTECBsps7jA2UC65dEDEDNKrWU732hjVnD1O_BtC8XT3uimqw'
        # DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCIsImtpZCI6Ilo5RG1oQWI1Qm10Zm9DcnB5d2ZRUyJ9.eyJpc3MiOiJodHRwczovL2Rldi12czd5em96ZW0yaXNva3VjLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzcxMzJmYTU1M2ExZDBkNGY2M2E0MWQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTczNTQ4MTMyNSwiZXhwIjoxNzM1NDg4NTI1LCJqdGkiOiJlM3N3WGFlR2dtTHZmWnNjdU1Xd05qIiwiY2xpZW50X2lkIjoid1MwOEdtcTRHWjcwZ21Vdm5uTmJnaGQxTklEOEhjOVciLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YXV0aG9ycyIsImdldDpib29rcyIsInBhdGNoOmF1dGhvcnMiLCJwYXRjaDpib29rcyIsInBvc3Q6YXV0aG9ycyIsInBvc3Q6Ym9va3MiXX0.XhXzBI9M__B2nTBgX9eUr1oKhjxbmTHiiXnjnTtIpYN1OWAmyMe4iaXWigTBCM0S2o0y2GvL6Zp--HwYgqYlj5MYl5KlaMEWdp2p6L8LImMs46qT7Ij_rn-sPyIAn2U1Qz8ix8i0MwiU6-pFQuWAFvstRU7_eB0fy9YfAnMFWxSNNLh3arFVFRfzXM8vH5PMzfqCgufbVbnZZrWiELspfdwEH2JlTmUP8eT1DXgV4_0TdSCKlLVmSMCxX0fWDqZQpfNPACp9-xL0mt69bTKHAfawgolMyF26aU44Y3PqJjy2uzrBaBBYMY1CDvKqq1l5E2XDsEoTqrPxI_TCKtPYeQ'
        # PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCIsImtpZCI6Ilo5RG1oQWI1Qm10Zm9DcnB5d2ZRUyJ9.eyJpc3MiOiJodHRwczovL2Rldi12czd5em96ZW0yaXNva3VjLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzcxMTEyY2EyNzAwOTcwZjY4NmI4MmQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTczNTQ4MTQ1OCwiZXhwIjoxNzM1NDg4NjU4LCJqdGkiOiIxckVnVGQ0VHZlYWRDTnRldFlmdEhaIiwiY2xpZW50X2lkIjoid1MwOEdtcTRHWjcwZ21Vdm5uTmJnaGQxTklEOEhjOVciLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YXV0aG9ycyIsImRlbGV0ZTpib29rcyIsImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9ycyIsInBhdGNoOmJvb2tzIiwicG9zdDphdXRob3JzIiwicG9zdDpib29rcyJdfQ.wu-zTzW99TYGI8Jp47qTd4jdPswqH0z_7yHid4sRxSNxFU-c3byAQ9OPTyLxHstTeQLiLTsUVbNSzhzUiE6bXhyFiWwzw5PuSbw0Cp1O3F8L7Rkd7Jhu0ILTntiPNhtAmMnSev6JAm2GxdwsyWTz_r68Pnvc6CizO0gVHCHzeKHpfbxkiQybeQHU7bOw6mLpq6PrwTAkH8ZEW1B4KYYUMUtOKYeVPa4CKXGq2_1Ofx6vT424N3O1w1Hxpo76ALt3tEmTlGC5yzisn8EkhBAMIlxd0KTyxEVxfLkO9KxWLnTPbVIHswP0g26mxot4VYuna1gmq3ZdwSsMExmpRxUKmQ'

        self.api = "https://capstone-3lm8.onrender.com/"
        # self.api = "http://localhost:5000/"
        self.assistant_auth_header = {'Authorization':
                                      'Bearer ' + os.environ['ASSISTANT_TOKEN']}
        self.director_auth_header = {'Authorization':
                                     'Bearer ' + os.environ['DIRECTOR_TOKEN']}
        self.producer_auth_header = {'Authorization':
                                     'Bearer ' + os.environ['PRODUCER_TOKEN']}
        self.database_path = os.environ['DATABASE_URL']
        self.database_path = os.environ['DATABASE_URL']

        self.new_author_1 = {
            'name': "John Ronald Reuel Tolkien",
            'age': 81,
            'gender': 'Male'
        }

        self.new_author_2 = {
            'name': "Sir Arthur Ignatius Conan Doyle",
            'age': 71,
            'gender': 'Male'
        }

        self.new_author_missing_name = {
            'age': 23,
            'gender': "Female"
        }

        self.author_update_age = {
            'age': 23
        }

        self.new_book_1 = {
            'title': "The Lord of the Rings",
            'release': "1954-07-29"
        }

        self.new_book_2 = {
            'title': "Sherlock Holmes",
            'release': "1887-07-29"
        }

        self.new_book_3 = {
            'title': "The Thorn Birds",
            'release': "1977-11-14"
        }

        self.book_no_title = {
            'release': "2030-09-13"
        }

    def tearDown(self):
        pass

# Testcase for Author API
    # Test GET Authors (with RBAC)
    def test_assistant_get_authors(self):
        res = requests.get(self.api + '/authors',
                           headers=self.assistant_auth_header)
        print(f"status_code: {res.status_code}")
        self.assertEqual(res.status_code, 200)


    def test_director_get_authors(self):
        res = requests.get(self.api + '/authors',
                           headers=self.director_auth_header)
        self.assertEqual(res.status_code, 200)


    def test_producer_get_authors(self):
        res = requests.get(self.api + '/authors',
                           headers=self.producer_auth_header)
        self.assertEqual(res.status_code, 200)


    def test_unauthorized_get_authors(self):
        res = requests.get(self.api + '/authors')
        self.assertEqual(res.status_code, 401)


    # Test POST authors (with RBAC)
    def test_director_post_author(self):
        res = requests.post(self.api + '/authors',
                            json=self.new_author_1, headers=self.director_auth_header)
        self.assertEqual(res.status_code, 200)


    def test_producer_post_author(self):
        res = requests.post(self.api + '/authors',
                            json=self.new_author_2,
                            headers=self.producer_auth_header)
        data = res.json()
        self.assertEqual(res.status_code, 200)


    def test_error_422_post_author(self):
        res = requests.post(self.api + '/authors',
                            json=self.new_author_missing_name,
                            headers=self.director_auth_header)
        self.assertEqual(res.status_code, 422)

    def test_assistant_unauthorized_delete_authors(self):
        res = requests.post(
            self.api + '/authors', json=self.new_author_2, headers=self.assistant_auth_header)
        self.assertEqual(res.status_code, 401)

    # Test DELETE authors (with RBAC)
    def test_producer_delete_author(self):
        res = requests.post(self.api + '/authors',
                            json=self.new_author_2, headers=self.producer_auth_header)
        self.assertEqual(res.status_code, 200)


    def test_delete_author_not_found(self):
        res = requests.delete(self.api + '/authors/1000',
                              headers=self.producer_auth_header)
        self.assertEqual(res.status_code, 404)


    # Test PATCH authors (with RBAC)
    def test_director_patch_author(self):
        res = requests.patch(self.api + '/authors/1',
                            json=self.author_update_age, headers=self.director_auth_header)
        data = res.json()
        self.assertEqual(res.status_code, 200)


    def test_producer_patch_not_found_author(self):
        res = requests.patch(self.api + '/authors/1000',
                            json=self.author_update_age, headers=self.producer_auth_header)
        self.assertEqual(res.status_code, 404)


# ------------------------------------------------
# Testcase for Book API
    # Test GET books (with RBAC)
    def test_assistant_get_books(self):
        res = requests.get(self.api + '/books', headers=self.assistant_auth_header)
        self.assertEqual(res.status_code, 200)


    def test_director_get_books(self):
        res = requests.get(self.api + '/books', headers=self.director_auth_header)
        self.assertEqual(res.status_code, 200)


    def test_producer_get_books(self):
        res = requests.get(self.api + '/books', headers=self.producer_auth_header)
        self.assertEqual(res.status_code, 200)


    def test_unauthorized_get_books(self):
        res = requests.get(self.api + '/books')
        self.assertEqual(res.status_code, 401)

    # Test POST book (with RBAC)
    def test_producer_post_book(self):
        res = requests.post(self.api + '/books',
                            json=self.new_book_2, headers=self.producer_auth_header)
        self.assertEqual(res.status_code, 200)


    def test_director_no_authorized_post_book(self):
        res = requests.post(self.api + '/books',
                            json=self.new_book_1, headers=self.director_auth_header)
        self.assertEqual(res.status_code, 401)


    def test_error_422_post_book(self):
        res = requests.post(
            self.api + '/actors', json=self.book_no_title, headers=self.director_auth_header)
        self.assertEqual(res.status_code, 422)


    # Test DELETE books (with RBAC)
    def test_producer_delete_book(self):
        res = requests.post(self.api + '/books',
                            json=self.new_book_3, headers=self.producer_auth_header)
        self.assertEqual(res.status_code, 200)


    def test_delete_book_not_found(self):
        res = requests.delete(self.api + '/books/1000',
                              headers=self.producer_auth_header)
        self.assertEqual(res.status_code, 404)

    # Test PATCH books (with RBAC)
    def test_director_patch_book(self):
        res = requests.patch(self.api + '/books/1',
                            json=self.book_no_title, headers=self.director_auth_header)
        self.assertEqual(res.status_code, 200)

    def test_producer_patch_not_found_book(self):
        res = requests.patch(self.api + '/books/1000',
                            json=self.book_no_title, headers=self.producer_auth_header)
        self.assertEqual(res.status_code, 404)


# run 'python test_app.py' to start tests
if __name__ == "__main__":
    unittest.main()
