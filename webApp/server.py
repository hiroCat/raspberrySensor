from flask import Flask, render_template, session, request
from flask_session import Session
import jinja2
import psycopg2

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.secret_key = 'bqkMquUfb4FZ0wcQXsGlalQd49o'
app.config.from_object(__name__)
Session(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/table', methods=["GET","POST"])
def getTable():
    print ("da"+ request.method)
    return render_template('index.html')
    # error = ''
    # try:
    #     if request.method == "POST":
    #         attempted_username = request.form['username']
    #         attempted_password = request.form['password']
    #         if attempted_username == "admin" and attempted_password == "password":
    #             return redirect(url_for('dashboard'))
    #         else:
    #             error = "Invalid credentials. Try Again."

    #     return render_template("login.html", error = error)

    # except Exception as e:
    #     #flash(e)
    #     return render_template("login.html", error = error)  
	
@app.route('/set_name', methods=['GET', 'POST'])
def set_name():
    print ("sdfasdf"+ request.method)
    print ("----------------------------")
    print (request.data)
    print (request.form.items())
    print ("-----------eee--------------")
    # for key in request.form.keys():
    #     for value in request.form.getlist(key):
    #         print (key+":"+value)
    for key in request.form.values():
        print (key)
    print ("-----------eee--------------")
    fromI = request.form.get('dateFrom', "default_name")
    toI = request.form.get('dateTo', "default_name")
    print(fromI)
    print(toI)
    return render_template('hello.html')

@app.route('/other', methods=['GET', 'POST'])
def other():
    return render_template('hellocopy.html')

@app.route('/chart', methods=['GET', 'POST'])
def chart():
    fromI = request.form.get('dateFrom', None)
    toI = request.form.get('dateTo', None)
    print(fromI)
    print(toI)
    json_string = """
            {
              labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July','du'],
              datasets: [{
                  label: 'first sensor',
                  backgroundColor: 'rgb(255, 99, 132)',
                  borderColor: 'rgb(255, 99, 132)',
                  data: [0, 10, 5, 2, 20, 30, 45,56,66],
                  fill: false
              },
              {
                  label: 'second sensor',
                  backgroundColor: 'rgb(30, 211, 24)',
                  borderColor: 'rgb(30, 211, 24)',
                  data: [10, 1, 50, 20, 2, 3, 50,67,54],
                  fill: false
              }]
          } """
    session['data'] = json_string
    return render_template('chart.html')

if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    sess = Session()
    sess.init_app(app)

    app.debug = True
    app.run()