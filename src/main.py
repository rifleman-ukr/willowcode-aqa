import os
import random

from flask import Flask
from flask import jsonify
from flask import request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

from src.generate_db.create_db import create_database

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
marshmallow = Marshmallow(app)


class WikiArticle(db.Model):
    title = db.Column(db.String(60), unique=True, primary_key=True)
    text = db.Column(db.String(280))
    text_version = db.Column(db.Integer)

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.version = 0


class ArticleSchema(marshmallow.Schema):
    class Meta:
        fields = ('title', 'text')


article_schema = ArticleSchema()


@app.route('/', methods=['POST'])
def add_article():
    title = request.json['title']
    text = request.json['text']

    db.session.add(new_article := WikiArticle(title, text))
    try:
        db.session.commit()
    except exc.IntegrityError:
        return "This article already exist, try to update it"
    else:
        return article_schema.jsonify(new_article)


@app.route('/', methods=['GET'])
def get_wiki():
    return jsonify(ArticleSchema(many=True).dump(WikiArticle.query.all()))


@app.route('/random', methods=['GET'])
def get_random_article():
    return jsonify(ArticleSchema().dump(random.choice(WikiArticle.query.all())))


def set_page_version(self, page_title, version):
    pass


if __name__ == "__main__":
    if not os.path.exists('db.sqlite'):
        create_database()
    app.run(debug=True)
