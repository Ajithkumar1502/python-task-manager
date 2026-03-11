from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# -----------------------------
# DATABASE INITIALIZATION
# -----------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()

# -----------------------------
# HOME PAGE - SHOW TASKS
# -----------------------------
@app.route("/")
def home():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    conn.close()

    return render_template("index.html", tasks=tasks)


# -----------------------------
# ADD TASK
# -----------------------------
@app.route("/add", methods=["GET","POST"])
def add_task():

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO tasks (title,description) VALUES (?,?)",
                       (title,description))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_task.html")


# -----------------------------
# DELETE TASK
# -----------------------------
@app.route("/delete/<int:id>")
def delete_task(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


# -----------------------------
# EDIT TASK
# -----------------------------
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit_task(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]

        cursor.execute(
        "UPDATE tasks SET title=?, description=? WHERE id=?",
        (title, description, id)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    cursor.execute("SELECT * FROM tasks WHERE id=?", (id,))
    task = cursor.fetchone()

    conn.close()

    return render_template("edit_task.html", task=task)


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)