# import nessacery libraries
import pyttsx3 
import time
from pydub import AudioSegment, silence
from pydub.playback import play
import os

# def removeUnWantedCharackters(text):
# 	modifiedText = []
# 	for paragraph in text:
# 		paragraph = paragraph.replace(",","")
# 		paragraph = paragraph.replace(".","")
# 		paragraph = paragraph.replace(";","")
# 		paragraph = paragraph.replace("\"","")
# 		modifiedText.append(paragraph)
# 	return modifiedText

# function make a list from the text by spliting sentances 
# if the sentance is keyword it put it alone and if not it put it apart 
# even index for original sentances and oneven for keywords
def keyWordOrNot(text):
    textToList = []
    for paragraph in text:
        paragraphToList = []
        sentance = ""
        
        for letter in paragraph:
            if letter == "{":
                if sentance.strip():  # Avoid adding empty sentences
                    paragraphToList.append(sentance.strip())
                sentance = "{"
            elif letter == "}":
                sentance += "}"
                print (sentance)
                paragraphToList.append(sentance.strip())
                sentance = ""
            else:
                sentance += letter
        
        if sentance.strip():  # Add any remaining sentence
            paragraphToList.append(sentance.strip())
        
        textToList.append(paragraphToList)

    return textToList

# combine the audio files 
# the used library does not have the ability to change voice variables of particular word in the text thus 
# it is been changed while moving in the text and combine the audio files 
# 
# reference: https://deepgram.com/learn/best-python-audio-manipulation-tools

def combineAudioFiles():
	sound1 = AudioSegment.from_wav("withVariablesChanges.wav")
	sound2 = AudioSegment.from_wav("temp.wav")

	combined = sound1 + sound2

	# play(combined)
	combined.export("withVariablesChanges.wav", format="wav")

# when combining audio files there still some silence the end of the audio thus the silence between the words in the complete 
# audio file is greate thus this function te decrease this silence (this function is made with the help of chatGPT)
def trim_silence(audio, target_silence_ms=50):
    """
    Reduce the leading and trailing silence of an audio segment to a target length.
    """
    non_silent_ranges = silence.detect_nonsilent(audio, min_silence_len=200, silence_thresh=-40)
    if non_silent_ranges:
        start_trim = max(0, non_silent_ranges[0][0] - target_silence_ms)
        end_trim = min(len(audio), non_silent_ranges[-1][1] + target_silence_ms)
        return audio[start_trim:end_trim]
    return audio

# turn text to speech (for text with keywords)
# https://python.plainenglish.io/exploring-text-to-speech-in-python-with-pyttsx3-a50d14b6b805
# https://pyttsx.readthedocs.io/_/downloads/en/stable/pdf/
def speakTextKeyWords(text):
	text = keyWordOrNot(text)
	# Initialize the engine
	engine = pyttsx3.init()
	voiceId = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"

	engine.setProperty('voice', voiceId)

	# the speech rate of full text is been modified to be less speed because, the defualt is to fast
	engine.setProperty("rate", 150)
	engine.save_to_file("", "withVariablesChanges.wav")
	# engine.say("hallo")
	for paragraph in text:
		for sentanceIndex in range(len(paragraph)):
			# the sentance is not keyword
			if sentanceIndex %2 == 0:
				# same as default installings
				engine.setProperty("rate", 150)
				engine.setProperty("pitch", 0.0)

				engine.save_to_file(paragraph[sentanceIndex], f'temp.wav')
				engine.runAndWait()

				temp = AudioSegment.from_wav("temp.wav")
				temp = trim_silence(temp, 200)
				temp.export("temp.wav", format="wav")

				combineAudioFiles()

			else:
				engine.setProperty("rate", 100)
				engine.setProperty("pitch", 0.0)

				engine.save_to_file(paragraph[sentanceIndex], f'temp.wav')
				engine.runAndWait()

				temp = AudioSegment.from_wav("temp.wav")
				temp = trim_silence(temp)
				temp.export("temp.wav", format="wav")

				combineAudioFiles()


	theCompination = AudioSegment.from_mp3("withVariablesChanges.wav")
	theCompination.export("withVariablesChanges.mp3", format="mp3")

	try:
		os.remove("temp.wav")
		os.remove("withVariablesChanges.wav")
	except:
		pass 



