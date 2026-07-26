import requests
from transformers import pipeline

# Load ML model
print("Loading Krates ML...")
krates_transformer = pipeline(
    "zero-shot-classification",
    model="typeform/distilbart-mnli-12-3"
)
print("Krates ML siap!")

def krates_berpikir(argumen_user):
    hasil_ml = krates_transformer(
        argumen_user,
        candidate_labels=[
            "pernyataan yang mempertimbangkan konteks dan alasan",
            "pernyataan yang menyimpulkan tanpa bukti atau konteks"
        ]
    )
    
    label = hasil_ml["labels"][0]
    keyakinan = hasil_ml["scores"][0]
    
    print(f"Debug — Label: {label}, Keyakinan: {keyakinan:.2%}")
    
    if "tanpa bukti" in label or keyakinan < 0.65:
        instruksi = f"""
        User berkata: "{argumen_user}"
        Argumen ini terdeteksi lemah atau ambigu.
        Sebagai Krates, tanya SATU pertanyaan yang memancing user menemukan kelemahannya sendiri.
        Jangan langsung koreksi — tanya dulu.
        """
    else:
        instruksi = f"""
        User berkata: "{argumen_user}"
        Argumen ini mempertimbangkan konteks dengan baik.
        Sebagai Krates, perdalam debatnya dari sudut pandang yang belum dipikirkan user.
        """
    
    return instruksi

def krates_respond(argumen_user):
    instruksi = krates_berpikir(argumen_user)
    
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "krates",
            "messages": [
                {"role": "user", "content": instruksi}
            ],
            "stream": False
        }
    )
    
    hasil = response.json()
    return hasil["message"]["content"]

# Loop utama Krates
print("\nKrates siap berdebat. Ketik 'keluar' untuk berhenti.\n")
while True:
    argumen = input("Kamu: ")
    if argumen.lower() == "keluar":
        print("Krates: Sampai jumpa. Teruslah mempertanyakan kebenaran.")
        break
    print(f"\nKrates: {krates_respond(argumen)}\n")