from flask import Flask, render_template, request, session
from wtforms import Form, StringField, SelectField, validators
import Process
import datetime


app = Flask(__name__)


@app.route('/' , methods=['GET', 'POST'])
def home():
    session['userid'] = 'Mary'
    form = MonthForm(request.form)
    if request.method == 'POST' and form.validate():
        monthMM = form.month.data
        checkMonth = int(monthMM)
        print(monthMM)

    now = datetime.datetime.now()
    todayMonth = now.month
    todayYear = now.year
    months = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December')

    if todayMonth == 2:
        prevMonth = 1
    else:
        prevMonth = todayMonth - 1

    if todayYear == 2018 :
        prevYear = 2017
    else :
        prevYear = now.year - 1

    usersList = []
    usersList = Process.processUser(session['userid'],todayMonth)
    savings = []
    limit = []
    limit = Process.limit(session['userid'],todayMonth)
    over = Process.over(session['userid'],todayMonth)
    displayHistory = []
    #displayHistory = Process.displayHistory(session['userid'],goalType)

    return render_template('homepage.html', users=usersList,checkMM=months[todayMonth],saving=savings,todayMonth=todayMonth, prevMonth=prevMonth, todayYear=todayYear, prevYear=prevYear,limits=limit,over=over,form=form,user = session['userid'],displayHistory=displayHistory)


class MonthForm(Form):
    month = SelectField('Month', [validators.DataRequired()],
                           choices=[('0', 'Select'),('2','February 2018'),('1','January 2018'), ('12', 'December 2017'), ('11', 'November 2017'),
                                    ('10', 'October 2017'), ('9', 'September 2017'), ('8', 'August 2017'), ('7', 'July 2017')],
                           default='')

@app.route('/selected', methods=['GET', 'POST'])
def selected():
    session['userid'] = 'Mary'

    now = datetime.datetime.now()
    todayMonth = now.month
    todayYear = now.year
    if todayMonth == 1:
        prevMonth = 12
    else :
        prevMonth = todayMonth - 1

    if todayYear == 2018 :
        prevYear = 2017
    else :
        prevYear = now.year - 1

    form = MonthForm(request.form)
    if request.method == 'POST' and form.validate():
        monthMM = form.month.data
        checkMonth = int(monthMM)
        print(monthMM)

        months = ('Null','January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December')

        usersList = []

        usersList = Process.processUser(session['userid'],checkMonth)
        limit = []
        limit = Process.limit(session['userid'], checkMonth)
        over = Process.over(session['userid'], checkMonth)

        return render_template('homepage.html',users=usersList,checkMM=months[checkMonth], count=len(usersList),limits=limit,over=over,form=form)


@app.route('/update/<string:postlist>/',methods=['GET','POST'])
def update_savingHistory(postlist):
    #session['userid'] = 'Mary'

    plist = postlist.split('$')
    name = plist[0]
    goalType = plist[1]
    displayHistory = []
    displayHistory = Process.displayHistory(session['userid'],goalType)
    print(displayHistory)

    now = datetime.datetime.now()
    todayMonth = now.month
    checkMonth = now.month
    todayYear = now.year

    #form = MonthForm(request.form)

    usersList = []
    usersList = Process.processUser(session['userid'],checkMonth)
    limit = []
    limit = Process.limit(session['userid'], checkMonth)
    over = Process.over(session['userid'], checkMonth)

    checkMM = 2
    prevMonth = 1
    prevYear = 2017

    form = MonthForm(request.form)
    return render_template('homepage.html',users=usersList,checkMM=checkMM,limits=limit,over=over,user=name,displayHistory=displayHistory,form=form)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run()

