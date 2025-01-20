from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from app.models.user import User
from app.services.event_service import combined_search, get_event_image

main_bp = Blueprint("main", __name__)

@main_bp.route('/api/events/search', methods=['GET'])
@cross_origin()
def search_events():
    try:
        # Get query parameters
        params = request.args
        keyword = params.get('keyword')
        city = params.get('city')
        state_code = params.get('stateCode')
        start_date = params.get('startDate')
        end_date = params.get('endDate')
        segment = params.get('segment')

        # Perform the search
        result = combined_search(
            keyword=keyword,
            city=city,
            state_code=state_code,
            start_date=start_date,
            end_date=end_date,
            segment=segment,
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/api/events/image/<event_id>', methods=['GET'])
@cross_origin()
def fetch_event_image(event_id):
    try:
        result = get_event_image(event_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route("/register", methods=["POST"])
@cross_origin()
def register_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        required_fields = ['username', 'email', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            favorites=data.get('favorites', [])
        )

        success, result = user.register()
        if success:
            return jsonify({"message": "User registered successfully", "user": result}), 201
        return jsonify({"error": result}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route("/login", methods=["POST"])
@cross_origin()
def login_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        if not all(k in data for k in ("email", "password")):
            return jsonify({"error": "Missing email or password"}), 400

        success, result = User.login(data["email"], data["password"])
        if success:
            return jsonify({"message": "Login successful", "user": result}), 200
        return jsonify({"error": result}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route("/favorites/<user_id>", methods=["POST"])
@cross_origin()
def add_to_favorites(user_id):
    try:
        data = request.get_json()
        if not data or 'favorite' not in data:
            return jsonify({"error": "No favorite provided"}), 400

        success, message = User.add_to_favorites(user_id, data['favorite'])
        if success:
            return jsonify({"message": message}), 200
        return jsonify({"error": message}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route("/favorites/<user_id>", methods=["DELETE"])
@cross_origin()
def remove_from_favorites(user_id):
    try:
        data = request.get_json()
        if not data or 'favorite' not in data:
            return jsonify({"error": "No favorite provided"}), 400

        success, message = User.remove_from_favorites(user_id, data['favorite'])
        if success:
            return jsonify({"message": message}), 200
        return jsonify({"error": message}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500