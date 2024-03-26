from flask import Flask, render_template, request, jsonify
from models.User import db, Article
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATTIONS'] = False
api = Api(app)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/welcome', methods=['GET'])
def welcome_page():
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


@app.route('/find_user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):

    user = Article.query.get(user_id)

    if user:
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        }), 200
    return jsonify({'error': 'Користувача з таким id нема'}), 404


@app.route('/user/remove_user/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):

    user = Article.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({
            'message': 'Видалено'
        }), 200
    return jsonify({'error': 'Користувача по id нема'}), 404


@app.route('/user/put_user/<int:user_id>', methods=['PUT'])
def put_user(user_id):
    user = Article.query.get(user_id)

    if user:

        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')

        article = Article(username=username, email=email, password=password)

        try:
            db.session.insert(article)
            db.session.commit()
            return "Дані змінено!!"
        except Exception as e:
            return f"Помилка! {str(e)}"
    return jsonify({'error': 'Користувача з таким id нема'})


if __name__ == '__main__':
    app.run(debug=True)

