from chatterbot import ChatBot
import spacy
import json
nlp = spacy.load("en_core_web_sm")
bot = ChatBot('bot', storage_adapter='chatterbot.storage.SQLStorageAdapter',
                    input_adapter = 'chatterbot.input.TerminalAdapter',
                    output_adapter = 'chatterbot.output.TerminalAdapter')
from chatterbot.trainers import ListTrainer

# trainer = ListTrainer(bot)
# with open('test.json') as f:
#   data = json.load(f)

# # print(data)
# for i in data['conversation']:
#     trainer.train(i)
# while True:
#     request = input('Van: ')
#     response = bot.get_response(request)
#     print(response)

