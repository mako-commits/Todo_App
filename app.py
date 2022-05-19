from flask import Flask, render_template,request,redirect,url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
import sys


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Pass123$@localhost:5432/todoapp'
#link SQLAlchemy to flask app
db = SQLAlchemy(app)

#cretae todo model
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    #

    #debugging statement
    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

#sync model with database
db.create_all()

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body={}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description']  = todo.description 
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        return jsonify(body)


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html', data= Todo.query.order_by('id').all())