from flask import Flask, render_template, send_from_directory
from config import Config
from models import db, Admin
from routes import auth_bp, opp_bp
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'serve_index'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(opp_bp)

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/admin.css')
def serve_css():
    return send_from_directory('static/css', 'admin.css')

@app.route('/admin.js')
def serve_js():
    return send_from_directory('static/js', 'admin.js')

import webbrowser
from threading import Timer

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Automatically open the browser
    Timer(1.5, lambda: webbrowser.open('http://127.0.0.1:8000/')).start()
    
    app.run(debug=True, port=8000, use_reloader=False)
