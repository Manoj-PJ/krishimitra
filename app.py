from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize extensions
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///krishimitra.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    
    # Initialize extensions with app
    db.init_app(app)
    CORS(app)
    
    # Import and register blueprints here if using
    # from routes.auth import auth_blueprint
    # app.register_blueprint(auth_blueprint)
    
    return app

app = create_app()

# Define models
class Farmer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    state = db.Column(db.String(50))
    district = db.Column(db.String(50))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Routes
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'mobile' not in data or 'password' not in data:
        return jsonify({'success': False, 'message': 'Invalid input'}), 400
    
    farmer = Farmer.query.filter_by(mobile=data['mobile']).first()
    
    if not farmer or not farmer.check_password(data['password']):
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'farmer': {
            'id': farmer.id,
            'name': farmer.name,
            'mobile': farmer.mobile
        }
    })

def initialize_database():
    with app.app_context():
        db.create_all()
        
        # Create test user if doesn't exist
        if not Farmer.query.filter_by(mobile="9876543210").first():
            test_user = Farmer(
                name="Testing now",
                mobile="324243522334",
                state="Maharashtra",
                district="Tumkauru"
            )
            test_user.set_password("test123")
            db.session.add(test_user)
            db.session.commit()

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)