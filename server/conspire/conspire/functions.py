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
def userinfo():
    try:
        user = User.query.filter_by(id=session['user_id']).one()
        return jsonify({'success': True, 'id': user.id, 'name': user.username, 'email': user.email})
    except NoResultFound:
        return jsonify({'success': False})


@app.route('/list/reactions', methods=["POST"])
@login_required
def list_reactions():
    articles = [get_article(a) for a in request.json['arxiv_ids']]
    reactions = {}
    for a in articles:
        result = {'reactions': [], 'myself': ''}
        for r in a.reactions:
            result['reactions'].append(r.reaction)
            if r.user_id == session['user_id']:
                result['myself'] = r.reaction
        reactions[a.arxiv_id] = result

    return jsonify({'success' : True, 'reactions': reactions})


@app.route('/list/comment_sizes', methods=["POST"])
@login_required
def list_comment_sizes():
    articles = [get_article(a) for a in request.json['arxiv_ids']]
    comment_sizes = {a.arxiv_id: len(a.comments) for a in articles}
    return jsonify({'success' : True, 'comment_sizes': comment_sizes})


@app.route('/get/comments', methods=["POST"])
@login_required
def list_comments():
    arxiv_id = request.json['arxiv_id']
    article = get_article(arxiv_id)
    comments = [{'comment': c.comment,
                 'username': c.user.username,
                 'created_at': c.created_at} for c in article.comments]
    return jsonify({'success' : True, 'comments': comments})


@app.route('/get/reactions', methods=["POST"])
@login_required
def list_reactions_single():
    arxiv_id = request.json['arxiv_id']
    article = get_article(arxiv_id)
    reactions = []
    myself = ''

    for r in article.reactions:
        reactions.append(r.reaction)
        if r.user_id == session['user_id']:
            myself = r.reaction

    return jsonify({'success' : True, 'reactions': reactions, 'myself': myself})


@app.route('/add/reaction', methods=["POST"])
@login_required
def add_reaction():
    article = get_article(request.json['arxiv_id'])
    reaction = request.json['reaction']
    if reaction and not reaction in Reaction.reaction_list:
        abort(403)

    try:
        r = Reaction.query.filter_by(article=article, user_id=session['user_id']).one()
        if reaction:
            r.reaction = reaction
        else:
            db.session.delete(r)
    except NoResultFound:
        r = Reaction()
        r.user_id = session['user_id']
        r.reaction = reaction
        r.article = article
        db.session.add(r)

    db.session.commit()

    return jsonify({'success' : True})


@app.route('/add/comment', methods=["POST"])
@login_required
def add_comment():
    article = get_article(request.json['arxiv_id'])
    comment = request.json['comment']
    if not comment:
        abort(403)

    c = Comment()
    c.user_id = session['user_id']
    c.comment = comment
    c.article = article
    db.session.add(c)
    db.session.commit()

    return jsonify({'success' : True})
