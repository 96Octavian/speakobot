#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

from telepot.loop import MessageLoop
from googleapiclient.discovery import build
import sys
import telepot
from telepot.delegate import per_inline_from_id, create_open, pave_event_space
import emoji
import sys
import time
import telepot
import json
import datetime
import logging
import argparse

"""
Inline translating bot
"""

# Deafults
LOG_FILENAME = './logspeakobot.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,format='%(asctime)s %(levelname)-8s %(message)s')

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="An inline translation bot")
parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")
parser.add_argument("-T", "--TOKEN", help="bot TOKEN identifier")

logger = logging.getLogger(__name__)

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
	def __init__(self, logger, level):
		#Needs a logger and a logger level.
		self.logger = logger
		self.level = level

	def write(self, message):
		# Only log if there is a message (not just a new line)
		if message.rstrip() != "":
			self.logger.log(self.level, message.rstrip())

# Replace stdout with logging to file at INFO level
#sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)

# If the log file is specified on the command line then override the default
args = parser.parse_args()
if args.log:
	LOG_FILENAME = args.log
# Check if the bot's TOKEN is given
if args.TOKEN:
	TOKEN = args.TOKEN
else:
	logging.error('No TOKEN specified. Abort')
	logging.info("You must specify the bot's TOKEN")
	sys.exit(0)

class InlineHandler(telepot.helper.InlineUserHandler, telepot.helper.AnswererMixin):
	def __init__(self, *args, **kwargs):
		super(InlineHandler, self).__init__(*args, **kwargs)

	def on_inline_query(self, msg):
		def compute_answer():
			query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
			print(self.id, ':', 'Inline Query:', query_id, from_id, query_string)

			articles = [{'type': 'article',
						'id': 'abc', 'title': query_string, 'message_text': query_string}]

			self.service = build('translate', 'v2',
				developerKey='AIzaSyDRRpR3GS1F1_jKNNM9HCNd2wJQyPG3oN0')
			print(self.service.translations().list(
				source='it',
				target='en',
				q=[query_string]
				).execute())

			return articles

		self.answerer.answer(msg, compute_answer)

	def on_chosen_inline_result(self, msg):
		from pprint import pprint
		pprint(msg)
		result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
		print(self.id, ':', 'Chosen Inline Result:', result_id, from_id, query_string)

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_inline_from_id(), create_open, InlineHandler, timeout=10),
])
#bot.message_loop(run_forever='Listening ...')

MessageLoop(bot).run_as_thread()

bot.sendMessage('66441008', 'Up and running')
logging.info('Bot started.')

# Keep the program running.
while 1:
    time.sleep(10)