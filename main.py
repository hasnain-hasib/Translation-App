
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from transformers import AutoTokenizer
import ctranslate2
import fasttext



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class TranslationRequest(BaseModel): 
    text: str
model_path = "quantiazed_model"
translator = ctranslate2.Translator(model_path)
tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
lid_model_path = "lid.176.ftz"
lid_model = fasttext.load_model(lid_model_path)


@app.get("/")
async def root():
    return HTMLResponse(content=open("static/index.html", "r").read(), status_code=200)

@app.post("/translate") 
async def translate(request: TranslationRequest):
    text = request.text


    predictions = lid_model.predict(text, k=1)
    detected_language = predictions[0][0].replace("__label__", "")

    source = tokenizer.convert_ids_to_tokens(tokenizer.encode(request.text))
    target_prefix = ["ben_Beng"]
    results = translator.translate_batch([source], target_prefix=[target_prefix])
    target = results[0].hypotheses[0][1:]  [1:]
    translation = tokenizer.decode(tokenizer.convert_tokens_to_ids(target))
    return {"translation": translation, "language": detected_language} 

@app.post("/language-detection")
async def language_detection(request: TranslationRequest):
    text = request.text
    predictions = lid_model.predict(text, k=1)
    detected_language = predictions[0][0].replace("__label__", "")

    return {"language": detected_language}
