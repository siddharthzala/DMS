from flask import Flask, redirect, render_template, request, session, url_for
from pymongo import DESCENDING, MongoClient

app = Flask(__name__)
app.config[
    "SECRET_KEY"
] = b"\xea\xf25\x12\xe3\x13\x1b\xc7\xee\xc4`\xca\x82\xdf\xa5\xe3\x8dK\n/\xefn\n\x8b"
client = MongoClient(
    "mongodb+srv://Defect:admin@cluster1.fxknt.mongodb.net/?retryWrites=true&w=majority"
)
db = client.Defect
print(db)
defect_info = db.defect_info
solution_defect = db.solution_defect


@app.route("/", methods=("GET", "POST"))
def login():
    error = None
    if request.method == "POST":
        users = db.login_details

        role = users.find_one({'User_Role': request.form['User_Role']})

        login_userid = users.find_one({"UserID": request.form["UserID"], "User_Role": request.form['User_Role']})

        if login_userid:
            if request.form["password"] == login_userid["password"]:
                session["UserID"] = request.form["UserID"]
            return redirect(url_for("usertester" if role['User_Role'] == 'Tester' else 'userdeveloper' if role[
                                                                                                              'User_Role'] == 'Developer' else 'userleader'))
        else:
            error = "Invalid credentials. Check for correct role,username and password"

    return render_template("login.html", error=error)


@app.route("/defect", methods=("GET", "POST"))
def createdefect():
    if request.method == "POST":
        UserID = request.form["UserID"]
        User_Role = request.form["User_Role"]
        DefectID = request.form["DefectID"]
        Date = request.form["Date"]
        Defect_title = request.form["Defect_title"]
        Defect_desc = request.form["Defect_description"]
        print(request.form)
        defect_info.insert_one(
            {
                "UserID": UserID,
                "User_Role": User_Role,
                "DefectID": DefectID,
                "Date": Date,
                "Defect_title": Defect_title,
                "Defect_description": Defect_desc,
            }
        )
        return redirect(url_for("usertester"))
    return render_template("create_defect.html")


@app.route("/alldefect")
def alldefect():
    seq = request.args.get("seq") or -1
    return render_template(
        "alldefect.html",
        defects=defect_info.find({}).sort(
            request.args.get("sort") or "Date",
            int(seq),
        ),
    )


@app.route("/assigned/<did>", methods=('GET', 'POST'))
def assigned(did):
    print(did)
    return did


@app.route("/tester")
def usertester():
    return render_template("tester.html")



@app.route("/developer")
def userdeveloper():
    return render_template("developer.html")


@app.route("/leader")
def userleader():
    return render_template("leader.html")


@app.route("/defect_solution", methods=('GET', 'POST'))
def defectsolution():
    if request.method == "POST":
        UserID = request.form["UserID"]
        User_Role = request.form["User_Role"]
        DefectID = request.form["DefectID"]
        Date = request.form["Date"]
        Defect_title = request.form["Defect_title"]
        Defect_desc = request.form["Defect_description"]
        Defect_sol = request.form["Defect_solution"]
        print(request.form)
        solution_defect.insert_one(
            {
                "UserID": UserID,
                "User_Role": User_Role,
                "DefectID": DefectID,
                "Date": Date,
                "Defect_title": Defect_title,
                "Defect_description": Defect_desc,
                "Defect_solution": Defect_sol
            }
        )
        return redirect(url_for("userdeveloper"))
    return render_template("defect_solution.html")


@app.route("/allsolution")
def allsolution():
    seq = request.args.get("seq") or -1
    return render_template(
        "displaysolution.html",
        defects=solution_defect.find({}).sort(
            request.args.get("sort") or "Date",
            int(seq),
        ),
    )


@app.route("/logout", methods=('GET', 'POST'))
def logout():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
