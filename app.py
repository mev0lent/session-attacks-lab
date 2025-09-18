from flask import Flask, request, redirect, make_response, render_template
app = Flask(__name__)

# "Session Store": In-memory dictionary to store session data (for demonstration purposes)
sessions = {}
users = {"khan":"nooniensingh"}

@app.route('/')
def index():
    session_id = request.cookies.get("session_id")
    user = sessions.get(session_id)

    if user:
        return render_template('dashboard.html', user=user, session_id=session_id)
    else:
        return render_template('index.html')
    
@app.before_request
def force_hostname():
    if request.host.startswith("127.0.0.1"):
        return redirect(request.url.replace("127.0.0.1", "localhost"))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if users.get(username) == password:
        # Check if a session_id already exists (fixation!)
        session_id = request.cookies.get('session_id')
        if not session_id:
            session_id = username + '123'  # still insecure
        sessions[session_id] = username
        resp = make_response(redirect('/'))
        resp.set_cookie('session_id', session_id)
        return resp
    return "Invalid credentials"

@app.route('/logout')
def logout():
    session_id = request.cookies.get('session_id')
    sessions.pop(session_id, None)
    resp = make_response("Logged out")
    resp.set_cookie('session_id', '', expires=0)
    return resp

@app.route('/show_session')
def show_session():
    session_id = request.cookies.get('session_id')
    return f"Your session ID is: {session_id}"

@app.route('/fixate')
def fixate():
    sid = request.args.get('sid')
    if not sid:
        return "No session ID provided"
    resp = make_response("Session ID set via URL. Now go log in.")
    resp.set_cookie('session_id', sid)
    return resp

if __name__ == "__main__":
    app.run(debug=True)