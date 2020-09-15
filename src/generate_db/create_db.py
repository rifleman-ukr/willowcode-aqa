import json

from src.main import WikiArticle
from src.main import db


def create_database():
    db.create_all()

    for article in json.load(open("db_data.json")):
        if article.get("title"):
            db.session.add(WikiArticle(article["title"], article.get("text")))
    db.session.commit()


if __name__ == "__main__":
    create_database()
