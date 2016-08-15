#!/usr/bin/env python

import os
from names import *
import archetypes
from random import Random

global random, archetypalChars, archetypalEvents, archetypalPlaces, protagonist, protagonistArchetypes

random=Random()
archetypalChars=[]
archetypalEvents={}
archetypalPlaces={}
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
	def __init__(self, beatnum, summary, conflict, d_mood, setting, archetype):
		self.beatnum=beatnum
		self.summary=summary
		self.archetype=archetype
		self.conflict=conflict
		self.d_mood=d_mood
		self.setting=setting
	def getConflict(self):
		return " vs. ".join([self.conflict[0].name(), self.conflict[1].name()])
	def createScene(self):
		header=random.choice(["FADE IN<br>", ""])+random.choice(["INT", "EXT"])+" "+(" ".join([random.choice(self.setting["qualities"]), random.choice(self.setting["names"])]))
		return "<p>"+header+"</p>"+"<center>"+self.genSceneDialogue()+"</center>"
	def genSceneDialogue(self):
		return self.createDialogueBlocks(self.createTemplatedLines())
	def createDialogueBlocks(self, items):
		ax=""
		for item in items:
			ax+="<p>"
			if("action" in item):
				ax+="</center>"+self.fillTemplateLines(item["action"])+"<br><center>"
			if("char" in item):
				ax+=self.conflict[item["char"]].name().upper()+"<br>"
				ax+=self.fillTemplateLines(item["line"])+"<br>"
			ax+="</p>"
		return ax
	def createTemplatedLines(self):
		# XXX template based on each archetype
		if(NATURE in self.conflict or SOCIETY in self.conflict):
			# single- or zero-character path
			if(self.conflict[0]==NATURE or self.conflict[0]==SOCIETY):
				if(self.conflict[1]==NATURE or self.conflict[1]==SOCIETY):
					# zero-character path
					return [{"action":random.choice(self.setting["names"])+" is "+random.choice(self.setting["qualities"])}]
				else:
					return [{"char":1, "line":self.summary+str(self.d_mood)}]
			elif(self.conflict[1]==NATURE or self.conflict[1]==SOCIETY):
				return [{"char":0, "line":self.summary+str(self.d_mood)}]
		elif(self.conflict[0]==self.conflict[1]):
			# XXX single character monologue
			return [{"char":0, "line":self.summary+str(self.d_mood)}]
		else:
			if(self.archetype["names"][0] in normalSceneTemplates):
				if(self.d_mood in normalSceneTemplates[self.archetype["names"][0]]):
					return normalSceneTemplates[self.archetype["names"][0]][self.d_mood]
			return [{"char":0, "line":self.summary}, {"char":1, "line":str(self.d_mood)}]
	def fillTemplateLines(self, line):
		ax=""
		if(type(line)==str):
			return line
		if(type(line)==type([])):
			for el in line:
				res=random.choice(el)
				if(type(res)==str):
					ax+=res
				else:
					ax+=self.fillTemplateLines(res)
		return ax

normalSceneTemplates={}
normalSceneTemplates["arrival"]={}
normalSceneTemplates["arrival"][1]=[
{ "char":0, "action":[["Kicks ground","Whistles"]], "line":[["Well, ",""], [["This ",["sucks", "looks lame"]], "What a promising arrival"]]},
{ "char":1, "line":[["Give it a chance", "You might like it"]]}
]

beatnames={
	"0": "Introductory Scene",
	"3": "State Theme",
	"6": "Call to Action",
	"9": "Break Into II",
	"16": "Fun And Games",
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
		if(len(characters[i].archetype["qualities"])>0):
			print((" "+random.choice(characters[i].archetype["qualities"])))
		print(" "+characters[i].occupation+" and "+random.choice(characters[i].archetype["names"]))
		print("</li>")
	print("</ul></p>")
	print("<p><table border=\"3\">")
	moodArr=[]
	last=0
	for act in beats:
		print("<tr>")
		for beat in act:
			last+=beat.d_mood
			moodArr.append(str(last))
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
	print("</p>")
	os.system("echo \""+(" ".join(moodArr))+"\" |graph -Tpng -X Beats -Y Happiness --auto-abscissa > story-shape.png")
	print("<p><img src=\"story-shape.png\"></p>")
	print("<h3>Screenplay</h3><br><center>")
	print("<p>"+title.upper()+"</p>")
	print("<p>An original screenplay by <a href=\"http://github.com/enkiv2/savethecat\">SaveTheCat</a></p>")
	print("</center>")
	for act in beats:
		for beat in act:
			print(beat.createScene())
	print("FADE OUT")
	print("</body></html>")

def setupArchetypes():
	global archetypalChars, archetypalEvents, protagonistArchetypes
	archetypalEvents["good"]=[]
	archetypalEvents["evil"]=[]
	archetypalEvents["neutral"]=[]
	archetypalPlaces["good"]=[]
	archetypalPlaces["evil"]=[]
	archetypalPlaces["neutral"]=[]
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
	for e in archetypes.settings:
		item={}
		item["names"]=[e["name"]]
		item["names"].extend(e["synonyms"])
		item["qualities"]=e["qualities"]
		item["nature"]=e["nature"]
		archetypalPlaces[e["nature"]].append(item)
	
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
	setting={}
	if(d_mood>0):
		pool=[]
		pool.extend(archetypalEvents["good"])
		pool.extend(archetypalEvents["neutral"])
		event=random.choice(pool)
		pool=[]
		pool.extend(archetypalPlaces["good"])
		pool.extend(archetypalPlaces["neutral"])
		setting=random.choice(pool)
	else:
		pool=[]
		pool.extend(archetypalEvents["evil"])
		pool.extend(archetypalEvents["neutral"])
		event=random.choice(pool)
		pool.extend(archetypalPlaces["evil"])
		pool.extend(archetypalPlaces["neutral"])
		setting=random.choice(pool)
	quality=""
	if(len(event["qualities"])>0):
		quality=random.choice(event["qualities"])
	summary=" ".join([quality, random.choice(event["names"]), "of", conflict[1].name(), "by", conflict[0].name()])
	return Beat(num, summary, conflict, d_mood, setting, event)

def genBeats(characters):
	beats=[]
	for actN in range(0,4):
		act=[]
		for beatN in range(0, 10):
			act.append(genBeat(actN*10+beatN, characters))
		beats.append(act)
	beats[0][0]=genBeat(0, characters, conflict=random.choice([[protagonist, random.choice(characters)], [random.choice(characters), protagonist]]))
	beats[0][6]=genBeat(6, characters, conflict=random.choice([[protagonist, random.choice(characters)], [random.choice(characters), protagonist]]))
	beats[0][9]=genBeat(9, characters, conflict=random.choice([[protagonist, random.choice(characters)], [random.choice(characters), protagonist]]))
	beats[1][9]=genBeat(19, characters, conflict=random.choice([[protagonist, random.choice(characters)], [random.choice(characters), protagonist]]))
	beats[2][7]=genBeat(27, characters, conflict=beats[1][9].conflict)
	beats[2][9]=genBeat(29, characters, d_mood=(-1*beats[2][7].d_mood), conflict=beats[1][9].conflict)
	beats[3][9]=genBeat(39, characters, d_mood=(-1*beats[0][0].d_mood), conflict=random.choice([[protagonist, random.choice(characters)], [random.choice(characters), protagonist]]))
	return beats

def main():
	setupArchetypes()
	
	characters=genCharacters(4)
	beats=genBeats(characters)
	beatSheet2HTML("Title Goes Here", beats, characters)

main()


