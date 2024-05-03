import psycopg2
from config import config
from flask import Flask, render_template, request

# Connect to the PostgreSQL database server
def connect(query):
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()
        
        # execute a query using fetchall()
        cur.execute(query)
        rows = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows
 
# app.py
app = Flask(__name__)


# serve form web page
@app.route("/")
def form():
    return render_template('home.html') #path to button

# handle both gender progeny report call for query
@app.route('/progeny_report', methods=['POST'])  
def progenyReport():
    rows = connect('SELECT * FROM progeny_report;')
    heads = ['EID', 'Visual Tag', 'Date of Birth', 'Dam', 'Sire', 'Number of Kids', 'Birth Weight', 'Weaning weight', 'Sell Weight']
    return render_template('progeny-report.html', rows=rows, heads=heads)

@app.route('/weight_comparisons', methods=['POST'])
def weight():
    rows = connect('SELECT * FROM weight_comparisons;')
    heads = ['EID', 'Visual Tag', 'Birth Weight', 'Weight Classification']
    return render_template('weight-comparisons.html', rows=rows, heads=heads)

@app.route('/winter_weights', methods=['POST'])
def wintWeights():
    rows = connect('SELECT eid, vistag, wt_val, weighdate FROM winter_weights NATURAL JOIN my_goat WHERE gender=\'Female\' ORDER BY eid')
    heads = ['EID', 'Visual Tag', 'Weight Value', 'Weighdate']
    return render_template('winter-weights.html', rows=rows, heads=heads)

# back button in UI
@app.route('/backbutton', methods = ['POST'])    #back button
def backbutton():
    return render_template('my-form.html')

if __name__ == '__main__':
    app.run(debug = True)