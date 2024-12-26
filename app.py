# app.py
from flask import Flask, render_template
from config import Config
from extensions import db, login_manager, mail
from models import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        from auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        from admin import admin as admin_blueprint
        app.register_blueprint(admin_blueprint, url_prefix='/admin')
        
        db.create_all()

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)