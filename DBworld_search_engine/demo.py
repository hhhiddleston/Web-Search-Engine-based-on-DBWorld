from flask import Flask, render_template, request, url_for, redirect
from tools.mysearcher import DBworldSearcher

"""
    DBWorld Search Engine Demo
    author: maggie

    Usage:
        export FLASK_APP=demo.py
        flask run -h 0.0.0.0 -p 5000

"""
app = Flask(__name__)
app._static_folder = "static"

sub_con_searcher = DBworldSearcher("index", ["subject", "content"])
auth_searcher = DBworldSearcher("index", ["author"])
conf_searcher = DBworldSearcher("index", ["subject"])
sent_searcher = DBworldSearcher("index", ["sent"])
ddl_searcher = DBworldSearcher("index", ["deadline"])

@app.route('/', methods=["GET", "POST"])
def mainpage():
    # POST and query not empty
    if request.method == "POST" and len(request.form["query"]):
        query = request.form["query"]
        filedid = request.form["field"]
        #print(filedid)
        return redirect(url_for('search', q=query, p=1, f=filedid))
    # GET
    return render_template("mainpage.html")

@app.route('/search', methods=["GET","POST"])
def search():
    # POST a new query
    if request.method == "POST":
        query = request.form["query"]
        filedid = request.form["field"]
        return redirect(url_for('search', q=query, p=1, f=filedid))

    # Search query
    query = request.args["q"]
    page = int(request.args["p"])
    filedid = request.args["f"]

    if filedid == "0":
        # search subject & content
        dbworld_searcher = sub_con_searcher
        tmp = dbworld_searcher.search(querytext=query, limit=page*10)
        time_cost = round(tmp.runtime, 3)
        results = [(x["sent"], x["author"], x["subject"],
            x["deadline"], x.highlights("content"), x["href"], x["webpage"], x["doctype"]) for x in tmp]
        return render_template("results.html",
            msg=[len(tmp), time_cost], query=query, page=page, results=results)

    elif filedid == "1":
        # search author
        dbworld_searcher = auth_searcher
        tmp = dbworld_searcher.search(querytext=query, limit=page*10)
        time_cost = round(tmp.runtime, 3)
        results = [(x["sent"], x["author"], x["subject"],
            x["deadline"], x["content"][:600], x["href"], x["webpage"], x["doctype"]) for x in tmp]
        return render_template("results.html",
            msg=[len(tmp), time_cost], query=query, page=page, results=results)

    elif filedid == "2":
        # search conference
        dbworld_searcher = conf_searcher
        tmp = dbworld_searcher.search(querytext=query, limit=page*10)
        time_cost = round(tmp.runtime, 3)
        results = [(x["sent"], x["author"], x.highlights("subject"),
            x["deadline"], x["content"][:600], x["href"], x["webpage"], x["doctype"]) for x in tmp]
        return render_template("results.html",
            msg=[len(tmp), time_cost], query=query, page=page, results=results)

    elif filedid == "3":
        # search sent date
        dbworld_searcher = sent_searcher
        tmp = dbworld_searcher.search(querytext=query, limit=page*10)
        time_cost = round(tmp.runtime, 3)
        results = [(x["sent"], x["author"], x["subject"],
            x["deadline"], x["content"][:600], x["href"], x["webpage"], x["doctype"]) for x in tmp]
        return render_template("results.html",
            msg=[len(tmp), time_cost], query=query, page=page, results=results)

    elif filedid == "4":
        # search ddl date
        dbworld_searcher = ddl_searcher
        tmp = dbworld_searcher.search(querytext=query, limit=page*10)
        time_cost = round(tmp.runtime, 3)
        results = [(x["sent"], x["author"], x["subject"],
            x["deadline"], x["content"][:600], x["href"], x["webpage"], x["doctype"]) for x in tmp]
        return render_template("results.html",
            msg=[len(tmp), time_cost], query=query, page=page, results=results)
