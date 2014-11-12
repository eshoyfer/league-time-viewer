from flask import Flask, render_template, request, redirect, flash, url_for, session
import sqlite3, hashlib
import league

app = Flask(__name__)

app.secret_key="SOMETHINGUNIQUEANDSECRET" # Don't use this key if you were actually going to deploy!

@app.route("/home", methods = ["GET","POST"])
@app.route("/", methods = ["GET","POST"])
def home():
    return render_template('home.html')

@app.route("/search", methods = ["GET","POST"])
def search():
	if request.method == "POST": # Search results
		query = request.form['user']
		try:
			found = True
			search_result_dict = league.search_user(query)
		except:
			# Not the cleanest...
			found = False
			search_result_dict = {}

		return render_template('results.html', found=found, search=search_result_dict)
	if request.method == "GET":
		return render_template('search.html')


@app.route("/user/<str_id>", methods = ["GET","POST"])
def user(str_id):
	try:
		username = league.get_user_by_id(str_id)
		userSuccess = True
	except:
		username = None
		userSuccess = False

	try:
		filename = league.get_times_plot(str_id)
		userPlaying = True
	except:
		filename = None
		userPlaying = False

	success = userSuccess and userPlaying
	return render_template('user.html', username=username, filename=filename, success=success)

@app.errorhandler(404)
def not_found(e): # Return rendering, 404
    return render_template('404.html'), 404
    
@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

if __name__=="__main__":
    app.debug=True
    app.run()
    #app.run(host="0.0.0.0",port=8888)
