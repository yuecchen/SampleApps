#!/usr/bin/env python3

import random

def sentence_maker():
	s_nouns = ["A dude", "My mother", "The king", "Some guy", "A cat with rabies", "A sloth", "Your homie", "This cool guy my gardener met yesterday", "Superman", "The host, a guy they call Ghost"]
	p_nouns = ["These dudes", "Both of my moms", "All the kings of the world", "Some guys", "All of a cattery's cats", "The multitude of sloths living under your bed", "Your homies", "Like, these, like, all these people", "Supermen"]
	s_verbs = ["eats", "rants", "kicks", "gives", "treats", "meets with", "creates", "hacks", "configures", "spies on", "diminishes", "meows on", "flees from", "tries to automate", "explodes"]
	p_verbs = ["eat", "kick", "give", "treat", "meet with", "create", "hack", "configure", "spy on", "diminish", "meow on", "flee from", "try to automate", "explode"]
	infinitives = ["to wash the car", "to make a pie.", "for no apparent reason.", "because the sky is green.", "for a disease.", "to be able to make toast explode.", "to know more about archeology."]
	sentence_list = random.choice(s_nouns), random.choice(s_verbs), random.choice(s_nouns).lower() or random.choice(p_nouns).lower(), random.choice(infinitives)
	sentence = ' '.join(sentence_list)
	return sentence


print(sentence_maker())
