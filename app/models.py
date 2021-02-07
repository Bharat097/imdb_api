from app import app, db, bcrypt
import datetime
import jwt


class User(db.Model):
    """Table schema."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, first_name, last_name, email, password, country, is_admin):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.generate_password_hash(password, app.config.get('BCRYPT_LOG_ROUNDS')).decode('utf-8')
        self.country = country
        self.is_admin = is_admin

    def save(self):
        """
        Persist the user in the database
        :param user:
        :return:
        """
        db.session.add(self)
        db.session.commit()
        return self.encode_auth_token(self.id)

    def encode_auth_token(self, user_id):
        """
        Encode the Auth token
        :param user_id: User's Id
        :return:
        """

        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=app.config.get('AUTH_TOKEN_EXPIRY_SECONDS')),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(token):
        """
        Decoding the token to get the payload and then return the user Id in 'sub'
        :param token: Auth Token
        :return:
        """
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError('Signature expired, Please sign in again')
        except jwt.InvalidTokenError:
            raise jwt.InvalidTokenError('Invalid token. Please sign in again')

    @staticmethod
    def get_by_id(user_id):
        """
        Filter a user by Id.
        :param user_id:
        :return: User or None
        """
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def get_by_email(email):
        """
        Check a user by their email address
        :param email:
        :return:
        """
        return User.query.filter_by(email=email).first()


class MovieData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    director = db.Column(db.String(255), nullable=False)
    imdb_score = db.Column(db.Float(precision=2), nullable=False)
    popularity = db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, name, director, imdb_score, popularity):
        self.name = name
        self.director = director
        self.imdb_score = imdb_score
        self.popularity = popularity

    def save(self):
        """
        Persist the Movie Data in the database
        :param movie:
        :return:
        """
        db.session.add(self)
        db.session.commit()
        return "Successfully Added Movie to DB"

    def __str__(self):
        return "{} - {}".format(self.name, self.imdb_score)

    @staticmethod
    def get_by_id(movie_id):
        """
        Filter a movie by Id.
        :param movie_id:
        :return: Movie or None
        """
        return MovieData.query.filter_by(id=movie_id).first()

    @staticmethod
    def get_by_name(name):
        """
        Check a movie by their name
        :param name:
        :return:
        """
        return MovieData.query.filter_by(name=name).first()

    def to_json(self):
        resp = {
            'Movie Name': self.name,
            'Director': self.director,
            'IMDB Rating': self.imdb_score,
            'Popularity': self.popularity
        }
        return resp
