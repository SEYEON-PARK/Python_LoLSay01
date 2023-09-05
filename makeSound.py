from gtts import gTTS
from playsound import playsound

text ="우리팀이 1점 얻었어요." # 텍스트 문자열

tts = gTTS(text=text, lang='ko')
tts.save("./sound/addOnePoint.mp3")
playsound("./sound/addOnePoint.mp3")


'''
from gtts import gTTS
from playsound import playsound

text ="상대팀이 1점 얻었어요."
text = text.encode('utf-8')

tts = gTTS(text=text, lang='ko')
tts.speed = 1.8
tts.save("./sound/addRedTeamOnePoint.mp3")
playsound("./sound/addRedTeamOnePoint.mp3")

'''
