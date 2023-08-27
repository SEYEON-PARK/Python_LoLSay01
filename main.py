import cv2
import cv2 as cv
from gtts import gTTS # 구글 TTS 서비스 이용하기 위해
import torch # 토치 추가
import numpy as np
import time
import matplotlib.pyplot as plt
import math
import os
import subprocess
from playsound import playsound # 소리를 실행하기 위해해
from PIL import Image



filepath = './02.webm'
video = cv2.VideoCapture(filepath) #'' 사이에 사용할 비디오 파일의 경로 및 이름을 넣어주도록 함
# video.set(cv2.CAP_PROP_POS_FRAMES, 30000)
# good_audio_path = 'audio.mp3'
# bad_audio_path = 

fps = video.get(cv2.CAP_PROP_FPS)
avg_color1=41 # 우리팀_3번(2번 인덱스)
avg_color2=43 # 우리팀_17번(16번 인덱스)
avg_color3=40 # 상대팀_17번(16번 인덱스)
avg_color4=42 # 상대팀_17번(16번 인덱스)
gap1=19
gap2=10
gap3=10
gap4=20
myTeam=0
redTeam=0
count=0 # 상대팀 일의 자리 숫자로 바뀔 때!
# miniCount=0 # 안 읽을 프레임 수

x2, y2, w2, h2 = 660, 13, 18, 20
text=""


while video.isOpened():
    run, frame = video.read()
    if not run:
        print("[프레임 수신 불가] - 종료합니다")
        exit(0)
        break
    img = cv2.cvtColor(frame, cv2.IMREAD_COLOR)
    cv2.imshow('video', frame)
    # plt.imshow(frame) # 좌표 얻기 위해
    # plt.show()
    if cv2.waitKey(11) & 0xFF == ord('q'): # 재생 속도 변경
        break

    # 우리팀 점수
    x, y, w, h = 613, 13, 18, 20
    crop_img = frame[y:y+h, x:x+w]
    avg_color_per_row = np.average(crop_img, axis=1)

    # 상대팀 점수(점수가 뒤에 생긴다!)
    crop_img2 = frame[y2:y2+h2, x2:x2+w2]
    avg_color_per_row2 = np.average(crop_img2, axis=1)

    if(np.average(avg_color_per_row, axis=1)[16]<20): # 끝났다면
        if(myTeam>redTeam):
            text="이겼어요! 축하해요~"
            tts = gTTS(text=text, lang='ko')
            tts.save("./sound/end.mp3")
            playsound("./sound/good1.mp3")
            playsound("./sound/end.mp3")
            os.remove("./sound/end.mp3") # 만든 파일은 바로 지우기!
        elif(myTeam<redTeam):
            text="졌어요. 아쉬워요."
            tts = gTTS(text=text, lang='ko')
            tts.save("./sound/end.mp3")
            playsound("./sound/bad1.mp3")
            playsound("./sound/end.mp3")
            os.remove("./sound/end.mp3") # 만든 파일은 바로 지우기!
        else:
            text="비겼어요. 다음에는 이겨봐요!"
            tts = gTTS(text=text, lang='ko')
            tts.save("./sound/end.mp3")
            playsound("./sound/end.mp3")
            os.remove("./sound/end.mp3") # 만든 파일은 바로 지우기!
        break

    # 우리팀 점수 검출
    print("my team"+str(np.average(avg_color_per_row, axis=1)[14])+" "+str(np.average(avg_color_per_row, axis=1)[16]))
    if(abs(np.average(avg_color_per_row, axis=1)[2]-avg_color1)>gap1 or abs(np.average(avg_color_per_row, axis=1)[16]-avg_color2)>gap2):
        myTeam+=1
        playsound("./sound/addOnePoint.mp3")
        text=str(myTeam)+"대"+str(redTeam)+"이에요!"
        tts = gTTS(text=text, lang='ko')
        avg_color1 = np.average(avg_color_per_row, axis=1)[2]
        avg_color2 = np.average(avg_color_per_row, axis=1)[16]
        if(myTeam==2):
            gap2=15
        elif(myTeam==3):
            gap2=16
        elif(myTeam==9):
            gap2=6
        elif(myTeam==12):
            gap2=16
        elif(myTeam==13):
            gap2=14
        print(myTeam, avg_color1)
        print(myTeam, avg_color2)
        tts.save("./sound/now.mp3")
        playsound("./sound/now.mp3")
        os.remove("./sound/now.mp3") # 만든 파일은 바로 지우기!


    # 상대팀 점수 검출
    # print("red team"+str(np.average(avg_color_per_row2, axis=1)[2])+" "+str(np.average(avg_color_per_row2, axis=1)[16]))
    # if(abs(np.average(avg_color_per_row2, axis=1)[16])>=18 and abs(np.average(avg_color_per_row2, axis=1)[16])<=24):
        # continue
    if(abs(np.average(avg_color_per_row2, axis=1)[2]-avg_color4)>gap4 or abs(np.average(avg_color_per_row2, axis=1)[16]-avg_color3)>gap3):
        '''
        count+=1
        if(count>=9 and count<=100):
            continue
        '''

        redTeam+=1
        playsound("./sound/addRedTeamOnePoint.mp3")
        text=str(myTeam)+"대"+str(redTeam)+"이에요!"
        tts = gTTS(text=text, lang='ko')
        print("red", redTeam, avg_color3)
        avg_color3 = np.average(avg_color_per_row2, axis=1)[16]
        avg_color4 = np.average(avg_color_per_row2, axis=1)[2]
        if(redTeam==2):
            gap3=20
        elif(redTeam==3):
            gap3=10
        elif(redTeam==9): # 뒤에 숫자(1의 자리)를 봐야 함!
            x2, y2, w2, h2 = 672, 13, 15, 20
            avg_color3=20
            avg_color4=24
            count+=1
            print("red 숫자 조정")
        tts.save("./sound/now.mp3")
        playsound("./sound/now.mp3")
        os.remove("./sound/now.mp3") # 만든 파일은 바로 지우기!
    
video.release()
cv2.destroyAllWindows()
