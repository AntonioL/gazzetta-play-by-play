from multiprocessing import Lock

class EventNotifier:

	def notify(self, players, event, play):
		pass

class ConsoleNotifier(EventNotifier):

	def __init__(self):
		EventNotifier.__init__(self)

	def notify(self, players, event, play):
		print("========================")
		print("{} minute || {} - {} || {}".format(play['minuto'], event['teamHome']['name'], event['teamAway']['name'], ', '.join(players)))
		print("------------------------")
		print(play['messaggio'].replace(u'\u200b', ''))