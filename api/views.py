from flask import redirect, render_template, url_for
from flask_login import login_user, logout_user

from app import app, db
from api.forms import EmailPasswordForm
from api.util.security import ts
from api.util.util import send_email
from api.models import User

@app.route('/accounts/create', methods=['GET', 'POST'])
def create_account():
    form = EmailPasswordForm()
    if form.validate_on_submit():
        user = User(
            email = form.email.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()

        # Here is sent the email confirmation link
        subject = 'Confirm your email'
        token = ts.dumps(self.email, salt='email-confim-key')

        confirm_url = url_for(
            'confirm_email',
            token=token,
            _external=True
        )

        html = render_template(
            'email/activate.html',
            confirm_url=confirm_url
        )

        send_email(user.email, subject, html)
        return redirect(url_for('index'))

    return render_template('accounts/create.html', form=form)

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt='email-confirm-key', max_age=86400)
    except:
        abort(404)

    user = User.query.filter_by(email=email).first_or_404()

    user.email_confirmed = True

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('signin'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = EmailPasswordForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = EmailPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user.is_correct_password(form.password.data):
            login_user(user)

            return redirect(url_for('index'))
        else:
            return redirect(url_for('signin'))
    return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
    logout_user(user)

    return redirect(url_for('index'))
