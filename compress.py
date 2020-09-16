import json
import os
from os import listdir
from os.path import isfile, join
import time
from tqdm import tqdm
from nltk.tokenize import wordpunct_tokenize


def isValidCapitalization(str):
    if str.islower():
        return True
    if str.isupper():
        return True
    # only first char is upper
    if str[0].isupper() and str[-(len(str) - 1):].islower():
        return True
    return False


class textCompressor:

    def __init__(self):
        self.words = []
        self.wordsDict = {}

        # Load words from file
        for word in open("words.txt", 'r').readlines():
            self.words.append(word)

        # remove \n characters
        for x in range(len(self.words)):
            self.words[x] = self.words[x].replace('\n', '')

        # ensure they are all lower case
        for x in range(len(self.words)):
            self.words[x] = self.words[x].lower()

        # convert words array to dict (faster to find indexes of words in array)
        for x in range(len(self.words)):
            self.wordsDict[self.words[x]] = x

    def compress(self, data):
        print("compressing...")

        outputBytes = bytearray()

        stringWords = data.split(" ")

        lastWasPlaintext = False

        # for each word
        for i in tqdm(range(len(stringWords))):
            word = stringWords[i]

            # for each subword (seperated by "\n")
            containsReturn = "\n" in word
            subWords = word.split("\n")

            for x in range(len(subWords)):
                subWord = subWords[x]

                tokens = wordpunct_tokenize(subWord)

                for subWord in tokens:
                    print("subWord: \"" + subWord + "\"")

                    # compress known words
                    if len(subWord) > 2 and isValidCapitalization(subWord) and subWord.lower() in self.words:
                        compWordBytes = bytearray(3)

                        # DEBUG
                        if True:
                            compressedWords.write("### ")
                            compressedWords.write(subWord)
                            compressedWords.write("\n")

                        # convert word to it's 3 byte index
                        if True:
                            intBytes = (self.wordsDict[subWord.lower()]).to_bytes(
                                4, byteorder="big", signed=True)

                            compWordBytes[0] = intBytes[1]
                            compWordBytes[1] = intBytes[2]
                            compWordBytes[2] = intBytes[3]

                        # store case state in the 0110-0000 bits
                        if True:
                            # word is lowercase
                            if subWord.islower():
                                compWordBytes[0] = compWordBytes[0] | 0

                            # subword is all upper case
                            elif subWord.isupper():
                                compWordBytes[0] = compWordBytes[0] | 32

                            # only first char is upper
                            elif subWord[0].isupper() and subWord[-(len(subWord) - 1):].islower():
                                compWordBytes[0] = compWordBytes[0] + 64

                        # if last byte represents a space
                        if lastWasPlaintext and outputBytes[len(outputBytes) - 1] == ord(" "):

                            # remove last byte
                            del outputBytes[len(outputBytes) - 1]

                            # tell this word to encode a space at the beginning.
                            # spacing information stored in 0001-1000
                            compWordBytes[0] = compWordBytes[0] | 16

                        # write bytes
                        if True:
                            # 1000-0000 bit signifies compressed word
                            outputBytes.append(compWordBytes[0] | 128)

                            outputBytes.append(compWordBytes[1])
                            outputBytes.append(compWordBytes[2])

                        # keep this line at the end
                        lastWasPlaintext = False

                    else:
                        # DEBUG
                        if len(subWord) > 2:
                            notCompressedWords.write("### ")
                            notCompressedWords.write(subWord)
                            notCompressedWords.write("\n")

                        for char in subWord:
                            outputBytes.append(ord(char))

                        # keep this line at the end
                        lastWasPlaintext = True

                # store return characters
                if containsReturn and x != (len(subWords) - 1):
                    outputBytes.append(ord("\n"))

                    # keep this line at the end
                    lastWasPlaintext = True

            # store a space character (unless this is the last word we are dealing with)
            if i < len(stringWords) - 1:

                # if lastWasPlaintext OR if last compressed word has already notated a space after it
                if lastWasPlaintext or outputBytes[len(outputBytes) - 3] & 8 != 0:
                    outputBytes.append(ord(" "))

                    # keep this line at the end
                    lastWasPlaintext = True
                else:
                    # tell the last compressed word to store a space after it
                    if True:
                        # spacing information stored in 0001-1000
                        outputBytes[len(outputBytes) - 3] = outputBytes[len(outputBytes) - 3] | 8


                    #outputBytes[len(outputBytes) - 3] | 8

        # display compression statistics
        print("file size reduced by",
              (1 - (len(outputBytes) / len(data))) * 100, "%")

        return outputBytes

    def decompress(self, data):

        outputBytes = bytearray()

        i = 0
        while(i < len(data)):
            # if compressed word
            # if highest bit is set
            if data[i] & 128:
                # check header bits 0001-1000 to determine spacing
                leftSpace = data[i] & 16
                rightSpace = data[i] & 8

                # grab integer representing capstate
                # 00 = allLower
                # 01 = allUpper
                # 10 = firstCharUpper restLower
                capState = (data[i] >> 5) & 3

                wordIndex = (data[i] << 16) | (
                    data[i + 1] << 8) | (data[i + 2])

                # limit to 19 bits
                wordIndex = wordIndex & 0b000001111111111111111111

                word = self.words[wordIndex]

                # allLower
                if capState == 0:
                    word = word.lower()

                # allUpper
                elif capState == 1:
                    word = word.upper()

                # firstCharUpper restLower
                elif capState == 2:
                    # first char is upper

                    # seperate cirst char and rest of word
                    if True:
                        firstChar = word[0]
                        word = word[-(len(word) - 1):]

                    # make firstChar upperCase
                    firstChar = firstChar.upper()

                    # Recombine firstChar and rest of word
                    word = firstChar + word

                    # ensure all other characters are lower
                    word[-(len(word) - 1):]

                if leftSpace:
                    outputBytes.append(ord(" "))

                for char in word:
                    outputBytes.append(ord(char))

                if rightSpace:
                    outputBytes.append(ord(" "))

                # keep this line at the end
                # skip over compressed word and point to next byte to examine
                i = i + 3

            # if plaintext char
            else:
                outputBytes.append(data[i])

                # keep this line at the end
                i = i + 1

        # convert bytes to string
        outputString = outputBytes.decode("utf-8")

        return outputString


textCompressor = textCompressor()

# open file to compress
with open("compress.txt", 'r') as input:
    data = input.read()

with open(f"./compressedWords.txt", "w") as compressedWords:

    with open(f"./notCompressedWords.txt", "w") as notCompressedWords:

        # open file to output to
        with open(f"./compressed.bin", "wb") as output:

            # open file to output to
            with open(f"./decompressed.txt", "w") as decompressed:

                compressedData = textCompressor.compress(data)
                output.write(compressedData)
                decompressedData = textCompressor.decompress(compressedData)
                decompressed.write(decompressedData)

                # import cProfile
                # cProfile.run(
                #     "textCompressor.compress(data)", sort='cumtime')
                # print("")
                # print("")
                # print("")
                # print("")
                # print("=====Decompressing=====")
                # cProfile.run(
                #     "textCompressor.decompress(compressedData)", sort='cumtime')


# check if results are the same
areTheSame = False

print("len(data): ", len(data))
print("len(decompressedData): ", len(decompressedData))


if len(data) == len(decompressedData):
    areTheSame = True
    for x in range(len(data)):
        if data[x] != decompressedData[x]:
            areTheSame = False
            print("Objects differ at index: ", x)
            break

if areTheSame:
    print("Test Passed: Arrays are the same!")
else:
    print("Test failed: Arrays differ")
