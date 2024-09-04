

import openai
from dotenv import load_dotenv
from app import crud, models
import os
import threading
from sqlalchemy.orm import Session

load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

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
            generate_text = response.choices[0].message['content'].strip()
            crud.create_generated_content(db, generate_text, search_term.id)
            return generate_text
        except Exception as e:
            print(f"Error occurred: {e}")
            return "Error occurred while generating content."   
    
