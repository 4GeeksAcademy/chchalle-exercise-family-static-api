import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")
jackson_family.add_member({
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7,13,22]
})
jackson_family.add_member({
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10,14,3]
})
jackson_family.add_member({
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
})

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_family_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def add_member_app():
    body = request.get_json()

    if not body:
        return jsonify({"message": "The request body is null"}), 400
    if 'first_name' not in body:
        return jsonify({"message": "You need to specify the first_name"}), 400
    if 'age' not in body:
        return jsonify({"message": "You need to specify the age"}), 400
    if 'lucky_numbers' not in body:
        return jsonify({"message": "You need to specify the lucky_numbers"}), 400

    added_member = jackson_family.add_member(body)
    
    return jsonify(added_member), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member_app(member_id):
    if member_id < 0:
        return jsonify({"message": "Invalid member_id"}), 400

    success = jackson_family.delete_member(member_id)
    if not success:
        return jsonify({"message": "Member not found"}), 404

    return jsonify({"done": True}), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member_app(member_id):
    family_member = jackson_family.get_member(member_id)
    if family_member is None:
        return jsonify({"message": "Member not found"}), 404
    
    return jsonify({
        "first_name": family_member["first_name"],  
        "id": family_member["id"],            
        "age": family_member["age"],
        "lucky_numbers": family_member["lucky_numbers"]
    }), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
