from flask import Flask, render_template, request, url_for

app = Flask(__name__)
from app import views
