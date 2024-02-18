from nltk import word_tokenize,pos_tag,sent_tokenize
import sqlite3
from fuzzywuzzy import fuzz
import spacy
from CreateVectorDB import CreateVectorDB
from summarizer import Summarizer
import os

class ResponseGenerator:
    def __init__(self,prompt):
        self.prompt = prompt
        self.required_tagged_words=['NN', 'NNS'] 
                                    # 'CD', 'NNP', 
                                    # 'NNPS', 'SYM', 'VB']
                                    # 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        self.dbfilename='./db/vector.db'
        self.hyperlinks=[]
        self.nouns=set()
        self.processed_prompt=" "
        self.process_prompt()
        self.extract_subject()
        
    def extract_subject(self):
        self.nlp=spacy.load('en_core_web_sm')
        processed=self.nlp(self.prompt)
        # for token in processed:
            # print(f'{token.text} <{token.dep_}>')
        self.subject=[token.text for token in processed if token.dep_ in ['ROOT','nsubj','poss']]
        print(f'Main subject of prompt: {self.subject}')
        
    def process_prompt(self):
        self.sentences=sent_tokenize(self.prompt)
        # print(self.sentences)
        self.words=set()
        for sent in self.sentences:
            words=word_tokenize(sent)
            for word in words:
                # print(pos_tag([word]))
                if pos_tag([word])[0][1] in self.required_tagged_words:
                    self.words.add(word)
                if pos_tag([word])[0][1]=="NN":
                    self.nouns.add(word)
                # print(f'{pos_tag([word])[0][0]} <{pos_tag([word])[0][1]}>')
        
    def save_pre_processed_data(self):
        with open(os.path.join('data','relevant_records.txt'),'w',encoding='utf-8') as file:
            file.write(self.relevant_records)
        print(f"Records saved in ./{os.path.join('data','relevant_records.txt')}")
        
    def extractive_summary(self,save=False):
        summarizer=Summarizer()
        self.summary=summarizer(self.relevant_records)
        if save:
            with open(os.path.join('data','summary.txt'),'w',encoding='utf-8') as file:
                file.write(self.summary)
            print(f"Summary saved in ./{os.path.join('data','summary.txt')}")
        else:
                print("This is the summary:")
                print(self.summary)
            
    def generate_summary(self):
        # print(self.words)
        self.relevant_records=set()
        self.relevant_records_final=set()
        
        with CreateVectorDB() as db:
            all_records=db.query('select * from data')
        # Create a connection to the SQLite database
        conn = sqlite3.connect(self.dbfilename)
        
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()
        # for word in self.words:
        if len(self.subject)!=0:
            for subject in self.subject:
                for record in cursor.execute(f"select * from data where title like'%{subject}%' and href like '%{subject}%'").fetchall():
                    self.relevant_records.add(record[2])
                    self.hyperlinks.append(record[1])
        else:
            self.processed_prompt=self.processed_prompt.join(self.nouns)
            for (title,_,body) in all_records:
                    self.relevant_records.add(body)
        conn.commit()
        conn.close()
        self.relevant_records=" ".join(self.relevant_records)
        self.save_pre_processed_data()
        self.extractive_summary(True)
        return self.summary
        # return " ".join(self.relevant_records)
