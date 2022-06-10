from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
app = Flask(__name__)

# db model
app.debug = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'loooong_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
P = [69,19,12]

#first logic
def random_color_first(number,p):
    while True:
        a = number - p[2]
        if a<0:
            res = 'Красный'
            break
        a = a -  p[1]
        if a <0:
            res = 'Зеленый'
            break
        a = a - p[0]
        if a < 0:
            res = 'Синий'
            break
    return res

def random_color_second(p):
    res = random.choices(['Синий',"Зеленый", "Красный"], weights = p)
    return res[0]

def solver_eq(a, b, c):
    a = float(a)
    b = float(b)
    c = float(c)
    D = b ** 2 - 4 * a * c
    result = ""
    if D < 0:
        result = ""
    elif D == 0:
        result = str(-1 * b / (2 * a))
    else:
        x1 = (-1 * b - D ** (1 / 2)) / (2 * a)
        x2 = (-1 * b + D ** (1 / 2)) / (2 * a)
        result = str(round(x1,3)) + ';' + str(round(x2,3))
    return result


class Equation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a = db.Column(db.Float, nullable=False)
    b = db.Column(db.Float, nullable=False)
    c = db.Column(db.Float, nullable=False)
    result = db.Column(db.String(50), nullable=True)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Id %r' % self.id


@app.route('/', methods=['POST', "GET"])
def home_page():
    if request.method == 'POST':
        a_coeff = request.form['a_coefficient']
        b_coeff = request.form['b_coefficient']
        c_coeff = request.form['c_coefficient']
        result = solver_eq(a_coeff, b_coeff, c_coeff)
        eq = Equation(a=a_coeff, b=b_coeff, c=c_coeff, result=result)
        try:
            db.session.add(eq)  # add
            db.session.commit()  # save
            return render_template('result.html', a=a_coeff, b=b_coeff, c=c_coeff, result=result)
        except:
            return "Error"
    return render_template('home_page.html')


@app.route('/history')
def show_history():
    # создание шаблона через который будем получать все записии из базы данных
    eq = Equation.query.order_by(Equation.registration_date.desc()).all()  # обращение к базе данных
    # передача списка в шаблон
    return render_template('history_page.html', eq=eq)

@app.route('/random', methods=['POST', "GET"])
def show_random():
    if request.method == 'POST':
        number = int(request.form['number'])
        if number<=100:
            color = random_color_first(number,P)
        else:
            color = "Введите число до 100"
        return render_template('random_color.html', color=color)
    else:
        return render_template('random_color.html', color='')


if __name__ == '__main__':
    app.run(debug=True)
