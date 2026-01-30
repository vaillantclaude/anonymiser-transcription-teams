from fastapi import FastAPI
from pydantic import BaseModel
from anonymisation import anonymiser_transcription
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # autorise toutes les origines
    allow_credentials=True,
    allow_methods=["*"],  # autorise GET, POST, OPTIONS, etc.
    allow_headers=["*"],
)

class Texte(BaseModel):
    contenu: str

@app.post("/anonymiser")
def anonymiser(t: Texte):
    resultat = anonymiser_transcription(t.contenu)
    return {"texte_anonymise": resultat}
