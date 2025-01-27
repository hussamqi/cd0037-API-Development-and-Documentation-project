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
        categories = Category.query.all()
        if not categories:
            abort(404)
        return jsonify({'categories': {category.id: category.type for category in categories}})

    @app.route("/questions")
    def retrieve_questions():
        selection = Question.query.all()
        current_questions = paginate_questions(request, selection)
        if not current_questions:
            abort(404)
        current_category_ids = [question.get('category') for question in current_questions]
        categories = {category.id: category.type for category in Category.query.order_by(Category.id).all()}
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
            try:
                question.delete()
                return jsonify({
                    'success': True
                })
            except:
                abort(422)
        else:
            abort(404)

    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()
        if 'searchTerm' in body.keys():
            selection = Question.query.filter(Question.question.ilike(f'%{body.get("searchTerm")}%')).all()
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
            try:
                question = body.get('question')
                answer = body.get('answer')
                difficulty = body.get('difficulty')
                category = body.get('category')
                question_object = Question(question=question, answer=answer, difficulty=difficulty, category=category)
                question_object.insert()
                return jsonify({
                    'success': True
                })
            except:
                abort(422)

    @app.route("/categories/<int:category_id>/questions")
    def retrieve_questions_by_category(category_id):
        selection = Question.query.filter_by(category=category_id).all()
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
            abort(404)

    @app.route("/quizzes", methods=["POST"])
    def create_quiz():
        body = request.get_json()
        quiz_category = body.get('quiz_category').get('type')
        previous_questions = body.get('previous_questions')
        category = Category.query.filter(Category.type.ilike(f'%{quiz_category}%')).one_or_none()
        if category:
            questions = Question.query.filter_by(category=category.id).all()
        else:
            questions = Question.query.all()
        questions = [question.format() for question in questions if question.id not in previous_questions]
        if questions:
            return jsonify(
                {
                 'question': random.choice(questions),
                 })
        else:
            return jsonify(
                {
                 'question': False,
                 })

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    @app.errorhandler(500)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 500, "message": "Internal server error"}),
            500,
        )
    return app

