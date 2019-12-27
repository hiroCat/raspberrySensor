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
    return render_template('index.html')

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