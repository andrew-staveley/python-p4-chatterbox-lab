from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.all()]
        return make_response(messages, 200)
    elif request.method == 'POST':
        new_message_json = request.get_json()
        new_message = Message(
            body=new_message_json['body'],
            username=new_message_json['username']
        )
        db.session.add(new_message)
        db.session.commit()
        message_dict = new_message.to_dict()
        return make_response(message_dict, 201) 

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if request.method == 'PATCH':
        patch_messsage_json = request.get_json()
        setattr(message, 'body', patch_messsage_json['body'])
        db.session.add(message)
        db.session.commit()
        message_dict = message.to_dict()
        return make_response(message_dict, 200)
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        response_body = {
            "delete_successful": True,
            "message": "Message deleted."
        }
        return make_response(response_body, 200)
    return response

if __name__ == '__main__':
    app.run(port=5555)
