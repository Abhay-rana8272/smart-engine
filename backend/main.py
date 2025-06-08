from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests from different origin

# Configuration for SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'articles.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Article model for storing blog articles
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    summary_and_tags = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content
        }

    def summary_dict(self):
        return {
            "title": self.title,
            "summary_and_tags": self.summary_and_tags or ""
        }

def init_db():
    """Create database and add some initial articles if empty."""
    db.create_all()
    if Article.query.count() == 0:
        # Seed initial articles
        seed_articles = [
            Article(
                title="The Journey to Mindfulness",
                content="Discover how mindfulness can improve your daily life with simple meditative practices.",
                summary_and_tags="Summary: Mindfulness meditation techniques to reduce stress and increase focus.\nTags: mindfulness, meditation, wellness"
            ),
            Article(
                title="Exploring Tech Innovations in 2024",
                content="A deep dive into emerging technologies like AI, quantum computing, and blockchain.",
                summary_and_tags="Summary: Overview of breakthrough tech trends including AI advancements and blockchain.\nTags: technology, AI, blockchain, innovation"
            ),
            Article(
                title="Travel Diaries: Hidden Gems of Europe",
                content="Experience the lesser-known but beautiful places to visit in Europe that few tourists find.",
                summary_and_tags="Summary: Discover hidden European travel destinations off the beaten path.\nTags: travel, Europe, adventure"
            ),
            Article(
                title="Healthy Living: Tips & Tricks",
                content="Practical advice for maintaining a balanced diet and active lifestyle.",
                summary_and_tags="Summary: Practical health tips for diet and exercise.\nTags: health, lifestyle, wellness"
            ),
            Article(
                title="Creative Writing Inspirations",
                content="Boost your creativity with tips and exercises from professional writers.",
                summary_and_tags="Summary: Writing techniques and exercises to foster creativity.\nTags: writing, creativity, arts"
            ),
        ]
        db.session.bulk_save_objects(seed_articles)
        db.session.commit()


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({"results": []})

    # Simple case-insensitive search in title or content
    search_pattern = f"%{query.lower()}%"
    matches = Article.query.filter(
        or_(
            Article.title.ilike(search_pattern),
            Article.content.ilike(search_pattern)
        )
    ).all()

    results = [article.to_dict() for article in matches]
    return jsonify({"results": results})


@app.route('/summarize', methods=['GET'])
def summarize():
    articles = Article.query.filter(Article.summary_and_tags.isnot(None)).all()
    enriched = [article.summary_dict() for article in articles]
    return jsonify({"enriched": enriched})


@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Smart Blog Search API running with DB."})


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000, debug=True)

