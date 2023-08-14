import chess
import chess.svg
import numpy as np
import random
import speech_recognition as sr
import os
from gtts import gTTS
from playsound import playsound
import warnings
warnings.filterwarnings('ignore')

phoneticSpelling = {
    'a' : 'ei',
    'b' : 'b',
    'c' : 'c', 
    'd' : 'd', 
    'e' : 'e', 
    'f' : 'f',
    'g' : 'g',
    'h' : 'h'
}
pieceNames = {
    'Q' : 'Queen',
    'K' : 'King',
    'R' : 'Rook',
    'B' : 'Bishop',
    'N' : 'Knight',
    'P' : 'Pawn'
}
pieceLetters = {
    "knight" : "N",
    "king" : "K", 
    "night" : "K",
    "queen" : "Q", 
    "bishop" : "B",
    "pawn" : "P", 
    "rook" : "R"
}
files = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
rows = ('1', '2', '3', '4', '5', '6', '7', '8')

def recordAndConvert():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak something...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            return "No speech detected."
        except sr.UnknownValueError:
            return "Sorry, could not understand audio."
        except sr.RequestError as e:
            return "Could not request results; {0}".format(e)
        
def textToSpeech(text: str):
    tts = gTTS(text)
    tts.save('dictation.mp3')
    os.system('afplay dictation.mp3')

def convertToChessMove():
    speech = recordAndConvert().lower()
    if "quit" in speech:
        return "quit"
    elif "cheat" in speech:
        return "cheat"
    elif "moves" in speech: 
        return "moves"
    elif "castles kingside" in speech:
        return "O-O"
    elif "castles queenside" in speech: 
        return "O-O-O"
    else:
        textArr = speech.split(" ")
        print(textArr)
        if textArr[0] not in pieceLetters.keys() and textArr[0][0] not in files:
            return "not a valid input. you said " + speech
        else:
            if textArr[0] in pieceLetters.keys():
                textArr[0] = pieceLetters[textArr[0]]
        if 'tonight' in textArr:
            textArr.insert(textArr.index("tonight") + 1, "knight")
            textArr[textArr.index("tonight")] = "to"
        if 'promotes' in textArr: 
            try: 
                textArr[textArr.index('promotes') + 1] = "=" 
                textArr[textArr.index('promotes') + 2] = pieceLetters[textArr[textArr.index('promotes') + 2]]
                textArr[textArr.index('promotes')] = ""
            except: 
                return "not a valid input. you said " + speech
        if 'takes' in textArr:
            textArr[textArr.index('takes')] = 'x'
        if 'P' in textArr: 
            textArr[textArr.index('P')] = ""
        if 'to' in textArr:
            textArr[textArr.index('to')] = ""
        ret = ""
        for i in textArr:
            ret += i
        if 'x' in ret:
            if ret[ret.index('x') -1] in rows: 
                ret = ret[0:ret.index('x')-1] + ret[ret.index('x'):len(ret)]
        return ret
def getDictateFlag():
    flag = input("would you like to moves to be dictated and to play with your voice? ").lower()
    while True:
        if flag in ('y', 'yes', 'n', 'no'): 
            break 
        else: 
            print('sorry not a valid input')
            flag = (input("would you like to moves to be dictated and to play with your voice? ")).lower()
            continue
    if flag in ('y', 'yes'):
        return True
    else:
        return False
    
def getPlayerColor():
    playerColor = (input('what color would you like to play as? ')).lower()
    while True:
        if playerColor in ('w', 'white', 'b', 'black', 'r', 'random'): 
            break 
        else: 
            print('sorry not a valid input')
            playerColor = (input('what color would you like to play as? ')).lower()
            continue
    if playerColor in ('w', 'white'):
        return True
    elif playerColor in ('b', 'black'):
        return False
    else: 
        return bool(random.getrandbits(1))

def promptLegalMoves(board: chess.Board, dictateFlag : bool):
    playterInput = ""
    if dictateFlag: 
        print('enter \"moves\" to see all legal moves, \"cheat\" to see the full board, or anything else to continue ')
        textToSpeech("Say moves to see all legal moves, cheat to see the full board, or anything else to continue")
        playerInput = recordAndConvert()
    else: 
        playerInput = (input('enter \"moves\" to see all legal moves, \"cheat\" to see the full board, or anything else to continue ')).lower()
    if playerInput == 'moves': 
        print(board.legal_moves)
    elif playerInput == 'cheat':
        print(board)



