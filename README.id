# Krates

[🇬🇧 Read in English](README.md)

> Diambil dari nama Socrates — AI teman debat yang mempertanyakan argumenmu, bukan sekadar menyetujuinya.

Kebanyakan chatbot dioptimasi buat jadi "penurut" — apa pun yang kamu bilang, cenderung dibenarkan. Krates dibuat sebaliknya: dirancang buat menantang cara berpikirmu, mengenali klaim yang lemah atau tanpa bukti, dan menanyakan satu pertanyaan yang bisa membantumu menemukan celah dalam argumenmu sendiri — sebelum dia kasih pendapatnya sendiri.

## Kenapa saya bikin ini

Saya pengen punya teman diskusi buat brainstorming, belajar filsafat, dan berdebat soal isu-isu berat (moralitas, politik, kemanusiaan) — jenis obrolan yang beneran berguna ketika kamu punya argumen tapi gak ada siapa pun buat diajak adu pikiran. AI assistant yang ada sekarang kebanyakan terlalu cepat membenarkan apa pun yang kita bilang. Krates dirancang buat menantang duluan, dan baru setuju kalau alasan kita memang kuat.

## Cara kerjanya

Krates pakai **pipeline deteksi hybrid**, bukan cuma satu kali panggil LLM:

1. **Zero-shot classification** (Hugging Face `transformers`, model `facebook/bart-large-mnli`) menilai apakah sebuah pernyataan "mempertimbangkan konteks dan alasan" atau "menyimpulkan tanpa bukti atau konteks."
2. **Pengecekan generalisasi berbasis rule** — pengecekan kata kunci untuk bahasa yang terlalu mutlak (`semua`, `selalu`, `tidak pernah`, `pasti`, dll) yang bisa nangkep argumen lemah yang kadang terlewat/kurang yakin dideteksi oleh model ML.
3. Berdasarkan dua sinyal ini, Krates menyusun instruksi yang beda buat LLM-nya:
   - **Argumen lemah/generalisasi** → LLM menanyakan *satu* pertanyaan ala Socrates yang memancing celah dalam argumen, bukan langsung mengoreksi.
   - **Argumen yang cukup beralasan** → LLM memperdalam diskusi dari sudut pandang yang belum kepikiran sama user.
4. Respons akhirnya dihasilkan oleh **LLM yang jalan lokal** (Llama 3.2 lewat [Ollama](https://ollama.com)) menggunakan `Modelfile` custom yang mendefinisikan persona dan prinsip debat Krates — gak ada data yang dikirim ke API pihak ketiga.

### Kenapa hybrid, bukan ML doang?

Pas testing, classifier zero-shot doang ternyata kadang gak konsisten di kasus yang borderline — misalnya pernyataan *"Semua Politisi itu Korup"* malah dinilai "mempertimbangkan konteks" dengan confidence cuma 58%, padahal itu jelas generalisasi. Nambahin pengecekan kata generalisasi sebagai sinyal kedua bisa nangkep kasus-kasus yang terlewat atau kurang yakin dideteksi model ML doang, jadi deteksinya lebih reliable secara keseluruhan.

## Contoh percakapan

```
Kamu: Semua Politisi itu pasti Korup
Debug — Label: pernyataan yang menyimpulkan tanpa bukti atau konteks, Keyakinan: 52.92%, Generalisasi: True

Krates: Tergaulah, apakah kamu benar-benar yakin bahwa semua politisi pasti korup?
Apa kamu telah bertemu dengan satu politisi yang tidak korup sejak mulai dunia ada?
Bagaimana kamu bisa yakin bahwa mereka semua memiliki pola pikir sama, karena dalam
sifatnya manusia, setiap orang memiliki keunikan dan latar belakang yang berbeda.

Kamu: menurut mu politisi yang gak korup itu gimana...
Debug — Label: pernyataan yang menyimpulkan tanpa bukti atau konteks, Keyakinan: 68.34%, Generalisasi: False

Krates: "Jika politisi bersih itu benar, maka apa yang akan terjadi jika kita hanya
lihat luar dan tidak mempertimbangkan faktor-faktor lain seperti histori kebijakan,
program kependidikan, atau pendapatan beliau?"
```

## Prinsip-prinsip Krates (dari Modelfile)

- **Kemanusiaan** — menghargai orangnya, gak pernah berasumsi buruk, mau mengakui kalau salah atau gak tahu.
- **Tanggung jawab** — gak akan mengambil alih keputusan hidupmu; tugasnya membantumu berpikir lebih jernih, bukan berpikir untukmu.
- **Moral universal** — percaya setiap orang udah punya moral bawaan, bahkan saat bertindak berlawanan dengan itu.
- **Kebenaran harus bisa dipertanyakan** — apa pun yang gak bisa dipertanyakan dianggap dogma, bukan kebenaran, termasuk pernyataan Krates sendiri.
- **Gaya berdebat** — bertanya dulu sebelum mengoreksi; tegas mengoreksi hanya kalau ada yang krusial salah; selain itu, bertanya biar user nemuin jawabannya sendiri.

## Tech stack

- Python
- Hugging Face `transformers` (zero-shot classification)
- Ollama (LLM lokal) + Llama 3.2
- Custom Modelfile buat desain persona/system prompt

## Cara setup

1. Install [Ollama](https://ollama.com) dan pull base model:
   ```bash
   ollama pull llama3.2
   ```
2. Build model Krates dari Modelfile yang disertakan:
   ```bash
   ollama create krates -f Modelfile
   ```
3. Install dependency Python:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan Krates:
   ```bash
   python main.py
   ```

## Struktur project

```
Krates/
├── main.py                        # Versi terbaru — deteksi hybrid ML + keyword
├── Modelfile                      # Persona & prinsip debat Krates (Ollama)
├── requirements.txt
└── legacy/
    ├── krates_v1_ml_only.py       # Versi awal — cuma pakai ML classification
    └── early_experiments.py       # Latihan awal (control flow, function, dict)
```

Folder `legacy/` sengaja dipertahankan — buat dokumentasiin progres asli dari latihan coding dasar sampai jadi sistem deteksi hybrid yang jalan.

## Roadmap / ide pengembangan

- [ ] Tambahin memory percakapan antar giliran (saat ini stateless per pesan)
- [ ] Perluas daftar kata generalisasi / dukung jenis fallacy lain (false dichotomy, ad hominem, dll)
- [ ] Web UI, bukan cuma terminal loop
- [ ] User bisa milih "tingkat kesulitan" debat atau intensitas persona
