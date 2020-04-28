#Script made by ComboDev UwU

#TODO-> Generate L/R poses with expressions. Expression generation already has been made, so you really just have to make the L/R thingy x3.

import sys
import itertools

class Program():
    name = ""
    oldLines = ""
    imageAString = ""
    debug = False
    path = ""
    expressionPath = ""
    l_suffix = ""
    r_suffix = ""
    l_count = 0
    r_count = 0
    full_sprite_pose_num = None
    composed_sprite_pose_num = None
    file_extension = ""
    posePrefixes = []
    expressionSuffixes = []
    full_sprite_list = []
    
    def __init__(self):
        if len(sys.argv) >= 2:
            if str(sys.argv[1]) == "-debug":
                self.debug = True
        self.startSetup()
        #self.getFileLines()
    def getFileLines(self):
        try:
            f = open("definitions.rpy","r")
            if f.mode != "r":
            #    print("Um... The file isn't opened in read mode.")
                return
            try:
                self.oldLines = f.readlines()
                f.close()
                if self.oldLines == None or self.oldLines == "":
                    print("ERROR: definitions.rpy not found or empty. Make sure it is located in the same folder as this script.")
                    return
                if self.debug:
                    print("Existing defintions.rpy file:\n==========\n")
                    for x in self.oldLines:
                        print(x, end='')
                    print("\n==========\nEND OF FILE.\n")
            except:
                print("Definitions.rpy cannot be read... Is it opened or being used somewhere else?")
        except:
            print("ERROR: definitions.rpy not found. Make sure it is located in the same folder as this script.")
    def startSetup(self):
        print('''------------------------------
DDLC Character Image Defintion Generator
Copyright ComboDev 2020
------------------------------''')
        print("Please enter the name of the character (the word after the image statement).")
        self.name = str(input())
        print("Thank you.")
        print("Where are your pose sprites located? (RELATIVE TO THE GAME FOLDER)")
        print("Ex: mod_assets/sayori")
        print("If your images are in the images folder of the game folder, please exclude the folder from the path.")
        print("Ex: images/sayori -> sayori")
        self.path = str(input())
        print("What's your images' file extension (with the dot)")
        print("Ex: .png")
        self.file_extension = str(input())
        print("Thank you.")
        print("Are you files containing full sprites? (Meaning an image is the FULL character) [Y/N]")
        if str(input()).lower() == "y":
            print("Do the files have incremental names? [Y/N]")
            if str(input()).lower() == "y":
                print("What's the last pose's number?")
                self.full_sprite_pose_num = self.getIntInput()
                self.GenerateFullSpriteDefinitions()
                print("All done!")
                return
            else:
                print("Please enter every sprites' file name without its extension.")
                print("Type \"Done!\" when you are done.")
                tmp = ""
                while tmp.lower() != "done!" and tmp.lower() != "done":
                    tmp = input()
                    if tmp.lower() != "done!" and tmp.lower() != "done":
                        self.full_sprite_list.append(str(tmp))
                self.GenerateFullSpriteDefinitions()
                print("All done!")
                return
        print("Next up, does your character have pose names (1) or are the poses numbered like the original Dokis? (2)")
        print("1 or 2?")
        posePrefix = str(input())
        while posePrefix != "1" and posePrefix != "2":
            print("Please type a valid answer T-T!")
            posePrefix = str(input())
        if posePrefix == "1":
            print("Please enter every poses' file name without its extension.")
            print("Type \"Done!\" when you are done.")
            tmp = ""
            while tmp.lower() != "done!" and tmp.lower() != "done":
                tmp = input()
                if tmp.lower() != "done!" and tmp.lower() != "done":
                    self.posePrefixes.append(str(tmp))
        elif posePrefix == "2":
            
            print("Are your poses seperated (L/R) like the Dokis? [Y/N]")
            if str(input()).lower() == "y":
                print("How many poses do you have for the left side?")
                self.l_count = self.getIntInput()
                print("How many poses do you have for the right side?")
                self.r_count = self.getIntInput()

                #Suffixes
                print("What's the suffix for the left side? (Ex: The Dokis' is \"l\")")
                self.l_suffix = str(input())
                print("What's the suffix for the right side? (Ex: The Dokis' is \"r\")")
                self.r_suffix = str(input())
                #So right now, you know how many poses you have for each sides and their suffixes, 
                # so you have everything you need for poses.
            else:
                print("How many poses do you have?")
                #try:
                self.composed_sprite_pose_num = self.getIntInput()
                
                for pose in range(1, self.composed_sprite_pose_num+1):
                    self.posePrefixes.append(str(pose))

        #Right now, you have name + prefixes
        print("Where are you expressions located? (Leave empty and click enter if it's the same path as the poses)")
        self.expressionPath = str(input())
        if self.expressionPath == "" or self.expressionPath == " ":
            self.expressionPath = self.path
        print("Are the expressions files named after letters like the original Dokis? [Y/N]")
        
        if str(input()).lower() == "y":
            print("What's the name of the last expression file excluding the extension? (It has to be one letter)")
            lastLetter = str(input())
            alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
            letterCount = 0
            lastLetterCount = None
            for letter in alphabet:
                letterCount += 1
                if lastLetterCount == None:
                    self.expressionSuffixes.append(str(letter))
                if letter == lastLetter:
                    lastLetterCount = letterCount
            #letterCount += 1
            if self.debug:
                print(lastLetter + ": " + str(lastLetterCount))
                #print(letterCount)
            if self.l_count == 0 and self.r_count == 0:
                self.GenerateComposedSpriteDefinitions()
            else:
                self.GenerateComposedPoseSpriteDefinitions()
            print("Done ^^!")
        else:
            print("Please enter every expression's file name without its extension.")
            print("Type \"Done!\" when you are done.")
            tmp = ""
            while tmp.lower() != "done!" and tmp.lower() != "done":
                tmp = input()
                if tmp.lower() != "done!" and tmp.lower() != "done":
                    self.expressionSuffixes.append(str(tmp))
            if self.l_count == 0 and self.r_count == 0:
                self.GenerateComposedSpriteDefinitions()
            else:
                self.GenerateComposedPoseSpriteDefinitions()
            print("Done ^^!")
        
        #Right now, you have name + prefixes + expressions
    def getIntInput(self):
        try:
            tmp = int(input())
        except:
            result = None
            while result == None:
                try:
                    print("Please type a valid answer T-T!")
                    tmp = int(input())
                    result = True
                except:
                    pass
        return tmp

    def GenerateFullSpriteDefinitions(self):
        result = "\n"
        if self.full_sprite_pose_num != None:
            #Max num
            for num in range(1, self.full_sprite_pose_num + 1):
                result += "image " + self.name + " " + str(num) + " = Image(\"" + self.path + "/" + str(num) + self.file_extension + "\")\n"
            if self.debug:
                print(result)
            self.GenerateCharacterDefinitionFile(result)
        else:
            for sprite in self.full_sprite_list:
                result += "image " + self.name + " " + sprite + " = Image(\"" + self.path + "/" + sprite + self.file_extension + "\")\n"
            if self.debug:
                print(result)
            self.GenerateCharacterDefinitionFile(result)

    def GenerateComposedSpriteDefinitions(self):
        result = ""
        for prefix in self.posePrefixes:
            for suffix in self.expressionSuffixes:
                result += "image " + self.name + " " + prefix + suffix + " = im.Composite((960, 960), (0, 0), \"" + self.path + "/" + prefix + self.file_extension + "\"" + ", (0, 0), \"" + self.expressionPath + "/" + suffix + self.file_extension + "\")\n"
            result += "\n"
        self.GenerateCharacterDefinitionFile(result)
    
    def GenerateComposedPoseSpriteDefinitions(self):
        result = ""
        l_list = []
        r_list = []
        for lpose in range(1, self.l_count + 1):
            l_list.append(lpose)
        for rpose in range(1, self.r_count + 1):
            r_list.append(rpose)
        combinations = list(itertools.product(l_list, r_list))
        combinationCount = 0
        for combination in combinations:
            
            if self.debug:
                print("COMBINATION")
                print(combination)
                print("L_LIST")
                print(l_list)
                print("R_LIST")
                print(r_list)
            combinationCount += 1
            for suffix in self.expressionSuffixes:
                result += "image " + self.name + " " + str(combinationCount) + suffix + " = im.Composite((960, 960), (0, 0), \"" + self.path + "/" + str(combination[0]) + self.l_suffix + self.file_extension + "\"" + ", (0, 0), \"" + self.path + "/" + str(combination[1]) + self.r_suffix + self.file_extension + "\"" + ", (0, 0), \"" + self.expressionPath + "/" + suffix + self.file_extension + "\")\n"
            result += "\n"
        self.GenerateCharacterDefinitionFile(result)

    def GenerateCharacterDefinitionFile(self, content):
        f = open(self.name + "_sprite_definitions" + ".rpy", "w")
        f.write(content)
        f.close()
inst = Program()