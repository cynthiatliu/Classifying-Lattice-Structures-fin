#File formatter
#Interactive hkl file formatting!

import math
import re
import string

#Main
def main():
    jobs = [0, 1, 2] #Will increase as I get more types of jobs
    
    #While the user wants to continue
    while True:
        
        good = False
        while good != True:
            try:
                job = int(eval(raw_input("What is the original appearance of the file you want to format? (Choose 0 to quit) \n\n1. Each line has x characters before hkl begins, and all data lines include hkl \n2. Sometimes when a positive number is followed by a negative number there is no space between the first number and the dash.\n3. Under construction; do not select.\n")))
                if job in jobs: good = True
            except:
                print ("Invalid input (must be a number corresponding to the original appearance) - try again?")
                
        if job == 0:
            print ("Goodbye :D")
            break
                
        #Giant switch
        if job == 1: #stuff before the hkl
            #File name
            good = False
            while good != True:
                try:
                    name = raw_input("What is the name of the file you want to read? Don't add an extension. ") + ".txt"
                    toEdit = open(name, 'r')
                    good = True
                except:
                    print ("That can't be the right file! Please try again")
                    
            #Number of spaces
            good = False
            while good != True:
                try:
                    numSpaces = int(math.sqrt(eval(raw_input("How many characters are there before the start of hkl in each line? ")))**2)
                    good = True
                except:
                    print ("Dude, that can't be a number of spaces")
                    
            #File name to write to
            good = False
            while good != True:
                try:
                    name2 = raw_input("What is the name of the file you want to write to? ") + ".txt"
                    edited = open(name2, 'w')
                    good = True
                except:
                    print ("You've got invalid letters in your file name! Take 'em out!")
                    
                    
            line = toEdit.readline()
            while line != '':
                if len(line) > numSpaces:
                    line = line[numSpaces:] #Rest of the line
                    edited.write(line)
                else:
                    edited.write("\n")
                line = toEdit.readline()
            
            print ("Done!")
            
        elif job == 2: #dashes connecting stuff that shouldn't be connected
            #File name
            good = False
            while good != True:
                try:
                    name = raw_input("What is the name of the file you want to read? Don't add an extension. ") + ".txt"
                    toEdit = open(name, 'r')
                    good = True
                except:
                    print ("That can't be the right file! Please try again")
                    
            #File name to write to
            good = False
            while good != True:
                try:
                    name2 = raw_input("What is the name of the file you want to write to? ") + ".txt"
                    edited = open(name2, 'w')
                    good = True
                except:
                    print ("You've got invalid letters in your file name! Take 'em out!")
                    
            line = toEdit.readline()
            while line != '':
                patt = re.compile(r'(\d+)-(\d+)')
                matches = patt.findall(line)
                for i in range(len(matches)):
                    stri = matches[i][0] + "-" + matches[i][1]
                    line = line.replace(stri, stri[0:string.rfind(stri, "-")] + " " + stri[string.rfind(stri, "-"):])
                edited.write(line)
                line = toEdit.readline()
                
            print ("Done!")
                    
        else: print ("Still in the works. Check back later?")
        
main()