def SpeakTextOrginal(text):
	
	# Initialize the engine
	engine = pyttsx3.init()
	voiceId = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
	
	engine.setProperty('voice', voiceId)
	
	# the speech rate of full text is been modified to be less speed because, the defualt is to fast
	engine.setProperty("rate", 150)
	# wholeText = ""
	# for x in text:
	# 	wholeText += x + " "
	engine.save_to_file(text, 'defaultTextNewSharks.mp3')
	engine.runAndWait()

introduction = """Hallo everyone! Today, we're going to dive deep into the fascinating world of {sharks}. These incredible creatures have roamed the oceans for over {400 million years}, long before the dinosaurs walked the earth. Sharks are often misunderstood and feared, but they play a crucial role in maintaining the health of our marine ecosystems. Over the next minutes, we’ll explore some interesting facts about them."""
evolutionAndDiversity = """Sharks belong to the class {Chondrichthyes}, which includes rays and skates. There are over {500 species} of sharks, ranging from the tiny {dwarf lanternshark}, which is only about {20 centimeter} long, to the massive {whale shark}, the largest fish in the ocean, reaching lengths of up to {12 meter} Sharks have evolved over hundreds of millions of years, adapting to various marine environments. This evolutionary history is evident in their diverse forms and functions. For example, {the hammerhead shark's} unique head shape allows for better {sensory perception}, while the streamlined body of {the great white shark} makes it an {efficient predator}."""
anatomyAndPhysiology = """Sharks are built for survival. Their skeletons are made of {cartilage}, which is {lighter} and more {flexible than bone}. This adaptation makes them agile swimmers. Sharks typically have multiple rows of teeth, with the number of rows varying by species. On average, most sharks have {5 to 15 rows of teeth} in each {jaw}. Some species, like {the bull shark}, may have as many as {50 rows of teeth} , which are continually replaced throughout their lives. Some species can shed thousands of teeth over a lifetime, ensuring they always have sharp tools for hunting. One of the most remarkable features of sharks is their {sensory system}. 
"""
anatomyAndPhysiology = """They have an acute sense of {smell}, capable of detecting blood from {kilometers} away. Additionally, sharks have {the ampullae of Lorenzini}, which are {electroreceptor} organs that allow them to sense the electrical fields produced by other organisms. This ability is particularly useful for hunting in murky waters where visibility is low. Sharks also have excellent {hearing}, which can detect prey from significant distances. Their lateral line system, a series of sensitive receptors along their sides, helps them detect {vibrations} and {movements} in the water, adding another layer to their predatory capabilities."""
humanInteractionAndConservation = """Despite their importance, many shark species are facing significant {threats} due to human activities. Overfishing, bycatch, and the demand for{shark fin soup} have led to dramatic declines in shark populations worldwide. Approximately {100 million} sharks are killed {each year}, with many species now listed as endangered or vulnerable. Additionally, habitat destruction and pollution further threaten their survival. Coral reefs, mangroves, and seagrass beds, which are essential habitats for many shark species, are being degraded at alarming rates. Marine pollution, especially{plastic waste,} can also be harmful, leading to ingestion and entanglement."""
fascinatingFactsAndLesser_KnownSpecies = """Now, let's explore some fascinating facts about sharks and highlight some {lesser}-known species. Did you know that some sharks can live for {centuries} The {Greenland shark}, for example, can live up to {400 years}, making it one of the longest-living vertebrates on the planet. {The goblin shark}, with its distinctive protruding snout and pink coloration, is another intriguing species. It inhabits {deep waters} and is rarely seen by humans. {The frilled shark}, often referred to as a "{living fossil}," has a primitive eel-like appearance and is thought to have changed little since prehistoric times. {The wobbegong shark}, also known as the {carpet shark}, has excellent camouflage and lies motionless on the ocean floor, waiting to ambush prey. These examples illustrate the incredible diversity and adaptability of sharks, which have enabled them to survive in various environments around the world."""
conclusion = """Sharks are truly remarkable creatures, integral to the health of our oceans. By understanding and appreciating their role in the marine ecosystem, we can better advocate for their protection and ensure that they continue to thrive for generations to come. Thank you for your attention. I hope this lecture has provided you with a deeper insight into the world of sharks and the importance of their conservation."""

text = [introduction, evolutionAndDiversity, anatomyAndPhysiology, humanInteractionAndConservation, fascinatingFactsAndLesser_KnownSpecies, conclusion]
# print (text)
	

SpeakTextOrginal(text)
speakTextKeyWords(text)