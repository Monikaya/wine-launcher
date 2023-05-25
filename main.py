import os
import json
import time

# Function I ngl stole from StackOverflow that clears linux terminal
# Link to original post: https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console
# 2nd answer from user "popcnt"
def cls():
    os.system("cls" if os.name == "nt" else "clear")


def getRunCommand():
    with open("config.json", "r") as jsonfile:
        data = json.load(jsonfile)
    return data["StartCommand"]

def getGameDirectory():
    with open("config.json", "r") as jsonfile:
        data = json.load(jsonfile)
    return data["GameDirectory"]


# Function that really just asks the user if they want to define a custom start command for their apps and if so, what would they like that command to be, and then loads itt into config.json
def setupUser():
    cls()

    customyn = input(
        "Let's get you setup with a shiny new config file!\nWe don't really need much from you, but would you like a custom start command for your apps? [Y/N] "
    )
    if customyn.lower() == "y":
        startcommand = input(
            "Cool! What would you like that command to be, then?\nWe only need the bit before before your .exe file for this\nRemember, you can always change it in the config.json file! "
        )
        time.sleep(2)
    elif customyn.lower() == "n":
        print(
            "Cool! In this case then, we'll use the default command I've prepared for you!"
        )
        time.sleep(2)
        startcommand = False
    else:
        print(
            "Seems like you've entered something that doesn't work here. Welp, guess we'll just send ya to do it again :D"
        )
        return
        
        cls()
        gameDirectory = input("Time to setup the directory where you'd like us to read games from!\nPlease provide a full path into the root dir of your games folder!\n")

        jsondata = {
            "StartCommand": startcommand if startcommand else "wine",
            "GameDirectory": gameDirectory
        }

        with open("config.json", "w") as jsonfile:
            json.dump(jsondata, jsonfile)
            print("Write successful! Thanks for helping me get you all setup!")
            time.sleep(2)
            print("Remember, you can always edit the config.json file to change these!")
            time.sleep(3)


# Actually launches the game and checks if the user has a custom script or multiple exe's to choose from
def launchGame(gameNumber):
    cls()
    gameDirectory = getGameDirectory()
    gameName = f"{os.listdir(gameDirectory)[gameNumber]}"
    runCommand = getRunCommand()

    executableChoices = []

    for exe in os.listdir(f"{gameDirectory}/{gameName}"):
        fileName, fileExtension = os.path.splitext(f"{gameDirectory}/{gameName}/{exe}")
        if fileExtension == ".exe":
            executableChoices.append(exe)

    if len(executableChoices) == 1:
        os.system(f'{runCommand} {gameDirectory}/"{gameName}"/"{executableChoices[0]}"')
    else:
        cls()
        count = 1
        print(
            "Looks like there are more than one executable files in your game dir! You'll have to pick one for us to launch!"
        )
        for choice in executableChoices:
            print(f"{count}) {choice}")
            count += 1
        gameChoice = input("")
        cls()
        print("Have fun!")
        time.sleep(1)
        os.system(
            f'{runCommand} games/"{gameName}"/"{executableChoices[int(gameChoice)]}"'
        )


# Lists the games and asks which one you wanna play
def displayGames():
    cls()
    count = 0
    gameDirectory = getGameDirectory()

    print(
        "Time to pick what to play! Select the number corresponding with the game you want!"
    )
    for game in os.listdir(gameDirectory):
        print(f"{count}) {game}")
        count += 1
    while True:
        userInputNumber = input("")
        try:
            gameNumber = int(userInputNumber)
            if gameNumber > int(count) or gameNumber < 0:
                print("What the frick, man. Not allowed. Gimmie a new number pls.")
            else:
                break
        except ValueError:
            print("I'm ngl that isn't a number. Please try again.")

    launchGame(gameNumber)


# Function that lets the user branch off into doing different things. Mainly either change some settings or just play some games!
def launchMenu():
    cls()
    menuSelection = input(
        "Welcome to the menu! Do you want to:\n1) Launch a game/app\n2) Mess around with your settings\n3) Exit the program\n"
    )
    if menuSelection == "1":
        displayGames()
    elif menuSelection == "2":
        print("Oopsie, not implemented yet :P Maybe check back later?")
        time.sleep(2)
        launchMenu()
        # changeSettings()
    elif menuSelection == "3":
        return
    else:
        cls()
        print(
            "Not really sure what that one was... Well, let's try it again, why don't we?"
        )
        launchMenu()


# Function that runs at startup and directs what the program should do now
def main():
    print("Hey! Welcome to the library!")

    while not os.path.exists("config.json"):
        setupUser()

    launchMenu()


main()
