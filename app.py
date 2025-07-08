from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rpg.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, default=1)
    health = db.Column(db.Integer, default=100)

    items = db.relationship('Item', backref='owner', lazy=True)

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(120))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)

@app.route('/api/characters', methods=['POST'])
def create_character():
    data = request.json
    name = data.get('name')

    new_character = Character(name=name)
    db.session.add(new_character)
    db.session.commit()

    return jsonify({'id': new_character.id, 'name': new_character.name, 'level': new_character.level, 'health': new_character.health}), 201

@app.route('/api/characters/<int:character_id>/items', methods=['POST'])
def add_item(character_id):
    data = request.json
    name =data.get('name')
    description = data.get('description')

    item = Item(name=name, description=description, character_id=character_id)
    db.session.add(item)
    db.session.commit()

    return jsonify({'id': item.id, 'name': item.name, 'description': item.description}), 201

@app.route('/api/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get_or_404(character_id)
    items = [{'id': item.id, 'name': item.name, 'description': item.description} for item in character.items]

    return jsonify({
        'id': character.id,
        'name': character.name,
        'level': character.level,
        'health': character.health,
        'items': items
    })

if __name__ == '__main__':
    with app.app_context():    
        db.create_all()
    app.run(debug=True)