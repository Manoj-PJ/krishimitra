from flask import Blueprint, request, jsonify
from services.ai_service import AIService

satellite_routes = Blueprint('satellite', __name__)

@satellite_routes.route('/analyze', methods=['POST'])
def analyze_satellite_data():
    data = request.json
    recommendation = AIService.predict_irrigation(
        data['soil_moisture'],
        data['weather']
    )
    return jsonify({"recommendation": recommendation})