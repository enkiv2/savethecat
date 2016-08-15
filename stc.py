#!/usr/bin/env python

from names import *
import archetypes
from random import Random

global random, archetypalChars, archetypalEvents, protagonist, protagonistArchetypes

random=Random()
archetypalChars=[]
archetypalEvents={}
protagonist=None
protagonistArchetypes=[]


class Character:
	def __init__(self, fname, lname, archetype):
		self.fname=fname
		self.lname=lname
		self.archetype=archetype
		self.mood=0
		self.occupation=""
	def name(self):
		return " ".join([self.fname, self.lname])

inhumanForceArchetype={"names":["force of nature"], "qualities":["vast", "inhuman"], "nature":"neutral"}
NATURE=Character("Nature", "", inhumanForceArchetype )
SOCIETY=Character("Society", "", inhumanForceArchetype )

class Beat:
	def __init__(self, beatnum, summary, conflict, d_mood):
		self.beatnum=beatnum
		self.summary=summary
		self.conflict=conflict
		self.d_mood=d_mood
	def getConflict(self):
		return " vs. ".join([self.conflict[0].name(), self.conflict[1].name()])

beatnames={
	"0": "Introductory Scene",
	"9": "Break Into II",
	"19": "Midpoint",
	"26": "All Is Lost",
	"29": "Break Into III",
	"39": "Final Scene"
}

def beatSheet2HTML(title, beats, characters):
	mood2mood={}
	mood2mood[-1]="-"
	mood2mood[1]="+"
	print("<html><head><title>"+title+"</title></head>")
	print("<body>")
	print("<h1>"+title+"</h1><br>")
	print("<h3>Plots</h3><br>")
	print("<p><b>A-plot:</b> "+beats[0][0].summary+". "+beats[1][9].summary+", but "+beats[2][9].summary+"</p><br>")
	print("<p><b>B-plot:</b> "+beats[1][0].summary+". "+beats[1][5].summary+", but "+beats[2][5].summary+"</p><br>")
	print("<p><h3>Dramatis Personae</h3><br>")
	print("<ul>")
	for i in range(2, len(characters)):
		print("<li>")
		print("<b>"+characters[i].name()+"</b>: ")
		print((" ".join(characters[i].archetype["qualities"])))
		print(" "+characters[i].occupation+" and "+random.choice(characters[i].archetype["names"]))
		print("</li>")
	print("</ul></p>")
	print("<p><table>")
	for act in beats:
		print("<tr>")
		for beat in act:
			print("<td>")
			
			print("<b>")
			print(beat.beatnum+1)
			if(str(beat.beatnum) in beatnames):
				print(": "+beatnames[str(beat.beatnum)])
			print("</b><br>")
			
			print(beat.summary+"<br>+/-: "+mood2mood[beat.d_mood]+"<br>&gt;&lt;: "+beat.getConflict())
			
			print("</td>")
		print("</tr>")
	print("</table>")
	print("</body></html>")

def setupArchetypes():
	global archetypalChars, archetypalEvents, protagonistArchetypes
	archetypalEvents["good"]=[]
	archetypalEvents["evil"]=[]
	archetypalEvents["neutral"]=[]
	for c in archetypes.characters:
		item={}
		item["names"]=[c["name"]]
		item["names"].extend(c["synonyms"])
		item["qualities"]=c["qualities"]
		item["nature"]=c["nature"]
		archetypalChars.append(item)
		if(c["name"] in ["hero", "anti-hero", "fool", "child", "self", "dreamer", "leader", "everyman", "poet", "rebel", "survivor"]):
			protagonistArchetypes.append(item)
	for e in archetypes.events:
		item={}
		item["names"]=[e["name"]]
		item["names"].extend(e["synonyms"])
		item["qualities"]=e["qualities"]
		item["nature"]=e["nature"]
		archetypalEvents[e["nature"]].append(item)
	
def genCharacter():
	ch=Character(random.choice(firstNames), random.choice(lastNames), random.choice(archetypalChars))
	ch.occupation=random.choice(occupations)
	return ch

def genCharacters(num):
	global protagonist
	protagonist=Character(random.choice(firstNames), random.choice(lastNames), random.choice(protagonistArchetypes))
	protagonist.occupation=random.choice(occupations)
	chars=[NATURE, SOCIETY, protagonist]
	for i in range(0, num):
		chars.append(genCharacter())
	return chars

def genBeat(num, characters, d_mood=None, conflict=None):
	if(conflict==None):
		conflict=[random.choice(characters), random.choice(characters)]
	if(d_mood==None):
		d_mood=random.choice([1, -1])
		if(conflict[0].archetype["nature"]=="good" and conflict[1].archetype["nature"]=="evil"):
			d_mood=1
		if(conflict[1].archetype["nature"]=="good" and conflict[0].archetype["nature"]=="evil"):
			d_mood=-1
	event={}
	if(d_mood>0):
		pool=[]
		pool.extend(archetypalEvents["good"])
		pool.extend(archetypalEvents["neutral"])
		event=random.choice(pool)
	else:
		pool=[]
		pool.extend(archetypalEvents["evil"])
		pool.extend(archetypalEvents["neutral"])
		event=random.choice(pool)
	quality=""
	if(len(event["qualities"])>0):
		quality=random.choice(event["qualities"])
	summary=" ".join([quality, random.choice(event["names"]), "of", conflict[1].name(), "by", conflict[0].name()])
	return Beat(num, summary, conflict, d_mood)

def genBeats(characters):
	beats=[]
	for actN in range(0,4):
		act=[]
		for beatN in range(0, 10):
			act.append(genBeat(actN*10+beatN, characters))
		beats.append(act)
	beats[0][0]=genBeat(0, characters, conflict=random.choice([[protagonist, random.choice(characters)], [random.choice(characters), protagonist]]))
	beats[1][9]=genBeat(0, characters, conflict=random.choice([[protagonist, random.choice(characters)], [random.choice(characters), protagonist]]))
	beats[2][7]=genBeat(0, characters, conflict=beats[1][9].conflict)
	beats[2][9]=genBeat(0, characters, d_mood=(-1*beats[2][7].d_mood), conflict=beats[1][9].conflict)
	beats[3][9]=genBeat(39, characters, d_mood=(-1*beats[0][0].d_mood), conflict=random.choice([[protagonist, random.choice(characters)], [random.choice(characters), protagonist]]))
	return beats

def main():
	setupArchetypes()
	
	characters=genCharacters(10)
	beats=genBeats(characters)
	beatSheet2HTML("Title Goes Here", beats, characters)

main()


