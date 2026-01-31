# ⚽ Fantacalcio Manager

Sistema completo per la gestione e il calcolo dei risultati del Fantacalcio con regolamento personalizzato.

## 🚀 Caratteristiche

- **Gestione Giornate**: Crea e organizza le giornate di campionato
- **Gestione Partite**: Inserisci le partite con squadra casa e trasferta
- **Formazioni**: Inserisci le formazioni complete (11 titolari) con ruoli P, D, C, A
- **Voti Manuali**: Inserisci voti base e bonus/malus manualmente per ogni giocatore
- **Import Excel**: Carica file Excel ufficiali con calcolo automatico dei bonus/malus
- **Calcolo Risultati**: Motore di calcolo completo secondo il regolamento specificato
- **Database SQLite**: Persistenza completa di tutti i dati

## 📋 Requisiti

- Python 3.8+
- Dipendenze elencate in `requirements.txt`

## 🛠️ Installazione

1. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

2. Avvia l'applicazione:
```bash
streamlit run app.py
```

3. Apri il browser all'indirizzo mostrato (di solito `http://localhost:8501`)

## 📊 Struttura del Progetto

```
fantacalcio/
│
├── app.py                  # Applicazione Streamlit (UI principale)
├── calc.py                 # Motore di calcolo con funzioni pure
├── db.py                   # Gestione database SQLite
├── excel_import.py         # Import e parsing file Excel
├── requirements.txt        # Dipendenze Python
└── README.md              # Questo file
```

## 🎮 Guida all'Uso

### 1. Crea una Giornata
- Vai in "Gestione Giornate"
- Inserisci il numero della giornata e una descrizione opzionale
- Clicca "Crea Giornata"

### 2. Aggiungi una Partita
- Vai in "Gestione Partite"
- Seleziona la giornata
- Inserisci i nomi delle due squadre (casa e trasferta)
- Clicca "Crea Partita"

### 3. Inserisci le Formazioni
- Vai in "Inserimento Formazioni"
- Seleziona giornata e partita
- Per ogni squadra, inserisci gli 11 titolari con ruolo (P, D, C, A)
- Salva la formazione

### 4. Inserisci i Voti

#### Opzione A: Import da Excel
- Vai in "Import da Excel"
- Scarica il template se necessario
- Carica il file Excel con i voti ufficiali
- Seleziona la partita e applica i voti alla squadra desiderata
- I bonus/malus vengono calcolati automaticamente

#### Opzione B: Inserimento Manuale
- Vai in "Inserimento Voti"
- Seleziona giornata e partita
- Per ogni giocatore, inserisci:
  - Voto base
  - Bonus/malus totale
  - Note (es: SV)

### 5. Calcola il Risultato
- Vai in "Calcolo Risultati"
- Seleziona giornata e partita
- Clicca "Calcola Risultato"
- Visualizza il risultato dettagliato con tutti i modificatori

## 📐 Regolamento Implementato

### A) Voto Totale Giocatore
`Voto totale = Voto base + Bonus/Malus`

### B) Bonus/Malus da Eventi (Import Excel)
- **+3** per gol fatto
- **+1** per assist
- **+3** per rigore segnato
- **+3** per rigore parato
- **-3** per rigore sbagliato
- **-2** per autogol
- **-0.5** per ammonizione
- **-1** per espulsione
- **Portiere**: -1 per ogni gol subito, +1 porta inviolata (se gs=0)

### C) Voto Totale Squadra
Somma dei voti totali degli 11 titolari

### D) Modificatore Difesa
- Basato sulla media dei voti base dei difensori
- Tabella modificatore:
  - <5.00: +4
  - 5.00-5.24: +3
  - 5.25-5.49: +2
  - 5.50-5.74: +1
  - 5.75-5.99: 0
  - 6.00-6.24: -1
  - 6.25-6.49: -2
  - 6.50-6.74: -3
  - 6.75-6.99: -4
  - ≥7.00: -5

- Correzioni modulo:
  - 3 difensori: +1
  - 4 difensori: 0
  - 5 difensori: -1
  - Oltre 4 difensori: -1 per ogni difensore extra

**Il modificatore generato si applica alla squadra avversaria**

