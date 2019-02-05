from flask import Flask, render_template ,session, escape, request, Response
from flask import url_for, redirect, send_from_directory, jsonify
from flask import send_file, make_response, abort
import os, sys
import json

app = Flask(__name__)
app.secret_key="green_coders_app"

from connector import Manager 
manager = Manager()

@app.route('/')
def basic_pages(**kwargs):
    return make_response(open('main.html').read())

@app.route('/getAllBasicQuestions', methods=['POST'])
def getAllBasicQuestions():
    return manager.getBasicQuestions(), 200, {'Content-Type': 'application/json'}

@app.route('/saveAllAnswers', methods=['POST'])
def saveAllAnswers():
    answers = request.json['answers']
    return manager.saveAllAnswers(answers.split(',')), 200, {'Content-Type':'application/json'}

@app.route('/pauseAnswering', methods=['POST'])
def pauseAnswering():
    answers = request.json['answers']
    return manager.pauseAnswering(answers.split(',')), 200, {'Content-Type':'application/json'}

@app.route('/continue', methods=['POST'])
def cont():
    id = request.json["id"]
    return manager.contd(id), 200, {'Content-Type':'application/json'}

@app.route('/generate',methods=['POST'])
def generate():
    path = manager.generate()
    response = send_from_directory(directory='/root/greencoders/',filename='greencoders.csv')
    return response
    

if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 5000)))
