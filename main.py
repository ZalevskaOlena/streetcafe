from flask import Flask, render_template, request, jsonify
from models.User import db, Article
from flask_restful import Api
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User.db'
app.config['SQLALCHEMY_TRACK_MODIFICATTIONS'] = False
api = Api(app)
db.init_app(app)


@app.route('/welcome', methods=['GET'])
def indexget():
    return render_template('welcome.html')


@app.route('/registration', methods=['POST'])
def registration():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    article = Article(username=username, email=email, password=password)

    try:
        db.session.add(article)
        db.session.commit()
        return "Успіх!"
    except Exception as e:
        return f"Виникла помилка! {str(e)}"


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Article.query.get(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        }), 200
    else:
        return jsonify({'error': 'Користувача з таким id нема'}), 404


@app.route('/user/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Article.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Видалено'}), 200
    else:
        return jsonify({'error': 'Користувача по id нема'}), 404


@app.route('/welcome/jsonn', methods=['POST'])
def json_post():
    data = request.json
    if data:
        print(data)
        return jsonify({"message": "супер"}), 200
    else:
        return jsonify({"message": "не супер"}), 400


if __name__ == '__main__':
    app.run(debug=True)
