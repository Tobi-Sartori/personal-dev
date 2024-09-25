import ollama
import hashlib

from rag.prompts import system_prompt
from cache.manager import CacheDB

class LlamaManager:
    def __init__(self):
        self.ollama = ollama
        self.model = 'llama3.1'
        self.db = CacheDB()


    def chat(self, question):
        question_hash = self.hash_question(question)
        cache_answer = self.verify_if_question_was_answered(question_hash)

        if cache_answer:
            return cache_answer
        
        messages = [{
            'role': 'system', 'content': system_prompt,
            'role': 'user', 'content': question}]
        
        model_answer = self.answer(messages)
        self.db.store_response(question_hash, model_answer)

        return model_answer
    
    def generate_answer(self, messages):
        response = self.ollama.chat(model=self.model, messages=messages)
        model_answer = response['message']['content']

        return model_answer
    
    def verify_if_question_was_answered(self, question_hash):
        cache_answer = self.db.get_response(question_hash)

        return cache_answer

    def hash_question(self, question):

        hash_object = hashlib.sha256(question.encode('utf-8'))  
        hashed_question = hash_object.hexdigest()

        return hashed_question

