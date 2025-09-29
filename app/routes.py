from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.models import User, Game, Prediction, Comment
from app.forms import (
    LoginForm,
    RegistrationForm,
    GameForm,
    PredictionForm,
    CommentForm,
    ManualResetPasswordForm
)
from urllib.parse import urlparse
from datetime import datetime

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    games = Game.query.order_by(Game.date).all()
    return render_template('index.html', games=games)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Ungültiger Benutzername oder Passwort')
            return redirect(url_for('routes.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('routes.index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registrierung erfolgreich! Bitte einloggen.')
        return redirect(url_for('routes.login'))
    return render_template('register.html', form=form)

@bp.route('/create_game', methods=['GET', 'POST'])
@login_required
def create_game():
    form = GameForm()
    if form.validate_on_submit():
        game = Game(
            team1=form.team1.data,
            team2=form.team2.data,
            location=form.location.data,
            date=form.date.data,
            user_id=current_user.id  # <<< hier
        )
        db.session.add(game)
        db.session.commit()
        flash("Spiel erfolgreich erstellt ✅", "success")
        return redirect(url_for('routes.index'))
    return render_template('create_game.html', form=form)

@bp.route('/tip/<int:game_id>', methods=['GET', 'POST'])
@login_required
def tip(game_id):
    game = Game.query.get_or_404(game_id)
    form = PredictionForm()
    if form.validate_on_submit():
        prediction = Prediction.query.filter_by(user_id=current_user.id, game_id=game.id).first()
        if not prediction:
            prediction = Prediction(user=current_user, game=game)
        prediction.tip_team1 = form.tip_team1.data
        prediction.tip_team2 = form.tip_team2.data
        db.session.add(prediction)
        db.session.commit()
        return redirect(url_for('routes.index'))
    return render_template('tipps.html', game=game, form=form)

@bp.route('/game/<int:game_id>', methods=['GET', 'POST'])
def game_detail(game_id):
    game = Game.query.get_or_404(game_id)
    comments = Comment.query.filter_by(game_id=game.id).order_by(Comment.timestamp.desc()).all()
    predictions = Prediction.query.filter_by(game_id=game.id).join(User).all()
    form = CommentForm()

    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(content=form.content.data, user=current_user, game=game)
        db.session.add(comment)
        db.session.commit()
        flash('Kommentar hinzugefügt ✅', 'success')
        return redirect(url_for('routes.game_detail', game_id=game.id))

    return render_template('game_detail.html', game=game, form=form, comments=comments, predictions=predictions)

@bp.route('/manual_reset_password', methods=['GET', 'POST'])
def manual_reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))

    form = ManualResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            user.set_password(form.password.data)
            db.session.commit()
            flash('Passwort erfolgreich geändert. Du kannst dich nun einloggen.', 'success')
            return redirect(url_for('routes.login'))
        else:
            flash('Benutzer nicht gefunden.', 'danger')
    return render_template('manual_reset_password.html', form=form)

@bp.route('/edit_game/<int:game_id>', methods=['GET', 'POST'])
@login_required
def edit_game(game_id):
    game = Game.query.get_or_404(game_id)
    
    # Nur der Ersteller darf bearbeiten
    if game.user_id != current_user.id:
        flash('Du darfst dieses Spiel nicht bearbeiten.', 'danger')
        return redirect(url_for('routes.index'))

    form = GameForm(obj=game)

    if form.validate_on_submit():
        game.team1 = form.team1.data
        game.team2 = form.team2.data
        game.date = form.date.data
        game.location = form.location.data
        db.session.commit()
        flash('Spiel aktualisiert ✅', 'success')
        return redirect(url_for('routes.index'))

    return render_template('edit_game.html', form=form, game=game)

@bp.route('/about')
def about():
    return render_template('about.html')