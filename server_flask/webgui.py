from flask import Flask, render_template
app = Flask(__name__)


@app.route('/login')
def loginpage():
    # return "<h1>Login Page<h1>"
    suggestions = [1,2,3,4]
    return render_template('homepage.html', suggestions_list=suggestions)

@app.route('/home')
def dashboard():
    # return "<h1>Home dashboard of %s <h1>" % user
    return render_template('index.html')

@app.route('/reports')
def reports():
    return "<h1>View Reports Page<h1>"

@app.route('/sendinstructions/<ip>')
def send_instructions(ip):
    return "<h1>Instructions Sending {0}<h1>".format(ip)



if __name__ == "__main__":
    app.run()