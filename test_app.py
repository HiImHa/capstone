
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
        # ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCIsImtpZCI6Ilo5RG1oQWI1Qm10Zm9DcnB5d2ZRUyJ9.eyJpc3MiOiJodHRwczovL2Rldi12czd5em96ZW0yaXNva3VjLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzcxMzIwZjU1M2ExZDBkNGY2M2EzYjAiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTczNTQ5MTUyMiwiZXhwIjoxNzM1NDk4NzIyLCJqdGkiOiJzYm5FYkVHNWhMVGVEcmtZRk54ODVWIiwiY2xpZW50X2lkIjoid1MwOEdtcTRHWjcwZ21Vdm5uTmJnaGQxTklEOEhjOVciLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YXV0aG9ycyIsImdldDpib29rcyJdfQ.IG1BU4nIxUo1R2XOSGs_SPCBnIA9niNg-8TRhaCbx8ofjdKVTgOoPX1M7NnI4-B9lpIP32Nhx_XaHvtibncSGLaXFE-cui9BU6TFAcfb4efxQNzPgHuUiwH8UcU0C3gVQUJSPveC1NURMKYkkk8-8UXwR6gk2Zu0cThYnbXA7ci632EHI_CVZbBhRxSYpRovn9NCEv9NpxRHzT44odWMvIEgDPD2xOOWUceWTx4abC-Kk_APu1O_jABSAMFSvAp69CtOAdjr7vnRID1GbevIf8gh__-q3rUkrrQIHhDBrWKIrhmfqvXRf4y1iamNFYb4_vv0V106fv0VTZm4b0Ed5A'
        # DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCIsImtpZCI6Ilo5RG1oQWI1Qm10Zm9DcnB5d2ZRUyJ9.eyJpc3MiOiJodHRwczovL2Rldi12czd5em96ZW0yaXNva3VjLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzcxMzJmYTU1M2ExZDBkNGY2M2E0MWQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTczNTQ5MTQ1OSwiZXhwIjoxNzM1NDk4NjU5LCJqdGkiOiIzWGtQd0g4b1BoQk5haWRNdDhwaE5ZIiwiY2xpZW50X2lkIjoid1MwOEdtcTRHWjcwZ21Vdm5uTmJnaGQxTklEOEhjOVciLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YXV0aG9ycyIsImdldDpib29rcyIsInBhdGNoOmF1dGhvcnMiLCJwYXRjaDpib29rcyIsInBvc3Q6YXV0aG9ycyIsInBvc3Q6Ym9va3MiXX0.NEPYG6dO9rMuEDWIn0Agv9fSMTM7Vkz2JZk73JsNmRIwdiMCWvhlMpYPu2JheI5XS5DlddD1jVxDCrPG9M16i7K8CPxYpJCv1pgnTVkTxv6rQ_nXXm1QbKRxS6DdTQ_y4X6jmOXKvVsWu85VkjwW49OorJOUJ_dHHHzxH7yFX0P97xBEQ0R8F566TLVanf5Avvh4REQAwmvLpYvinZW3fUg8L62bS4BKry1lo3LdXUoE_TN60hbo8gPzlgiURSkj3CxMMyJz25fkQFdnz5YI2tUCzVC913ASQ7ADUHcdBxj5xRcO1CtPlv2rUu5mvIMNUdMSemiNU_xoS6IxNu4ScA'
        # PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCIsImtpZCI6Ilo5RG1oQWI1Qm10Zm9DcnB5d2ZRUyJ9.eyJpc3MiOiJodHRwczovL2Rldi12czd5em96ZW0yaXNva3VjLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzcxMTEyY2EyNzAwOTcwZjY4NmI4MmQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTczNTQ5MTU3MSwiZXhwIjoxNzM1NDk4NzcxLCJqdGkiOiJodGdWcVhrRFROeTM4Rjc3N2YzQkJaIiwiY2xpZW50X2lkIjoid1MwOEdtcTRHWjcwZ21Vdm5uTmJnaGQxTklEOEhjOVciLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YXV0aG9ycyIsImRlbGV0ZTpib29rcyIsImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9ycyIsInBhdGNoOmJvb2tzIiwicG9zdDphdXRob3JzIiwicG9zdDpib29rcyJdfQ.C3jhbPxQh9vLT4PrA6mov0H7HOcEJ5KCjlDGdBOTFlSPxpDbS5W2IqpSP4htvFboTMPBMDLgJ_byKQYoX-KmHNXWeKi-w5Qr9gVS7bdEdhCvw7vEIV4OT1uskuAM0yHYWWZ3dDHM5Bzb1vxD5rLwH-sUZcEZ2pzV5dCfc599v3xjfk4TPC4Lvf2UtdPXG-dldYHD5r00WAmhlQEp99xll9GWNEc2U_1cowiJUENEtsDmLj1iUAMuFrMUM1b61tRmwUMRSIXLnqjqpV94-2ZDwv4pqh3kjp2O79MVFAPStLcyGZI91tzBmmen2QD2XB_gIy-fs1OfSa7hLMYDP21Gjw'

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
