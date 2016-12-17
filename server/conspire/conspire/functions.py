from flask import session, request, abort, jsonify

from conspire import app, login_required
from conspire.models import db, User, Article, Reaction, Comment

import json
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError


def get_article(arxiv_id):
    if not arxiv_id:
        abort(403)

    try:
        article = Article.query.filter_by(arxiv_id=arxiv_id).one()
    except NoResultFound:
        try:
            article = Article()
            article.arxiv_id = arxiv_id
            db.session.add(article)
            db.session.commit()
        except IntegrityError as e:
            reason = e.message
            if reason.endswith('is not unique'):
                article = Article.query.filter_by(arxiv_id=arxiv_id).one()
    return article


@app.route('/userinfo')
@login_required
def userinfo():
    user = User.query.filter_by(id=session['user_id']).one()
    return jsonify({'id': user.id, 'name': user.username, 'email': user.email})


@app.route('/list/reactions')
@login_required
def list_reactions():
    articles = [get_article(a) for a in request.json['arxiv_ids']]
    reactions = {a.arxiv_id: [r.reaction for r in a.reactions] for a in articles}
    return jsonify({'sucess' : True, 'reactions': reactions})


@app.route('/list/comment_sizes')
@login_required
def list_comment_sizes():
    articles = [get_article(a) for a in request.json['arxiv_ids']]
    comment_sizes = {a.arxiv_id: len(a.comments) for a in articles}
    return jsonify({'sucess' : True, 'comment_sizes': comment_sizes})


@app.route('/list/comments/<arxiv_id>')
@login_required
def list_comments(arxiv_id):
    article = get_article(arxiv_id)
    comments = [{'comment': c.comment,
                 'username': c.user.username} for c in article.comments]
    return jsonify({'sucess' : True, 'comments': comments})


@app.route('/list/reactions/<arxiv_id>')
@login_required
def list_reactions_single(arxiv_id):
    article = get_article(arxiv_id)
    reactions = [r.reaction for r in article.reaction]
    return jsonify({'sucess' : True, 'reactions': reactions})


@app.route('/add/reaction')
@login_required
def add_reaction():
    article = get_article(request.json['arxiv_id'])
    reaction = request.json['reaction']
    if reaction and not reaction in Reaction.reaction_list:
        abort(403)

    try:
        r = Reaction.query.filter_by(arxiv_id=arxiv_id, user_id=user_id).one()
        r.reaction = reaction
    except NoResultFound:
        r = Reaction()
        r.user_id = session['user_id']
        r.reaction = reaction
        db.session.add(r)

    db.session.commit()

    return jsonify({'sucess' : True})


@app.route('/add/comment')
@login_required
def add_comment():
    article = get_article(request.json['arxiv_id'])
    comment = request.json['comment']
    if not comment:
        abort(403)

    c = Comment()
    c.user_id = session['user_id']
    c.comment = comment
    db.session.add(c)
    db.session.commit()

    return jsonify({'sucess' : True})
