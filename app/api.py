from flask import Blueprint, jsonify
from app.models import Game, Prediction, User

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/games')
def get_games():
    games = Game.query.all()
    return jsonify([{
        'id': g.id,
        'team1': g.team1,
        'team2': g.team2,
        'date': g.date.isoformat(),
        'result_team1': g.result_team1,
        'result_team2': g.result_team2
    } for g in games])

@bp.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email
    } for u in users])

@bp.route('/predictions')
def get_predictions():
    predictions = Prediction.query.all()
    return jsonify([{
        'id': p.id,
        'user_id': p.user_id,
        'game_id': p.game_id,
        'tip_team1': p.tip_team1,
        'tip_team2': p.tip_team2
    } for p in predictions])