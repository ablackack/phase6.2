import sqlite3
import csv
import json


class Database(object):

	def __init__(self, db):
		# Initializing the needed variables and objects for the database connection
		self.con = sqlite3.connect(db)
		self.cur = self.con.cursor()

	def get_config(self):
		confdict = ""
		with open("config.json", "r") as conf:
			confdict = json.load(conf)
			conf.close()

		return confdict

	def delete_table(self, table):
		format_str = """DROP TABLE {tab}"""
		command = format_str.format(tab=table)
		self.cur.execute(command)
		self.con.commit()

	def create_table(self, tablename):
		format_str = """
				CREATE TABLE IF NOT EXISTS {name} (
						id INTEGER PRIMARY KEY,
						question VARCHAR(100),
						answer VARCHAR(100),
						add_info VARCHAR(50),
						phase INTEGER,
						created DATE,
						asked DATE);"""
		command = format_str.format(name=tablename)
		self.cur.execute(command)
		self.con.commit()

	def migrate_phase6_csv(self, csvfile, delimiter):
		with open(csvfile, "r") as csvf:
			reader = csv.reader(csvf, delimiter=delimiter)
			csvlist = list(reader)

		for p in csvlist:
			format_str = """SELECT name FROM sqlite_master WHERE type="table" AND name="{tab}";"""
			command = format_str.format(tab=p[2])
			if self.cur.execute(command) == '':
				self.create_table(p[2])

			format_str = """INSERT INTO {tab} (id, question, answer, add_info, phase, created, asked)
				VALUES (NULL, "{que}", "{ans}", "{inf}", "{pha}", "{cre}", "{ask}");"""
			command = format_str.format(tab=p[2], que=p[0], ans=p[1], inf=p[3], pha=p[5], cre=p[6], ask=p[7])
			self.cur.execute(command)

		conf = self.get_config()
		result = self.cur.fetchall()
		for r in result:
			# TODO: Chnaging Date from last asked to next questioning
			element_id = r[4]
			lastQues = r[6]

			print(element_id, lastQues)

		self.con.commit()

	def get_question(self):
		# Getting all all questions due today
		questions = []
		result = self.cur.fetchall()
		for r in result:
			if r.

