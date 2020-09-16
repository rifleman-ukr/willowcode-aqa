import json
import os
import random

from flask import Flask
from flask import abort
from flask import jsonify
from flask import request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class WikiArticle(db.Model):
    title = db.Column(db.String(60), unique=True, primary_key=True)
    text = db.Column(db.String(280))
    text_version = db.Column(db.Integer)

    def __init__(self, title, text, version=1):
        self.title = title.lower().capitalize()
        self.text = json.dumps([{"text_version": 0,
                                 "text": "An empty article"},
                                {"text_version": 1,
                                 "text": text}])
        self.text_version = version


class ArticleSchema(Marshmallow(app).Schema):
    class Meta:
        fields = ('title', 'text', 'text_version')


@app.route('/', methods=['POST'])
def add_article() -> dict:
    if isinstance(request.json['title'], str):
        title = request.json['title'].lower().capitalize()
        text = request.json['text']

        if article := WikiArticle.query.get(title):
            versions = json.loads(article.text)
            if text in [old_version['text'] for old_version in versions]:
                return jsonify({"error": "This text is outdated"})
            versions.append({"text_version": (version := len(versions)),
                             "text": text})
            article.text = json.dumps(versions)
            article.text_version = version
        else:
            db.session.add(article := WikiArticle(title, text))
        db.session.commit()
        return parse_db(ArticleSchema().dump(article))
    else:
        abort(415)


@app.route('/', methods=['GET'])
def get_wiki() -> dict:
    return parse_db(ArticleSchema(many=True).dump(WikiArticle.query.all()))


@app.route('/random', methods=['GET'])
def get_random_article() -> dict:
    return parse_db(
        ArticleSchema().dump(random.choice(WikiArticle.query.all())))


@app.route('/version_set', methods=['POST'])
def set_page_version():
    if request.headers.get('Authorization') == 'admin':
        version = request.json['version']
        title = request.json['title'].lower().capitalize()
        if type(version) is not int:
            abort(415)
        if article := WikiArticle.query.get(title):
            if version > len(json.loads(article.text)) or version < 0:
                return jsonify({"error": "This version does not exist"})
            article.text_version = version
            db.session.commit()
            return parse_db(ArticleSchema().dump(article))
        else:
            abort(404)
    else:
        abort(401)


@app.route("/versions", methods=['GET'])
def get_article_versions():
    if request.headers.get('Authorization') == 'admin':
        if not isinstance(request.json['title'], str):
            abort(415)
        title = request.json['title'].lower().capitalize()
        if article := WikiArticle.query.get(title):
            return jsonify({"title": article.title,
                            "versions": [version for version
                                         in json.loads(article.text)]})
        else:
            abort(404)
    else:
        abort(401)


def parse_db(schema):
    if isinstance(schema, list):
        response = list()
        for article in schema:
            for version in json.loads(article['text']):
                if version['text_version'] == article['text_version']:
                    response.append({"title": article['title'],
                                     "text": version['text']})
    else:
        for version in json.loads(schema['text']):
            if version['text_version'] == schema['text_version']:
                response = {"title": schema['title'], "text": version['text']}
    return jsonify(response)


if __name__ == "__main__":
    if not os.path.exists(os.path.join(os.path.dirname(__file__),
                                       "db.sqlite")):
        db.create_all()
        for article in json.load(open(os.path.join(os.path.dirname(__file__),
                                                   "db_data.json"))):
            if article.get("title"):
                db.session.add(WikiArticle(article["title"],
                                           article.get("text")))
        db.session.commit()
    app.run(threaded=True)
