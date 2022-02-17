import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/categories")
    def retrieve_categories():
        return jsonify({'categories': [category.type for category in Category.query.all()]})

    @app.route("/questions")
    def retrieve_questions():
        selection = Question.query.all()
        current_questions = paginate_questions(request, selection)
        current_category_ids = [question.get('category') for question in current_questions]
        categories = [category.type for category in Category.query.all()]
        current_category = [category.format() for category in
                            Category.query.filter(Category.id.in_(current_category_ids)).all()]
        return jsonify(
            {'questions': current_questions,
             'total_questions': len(selection),
             'categories': categories,
             'current_category': current_category
             })

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.filter_by(id=question_id).one_or_none()
        if question:
            question.delete()
            return jsonify({
                'success': True
            })

    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()
        if 'searchTerm' in body.keys():
            selection = Question.query.filter(Question.question.ilike(f'%{body.get("searchTerm")}%')).all()
            if selection:
                questions = paginate_questions(request, selection)
                current_category_ids = [question.get('category') for question in questions]
                current_category = [category.format() for category in
                                    Category.query.filter(Category.id.in_(current_category_ids)).all()]
                return jsonify(
                    {'questions': questions,
                     'total_questions': len(selection),
                     'current_category': current_category
                     })
        else:
            question = body.get('question')
            answer = body.get('answer')
            difficulty = body.get('difficulty')
            category = int(body.get('category')) + 1
            question_object = Question(question=question, answer=answer, difficulty=difficulty, category=category)
            question_object.insert()
            return jsonify({
                'success': True
            })

    @app.route("/categories/<int:category_id>/questions")
    def retrieve_questions_by_category(category_id):
        selection = Question.query.filter_by(category=category_id+1).all()
        if selection:
            questions = paginate_questions(request, selection)
            current_category_ids = [question.get('category') for question in questions]
            current_category = [category.format() for category in
                                Category.query.filter(Category.id.in_(current_category_ids)).all()]
            return jsonify(
                {'questions': questions,
                 'total_questions': len(selection),
                 'current_category': current_category
                 })

    @app.route("/quizzes", methods=["POST"])
    def get_quizzes():
        body = request.get_json()
        quiz_category = body.get('quiz_category').get('type')
        previous_questions = body.get('previous_questions')
        category = Category.query.filter(Category.type.ilike(f'%{quiz_category}%')).one_or_none()
        if category:
            questions = [question.format() for question in Question.query.filter_by(category=category.id).all()]
        else:
            questions = [question.format() for question in Question.query.all()]
        questions = [question for question in questions if question.get('id') not in previous_questions]
        if questions:
            return jsonify(
                {
                 'question': random.choice(questions),
                 })
        else :
            return jsonify(
                {
                 'question': False,
                 })



    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

