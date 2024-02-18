from duckduckgo_search import DDGS
import bs4 as bs
import requests

class ScrapData:
    def __init__(self,prompt="cars",num_results=10):
        self.prompt = prompt
        self.num_results = num_results
    
    def scrap(self): 
        with DDGS() as ddgs:
            self.results = [r for r in ddgs.text(self.prompt, max_results=self.num_results)]
        return self.results
    