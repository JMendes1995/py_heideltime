from py_heideltime import py_heideltime


text = "The start of the war in Europe is generally held to be 1 September 1939,"\
        "beginning with the German invasion of Poland; the United Kingdom and France declared war on Germany two days later."\
        "The dates for the beginning of war in the Pacific include the start of the Second Sino-Japanese War on 7 July 1937,"\
        "or even the Japanese invasion of Manchuria on 19-09-1931."
with open('avatar.txt', 'rb') as f:
  text1 = f.read()

text2 = '''
Thurs August 31st - News today that they are beginning to evacuate the London children tomorrow. Percy is a billeting officer. I can't see that they will be much safer here.
'''

results = py_heideltime(str(text1))

#print(len(results[0]))
#print(results[-1])