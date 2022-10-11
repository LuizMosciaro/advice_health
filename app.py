import uuid
from flask import Flask,request,render_template,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key = "my-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///person.sqlite3"

db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column("id",db.Integer,primary_key=True,autoincrement=True)
    client = db.Column(db.String(150))
    model = db.Column(db.String(150))
    color = db.Column(db.String(50))

    def __init__(self,client,color,model):
        self.client = client
        self.model = model
        self.color = color

USER_DATA = {
    "admin":"123"
}

@app.get("/")
@app.get("/index")
def index():
    sistema = "Sales Management System"
    shop = "Carford Carshop"
    name = "Luiz Mosciaro"
    return render_template("index.html",sistema=sistema,shop=shop,name=name)

@app.get("/contato")
def contato():
    name = "Luiz Mosciaro"
    telefone = " +55 (92) 99275-4311"
    email = "edu.mosciaro@live.com"
    github = "https://github.com/LuizMosciaro"
    linkedin = "https://www.linkedin.com/in/luizmosciaro/"
    return render_template("contato.html",telefone=telefone,email=email,github=github,linkedin=linkedin,name=name)

@app.route("/autenticar",methods=["POST","GET"])
def autenticar():
    if request.method =="POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        shop = "Carford Carshop"
        name = "Luiz Mosciaro"
        person = Person.query.all()
        if usuario == "admin" and senha == "123":
            return render_template("table.html",shop=shop,name=name,person=person)
        else:
            flash("\nErro: Login Invalido")
            return redirect("/index")

@app.route("/add",methods=["POST","GET"])
def add():
    name = "Luiz Mosciaro"
    if request.method =="POST":
        client = request.form['client']
        if client:
            sales_opt = request.form.get("sale-avaiable")
            if sales_opt is None:
                flash(f"\nWarning: Sale Opportunity not avaiable for client {client}")
                return redirect("/index")
            model = request.form['model']
            color = request.form['color']
            person = Person(client=client,model=model,color=color)
            db.session.add(person)
            db.session.commit()
            flash(f"\nClient:{client} registred")
            return redirect(url_for("index"))
        
        else:
            flash("\nErro: Person's name required")
            return redirect("/index")
    return render_template("add.html",name=name)

@app.route("/delete/<int:id>")
def delete(id):
    person = Person.query.get(id)
    db.session.delete(person)
    db.session.commit()
    flash(f"\nClient ID {id} deleted")
    return redirect(url_for("index"))


if __name__=="__main__":
    app.run(debug=True)
    db.session.commit()
    db.create_all()
