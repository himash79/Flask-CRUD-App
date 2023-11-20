import os

import psycopg2
from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://[USERNAME]:[PASSWORD]@localhost:5432/[DATABASE]'
UPLOAD_FOLDER = 'static/resources'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)


class Users_user(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    image = db.Column(db.String(200))
    status = db.Column(db.String(1))


@app.route('/')
def hello_world():
    users = Users_user.query.order_by(Users_user.id).all()
    return render_template('index.html', users=users)


@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']

        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename).replace("\\", "/"))
        image = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace("\\", "/").replace("static/", " ").strip()

        status = request.form['status']

        new_user = Users_user(id=id, name=name, email=email, image=image, status=status)
        db.session.add(new_user)
        db.session.commit()
        flash('User Added Successfully !', 'info')
        return redirect('/')
    except Exception as e:
        flash('User Added Failed !', 'error')
        print(e)
        return redirect('/')


@app.route('/delete/<string:id>')
def delete_user(id):
    try:
        user = Users_user.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        flash('User Deleted Successfully !', 'info')
        return redirect('/')
    except:
        flash('User Deleted Failed !', 'error')
        return 'There was an error !'


@app.route('/update/<string:id>', methods=['POST', 'GET'])
def update_user(id):
    try:
        if request.method == 'GET':
            user = Users_user.query.get_or_404(id)
            return render_template('update.html', user=user)
        else:
            user = Users_user.query.get_or_404(id)

            user.name = request.form['name']
            user.email = request.form['email']

            file = request.files['file']
            filename = secure_filename(file.filename)
            if not filename == "":
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename).replace("\\", "/"))
                user.image = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace("\\", "/").replace("static/",
                                                                                                            " ").strip()

            user.status = request.form['status']
            db.session.commit()
            flash('User Update Successfully !', 'info')
            return redirect('/')
    except Exception as e:
        flash('User Update Failed !', 'info')
        print(e)
        return redirect('/')


@app.route('/back', methods=['POST', 'GET'])
def redirectPage():
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
