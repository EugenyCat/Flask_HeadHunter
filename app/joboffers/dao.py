from app.authorization.dao import User
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize




class Joboffer:

    regex = re.compile("[A-Za-z]+")
    m = PorterStemmer()

    def __init__(self, offer_id, author_id, title, description, skills, liked=0):
        self.offer_id = offer_id
        self.author_id = author_id
        self.title = title
        self.description = description
        self.skills = skills
        self.liked = liked
        self.score = 0


    def search_offer(self, search_str):
        m = PorterStemmer()

        search_str = word_tokenize(search_str)
        search_str = [self.stemming(word) for word in search_str]

        offer = " ".join([self.title, self.description, self.skills])
        offer = word_tokenize(offer)
        offer = [self.stemming(word) for word in offer]
        intersection = set(search_str) & set(offer)
        if len(intersection) > 0:
            self.score = len(intersection)
            return len(intersection)




    def stemming(self, text, mystem=m):
        try:
            return " ".join(mystem.stem(text)).strip()
        except:
            return " "