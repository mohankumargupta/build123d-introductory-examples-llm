from google import genai
from google.genai import types
from dotenv import load_dotenv
import os


load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={'api_version':'v1alpha'},
)

"""response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works"
)
"""

with open("gemini_prompt.txt", "r") as f:
    content = f.read()

response = client.models.generate_content(
    model="gemini-2.0-flash", 
    contents=content,
    config=types.GenerateContentConfig(
        temperature=0.25,
        tools=[types.Tool(
            google_search=types.GoogleSearchRetrieval
        )]  
    )
)

response_text = response.text

with open("gemini_response.py", "w") as f:
    response_text = response_text.replace("```python", "").replace("```", "")
    f.write(response_text)

