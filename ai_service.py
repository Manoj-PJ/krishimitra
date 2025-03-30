import pandas as pd
from sklearn.ensemble import RandomForestClassifier

class AIService:
    @staticmethod
    def predict_irrigation(soil_moisture, weather_data):
        # Example: Simple irrigation recommendation
        if soil_moisture < 30:
            return "Irrigate now - soil is dry"
        elif soil_moisture > 80:
            return "No irrigation needed - soil is wet"
        else:
            return "Monitor soil - irrigation may be needed soon"