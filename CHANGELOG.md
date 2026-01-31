# 📝 Changelog

Tutte le modifiche importanti a questo progetto saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce al [Semantic Versioning](https://semver.org/).

## [1.1.0] - 2025-01-31

### ✨ Aggiunto

#### UX Improvements
- **Feedback migliorato**: Messaggi di successo più evidenti con popup temporaneo
- **Reset automatico campi**: Form si svuotano automaticamente dopo la creazione
- **Import formazione via copia/incolla**: Supporto per incollare formazioni da siti web
  - Supporta multipli formati: "P Nome", "Nome (P)", "Portiere: Nome"
  - **NEW fantageneration**: Riconoscimento automatico formato compatto `(P) Sommer(D) Bastoni...`
  - Deduzione automatica ruoli se non specificati
  - Anteprima prima del salvataggio
  - Filtro automatico header e statistiche
- **Import Excel più tollerante**: Riconosce variazioni nei nomi delle colonne
  - Supporta "Ruolo", "R", "Role", "Pos", "Posizione"
  - Supporta "Nome", "Name", "Giocatore", "Player"
  - Messaggi di errore più dettagliati con colonne disponibili

### 🔧 Migliorato

#### Gestione Giornate
- Form con `clear_on_submit=True` per reset automatico
- Auto-incremento numero giornata suggerito
- Delay di 1.5s per visualizzare il messaggio di successo

#### Gestione Partite
- Form con reset automatico dopo creazione
- Messaggio di conferma più chiaro
- Delay visivo per feedback

#### Inserimento Formazioni
- Doppio metodo: Manuale o Copia/Incolla
- Radio button per scegliere il metodo
- Parser intelligente per testo incollato
- Supporto formati multipli:
  - `P Maignan` (ruolo + nome)
  - `Maignan (P)` (nome + ruolo)
  - `Portiere: Maignan` (ruolo esteso)
  - Deduzione automatica posizioni

#### Import Excel
- Normalizzazione colonne migliorata
- Rimozione caratteri speciali
- Mapping flessibile nomi colonne
- Errori più descrittivi con lista colonne trovate

### 🐛 Risolto

- **Excel Import Error**: "Colonna obbligatoria 'ruolo' non trovata"
  - Causa: Nome colonna con maiuscole o caratteri speciali
  - Soluzione: Normalizzazione e mapping flessibile
- **Inserimenti multipli**: Possibilità di creare duplicati per errore
  - Soluzione: Reset automatico campi dopo submit
- **Mancanza feedback**: Utente non sicuro se azione completata
  - Soluzione: Messaggi success con delay visivo

### 📊 Statistiche v1.1.0

- **Nuove funzioni**: 1 (parse_formazione_da_testo)
- **Funzioni modificate**: 4 (render_giornate, render_partite, render_formazione_squadra, leggi_excel_voti)
- **Bug risolti**: 3
- **Miglioramenti UX**: 5

---

## [1.0.0] - 2025-01-31

### ✨ Aggiunto

#### Core Features
- Sistema completo di gestione giornate di campionato
- Gestione partite con squadra casa e trasferta
- Inserimento formazioni (11 titolari) con ruoli P, D, C, A
- Inserimento voti manuali con voto base e bonus/malus
- Import automatico da file Excel con calcolo bonus/malus
- Motore di calcolo completo secondo regolamento specificato
- Visualizzazione risultati dettagliati con breakdown modificatori

#### Database
- Database SQLite con SQLAlchemy ORM
- Modelli: Giornata, Partita, Formazione, Voto
- Persistenza completa di tutti i dati
- Relazioni e cascade delete configurati
- Sistema di override manuali voti

#### Import Excel
- Supporto colonne: Ruolo, Nome, Voto, Gf, Gs, Rp, Rf, Rs, Au, Amm, Esp, Ass
- Parsing automatico voto con supporto per asterisco (es. "6*" -> SV)
- Calcolo automatico bonus/malus da eventi
- Fallback automatico per giocatori non trovati (6.0, bonus 0, SV)
- Template Excel scaricabile

#### Calcolo Risultati
- Implementazione regolamento A: Voto totale giocatore
- Implementazione regolamento B: Bonus/malus da eventi
- Implementazione regolamento C: Voto totale squadra
- Implementazione regolamento D: Modificatore difesa
- Implementazione regolamento E: Modificatore centrocampo
- Implementazione regolamento F: Modificatore attacco
- Implementazione regolamento G: Vantaggio casa (+2)
- Implementazione regolamento H: Conversione punteggio in gol

#### UI Streamlit
- Navigazione a menu laterale
- Dashboard con panoramica
- Form interattivi per tutte le operazioni CRUD
- Tab per gestione squadra casa/trasferta
- Tabelle dinamiche con pandas
- Visualizzazione risultati dettagliata
- Metrics e indicatori visivi

#### Testing
- Suite di test completa per motore di calcolo
- Test bonus/malus da eventi
- Test modificatori (difesa, centro, attacco)
- Test conversione punteggio -> gol
- Test partita completa end-to-end

#### Documentazione
- README.md completo con guida utilizzo
- TECHNICAL_DOCS.md con documentazione tecnica
- DEPLOYMENT.md con guide deployment per varie piattaforme
- CHANGELOG.md (questo file)
- Commenti estensivi in tutto il codice
- Type hints per tutte le funzioni

#### Utilità
- Script di avvio rapido (start.sh)
- .gitignore configurato
- requirements.txt con tutte le dipendenze
- File Excel di esempio con voti realistici

### 🏗️ Architettura

- Separazione concerns: UI, Logic, Data, I/O
- Funzioni pure e testabili nel motore di calcolo
- Repository pattern per accesso dati
- Type safety con Python type hints
- Modularità e riusabilità codice

### 🎨 Design Choices

- Streamlit per UI rapida e interattiva
- SQLite per semplicità deployment
- pandas/openpyxl per Excel (standard de facto)
- SQLAlchemy ORM per astrazione database
- Funzioni pure per logic testabile

### 📊 Statistiche Progetto

- **Linee di codice**: ~2000+
- **File Python**: 5 moduli principali
- **Test**: 15+ test unitari
- **Documentazione**: 4 file markdown estesi
- **Dipendenze**: 4 package Python

### 🔐 Sicurezza

- Input validation su tutti i form
- SQL injection prevention via ORM
- Type checking estensivo
- Error handling robusto

### ⚡ Performance

- Database indexing su FK
- Caching di DatabaseManager
- Session state per UI reattiva
- Lazy loading relazioni ORM

### 🌐 Compatibilità

- Python 3.8+
- Streamlit 1.31+
- SQLAlchemy 2.0+
- pandas 2.2+
- Multi-piattaforma (Windows, macOS, Linux)

---

## [Unreleased]

### 🚀 Planned Features

- [ ] Sistema autenticazione multi-utente
- [ ] Export risultati in PDF
- [ ] Grafici e statistiche avanzate
- [ ] API REST per integrazione esterna
- [ ] Mobile app nativa
- [ ] Sistema notifiche email
- [ ] Backup automatico database
- [ ] Modalità dark/light theme
- [ ] Supporto campionati multipli
- [ ] Integrazione con API dati ufficiali

### 🐛 Known Issues

Nessun bug critico noto al momento.

### 💡 Ideas for Future

- Dashboard analytics con trend performance
- Sistema di raccomandazioni formazioni
- Social features (condivisione risultati)
- Integrazione Telegram bot
- Modalità offline PWA

---

**Formato Versioning**: MAJOR.MINOR.PATCH

- **MAJOR**: Breaking changes
- **MINOR**: Nuove features backward-compatible
- **PATCH**: Bug fixes

**Data ultimo aggiornamento**: 31 Gennaio 2025
