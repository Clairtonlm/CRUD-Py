# models.py
from extensions import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import re

class User(UserMixin, db.Model):
    """Modelo de usuário com recursos de segurança aprimorados"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    login_attempts = db.Column(db.Integer, default=0)
    reset_token = db.Column(db.String(100), unique=True)
    reset_token_expiry = db.Column(db.DateTime)

    @staticmethod
    def is_valid_email(email):
        """Valida formato do email"""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))

    def set_password(self, password):
        """Define senha com hash"""
        if len(password) < 8:
            raise ValueError("Senha deve ter pelo menos 8 caracteres")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica senha"""
        return check_password_hash(self.password_hash, password)

    def register_login(self):
        """Registra login bem-sucedido"""
        self.last_login = datetime.utcnow()
        self.login_attempts = 0
        db.session.commit()

    def register_failed_login(self):
        """Registra tentativa falha de login"""
        self.login_attempts += 1
        db.session.commit()

    @property
    def is_authenticated(self):
        """Return True if user is authenticated."""
        return True if self.is_active else False

    def __repr__(self):
        return f'<User {self.username}>'