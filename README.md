# Text Compression

This repository contains a custom text compression algorithm, optimized for the english language. They key insight to the creation of this algorithm is that there are around 400,000 English words and the average English word is 5.1 characters long (not including the spaces next to it). as a result, we can assign a mapping of all english words to 19 bit combinations. I store these 19 bits inside 3 bytes, which left space for storing the upper/lower case of the each word, and whether they have spaces to the right or left of them. If a word or combination of characters is not in the known dictionary of words, or if encoding it would not decrease file size, it is stored as plain-text / 7 bit ascii.

This algorithm typically reduces file sized of english text by 40-50%

## Notes

- The compression algorithm currently only works with input text files containing ASCII characters with values lower than 127

- While decompression is straightforward. The compression algorithm must identify compressable words in order to compress them. Words are currently identified by checking if each sequnce of characters between space characters is a word. Some exceptions apply to account for punctuation marks. Improving the identification of words may result in greater compression.

- This algorithm could easilly be optimized for other languages by using a words.txt mapping for their language. So long as that language uses ASCII characters and words.txt does not exceed 524288 (2^19) words.

## Sources

words.txt gotten from https://github.com/dwyl/english-words/blob/master/words.txt
