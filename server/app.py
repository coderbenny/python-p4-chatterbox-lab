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

@app.route('/messages', methods=['GET','POST'])
def messages():
    
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        
        messages_list = [message.to_dict() for message in messages]
        return jsonify(messages_list), 200
    
    elif request.method == 'POST':
        data=request.json
        username = data.get("username")
        body = data.get("body")
        
        if username is None or body is None:
            return jsonify({"error": "Missing required fields"}), 400
        
        new_message = Message(username=username,body=body)
        
        db.session.add(new_message)
        db.session.commit()
        
        return jsonify(new_message.to_dict()), 201
        
@app.route('/messages/<int:id>', methods=['GET','PATCH','DELETE'])
def messages_by_id(id):
    
    if request.method == 'GET':
        message = Message.query.filter_by(id=id).first()
        
        if not message:
            return jsonify({"error": "Message not found"}), 404

        return jsonify(message.to_dict()), 200
    
    elif request.method == 'PATCH':
        message = Message.query.filter_by(id=id).first()

        if not message:
            return jsonify({"error": "Message not found"}), 404
        
        data = request.json
        for attr, value in data.items():
            setattr(message, attr, value)
        
        db.session.commit()
        
        return jsonify(message.to_dict()), 200
    
    elif request.method == 'DELETE':
        message = Message.query.filter_by(id=id).first()

        if not message:
            return jsonify({"error": "Message not found"}), 404

        db.session.delete(message)
        db.session.commit()
        
        return jsonify({"deleted":"Message deleted succesfully"})            
    
if __name__ == '__main__':
    app.run(port=5555)
