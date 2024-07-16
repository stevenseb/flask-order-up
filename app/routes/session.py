from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import LoginForm
from app.models import Employee

bp = Blueprint('session', __name__, url_prefix='/session')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('orders.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(employee_number=form.employee_number.data).first()
        if employee and employee.check_password(form.password.data):
            login_user(employee)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('orders.index'))
        else:
            flash('Invalid employee number or password', 'danger')
    
    return render_template('login.html', form=form)

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('session.login'))
