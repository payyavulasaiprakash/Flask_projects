from flask import Flask,request,render_template,redirect,url_for,session

app=Flask(__name__)
app.secret_key='hey'
user_notes={}
notes=[]
@app.route("/",methods=['GET','POST'])
def home():
    if request.method=="POST":
        user_name=request.form.get("user_name")
        if user_name in session:
            user_notes[user_name]=notes
        else:
            session[user_name]=user_name
            user_notes[user_name]=[]
        return redirect(url_for("index",user_name=user_name))
        # return render_template("notes.html",user_name=user_name,notes=notes)
    else:
        return render_template("home.html")

@app.route("/add_notes/<user_name>",methods=['GET','POST'])
def index(user_name):
    if request.method=="POST":
        if user_name in session:
            note=request.form.get("note")
            user_notes[user_name].append(note)
            return render_template("notes.html",user_name=user_name,notes=user_notes[user_name])
        else:
            return render_template("home.html")
    else:
        return render_template("notes.html",user_name=user_name,notes=user_notes[user_name])

if __name__=='__main__':
    app.run(debug=True,port=8000)