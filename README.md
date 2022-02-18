# Udacitrivia

This Project is a simple trivia game where geeks can test their knowledge various categories 
like science, history, sports ..etc

## Basic functionality 

1. Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.


## Getting started

### Pre-requisites and Local Development

Developers using this project should already have Python3, pip and node installed on their local machines.
It's recommended to use virtual environment before installing requirements.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

create .env file in the backend directory, copy the content from .env.example file and update the values with your DB host, port, user, password, name

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 



#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 405: method not allowed
- 500: Internal server error

### Endpoints 
#### GET /categories
- General:
    - Returns a dictionary of categories where key is the category ID and value is the category name
- Sample: `curl http://127.0.0.1:5000/categories`
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }
}
```
#### GET /questions
- General:
    - Returns a dictionary of categories where key is the category ID and value is the category name
    - Returns a list of current categories in questions returned within the same request, each item a dictionary is where key is the category ID and value is the category name
    - Returns a list of question objects, and total number of questions
    - Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/books`
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": [
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "total_questions": 28
}
```

#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns Success = True if it was deleted successfully 
- `curl -X DELETE http://127.0.0.1:5000/questions/12`
```
{
    "success": true
}
```

#### POST /questions -Create a new question-
- General:
    - Creates a new question using the submitted question, answer, difficulty and category. Returns Success = True if it was created successfully 
    - `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Test Question from curl", "answer": "Test Answer form curl", "difficulty": 10, "category": 1}'`
```
{
    "success": true 
}
```

#### POST /questions -Create a new question-
- General:
    - Search for question(s) using the submitted searchTerm. 
    - Returns a list of current categories in questions returned within the same request, each item a dictionary is where key is the category ID and value is the category name
    - Returns a list of question objects, and total number of questions
    - Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1.
    - `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm" : "paint"}'`
```
{
  "current_category": [
    {
      "id": 2, 
      "type": "Art"
    }
  ], 
  "questions": [
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "total_questions": 2
}

```

#### GET /categories/{category_id}/questions
- General:
    - Returns a list of current categories in questions returned within the same request, each item a dictionary is where key is the category ID and value is the category name
    - Returns a list of question objects, and total number of questions
    - Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/categories/6/questions`
```
{
  "current_category": [
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ], 
  "total_questions": 2
}
```

#### POST /quizzes
- General:
    - Returns a new random question from a provided category or from the whole categories if no category provided. if all the questions were consumed previously and every question ID in the Database is presented in the previous_questions attribute it will return question = False.
    - `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category" : {"type": "sports", "id" : 6}, "previous_questions" : [10]}'`
```
{
  "question": {
    "answer": "Uruguay", 
    "category": 6, 
    "difficulty": 4, 
    "id": 11, 
    "question": "Which country won the first ever soccer World Cup in 1930?"
  }
}
```

## Deployment N/A

## Authors
Hossameldein Elfayoumi

## Acknowledgements 
The awesome team at Udacity and all the instructors.
