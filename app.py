from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Import and register blueprints
from routes.main_routes import main_bp
from routes.upload_routes import upload_bp
from routes.rag_routes import rag_bp

app.register_blueprint(main_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(rag_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
