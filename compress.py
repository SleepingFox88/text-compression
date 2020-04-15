
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

# open file to compress
with open("compress.txt", 'r') as input:
    data = input.read()

with open(f"./compressedWords.txt", "w") as compressedWords:

    with open(f"./notCompressedWords.txt", "w") as notCompressedWords:

        # open file to output to
        with open(f"./compressed.bin", "wb") as output:

            stringWords = data.split(" ")

            numCompressedWords = 0

            # for each word
            for word in stringWords:

                # for each subword (seperated by "\n")
                containsReturn = "\n" in word
                subWords = word.split("\n")

                for x in range(len(subWords)):
                    subWord = subWords[x]

                    # make word lowercase for comparisons
                    lowWord = subWord.lower()

                    # compress known words
                    if lowWord in words:
                        numCompressedWords = numCompressedWords + 1

                        # DEBUG
                        if True:
                            compressedWords.write("### ")
                            compressedWords.write(lowWord)
                            compressedWords.write("\n")

                        intBytes = (words.index(lowWord)).to_bytes(
                            4, byteorder="big", signed=True)

                        # Highest bit signifies compressed word
                        outputBytes.append(intBytes[1] + 128)

                        outputBytes.append(intBytes[2])
                        outputBytes.append(intBytes[3])

                    # compressable word + punctuation mark
                    elif lowWord[:-1] in words:
                        numCompressedWords = numCompressedWords + 1

                        # DEBUG
                        if True:
                            compressedWords.write("P## ")
                            compressedWords.write(lowWord)
                            compressedWords.write("\n")

                        intBytes = (words.index(lowWord[:-1])).to_bytes(
                            4, byteorder="big", signed=True)

                        # Highest bit signifies compressed word
                        outputBytes.append(intBytes[1] + 128)

                        outputBytes.append(intBytes[2])
                        outputBytes.append(intBytes[3])

                        # append punctuation character
                        outputBytes.append(ord(lowWord[-1:]))

                    # store non compressable strings in plaintext
                    else:

                        # DEBUG
                        if True:
                            notCompressedWords.write("### ")
                            notCompressedWords.write(subWord)
                            notCompressedWords.write("\n")

                        for char in subWord:
                            outputBytes.append(ord(char))

                    # store return characters
                    if containsReturn and x != (len(subWords) - 1):
                        outputBytes.append(ord("\n"))

            output.write(outputBytes)


print("(", numCompressedWords, "/", len(stringWords), ")", " words compressed")
numCompressedWords

print("file size reduced by", (1 - (len(outputBytes) / len(data))) * 100, "%")
