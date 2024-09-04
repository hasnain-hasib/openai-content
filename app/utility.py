import openai
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app import crud, models
import os
import threading


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



semaphore = threading.Semaphore(5)

def generate_content(db: Session, topic: str) -> str:
    with semaphore:
        search_term = crud.get_search_term(db, topic)
        if not search_term:
            search_term = crud.create_search_term(db, topic)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    
                    {"role": "system", "content": "Assistant"},
                    {"role": "user", "content": f"Write an article about {topic}"}
                    
                    
                ]
            )
            generated_text = response.choices[0].message['content'].strip()
            
            crud.create_generated_content(db, generated_text, search_term.id)
            return generated_text
        
        except Exception as e:
            print(f"Error occurred: {e}")
            error_message = "Error occurred while generating content."
            
            crud.create_generated_content(db, error_message, search_term.id)
            return error_message
