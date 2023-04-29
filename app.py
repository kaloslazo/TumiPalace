from flask import(
    Flask,
    render_template,
);
from flask_sqlalchemy import SQLAlchemy;
from flask_migrate import Migrate;


# ===: General config
app = Flask(__name__); # app.py works as flask instance.
db = SQLAlchemy(app);


# ===: Routes
@app.route('/', methods=['GET'])
def main():
    return render_template('index.html');


# ===: Main flow
if __name__ == "__main__":
    app.run(debug=True);
    print("App running.");
else:
    print("Error.");