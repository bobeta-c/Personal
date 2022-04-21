# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 10:14:41 2022

@author: Bobeta
"""

Human = "* * * * * * * * G D V E K G K K I F I M K C S Q C H T V E K G G K H K T G P N L H G L F G R K T G Q A P G Y S Y T A A N K N K G I I W G E D T L M E Y L E N P K K Y I P G T K M I F V G I K K K E E R A D L I A Y L K K A T N E"
Tuna = "* * * * * * * * G D V A K G K K T F V Q K C A Q C H T V E N G G K H K V G P N L W G L F G R K T G Q A E G Y S Y T D A N K S K G I V W N N D T L M E Y L E N P K K Y I P G T K M I F A G I K K K G E R Q D L V A Y L K S A T S *"
Whale = "* * * * * * * * G D V E K G K K I F V Q K C A Q C H T V E K G G K H K T G P N L H G L F G R K T G Q A V G F S Y T D A N K N K G I T W G E E T L M E Y L E N P K K Y I P G T K M I F A G I K K K G E R A D L I A Y L K K A T N E"
R_monkey = "* * * * * * * * G D V E K G K K I F I M K C S Q C H T V E K G G K H K T G P N L H G L F G R K T G Q A P G Y S Y T A A N K N K G I T W G E D T L M E Y L E N P K K Y I P G T K M I F V G I K K K E E R A D L I A Y L K K A T N E"
Chicken = "* * * * * * * * G D I E K G K K I F V Q K C S Q C H T V E K G G K H K T G P N L H G L F G R K T G Q A E G F S Y T D A N K N K G I T W G E D T L M E Y L E N P K K Y I P G T K M I F A G I K K K S E R V D L I A Y L K D A T S K"
Pig =     "* * * * * * * * G D V E K G K K I F V Q K C A Q C H T V E K G G K H K T G P N L H G L F G R K T G Q A P G F S Y T D A N K N K G I T W G E E T L M E Y L E N P K K Y I P G T K M I F A G I K K K G E R E D L I A Y L K K A T N E"
Yeast =   "* * * T E F K A G S A K K G A T L F K T R C E L C H T V E K G G P H K V G P N L H G I F G R H S G Q A Q G Y S Y T D A N I K K N V L W D E N N M S E Y L T N P K K Y I P G T K M A F G G L K K E K D R N D L I T Y L K K A C E *"
Fly =     "* * * * G V P A G D V E K G K K I F V Q R C A Q C H T V E A G G K H K V G P N L H G L F G R K T G Q A A G F A Y T N A N K A K G I T W Q D D T L F E Y L E N P K K Y I P G T K M I F A G L K K P N E R G D L I A Y L K S A T K *"


empty_list = [0,0]
Animals = {"Human": [Human]+empty_list.copy(),"Tuna": [Tuna]+empty_list.copy(), "Whale": [Whale]+empty_list.copy(), "R_monkey": [R_monkey]+empty_list.copy(), "Chicken": [Chicken]+empty_list.copy(), "Pig": [Pig]+empty_list.copy(), "Yeast": [Yeast]+empty_list.copy(), "Fly": [Fly]+empty_list.copy()}
for x in range(len(Human)):
    for y in Animals:
        if Human[x] != Animals[y][0][x]:
            Animals[y][1] += 1
for x in Animals:
    Animals[x][2] = str(round((Animals[x][1]/len(Human))*100,2))+"%"
    
for x in Animals:
    print(x+' ' +Animals[x][2])