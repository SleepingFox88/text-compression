
import json
import os
from os import listdir
from os.path import isfile, join
import time
from tqdm import tqdm

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

# open file to output to
with open(f"./compressed.bin", "wb") as output:

    # open file to compress
    with open("compress.txt", 'r') as input:

        # for each line in file
        for line in tqdm(input.readlines()):

            lineWords = line.split(" ")

            # for each word
            for word in lineWords:
                word = word.lower()

                # compress known words
                if word in words:

                    intBytes = (words.index(word)).to_bytes(
                        4, byteorder="big", signed=True)

                    # Highest bit signifies compressed word
                    outputBytes.append(intBytes[1] + 128)

                    outputBytes.append(intBytes[2])
                    outputBytes.append(intBytes[3])

                # store non compressable strings in plaintext
                else:
                    for char in word:
                        outputBytes.append(ord(char))

    output.write(outputBytes)
