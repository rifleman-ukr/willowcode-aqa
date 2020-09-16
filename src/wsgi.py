import json
import os
from main import WikiArticle
from main import app
from main import db

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
    app.run(host='0.0.0.0')
