from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

# Database Configuration
DATABASE_URL = 'sqlite:///naruto.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# NarutoCharacter class definition
class NarutoCharacter(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    village = Column(String)
    powers = Column(String)

Base.metadata.create_all(engine)

@app.route('/add_character', methods=['POST'])
def add_character():
    data = request.get_json()
    name = data.get("name")
    village = data.get("village")
    powers = ",".join(data.get("powers", []))

    session = Session()
    character = NarutoCharacter(name=name, village=village, powers=powers)
    session.add(character)
    session.commit()
    session.close()

    return jsonify({"message": "Character added successfully"})

@app.route('/characters/<character_id>', methods=['GET'])
def get_character_info(character_id):
    session = Session()
    character = session.query(NarutoCharacter).filter_by(id=character_id).first()
    session.close()

    if character:
        return jsonify({
            "name": character.name,
            "village": character.village,
            "powers": character.powers.split(',')
        })
    return jsonify({"message": "Character not found"}), 404

@app.route('/characters', methods=['GET'])
def get_all_characters():
    session = Session()
    characters = session.query(NarutoCharacter).all()
    session.close()

    character_list = []
    for character in characters:
        character_list.append({
            "id": character.id,
            "name": character.name,
            "village": character.village,
            "powers": character.powers.split(',')
        })

    return jsonify(character_list)

@app.route('/characters/<character_id>', methods=['PATCH'])
def update_character(character_id):
    session = Session()
    character = session.query(NarutoCharacter).filter_by(id=character_id).first()

    if character:
        data = request.get_json()
        if "name" in data:
            character.name = data["name"]
        if "village" in data:
            character.village = data["village"]
        if "powers" in data:
            character.powers = ",".join(data["powers"])

        session.commit()
        session.close()

        return jsonify({"message": "Character updated successfully"})
    else:
        return jsonify({"message": "Character not found"}), 404

@app.route('/characters/<character_id>', methods=['DELETE'])
def delete_character(character_id):
    session = Session()
    character = session.query(NarutoCharacter).filter_by(id=character_id).first()

    if character:
        session.delete(character)
        session.commit()
        session.close()
        return jsonify({"message": "Character deleted successfully"})
    else:
        session.close()
        return jsonify({"message": "Character not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
