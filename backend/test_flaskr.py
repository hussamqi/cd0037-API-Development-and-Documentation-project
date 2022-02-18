import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, USERNAME, PASSWORD, PORT, HOST
TEST_DB_NAME = 'trivia_test'

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path =  f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{TEST_DB_NAME}'
        setup_db(self.app, self.database_path)
        self.new_question = {'question': 'Test Question',
                             'answer': 'Test Answer',
                             'difficulty': 5,
                             'category': 1}
        self.new_quiz = {'quiz_category' : {'type': 'sports', 'id' : 6},
                         'previous_questions' : []}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["categories"])
        self.assertTrue(len(data["categories"]))

    def test_405_get_categories_with_wrong_request(self):
        res = self.client().post("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["current_category"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=9999")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_question_search_with_results(self):
        res = self.client().post("/questions", json={"searchTerm": "paint"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["total_questions"])
        self.assertEqual(len(data["questions"]), 2)
        self.assertTrue(data["current_category"])
        self.assertEqual(len(data["current_category"]), 1)

    def test_get_question_search_without_results(self):
        res = self.client().post("/questions", json={"searchTerm": "bhjabdjkhasvbk"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(len(data["questions"]), 0)
        self.assertEqual(len(data["current_category"]), 0)

    def test_delete_question(self):
        res = self.client().delete("/questions/6")
        data = json.loads(res.data)
        book = Question.query.filter(Question.id == 6).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(book, None)

    def test_404_if_question_does_not_exist(self):
        res = self.client().delete("/questions/9999")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post("/questions/45", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_retrieve_questions_by_category(self):
        res = self.client().get("/categories/6/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["current_category"]))

    def test_404_sent_requesting_beyond_valid_category_id(self):
        res = self.client().get("/categories/99999/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_create_quiz(self):
        res = self.client().post("/quizzes", json=self.new_quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])
        self.assertEqual(len(data["question"].keys()), 5)

    def test_requesting_beyond_available_questions_in_create_quiz(self):
        questions_ids = [ question[0] for question in Question.query.with_entities(Question.id).all()]
        self.new_quiz['previous_questions'] = questions_ids
        res = self.client().post("/quizzes", json=self.new_quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(data["question"])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()