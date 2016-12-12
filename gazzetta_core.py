import time, math, requests, json

BASE_URL = "http://xml2.temporeale.gazzettaobjects.it/trsport/tempo-reale/json"

#Get all the matches of today
def get_today_matches():
	global BASE_URL
	#1. Build the URL
	url = "{}/{}/{}-events.json?_={}".format(BASE_URL, "calendario-eventi", time.strftime("%Y%m%d"), math.floor(time.time()))
	#2. Make the request
	r = requests.get(url)
	#3. The beautiful of it
	doc = json.loads(r.text)
	for competition in doc['competizione']:
		if competition['disciplina'] != 'calcio': continue
		for event in competition['eventi']:
				#(event, competition)
				yield (event, competition)

def matches_terminated(ids):
	for (match, _) in get_today_matches():
		if match['id'] in ids and match['status'] == 'LIVE': return False
	return True

class Gazzetta_PlayByPlay:

	def __init__(self, event, competition, players, notifier):
		self.event = event
		self.competition = competition
		self.players = players
		self.notifier = notifier

	def pbp_url(self):
		return "{}/{}/{}/{}/{}/cronaca.json?_={}".format(BASE_URL, "calcio", time.strftime("%Y"), self.competition['id'], self.event['id'], math.floor(time.time()))

	def __call__(self):
		messages = set()
		while True:
			r = requests.get(self.pbp_url())
			doc = json.loads(r.text)
			for play in doc["cronacaJson"][::-1]:
				if play['idMessaggio'] in messages: continue
				messages.add(play['idMessaggio'])
				involved = []
				for player in self.players:
					if player in play['messaggio']: involved.append(player)
				if len(involved):
					self.notifier.notify(involved, self.event, play)
			time.sleep(45)