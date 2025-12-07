# NEL Demo - spaCy NER+NEL GUI

**[🇬🇧 Engleska verzija / English version](README.md)**

Jednostavna demonstraciona aplikacija za Prepoznavanje Imenovanih Entiteta (NER) i Povezivanje Imenovanih Entiteta (NEL) korišćenjem spaCy modela sa minimalnim GUI interfejsom.

## Karakteristike

- ✅ **Jednostavna instalacija**: Automatski instaleri za Windows (PowerShell) i Linux/Mac (Bash)
- ✅ **Provera verzije Python-a**: Osigurava da je instaliran Python 3.10 ili viši
- ✅ **Virtuelno okruženje**: Automatski kreira i upravlja virtuelnim okruženjem
- ✅ **Fleksibilne zavisnosti**: Izbor između standardnog spaCy ili spacy-transformers
- ✅ **Jednostavan GUI**: Korisnički interfejs napravljen sa tkinter-om
- ✅ **Upravljanje modelima**: Učitavanje custom treniranih modela iz `models/` direktorijuma
- ✅ **Obrada teksta**: Obrada bilo kog teksta i ekstrakcija imenovanih entiteta
- ✅ **Transliteracija ćirilice**: Automatska transliteracija sa ćiriličnog na latinično pismo za bolju NER tačnost
- ✅ **Pametno deljenje teksta**: Automatski deli velike tekstove po granicama paragrafa
- ✅ **Vizuelni izlaz**: Generisanje lepih HTML vizuelizacija koristeći displaCy
- ✅ **Upravljanje izlazom**: Čuvanje svih izlaza u `data/outputs/` sa vremenskim oznakama
- ✅ **Sveobuhvatno testiranje**: Kompletna test suite sa pytest

## Struktura projekta

```
NEL_Demo/
├── install.ps1              # Windows instaler (PowerShell)
├── install.sh               # Linux/Mac instaler (Bash)
├── requirements.txt         # Python zavisnosti
├── README.md               # Engleski README
├── README.sr.md            # Ovaj fajl (srpska verzija)
├── src/
│   ├── gui.py              # Glavna GUI aplikacija
│   └── text_chunker.py     # Modul za deljenje teksta za velike dokumente
├── tests/
│   └── test_text_chunker.py # Test suite za deljenje teksta
├── models/                 # Postavite vaše trenirane modele ovde
│   └── {ime_modela}/
│       └── model-best/     # Vaš trenirani spaCy model
├── inputs/                 # Ulazni tekstualni fajlovi
│   └── sample_text.txt     # Primer tekstualnog fajla
├── data/
│   └── outputs/            # HTML vizuelizacije izlaza
└── venv/                   # Virtuelno okruženje (kreirano od strane instalera)
```

## Zahtevi

- **Python**: 3.10 ili viši
- **Operativni sistem**: Windows, Linux, ili macOS
- **spaCy model**: Trenirani spaCy model postavljen u `models/{ime_modela}/model-best/`

## Instalacija

### Windows (PowerShell)

1. Otvorite PowerShell
2. Pozicionirajte se u direktorijum projekta (cd komanda)
3. Pokrenite instaler:

```powershell
.\install.ps1
```

### Linux/Mac (Bash)

1. Otvorite terminal
2. Pozicionirajte se u direktorijum projekta  
3. Pokrenite instaler:

```bash
./install.sh
```

### Šta instaler radi

Instaler će:
1. ✅ Proveriti da li je instaliran Python 3.10+
2. ✅ Kreirati virtuelno okruženje u `venv/`
3. ✅ Aktivirati virtuelno okruženje
4. ✅ Ažurirati pip na najnoviju verziju
5. ✅ Pitati vas da izaberete između:
   - Standardnog spaCy (brži, manji)
   - spacy-transformera (precizniji, veći)
6. ✅ Instalirati sve potrebne zavisnosti

## Podešavanje modela

### Unapred instaliran model

Srpski NER+NEL model (`trsic4-CNN-ner-nel`) je već instaliran u `models/` direktorijumu i spreman je za upotrebu. Nije potrebno dodatno podešavanje!

### Korišćenje vašeg sopstvenog treniranog modela

Ako imate trenirani spaCy model:

1. Kreirajte direktorijum: `models/{ime_vašeg_modela}/`
2. Postavite vaš trenirani model u: `models/{ime_vašeg_modela}/model-best/`

Struktura treba da izgleda ovako:
```
models/
└── ime_vašeg_modela/
    └── model-best/
        ├── config.cfg
        ├── meta.json
        ├── tokenizer
        ├── ner/
        └── ... (ostali fajlovi modela)
```

## Korišćenje

