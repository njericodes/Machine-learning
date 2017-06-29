#coding a simple chatbot
from textblob import TextBlob
import random
import logging
import os

os.environ['NLTK_DATA'] = os.getcwd() + '/nltk_data'

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

GREETINGS = ("hello", "hi", "how are you", "hi obama", "what's up")
RESPONSE = ["how are you", "hello to you", "hello"]
LOML = ("michelle", "michelle obama")

RANDOM_ANSWER =[ "Obama out!", 
                 "You just kinda gotta let it *dusts shoulder* you know", 
                 "Its what you gotta do",
                 "Hey! Get outta here", 
                 "All of you know who I am"]
                 
OBAMA_COMEBACK = ["I'd like to know what I'm talking about before I speak",
                  "Listen! You're in my house!",
                  "What the heck are you talking about?",
                  "He thought happy hour started earlier", 
                  "What more do you think I should do"]

def greeting(sentence):
    for word in sentence.words:
        if word.lower() in GREETINGS:
            return random.choice(RESPONSE)
        
def obama_reply(sentence):
    logger.info("ObamaBot: respond to %s", sentence)
    resp = respond(sentence)
    return resp

def find_pronoun(sent):
    pronoun = None
    for w,p in sent.pos_tags:
        if p == 'PRP' and w.lower() == 'you':
            pronoun = 'I'
        if p == 'PRP' and w == 'I':
            pronoun = "You"
    return pronoun

def find_noun(sent):
    noun = None
    if not noun:
        for w,p in sent.pos_tags:
            if p == 'NN':
                noun = w
                break
    if noun:
        logger.info("Found noun: %s", noun)
    
    return noun

def find_verb(sent):
    verb = None
    pos = None
    for w,p in sent.pos_tags:
        if p.startswith('VB'):
            verb = w
            pos = p
            break
    return verb, pos

def find_adj(sent):
    adj = None
    for w,p in sent.pos_tags:
        if p == 'JJ':
            adj = w
            break
    return adj
            
def an_and_a(word):
    return True if word[0] in 'aeiou' else False

def construct_response(pronoun, noun, verb):
    response = []
    
    if pronoun:
        response.append(pronoun)
    
    
    return "f"

def about_obama(pronoun, noun, adjective, verb):
    resp = None
    if pronoun == 'I' and (noun and adjective):
        if noun:
            if random.choice((True, False)):
                resp = random.choice(OBAMA_NOUN).format(**{'noun': noun})
        else:
            resp = random.choice(OBAMA_VERB).format(**{'verb':verb})  
    return resp

OBAMA_NOUN = ["You're about four and a half years late on {noun} issue", 
              "I was fighting the {noun} fight!", 
              "Was that my {noun} oh goodness! Thats alright.",
              "The fact of the matter is the {noun} was 1.3 trillion dollars. 1.3!",  
              "And we've got {noun} in this country! Which is great too!", 
              "Ask Michelle about {noun}", 
              "Your {noun} wasn't complicated, it was wrong!", 
              "This is the kinda {noun} designed to divide us", 
              "This is Barack Obama's {noun} plan",
              "We we have fewer horses and {noun}"]
              
OBAMA_VERB = ["I'm looking forward to you {verb} me as well", 
              "What the heck are you {verb} about", 
              "Please {verb} governor", 
              "I know cuz I {verb} both of them", 
              "Well, I would have to investigate more Bill's {verb} before I accurately judge whether he was infact a brother", 
              "You said it was going to be {verb} and easy. You were wrong.",
              "I don't understand {verb}",
              "Who are they {verb} for?",
              "This is part of the {verb} I've been going through for the past fifteen months",
              "You're gonna sue me for {verb} my job?"]
              
def preprocess_text(sentence):
    processed = []
    words = sentence.split(' ')
    for w in words:
        if w == 'i':
            w = 'I'
        if w == "i'm":
            w = "I'm"
        if w.lower() in LOML:
            w = "LOML"
        processed.append(w)
        
    return ' '.join(processed)
    
def respond(sentence):
    processed = preprocess_text(sentence)
    parsed = TextBlob(processed)
    
    pronoun, noun, adjective, verb = token_sentence(parsed)
    
    resp = about_obama(pronoun, noun, adjective, verb)
    
    if not resp:
        resp = greeting(parsed)
        
    if not resp:
        if not pronoun:
            resp = random.choice(RANDOM_ANSWER)
        elif pronoun == 'I' and not verb:
            resp = random.choice(OBAMA_COMEBACK)
        else:
            resp = construct_response(pronoun, noun, verb)
    
    if not resp:
       resp = random.choice(RANDOM_ANSWER)
     
    logger.info("Returning phrase '%s'", resp)
    
    return resp
    
def token_sentence(sentence):
    pronoun = None
    noun = None
    verb = None
    adjective = None
    
    for s in sentence.sentences:
        pronoun = find_pronoun(s)
        noun = find_noun(s)
        verb = find_verb(s)
        adjective = find_adj(s)
    
    return pronoun, noun, adjective, verb

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 0:
        out = sys.argv[1]
    else:
        out = "Issa ObamaBot"
    print(obama_reply(out))
