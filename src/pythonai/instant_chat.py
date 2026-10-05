from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model

model = init_chat_model(model="gemma4:31b-cloud", model_provider="ollama") # actually it automatically infer the provider but you can be deterministic
resp = model.invoke("hello in a single word")
print(resp)
print(resp.content)