def getPlayerMove(board : chess.Board, dictateFlag : bool, moveNo : int):
    while True:
        if dictateFlag:
            if moveNo == 1:
                textToSpeech("Dictate a move in standard algebraic notation, cheat to see the board, moves to see all legal moves, or say quit to quit. Press any key before you speak.")
            input()
            userInput = convertToChessMove()
        else:
            userInput = input('enter a move in standard algebraic notation or \"q\" to quit ')
        if userInput in ("q", "quit"):
            return False
        elif userInput == 'moves': 
            print(board.legal_moves)
            return getPlayerMove(board, dictateFlag, moveNo)
        elif userInput == 'cheat':
            chess.svg.board(board)
            return getPlayerMove(board, dictateFlag, moveNo)
        else:
            try:
                move = board.parse_san(userInput)
            except:
                if dictateFlag:
                    textToSpeech("Not a valid move")
                print("not a valid move")
                promptLegalMoves(board, dictateFlag)
                continue
            else: 
                return move
    
        
def getComputerMoveRandom(board: chess.Board):
    move = random.choice(list(board.legal_moves))
    return move

def moveToSpeechText(board : chess.Board, move : chess.Move):
    moveSan = board.san(move)
    ret = ""
    if moveSan == 'O-O': 
        ret = "Castles kingside"
    elif moveSan == 'O-O-O':
        ret = "Castles queenside"
    else: 
        moveArr = [*moveSan]
        if 'x' in moveArr:
            moveArr[moveArr.index('x')] = 'takes'
        if 'a' in moveArr:
            moveArr[moveArr.index('a')] = 'ei'
        if moveArr[0] not in ('Q', 'K', 'N', 'B', 'R'):
            moveArr.insert(0, 'P')
        if '=' in moveArr:
            moveArr[moveArr.index('=')] = 'promotes to'
            moveArr[moveArr.index('=') + 1] = pieceNames[moveArr.index('=') + 1]
        else:
            if 'takes' not in moveArr and '+' not in moveArr:
                moveArr.insert(len(moveArr) - 2, 'to')
            elif 'takes' not in moveArr and '+' in moveArr:
                moveArr.insert(len(moveArr) - 3, 'to')
                moveArr[-1] = 'with check'
            moveArr[0] = pieceNames[moveArr[0]]
        temp = ""
        for i in moveArr:
            temp = temp + i + " "
        ret = temp
    return ret
def moveToText(board : chess.Board, move : chess.Move):
    moveSan = board.san(move)
    ret = ""
    if moveSan == 'O-O': 
        ret = "Castles kingside"
    elif moveSan == 'O-O-O':
        ret = "Castles queenside"
    else: 
        moveArr = [*moveSan]
        if 'x' in moveArr:
            moveArr[moveArr.index('x')] = 'takes'
        if moveArr[0] not in ('Q', 'K', 'N', 'B', 'R'):
            moveArr.insert(0, 'P')
        if '=' in moveArr:
            moveArr[moveArr.index('=')] = 'promotes to'
            moveArr[moveArr.index('=') + 1] = pieceNames[moveArr.index('=') + 1]
        else:
            if 'takes' not in moveArr and '+' not in moveArr:
                moveArr.insert(len(moveArr) - 2, 'to')
            elif 'takes' not in moveArr and '+' in moveArr:
                moveArr.insert(len(moveArr) - 3, 'to')
                moveArr[-1] = 'with check'
            moveArr[0] = pieceNames[moveArr[0]]
        temp = ""
        for i in moveArr:
            temp = temp + i + " "
        ret = temp
    return ret

def playBlindFoldChessWithRandom():
    startColor = getPlayerColor()
    dictateFlag = getDictateFlag()
    board = chess.Board()
    moveNo = 1
    if startColor: #player is white
        print("You are playing as white")
        while(board.outcome() == None):
            print('Move Number: ' + str(moveNo))
            playerMove = getPlayerMove(board, dictateFlag, moveNo)
            if playerMove == False:
                break
            if dictateFlag:
                textToSpeech('you played ' + moveToSpeechText(board, playerMove))
            print('you played ' + moveToText(board, playerMove))
            board.push(playerMove)
            if not board.is_game_over():
                computerMove = getComputerMoveRandom(board)
                if dictateFlag:
                    textToSpeech('the computer played ' + moveToSpeechText(board, computerMove))
                print('the computer played ' + moveToText(board, computerMove))
                board.push(computerMove)
                print('\n')
                moveNo += 1
        print(board.outcome())
    else: 
        print("You are playing as black")
        while(board.outcome() == None):
            print('Move Number: ' + str(moveNo))
            computerMove = getComputerMoveRandom(board)
            if dictateFlag:
                textToSpeech('the computer played ' + moveToSpeechText(board, computerMove))
            print('the computer played ' + moveToText(board, computerMove))
            board.push(computerMove)
            if not board.is_game_over():
                playerMove = getPlayerMove(board, dictateFlag, moveNo)
                if playerMove == False:
                    break
                if dictateFlag:
                    textToSpeech('you played ' + moveToSpeechText(board, playerMove))
                print('you played ' + moveToText(board, playerMove))
                print('\n')
                board.push(playerMove)
                moveNo += 1
        print(board.outcome())


    

playBlindFoldChessWithRandom()