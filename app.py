from multiprocessing import Process, Lock, Value
from multiprocessing.managers import BaseManager
from gazzetta_core import *
from notifier import *
import time, sys

if __name__ == '__main__':
	teams_to_track = {}
	while True:
		inp = input()
		if len(inp.strip()) == 0: break
		(player, team) = inp.split("|")
		if team not in teams_to_track: teams_to_track[team] = []
		teams_to_track[team].append(player)

	matches_to_track = []

	processes = []

	BaseManager.register('Notifier', ConsoleNotifier)
	m = BaseManager()
	m.start()

	#Have to investigate whether access to the notifiers are synchronized from the BaseManager
	#It is not clear from the Python documentation the concurrent model of the BaseManager.
	notifier = m.Notifier()

	for (event, competition) in get_today_matches():
		#if event['status'] != 'LIVE': continue
		players = []
		if event['teamHome']['name'] in teams_to_track: players += teams_to_track[event['teamHome']['name']]
		if event['teamAway']['name'] in teams_to_track: players += teams_to_track[event['teamAway']['name']]
		if len(players):
			if len(matches_to_track) == 0:
				print("Tracked matches:")
			matches_to_track.append(event['id'])
			#This needs to be fixed since the notifier is shared but the object is not exactly
			#designed to be shared. I need to use the Manager.
			p = Process(target=Gazzetta_PlayByPlay(event, competition, players, notifier))
			p.daemon = True
			processes.append(p)
			print("\t{} - {}".format(event['teamHome']['name'], event['teamAway']['name']))

	if len(matches_to_track):

		for p in processes:
			p.start()

		time.sleep(60)

		while not(matches_terminated(matches_to_track)):
			time.sleep(300)

		sys.exit(1)
	else:
		print("No match of interest to track")