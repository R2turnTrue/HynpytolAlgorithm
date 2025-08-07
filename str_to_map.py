import sys
print('Let\'s write to', sys.argv[1])
f = open(sys.argv[1], 'w', encoding='utf-8')

HEIGHT = 480 / 32
WIDTH = 640 / 32

s = """
####################
####################
#######       m ####
#######  ### m m####
#######  #### m ####
#######  ####m m####
#######  ####   ####
######   ####   ####
#### m m####m m ####
##m m m ## m m m####
## mpm ###m m m#####
##m m ####vU m######
####################
####################
####################
"""


"""
####################
####v###############
#### ###m m    #####
###m            ####
#### ######### #####
#### ######### #####
###m    R   m# #####
###     L   ## #####
############## #####
############    ####
####    m  m     ###
#### ##p#####  #####
#### ## ##### m#####
####    ############
####################
"""

arrstr = "[\n"
lines = s.splitlines()[1:] # remove first line because it is empty

for line in lines:
    arrstr += "    ["
    for c in line:
        if c == ' ':
            arrstr += "0,"
        elif c == '#':
            arrstr += "1,"
        elif c == 'm':
            arrstr += "2,"
        elif c == 'L':
            arrstr += "3,"
        elif c == 'R':
            arrstr += "4,"
        elif c == 'U':
            arrstr += "5,"
        elif c == 'D':
            arrstr += "6,"
        elif c == 'p':
            arrstr += "7,"
        elif c == 'v':
            arrstr += "8,"
    arrstr = arrstr[:-1] + "],\n"

arrstr = arrstr[:-1] + "\n]"

f.write(arrstr)
f.close()

print('Done writing to', sys.argv[1])