### E) Modificatore Centrocampo
- Se numero diverso di centrocampisti: aggiungi 5 d'ufficio a chi ne ha meno
- Calcola differenza assoluta delle somme:
  - <1: 0
  - 1-1.99: 0.5
  - 2-2.99: 1.0
  - 3-3.99: 1.5
  - 4-4.99: 2.0
  - 5-5.99: 2.5
  - 6-6.99: 3.0
  - 7-7.99: 3.5
  - ≥8: 4.0

Positivo a chi ha somma maggiore, negativo all'altro

### F) Modificatore Attacco
Per ogni attaccante con bonus/malus = 0:
- Voto base 6.50-6.99: +0.5
- Voto base 7.00-7.49: +1.0
- Voto base ≥7.50: +1.5

### G) Vantaggio Casa
+2 alla squadra di casa

### H) Conversione Punteggio in Gol
- <66: 0 gol
- 66-71.99: 1 gol
- 72-76.99: 2 gol
- 77-80.99: 3 gol
- 81-84.99: 4 gol
- Oltre 85: +1 gol ogni 4 punti aggiuntivi

## 📄 Formato File Excel

Il file Excel deve contenere le seguenti colonne:

| Colonna | Descrizione | Obbligatoria |
|---------|-------------|--------------|
| Ruolo | P, D, C, A | Sì |
| Nome | Nome del giocatore | Sì |
| Voto | Voto base (può contenere *) | Sì |
| Gf | Gol fatti | No |
| Gs | Gol subiti | No |
| Rp | Rigori parati | No |
| Rf | Rigori fatti | No |
| Rs | Rigori sbagliati | No |
| Au | Autogol | No |
| Amm | Ammonizioni | No |
| Esp | Espulsioni | No |
| Ass | Assist | No |

**Note sul Voto:**
- Se contiene `*` (es: "6*"), viene interpretato come voto con nota SV
- Se il giocatore non è nel file Excel, viene applicato fallback: voto 6.0, bonus/malus 0, nota SV

## 🗃️ Database

Il database SQLite (`fantacalcio.db`) viene creato automaticamente al primo avvio.

**Tabelle:**
- `giornate`: giornate di campionato
- `partite`: partite tra squadre
- `formazioni`: giocatori titolari di ogni squadra
- `voti`: voti e statistiche di ogni giocatore

## 🔧 Funzioni Pure e Testabili

Il motore di calcolo in `calc.py` è implementato con funzioni pure, facilmente testabili:

```python
from calc import calcola_bonus_malus_da_eventi, calcola_modificatore_difesa

# Esempio: calcola bonus/malus
bonus = calcola_bonus_malus_da_eventi(
    gol_fatti=2,
    assist=1,
    ammonizioni=1,
    ruolo='A'
)
# Risultato: +6.5 (2 gol = +6, 1 assist = +1, 1 amm = -0.5)

# Esempio: calcola modificatore difesa
mod = calcola_modificatore_difesa(
    voti_base_difensori=[6.0, 6.5, 7.0, 5.5],
    numero_difensori=4
)
# Risultato basato sulla media 6.25 e modulo 4 difensori
```

## 🐛 Risoluzione Problemi

### Il database non si crea
- Verifica i permessi della directory
- Controlla che SQLAlchemy sia installato correttamente

### Errore durante l'import Excel
- Verifica che il file contenga le colonne obbligatorie (Ruolo, Nome, Voto)
- Controlla che i nomi delle colonne siano scritti correttamente
- Usa il template fornito come riferimento

### I calcoli non sono corretti
- Verifica che tutte le formazioni abbiano 11 giocatori
- Controlla che i voti siano stati inseriti per tutti i giocatori
- Verifica i ruoli assegnati (P, D, C, A)

## 📝 Note Tecniche

- **Framework UI**: Streamlit 1.31.0
- **Database**: SQLite con SQLAlchemy ORM
- **Excel**: pandas + openpyxl
- **Calcoli**: Funzioni pure Python con type hints
- **Persistenza**: Completa, i dati rimangono tra le sessioni

## 🤝 Contributi

Il codice è strutturato in modo modulare per facilitare estensioni e modifiche.

## 📄 Licenza

Progetto didattico per gestione Fantacalcio.

---

**Buon divertimento con il tuo Fantacalcio! ⚽🏆**
