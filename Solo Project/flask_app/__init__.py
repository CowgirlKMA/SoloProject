from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "2a18f50a1987161345db271c29be6aecc585ff870722e895919864929d4d0aae"