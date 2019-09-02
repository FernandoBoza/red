import re

mathCommands = ['what is', 'get me the', 'find me the']
command = 'what is the square root of 100 / 3'

for i in mathCommands:
   if i in command:
      s = command.replace(i, '')
      try:
         print( s + ' is '+  str(eval(s)))
      except:
         print('this')