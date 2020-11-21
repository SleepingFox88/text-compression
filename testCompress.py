def testCompression():
    # assert(False), "test failed"
    compressedData = compressor.compress("Hello World") #has a tab between the words

def testDecompression():
    pass

if __name__ == "__main__":

    # initialize
    if True:
        from compress import textCompressor
        compressor = textCompressor()

    # tests
    if True:
        testCompression()
        testDecompression()
        print("Everything passed")