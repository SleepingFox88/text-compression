
import json
import os
from os import listdir
from os.path import isfile, join
import time

words = []


# Load words from file
for word in open("words.txt", 'r').readlines():
    words.append(word)

# remove \n characters
for x in range(len(words)):
    words[x] = words[x].replace('\n', '')

# ensure they are all lower case
for x in range(len(words)):
    words[x] = words[x].lower()

# print(words)

outputBytes = bytearray()

# open file to output to
with open(f"./compressed.bin", "wb") as output:

    # open file to compress
    with open("compress.txt", 'r') as input:

        # for each line in file
        for line in input.readlines():

            lineWords = line.split(" ")

            # for each word
            for word in lineWords:
                word = word.lower()
                # print(word)
                if word in words:
                    # print("true")
                    print(words.index(word))

                    intBytes = (words.index(word)).to_bytes(
                        4, byteorder="big", signed=True)

                    outputBytes.append(intBytes[1])
                    outputBytes.append(intBytes[2])
                    outputBytes.append(intBytes[3])

    output.write(outputBytes)

    # print(intBytes[0])
    # print(intBytes[1])

    # newFileByteArray = bytearray(newFileBytes)
    # output.write(newFileByteArray)
