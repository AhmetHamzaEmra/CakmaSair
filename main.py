from __future__ import absolute_import, division, print_function
import time 
import os
import pickle
import tweepy
from six.moves import urllib

import tflearn
from tflearn.data_utils import *

char_idx_file = 'char_idx.pickle'
maxlen = 30
print('Loading previous char_idx')
char_idx = pickle.load(open(char_idx_file, 'rb'))

g = tflearn.input_data([None, maxlen, len(char_idx)])
g = tflearn.lstm(g, 512, return_seq=True)
g = tflearn.dropout(g, 0.5)
g = tflearn.lstm(g, 512, return_seq=True)
g = tflearn.dropout(g, 0.5)
g = tflearn.lstm(g, 512)
g = tflearn.dropout(g, 0.5)
g = tflearn.fully_connected(g, len(char_idx), activation='softmax')
g = tflearn.regression(g, optimizer='adam', loss='categorical_crossentropy',
                       learning_rate=0.001)

model = tflearn.SequenceGenerator(g, dictionary=char_idx,
                              seq_maxlen=maxlen,
                              clip_gradients=5.0)


model.load("cakmasair/14.tflearn")
print("Model is ready!")


def generate_poem(start_string):
	start_string = "               <start>" + start_string

	generated = model.generate(200, temperature=0.5, seq_seed=start_string[-30:])

	return generated.replace(start_string[-30:], " ")




auth = tweepy.OAuthHandler('XXXXXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXXXXXXXXXXX')
auth.set_access_token("XXXXXXXXXXXX-XXXXXXXXXXXX", "XXXXXXXXXXXXXXXXXXXXXXXX")
api = tweepy.API(auth)

mentions = api.mentions_timeline()
num_tweets = api.user_timeline()

print(len(mentions)-len(num_tweets))


while True:

	users = []
	
	then = time.time()

	print("Reset Time!")

	while True:


		mentions = api.mentions_timeline()
		num_tweets = api.user_timeline()

		num_unreplied = len(mentions)-len(num_tweets)
		print(num_unreplied)
		for m in mentions[:num_unreplied]:
			id_num = m.user.id
			if id_num in users:
				reply = "@" + m.user.screen_name +" You already use your limit please try again later!"
				try:
				    api.update_status(reply, m.id)
				except tweepy.error.TweepError:
				    pass
				
				
			else:
				users.append(id_num)
				start_ = m.text
				start_ = start_.replace("@Cakma_Sair", "")
				poem = generate_poem(start_)
				poem = "@" + m.user.screen_name + " " + start_ + poem

				try:
				    api.update_status(poem, m.id)
				except tweepy.error.TweepError:
				    pass
				


		# time to reset (1 min now)
		time.sleep(30)

		if ((time.time()-then) // 60) == 5:
			break

