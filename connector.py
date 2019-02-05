import sys, os
from flask import Flask, jsonify, request
from bson.objectid import ObjectId
import pymongo
from pymongo import MongoClient
from flask import Flask, jsonify, request
from datetime import datetime
from datetime import timedelta
import uuid
import dateutil.parser as parser
import hashlib
import csv, time

client = MongoClient('localhost', 27017)
mongo = client.greencoders

class Manager:
	def getBasicQuestions(self):
		data = mongo.questions
		query = {}
		#query[''] = ''
		questionList = {}
		i = 1 
		for q in data.find(query).sort('number',pymongo.ASCENDING):
			question = {}
			question['q'] = q['question']
			question['n'] = q['number']
			question['c'] = q['choice']
			question['t'] = q['type']
			questionList['q'+str(i)] = question
			i = i + 1	
                #f = open("demofile.txt", "w")
                #f.write(str({'status':'success','result':questionList}))
                return jsonify({'status':'success','result':questionList})	

	def saveAllAnswers(self, answers):
		data = mongo.answers
		json = {}
		i = 0
		while i < len(answers):
			que = 'question'+str(i+1)
			json[que] = answers[i]
			i = i + 1
		print(json)
		if data.insert(json):
			return jsonify({'status':'success'})
		else:
			return jsonify({'status':'failed'})

        def pauseAnswering(self, answers):
                data = mongo.pause
                json = {}
                i = 0
                while i < len(answers):
                    que = 'question'+str(i+1)
                    json[que] = answers[i]
                    i = i + 1
                saveId = data.insert(json)
                print(saveId)
                if saveId:    
                    return jsonify({'status':'success','saveId': 'http://51.75.249.196:5000/?continue='+str(saveId)})
                else:
                    return jsonify({'status': 'failed'})

        def contd(self, id):
                data = mongo.pause
                query = {}
                query['_id'] = ObjectId(id)
                new_data = data.find_one(query)
                del new_data['_id']
                output = {'status' : 'success', 'data': new_data}
                return jsonify(output)

        def generate(self):
                data = mongo.answers
                json = []
                i = 0
                questions = mongo.questions
                questArr = []
                for quest in questions.find({}).sort('number',pymongo.ASCENDING):
                    questArr.append(quest['question'].encode('utf-8').strip())
                json.append(questArr)
                for q in data.find({}):
                    arr = []
                    for x in range(0,88):
                        question = 'question' + str(x+1)
                        arr.append(q[question])
                    json.append(arr)
                myFile = open('greencoders.csv','w')
                with myFile:
                    writer = csv.writer(myFile)
                    writer.writerows(json)
                return 'abc.csv'
