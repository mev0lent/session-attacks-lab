from flask import Flask, request, redirect, make_response, render_template
app = Flask(__name__)

# "Session Store": In-memory dictionary to store session data (for demonstration purposes)
sessions = {}
users = {"khan":"nooniensingh"}

comments = []  # In-memory comment store

@app.route('/', methods=['GET', 'POST'])
def index():
    session_id = request.cookies.get("session_id")
    user = sessions.get(session_id)

    # saving a comment via GET
    comment_from_url = request.args.get('comment')
    if comment_from_url and comment_from_url not in comments:
        comments.append(comment_from_url)

    # saving a comment via POST
    if request.method == 'POST' and user:
        comment = request.form['comment']
        comments.append(comment)  # ⚠️ Deliberate XSS vulnerability
        return redirect('/')

    if user:
        return render_template('dashboard.html', user=user, session_id=session_id, comments=comments)
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