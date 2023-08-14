""" """
from datetime import datetime
from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask import redirect, url_for

from .notes import Notes

app = Flask(__name__)

@app.route('/')  # decorator
def index():
    """ index """
    username = "Brad Montgomery"
    notes = Notes()
    response = render_template(
        "index.html",
        name=username,
        notes=notes.get_notes()
    )
    notes.close()
    return response

@app.route("/create", methods=['GET', 'POST'])
def add_note():
    """ Add a note """
    if request.method == "POST":
        notes = Notes()
        notes.add_note(request.form["content"])
        # redirect after POST
        return redirect(url_for('index'))

    # GET requests...
    return render_template("create.html")


@app.route("/delete/<int:note_id>", methods=["GET", "POST"])
def delete_note(note_id):
    """ Delete a note """
    if request.method == "POST":
        notes = Notes()
        notes.remove_note(note_id)
        return redirect(url_for("index"))  # redirect after POST

    # GET request: Show the content of the note...
    notes = Notes()
    return render_template("confirm.html", note=notes.get_note(note_id))


@app.route("/time")
def time():
    """ do something """
    t = datetime.now()
    content = {"time": t.strftime("%c")}
    return jsonify(content)
