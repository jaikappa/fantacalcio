# ⚡ Quick Start Guide

Guida rapida per avviare l'applicazione in 3 passi.

## 🚀 Avvio Rapido (3 passi)

### 1️⃣ Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 2️⃣ Avvia l'applicazione

```bash
streamlit run app.py
```

Oppure usa lo script di avvio:

```bash
./start.sh
```

### 3️⃣ Apri il browser

L'applicazione si aprirà automaticamente su: **http://localhost:8501**

---

## 📝 Primo Utilizzo

### Passo 1: Crea una Giornata
1. Clicca su "📅 Gestione Giornate" nel menu laterale
2. Vai nella tab "Crea Nuova Giornata"
3. Inserisci numero giornata (es: 1)
4. Aggiungi una descrizione (opzionale)
5. Clicca "✅ Crea Giornata"

### Passo 2: Crea una Partita
1. Clicca su "⚽ Gestione Partite"
2. Tab "Crea Nuova Partita"
3. Seleziona la giornata creata
4. Inserisci nome squadra casa (es: "Milan")
5. Inserisci nome squadra trasferta (es: "Inter")
6. Clicca "✅ Crea Partita"

### Passo 3: Inserisci le Formazioni
1. Vai in "👥 Inserimento Formazioni"
2. Seleziona giornata e partita
3. Per la squadra casa:
   - Inserisci 11 giocatori con ruoli (P, D, C, A)
   - Clicca "✅ Salva Formazione"
4. Ripeti per la squadra trasferta

### Passo 4: Inserisci i Voti

**Opzione A - Import da Excel (Consigliato)**:
1. Vai in "📊 Import da Excel"
2. Scarica il template se necessario
3. Compila il file Excel con i voti
4. Carica il file
5. Seleziona la partita e applica i voti

**Opzione B - Manuale**:
1. Vai in "📝 Inserimento Voti"
2. Per ogni giocatore inserisci voto base e bonus/malus
3. Salva i voti

### Passo 5: Calcola il Risultato
1. Vai in "🧮 Calcolo Risultati"
2. Seleziona giornata e partita
3. Clicca "🧮 Calcola Risultato"
4. Visualizza il risultato dettagliato!

---

## 📊 Esempio File Excel

Il tuo file Excel deve avere queste colonne:

| Ruolo | Nome | Voto | Gf | Gs | Rp | Rf | Rs | Au | Amm | Esp | Ass |
|-------|------|------|----|----|----|----|----|----|-----|-----|-----|
| P | Maignan | 6.5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| D | Calabria | 6.0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| C | Reijnders | 7.0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| A | Giroud | 7.5 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**Note**:
- Se un giocatore ha "6*" come voto, viene interpretato come 6.0 con nota SV
- I bonus/malus vengono calcolati automaticamente dagli eventi
- Giocatori non trovati ricevono voto 6.0, bonus 0, nota SV

---

## 🎮 Comandi Utili

### Avvio
```bash
streamlit run app.py
```

### Test
```bash
python test_calc.py
```

### Porta personalizzata
```bash
streamlit run app.py --server.port 8080
```

### Modalità development
```bash
streamlit run app.py --server.runOnSave true
```

---

## 🐛 Troubleshooting

### L'app non si avvia
- Verifica di avere Python 3.8+ installato: `python --version`
- Reinstalla dipendenze: `pip install -r requirements.txt --upgrade`

### Porta già in uso
- Cambia porta: `streamlit run app.py --server.port 8080`

### Database non si crea
- Verifica i permessi della directory
- Il file `fantacalcio.db` verrà creato automaticamente

### Import Excel fallisce
- Controlla che il file abbia le colonne richieste
- Usa il template fornito come base
- Verifica che i nomi delle colonne siano corretti

---

## 📚 Documentazione Completa

- **README.md**: Guida completa utilizzo
- **TECHNICAL_DOCS.md**: Documentazione tecnica
- **DEPLOYMENT.md**: Guide deployment
- **CHANGELOG.md**: Storico modifiche

---

## 🆘 Supporto

Per problemi o domande:
1. Leggi la documentazione completa nel README.md
2. Controlla TECHNICAL_DOCS.md per dettagli tecnici
3. Esegui i test: `python test_calc.py`

---

**Buon divertimento con il Fantacalcio! ⚽🎉**
