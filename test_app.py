
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
        # ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCIsImtpZCI6Ilo5RG1oQWI1Qm10Zm9DcnB5d2ZRUyJ9.eyJpc3MiOiJodHRwczovL2Rldi12czd5em96ZW0yaXNva3VjLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzcxMzIwZjU1M2ExZDBkNGY2M2EzYjAiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTczNTQ3MTY5NywiZXhwIjoxNzM1NDc4ODk3LCJqdGkiOiJjVHlXTTZGeGhkTjVaNlY1Z0RFTE1uIiwiY2xpZW50X2lkIjoid1MwOEdtcTRHWjcwZ21Vdm5uTmJnaGQxTklEOEhjOVciLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YXV0aG9ycyIsImdldDpib29rcyJdfQ.yTt2JjLrj1pAQUIrxkke6Sm3IPHnuu8of7M0xZ-N-rPafFzqvLbptAhfuOUyhLQ_ftu2MASFpBs7LY6xMzPT2SiSo-PzUhvT0tFdSOIX1R2_vHLKlwh92tbPPDW4AYU1v3JfjmfDXwBNMZgp793MRQHNDXZVqxij0QchmCax8e3ra6sDY28qXwgBAxfDaRiMyRrwvoByvHSab_Nc16DG9MxXe9MLCO1_I7ebsAgApCyxULbKHxalpQsAu93Okz74hQv-6VPtZYIEDlXpRfXxMiujRyJPNbqVJFU4wqGpta8_kT6SgEbkcIojUDjs3uhZi-hy4_xHL6lv9a6r4JqUYg'
        # DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCIsImtpZCI6Ilo5RG1oQWI1Qm10Zm9DcnB5d2ZRUyJ9.eyJpc3MiOiJodHRwczovL2Rldi12czd5em96ZW0yaXNva3VjLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzcxMzJmYTU1M2ExZDBkNGY2M2E0MWQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTczNTQ3MTk0MywiZXhwIjoxNzM1NDc5MTQzLCJqdGkiOiIyZmQ2S1BuZ1ZhV29tbmhBTjVnbWVtIiwiY2xpZW50X2lkIjoid1MwOEdtcTRHWjcwZ21Vdm5uTmJnaGQxTklEOEhjOVciLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YXV0aG9ycyIsImdldDpib29rcyIsInBhdGNoOmF1dGhvcnMiLCJwYXRjaDpib29rcyIsInBvc3Q6YXV0aG9ycyIsInBvc3Q6Ym9va3MiXX0.ahmGpjMB1gbmGjJ47Jrlaww0LYI_hteARb2J_N8nFA7GLxD1cfGZK5mbxK_L0um4YMYDo-0a1gzcWU_G9tXI0BaJbe_thfUSPEv_UaS5A-IC22GXdJULBwdxX7BujzMUlN0mfmGn6JwHj-3MO7jY73iE1TD2EdQmicGQ1V0x9rrYzG44gaHFY2FsF6pEK9QP65SsfTIBfuIoiumyp0Wx6EIEud6QRTNffUsdJGAyu8nV9IpND3-JPL4-2A7zxDVMJiGYfykZ-YmkB8fq1f1STxhiE1CtkHuabqan-M5CojhIVS1490dTMq4o-6aK0fsFtXc-XmbVYClLxqbZxrpc0Q'
        # PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCIsImtpZCI6Ilo5RG1oQWI1Qm10Zm9DcnB5d2ZRUyJ9.eyJpc3MiOiJodHRwczovL2Rldi12czd5em96ZW0yaXNva3VjLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzcxMTEyY2EyNzAwOTcwZjY4NmI4MmQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTczNTQ3MDI4MSwiZXhwIjoxNzM1NDc3NDgxLCJqdGkiOiI5cUM1QWZwWkU3RjFlaUtONmJjTUhuIiwiY2xpZW50X2lkIjoid1MwOEdtcTRHWjcwZ21Vdm5uTmJnaGQxTklEOEhjOVciLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YXV0aG9ycyIsImRlbGV0ZTpib29rcyIsImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9ycyIsInBhdGNoOmJvb2tzIiwicG9zdDphdXRob3JzIiwicG9zdDpib29rcyJdfQ.XeoB0m2-Q2hkN1TWwC-z93a0DXpNEY1oyHu6e93J_UosyU6T4YUqQZj9xpSd2sdRzfFe3c0_FdwFjYjHiJrVxO0Bb4FrOe3kv5uz7AS1Pm3nmAJ2505BbWjq7z-SxaGy6RHezM0iLZ5oBpOaQzgnxFW9EoY9ru9Vm443dCIRH297Nm-JypPYm61nkgFwd5gKbqTpM32DZNLlxbuh95ci3jh_IZAtc2YrvCAJDY7IK3Y_e6bglgx_a3vek86ljGJ3itEd36_ewmOxcNZ2NAeAUmAtqz3JhJeEejvZEWp2id7csQApaLG4ICT8uV3ietnbRfE99cSATY5x6WaAKIq7hQ'

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
