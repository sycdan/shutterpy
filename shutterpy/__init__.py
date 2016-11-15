import flask
import imagehash
import os

from flask_login import LoginManager, UserMixin
from PIL import Image

from shutterpy import config

app = flask.Flask(__name__)
login_manager = LoginManager(app)


class User(UserMixin):
    def __init__(self, **kwargs):
        self.username = None
        self.password = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def build(cls, section):
        user = cls(**{x: section.get(x) for x in section})
        user.id = section.name.split('/', 1)[1]
        return user

    @classmethod
    def find(cls, username):
        for section_key in config.sections():
            if section_key.lower().startswith('user/'):
                section = config.section(section_key)
                if section.get('username') == username:
                    return cls.build(section)

    @classmethod
    def load(cls, id):
        section = config.section('user/%s' % id, silent=True)
        if section:
            return cls.build(section)


@login_manager.user_loader
def load_user(user_id):
    return Users.load(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return flask.Response(
        'Please enter valid credentials.',
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'},
    )


@login_manager.request_loader
def load_user_from_request(request):
    auth = request.authorization
    if auth:
        user = User.find(auth.username)
        if user and user.password == auth.password:
            flask.g.user = user
            return user

    return None


def resolve_path(path):
    return os.path.abspath(os.path.join(app.config['SHUTTERPY_ROOT'], path))


def get_hash(file_path):
    return str(imagehash.average_hash(Image.open(file_path)))


def ensure_cache_dir():
    cache_dir = resolve_path('.shutterpy/cache')
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)
    return cache_dir


def get_ext(path):
    _, ext = os.path.splitext(path)
    return ext.lstrip('.').lower()


def detect_image_type(file_path):
    return {
        'png': 'PNG',
    }.get(get_ext(file_path), 'JPEG')


def get_mimetype(file_path):
    return {
        'png': 'image/png',
    }.get(get_ext(file_path), 'image/jpg')


def get_thumbnail(path):
    _, ext = os.path.splitext(path)
    file_path = resolve_path(path)
    cache_dir = ensure_cache_dir()
    cache_path = os.path.join(cache_dir, get_hash(file_path) + ext)

    if not os.path.exists(cache_path):
        im = Image.open(file_path)
        im.thumbnail((128, 128))
        im.save(cache_path, detect_image_type(file_path))

    return Image.open(cache_path)