### Pokretanje aplikacije

**Windows:**
```powershell
.\venv\Scripts\Activate.ps1
python src/gui.py
```

**Linux/Mac:**
```bash
source venv/bin/activate
python src/gui.py
```

### Korišćenje GUI-a

1. **Izaberite model**: 
   - Izaberite vaš model iz padajuće liste
   - Kliknite "Load Model" da ga učitate
   - Sačekajte poruku potvrde

2. **Konfigurišite opcije obrade**:
   - **Transliteracija ćirilice u latinicu**: Podrazumevano uključeno (ako je instaliran paket `cyrtranslit`)
   - Ova opcija automatski konvertuje ćirilični tekst u latinicu pre obrade za bolje prepoznavanje entiteta

3. **Unesite tekst**:
   - Ukucajte ili nalepite tekst u polje za unos
   - Ili kliknite "Load Sample Text" za demo
   - Ili kliknite "Load from File" da učitate tekstualni fajl iz `inputs/` fascikle

4. **Obradite tekst**:
   - Kliknite "Process Text (NER)" da analizirate tekst
   - Pogledajte entitete u sekciji rezultata
   - HTML vizuelizacija se automatski čuva

5. **Pogledajte rezultate**:
   - Kliknite "View Last Output" da otvorite HTML u vašem pretraživaču
   - Kliknite "Open Output Folder" da vidite sve sačuvane izlaze

### Funkcija transliteracije ćirilice

Aplikacija uključuje automatsku transliteraciju ćirilice u latinicu za poboljšanje tačnosti NER-a kada koristite modele trenirane prvenstveno na latiničnom pismu:

- **Automatska konverzija**: Konvertuje ćirilični tekst sa sedam jezika (srpski, crnogorski, makedonski, ruski, ukrajinski, kazahstanski, bugarski) u latinično pismo pre obrade
- **Podrazumevano uključeno**: Opcija transliteracije je podrazumevano označena (ako je `cyrtranslit` instaliran)
- **Može se isključiti**: Može se onemogućiti preko checkbox-a ako preferirate direktnu obradu ćiriličnog teksta
- **Čuva entitete**: Latinični tekst ostaje nepromenjen; samo se ćirilični karakteri transliterišu
- **Bolja tačnost**: Modeli trenirani na latiničnom pismu tipično imaju bolje performanse sa transliterovanim tekstom

**Primer**: Ćirilični tekst "Новак Ђоковић рођен у Београду" se automatski transliteriše u "Novak Đoković rođen u Beogradu" pre slanja u NER pipeline.

**Napomena**: Ako imate model specifično treniran na ćiriličnom tekstu, možete onemogućiti ovu opciju tako što ćete odznačiti polje "Transliteriši ćirilicu u latinicu pre obrade".

### Primer

Probajte ovaj primer teksta:
```
Народна банка Србије је централна банка Републике Србије са седиштем у Београду. 
Гувернер Народне банке Србије је Јоргованка Табаковић која се налази на тој позицији од 2012. године. 
Новак Ђоковић је српски тенисер рођен у Београду 1987. године.
```

Aplikacija će:
- Ekstraktovati entitete kao što su "Народна банка Србије" (ORG), "Јоргованка Табаковић" (PERSON), "Београд" (GPE)
- Prikazati oznake entiteta i pozicije
- Generisati HTML vizuelizaciju sa istaknutim entitetima
- Sačuvati izlaz u `data/outputs/ner_output_YYYYMMDD_HHMMSS.html`

### Obrada teksta sa deljenjem po paragrafima

Aplikacija automatski koristi deljenje za svaki tekst sa više paragrafa:
- **Pametno deljenje**: Paragrafi se grupišu u odgovarajuće veličine (do 100K karaktera svaki) da bi se sačuvala logička struktura i poboljšala preciznost NER-a
- **Automatska obrada**: Svaki deo se obrađuje odvojeno sa spaCy NER-om
- **Spojeni izlaz**: Svi delovi se kombinuju u jednu HTML vizuelizaciju
- **Vizuelno razdvajanje**: Prelomi sekcija se dodaju između delova u izlazu
- **Bolji kontekst**: Obrada teksta sa granicama paragrafa pomaže spaCy-u da održi jasniji kontekst za prepoznavanje entiteta

Tekstovi sa jednim paragrafom se obrađuju normalno bez dodatnog opterećenja deljenja. Ovaj pristup osigurava optimalnu NER performansu uz održavanje čitljivosti i strukture originalnog teksta.

## Format izlaza

Svaki obrađeni tekst generiše HTML fajl sa:
- Originalnim tekstom sa istaknutim entitetima
- Entitetima obojenim po tipu
- Interaktivnom vizuelizacijom
- Vremenskom oznakom u nazivu fajla

