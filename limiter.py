from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri='memory://'
    )

def init_limiter(app):
    limiter.init_app(app)