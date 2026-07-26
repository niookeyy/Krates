import requests
from transformers import pipeline

# Load ML model
print("Loading Krates ML...")
krates_transformer = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)
print("Krates ML siap!\n")

kata_generalisasi = ["semua", "selalu", "tidak pernah", "setiap", "pasti", "mustahil"]

def krates_berpikir(argumen_user):
    # Cek generalisasi dulu
    argumen_lower = argumen_user.lower()
    ada_generalisasi = any(kata in argumen_lower for kata in kata_generalisasi)
    
    hasil_ml = krates_transformer(
        argumen_user,
        candidate_labels=[
            "pernyataan yang mempertimbangkan konteks dan alasan",
            "pernyataan yang menyimpulkan tanpa bukti atau konteks"
        ]
    )
    
    label = hasil_ml["labels"][0]
    keyakinan = hasil_ml["scores"][0]
    
    print(f"Debug — Label: {label}, Keyakinan: {keyakinan:.2%}, Generalisasi: {ada_generalisasi}")
    
    if "tanpa bukti" in label or keyakinan < 0.70 or ada_generalisasi:
        return f'User berkata: "{argumen_user}". Argumen lemah karena generalisasi tanpa bukti. Sebagai Krates, tanya SATU pertanyaan yang memancing user menemukan kelemahannya sendiri. Jangan langsung koreksi.'
    else:
        return f'User berkata: "{argumen_user}". Argumen kuat. Sebagai Krates, perdalam debatnya dari sudut pandang yang belum dipikirkan user.'

    # label = hasil_ml["labels"][0]
    # keyakinan = hasil_ml["scores"][0]
    # print(f"Debug — Label: {label}, Keyakinan: {keyakinan:.2%}")
    # if "tanpa bukti" in label or keyakinan < 0.70:
    #     return f'User berkata: "{argumen_user}". Argumen lemah. Sebagai Krates, tanya SATU pertanyaan yang memancing user menemukan kelemahannya sendiri. Jangan langsung koreksi.'
    # else:
    #     return f'User berkata: "{argumen_user}". Argumen kuat. Sebagai Krates, perdalam debatnya dari sudut pandang yang belum dipikirkan user.'

def krates_respond(argumen_user):
    instruksi = krates_berpikir(argumen_user)
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "krates",
            "messages": [{"role": "user", "content": instruksi}],
            "stream": False
        }
    )
    return response.json()["message"]["content"]

# Loop utama
print("Krates siap berdebat. Ketik 'keluar' untuk berhenti.\n")
while True:
    argumen = input("Kamu: ")
    if argumen.lower() == "keluar":
        print("Krates: Sampai jumpa. Teruslah mempertanyakan kebenaran.")
        break
    print(f"\nKrates: {krates_respond(argumen)}\n")