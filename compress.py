
import json
import os
from os import listdir
from os.path import isfile, join
import time
from tqdm import tqdm


def isValidCapitalization(str):
    if str.islower():
        return True
    if str.isupper():
        return True
    # only first char is upper
    if str[0].isupper() and str[-(len(str) - 1):].islower():
        return True
    return False


words = []


# Load words from file
print("loading words from file...")
for word in open("words.txt", 'r').readlines():
    words.append(word)

print("removing return characters...")
# remove \n characters
for x in range(len(words)):
    words[x] = words[x].replace('\n', '')

print("initializing lowercase...")
# ensure they are all lower case
for x in range(len(words)):
    words[x] = words[x].lower()

outputBytes = bytearray()

print("compressing...")

# open file to compress
with open("compress.txt", 'r') as input:
    data = input.read()

with open(f"./compressedWords.txt", "w") as compressedWords:

    with open(f"./notCompressedWords.txt", "w") as notCompressedWords:

        # open file to output to
        with open(f"./compressed.bin", "wb") as output:

            stringWords = data.split(" ")

            numCompressedWords = 0

            lastWasPlaintext = False

            # for each word
            for i in tqdm(range(len(stringWords))):
                word = stringWords[i]

                # for each subword (seperated by "\n")
                containsReturn = "\n" in word
                subWords = word.split("\n")

                for x in range(len(subWords)):
                    subWord = subWords[x]

                    # compress known words
                    if subWord.lower() in words and isValidCapitalization(subWord):
                        compWordBytes = bytearray(3)
                        numCompressedWords = numCompressedWords + 1

                        # DEBUG
                        if True:
                            compressedWords.write("### ")
                            compressedWords.write(subWord.lower())
                            compressedWords.write("\n")

                        # convert word to it's 3 byte index
                        if True:
                            intBytes = (words.index(subWord.lower())).to_bytes(
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
                        if lastWasPlaintext and outputBytes[len(outputBytes) - 1] == " ":
                            # remove last byte
                            del outputBytes[len(outputBytes) - 1]

                            # tell this word to encode a space at the beginning.
                            # spacing information stored in 0001-1000
                            compWordBytes[0] | 16

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
                        if True:
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

                # store a space character (unless this is the last word we are dealin with)
                if i < len(stringWords) - 1:

                    if lastWasPlaintext:
                        outputBytes.append(ord(" "))

                        # keep this line at the end
                        lastWasPlaintext = True
                    else:
                        # tell the last compressed word to store a space after it
                        if True:
                            # spacing information stored in 0001-1000
                            outputBytes[len(outputBytes) -
                                        3] = outputBytes[len(outputBytes) - 3] | 8

            output.write(outputBytes)


print("(", numCompressedWords, "/", len(stringWords), ")", " words compressed")
numCompressedWords

print("file size reduced by", (1 - (len(outputBytes) / len(data))) * 100, "%")
