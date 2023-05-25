import re
import spacy
from spaczz.matcher import FuzzyMatcher

# remove common words, spaces from addresses
def refine_string(ad):
    punc_pattern = r'[^\w\s]'
    ad = re.sub(punc_pattern, ' ', ad)
    ad = re.sub('pin', ' ', ad)
    ad = re.sub('pune', ' ', ad)
    ad = ad.split(' ')
    ad = [i for i in ad if not i == '']
    ad = ' '.join(ad)
    return ad

# replace the matches with correct ones
def correct_string(ad, matcher, nlp):
    doc = nlp(ad)
    matches = matcher(doc)
    for i in range(len(matches)):
        match_id, start, end, counts = matches[i]
        match_text = doc[start:end:].text
        if match_text != match_id and counts > 85:
            temp_ad = [doc[:start].text]
            temp_ad += [match_id]
            temp_ad += [doc[end:].text]
            doc = nlp(' '.join(temp_ad).strip())
    return doc.text


class preProcessor:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.cleaned_addr_list = self.clean_addr()
        self.corrected_addr_list = self.correct_addr()
        pass

    def clean_addr(self):        
        with open(self.filename, 'r', encoding="utf8") as file:
            addr = [i.strip().split(',')[1].strip().lower() for i in file]

        cleaned_addr = []
        for ad in addr:
            # preprocess-the string
            ad = refine_string(ad)
            if len(ad) <= 7:
                temp_ad = ''.join(ad.split(' '))
                alpha_c = 0
                for i in temp_ad:
                    if i.isalpha():
                        alpha_c += 1
                
                # this is to include small addresses like 'd p rd', 'jm rd', 'iiser', 'ncl col'
                if alpha_c == len(temp_ad) and alpha_c >=4 : 
                    cleaned_addr.append(ad)
            else:
                cleaned_addr.append(ad)


        return cleaned_addr
    
    def correct_addr(self):
        nlp = spacy.blank('en')
        matcher = FuzzyMatcher(nlp.vocab)
        matcher.add("apartment", list(map(nlp, ['appt', 'aprt', 'apartment'])), kwargs=[{"fuzzy_func": "simple"}])
        matcher.add("college", list(map(nlp, ['college'])))
        matcher.add("society", list(map(nlp, ['soc', 'society'])))
        matcher.add("colony", list(map(nlp, ['col', 'colony', 'colnay', 'coloni','conlay'])))
        matcher.add("chawl", list(map(nlp, ['chal', 'chawl'])))
        matcher.add("chowk", list(map(nlp, ['chowk', 'choul'])))
        matcher.add("street", list(map(nlp, ['street', 'strit', 'st'])))
        matcher.add("street", list(map(nlp, ['street', 'strit', 'st'])))
        matcher.add("gaon", list(map(nlp, ['gav', 'gaon'])))
        matcher.add("nagar", list(map(nlp, ['ngr', 'nagar'])))
        matcher.add("flat no", list(map(nlp, ['f no', 'flt no'])))

        corrected_addr = [correct_string(addr, matcher, nlp) for addr in self.cleaned_addr_list]

        corrected_addr = list(set(corrected_addr))
        return corrected_addr
