from chatterbot import ChatBot
import spacy
nlp = spacy.load("en_core_web_sm")
bot = ChatBot('bot')
from chatterbot.trainers import ListTrainer

trainer = ListTrainer(bot)

trainer.train([
    'How are you?',
    'I am good.',
    'That is good to hear.',
    'Thank you',
    'You are welcome.',
])
while True:
    request = input('Van: ')
    response = bot.get_response(request)
    print(response)

