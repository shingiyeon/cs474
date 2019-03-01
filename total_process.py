import methods
import decoder
import postprocessing
import nltk
if __name__ == "__main__":
   # nltk.download()
    #methods.preprocessing("./data/temp/")
    decoder.predict()
    postprocessing.postprocessing("./")