Izlazni fajlovi se čuvaju u: `data/outputs/`

## Rešavanje problema

### "Python is not installed or not in PATH"
- Instalirajte Python 3.10 ili viši sa [python.org](https://www.python.org/downloads/)
- Uverite se da ste označili "Add Python to PATH" tokom instalacije

### "No models found"
- Uverite se da ste postavili trenirani model u `models/{ime_modela}/model-best/`
- Proverite da li je struktura direktorijuma modela ispravna
- Pokušajte da preuzmete pre-trenirani model (pogledajte "Podešavanje modela")

### "Error loading model"
- Verifikujte da su fajlovi modela kompletni i nisu oštećeni
- Uverite se da je model kompatibilan sa vašom verzijom spaCy-a
- Pokušajte ponovo da preuzmete ili trenirate model

### GUI se ne pokreće
- Uverite se da ste aktivirali virtuelno okruženje
- Proverite da su sve zavisnosti instalirane: `pip list`
- Na Linuxu, možda treba da instalirate tkinter: `sudo apt-get install python3-tk`

## Napredno korišćenje

### Treniranje vašeg sopstvenog modela

Da trenirate custom NER+NEL model sa spaCy-em:

1. Pripremite vaše podatke za treniranje
2. Kreirajte spaCy projekat ili config
3. Trenirajte model:
   ```bash
   python -m spacy train config.cfg --output ./models/moj_model
   ```
4. Trenirani model će biti u `models/moj_model/model-best/`

Za više informacija, pogledajte [spaCy dokumentaciju za treniranje](https://spacy.io/usage/training).

### Korišćenje Transformer modela

Za bolju preciznost, koristite modele bazirane na transformer-ima:

1. Instalirajte spacy-transformers tokom podešavanja (opcija 2)
2. Trenirajte ili preuzmite transformer model
3. Postavite ga u models direktorijum

Napomena: Transformer modeli su veći i sporiji, ali precizniji.

## Zavisnosti

Osnovne zavisnosti (instaliraju se automatski):
- `spacy>=3.7.0` - Osnovna NLP biblioteka
- `cyrtranslit>=1.0.0` - Transliteracija ćirilice u latinicu
- `tkinter-tooltip>=2.0.0` - GUI tooltips (opciono)

Opciono:
- `spacy-transformers` - Za modele bazirane na transformer-ima

Razvojne zavisnosti:
- `pytest` - Za pokretanje testova

## Testiranje

Projekat uključuje sveobuhvatne testove za funkcionalnost deljenja teksta.

Da pokrenete testove:

```bash
# Prvo aktivirajte virtuelno okruženje
# Windows:
.\venv\Scripts\Activate.ps1

# Linux/Mac:
source venv/bin/activate

# Instalirajte pytest (ako već nije instaliran)
pip install pytest

# Pokrenite sve testove
python -m pytest tests/test_text_chunker.py -v

# Pokrenite specifičnu test klasu
python -m pytest tests/test_text_chunker.py::TestChunkText -v
```

Test suite uključuje:
- **Testove deljenja paragrafa**: Verifikacija ispravnog rukovanja različitim formatima paragrafa
- **Testove deljenja teksta**: Osiguravanje pravilnog deljenja na različitim granicama veličine
- **Testove spajanja HTML-a**: Validacija ispravnog spajanja više HTML izlaza
- **Testove graničnih slučajeva**: Testiranje Unicode-a, specijalnih karaktera, veoma dugih rečenica
- **Integracione testove**: Validacija celokupnog radnog toka

## Licenca

Ovaj projekat je posvećen javnom domenu pod CC0 1.0 Universal (CC0 1.0) Public Domain Dedication - pogledajte LICENSE fajl za detalje.

## Doprinos

Doprinosi su dobrodošli! Slobodno pošaljite Pull Request.

## Podrška

Za pitanja ili probleme:
- Proverite sekciju za rešavanje problema
- Posetite [spaCy dokumentaciju](https://spacy.io/)
- Otvorite issue na GitHub-u

## Zahvalnice

- Napravljeno sa [spaCy](https://spacy.io/)
- Vizuelizacija omogućena pomoću [displaCy](https://spacy.io/usage/visualizers)
- GUI napravljen sa Python-ovim tkinter-om

Napravili:
- [**TESLA** - Text Embeddings - Serbian Language Applications](https://tesla.rgf.bg.ac.rs/)
- [**Language Resources and Technologies Society - Jerteh**](https://jerteh.rs/)

---

**Srećno prepoznavanje entiteta! 🎯**
