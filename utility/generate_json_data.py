#!/usr/bin/env python3

import random

FILENAME = "photodata.txt"
MAX_ALBUMID = 100
MAX_ID = 6001

def random_alphanum():
        return ''.join(random.choice('0123456789abcded') for i in range(6))

def sentence_maker():
        s_nouns = ["A dude", "My mother", "The king", "Some guy", "A cat with rabies", "A sloth", "Your homie", "This cool guy my gardener met yesterday", "Superman", "The host, a guy they call Ghost", "Henry Ford", "Al Kaline", "Gordie Howe", "The cross species Chimera", "Babe Ruth", "Loni Anderson", "The incredible hulk", "Digital Pig Snuggler"]
        p_nouns = ["These dudes", "Both of my moms", "All the kings of the world", "Some guys", "All of a cattery's cats", "The multitude of sloths living under your bed", "Your homies", "Like, these, like, all these people", "Supermen", "Pack of dudes", "Drunken mob", "Crew of the USS Enterprise", "1968 Detroit Tigers"]
        s_verbs = ["eats", "rants", "kicks", "gives", "treats", "meets with", "creates", "hacks", "configures", "spies on", "diminishes", "meows on", "flees from", "tries to automate", "explodes", "spreads it around like wildfire", "hands", "deletes", "flies", "lopes"]
        p_verbs = ["eat", "kick", "give", "treat", "meet with", "create", "hack", "configure", "spy on", "diminish", "meow on", "flee from", "try to automate", "explode", "devastate"]
        infinitives = ["to wash the car", "to make a pie", "for no apparent reason", "because the sky is green", "for a disease", "to be able to make toast explode", "to know more about archeology", "as the Whole World Wonders", "because she said so", "to swab the deck", "for a view"]
        sentence_list = random.choice(s_nouns), random.choice(s_verbs), random.choice(s_nouns).lower() or random.choice(p_nouns).lower(), random.choice(infinitives)
        sentence = ' '.join(sentence_list)
        return sentence

FILE = open(FILENAME, 'w')
print("Generating photo data with %d records" % MAX_ID)

album_count = 1
album_id = 1

#print("[")
FILE.write("[\n")
for x in range(1, MAX_ID):
	#print("  {")
	FILE.write("  {\n")
	#if album_count <= MAX_ALBUMID:
	if album_count < MAX_ALBUMID:
		album_count += 1
	else:
		album_count = 1
		album_id += 1
	#print('   "albumId": %d,' % album_id)
	FILE.write('   "albumId": %d,\n' % album_id)
	#print('   "Id": %d,' % x)
	FILE.write('   "Id": %d,\n' % x)
	#print('   "title": "'+sentence_maker()+'",')
	FILE.write('   "title": "'+sentence_maker()+'",\n')
	#print('   "url": "http://placeholder.org/'+str(album_id)+'00/'+random_alphanum()+'",') 
	FILE.write('   "url": "http://placeholder.org/'+str(album_id)+'00/'+random_alphanum()+'",\n') 
	#print('   "thumbnailUrl": "http://placeholder.org/'+str(album_id)+'00/'+random_alphanum()+'.jpg",') 
	FILE.write('   "thumbnailUrl": "http://placeholder.org/'+str(album_id)+'00/'+random_alphanum()+'.jpg",\n') 
	#print("  },")
	FILE.write("  },\n")
#print("]")
FILE.write("]\n")
FILE.close()
