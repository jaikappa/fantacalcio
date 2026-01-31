# 📚 Documentazione Tecnica

## Architettura del Progetto

### Stack Tecnologico

```
Frontend: Streamlit (UI interattiva)
Backend: Python 3.8+
Database: SQLite (SQLAlchemy ORM)
Import: pandas + openpyxl
```

### Struttura Modulare

```
fantacalcio/
│
├── app.py              # UI Streamlit (Controller + View)
├── calc.py             # Motore di calcolo (Business Logic)
├── db.py               # Database Manager (Data Access Layer)
├── excel_import.py     # Import Excel (Data Processing)
├── requirements.txt    # Dipendenze
└── test_calc.py        # Test unitari
```

## Moduli Principali

### 1. db.py - Database Manager

**Responsabilità**: Gestione persistenza dati con SQLAlchemy ORM

**Modelli**:

```python
Giornata
├── id: int (PK)
├── numero: int (unique)
├── descrizione: str
├── data_creazione: datetime
└── partite: relationship -> Partita[]

Partita
├── id: int (PK)
├── giornata_id: int (FK)
├── squadra_casa: str
├── squadra_trasferta: str
└── formazioni: relationship -> Formazione[]

Formazione
├── id: int (PK)
├── partita_id: int (FK)
├── squadra: str ('casa' | 'trasferta')
├── giocatore: str
├── ruolo: str ('P' | 'D' | 'C' | 'A')
├── posizione: int (1-11)
└── voto: relationship -> Voto

Voto
├── id: int (PK)
├── formazione_id: int (FK)
├── voto_base: float
├── bonus_malus_totale: float
├── gol_fatti, gol_subiti, etc.: int
├── is_manual_override: bool
└── note: str
```

**API Principale**:

```python
db = DatabaseManager('fantacalcio.db')

# CRUD Giornate
db.create_giornata(numero, descrizione)
db.get_all_giornate()
db.get_giornata(id)
db.delete_giornata(id)

# CRUD Partite
db.create_partita(giornata_id, casa, trasferta)
db.get_partite_giornata(giornata_id)
db.get_partita(id)
db.delete_partita(id)

# Formazioni
db.add_formazione(partita_id, squadra, giocatore, ruolo, pos)
db.get_formazione_partita(partita_id, squadra)
db.clear_formazione(partita_id, squadra)

# Voti
db.update_voto(formazione_id, **kwargs)
```

### 2. calc.py - Motore di Calcolo

**Responsabilità**: Implementazione pura del regolamento

**Funzioni Pure** (no side effects, testabili):

```python
# A) Voto giocatore
calcola_voto_totale(voto_base, bonus_malus) -> float

# B) Bonus/Malus da eventi
calcola_bonus_malus_da_eventi(
    gol_fatti, gol_subiti, rigori_parati, 
    rigori_fatti, rigori_sbagliati, autogol,
    ammonizioni, espulsioni, assist, ruolo
) -> float

# C) Voto squadra
calcola_voto_totale_squadra(voti_giocatori) -> float

# D) Modificatore difesa
calcola_modificatore_difesa(
    voti_base_difensori, numero_difensori
) -> float

# E) Modificatore centrocampo
calcola_modificatore_centrocampo(
    voti_casa, voti_trasferta
) -> (float, float)

# F) Modificatore attacco
calcola_modificatore_attacco(attaccanti) -> float

# H) Conversione gol
calcola_gol_da_punteggio(punteggio) -> int

# Calcolo completo
calcola_risultato_partita(
    formazione_casa, formazione_trasferta
) -> dict
```

**Output calcola_risultato_partita**:

```python
{
    'casa': {
        'voto_squadra': float,
        'modificatore_difesa_generato': float,
        'modificatore_difesa_subito': float,
        'modificatore_centrocampo': float,
        'modificatore_attacco': float,
        'vantaggio_casa': float,
        'punteggio_totale': float,
        'gol': int,
        'num_difensori': int,
        'num_centrocampisti': int,
        'num_attaccanti': int
    },
    'trasferta': { ... },
    'risultato_finale': "3 - 1"
}
```

### 3. excel_import.py - Import Excel

**Responsabilità**: Parsing e validazione file Excel

**Funzioni Principali**:

```python
# Parsing voto (gestisce "6*" -> 6.0 + nota "SV")
parse_voto_excel(voto_str) -> (float, str)

# Lettura file
leggi_excel_voti(filepath) -> DataFrame

# Calcolo bonus/malus da riga Excel
calcola_bonus_malus_excel(row) -> float

# Applicazione voti a formazione
applica_voti_excel_a_formazione(
    df_excel, formazione, use_fallback
) -> formazione_aggiornata

# Import completo
importa_voti_excel(filepath) -> {
    'df': DataFrame,
    'summary': dict,
    'success': bool,
    'message': str
}

# Export template
esporta_template_excel(filepath)
```

**Fallback Automatico**:
Se giocatore non trovato in Excel:
- `voto_base = 6.0`
- `bonus_malus = 0.0`
- `nota = "SV"`

### 4. app.py - Interfaccia Streamlit

**Responsabilità**: UI e routing

**Pagine**:

```python
render_home()          # Dashboard
render_giornate()      # CRUD giornate
render_partite()       # CRUD partite
render_formazioni()    # Input formazioni
render_voti()          # Input voti manuali
render_excel()         # Import Excel
render_calcolo()       # Visualizzazione risultati
```

**Architettura UI**:

```
Sidebar (Menu)
    ├── Home
    ├── Gestione Giornate
    ├── Gestione Partite
    ├── Inserimento Formazioni
    ├── Inserimento Voti
    ├── Import Excel
    └── Calcolo Risultati

Main Area (Contenuto pagina corrente)
    └── Tabs/Forms/Tables dinamici
```

**Session State**:

```python
st.session_state.page = 'home'
st.session_state.selected_giornata = None
st.session_state.selected_partita = None
```

## Flusso di Lavoro Completo

```
1. SETUP
   └── Utente crea Giornata
       └── db.create_giornata()
       
2. PARTITA
   └── Utente crea Partita
       └── db.create_partita()
       
3. FORMAZIONI
   └── Utente inserisce 11 titolari per squadra
       ├── db.add_formazione() x 11 (casa)
       └── db.add_formazione() x 11 (trasferta)
       
4. VOTI
   └── Opzione A: Import Excel
       ├── excel_import.importa_voti_excel()
       └── excel_import.applica_voti_excel_a_formazione()
   └── Opzione B: Inserimento Manuale
       └── db.update_voto() per ogni giocatore
       
5. CALCOLO
   └── Recupera formazioni da db
   └── calc.calcola_risultato_partita()
       ├── Calcola voti giocatori
       ├── Calcola voto squadra
       ├── Applica modificatori (difesa, centro, attacco)
       ├── Applica vantaggio casa
       └── Converte punteggio in gol
       
6. VISUALIZZAZIONE
   └── Mostra risultato dettagliato
       ├── Rosa titolare con voti
       ├── Breakdown modificatori
       └── Risultato finale in gol
```

## Algoritmi Chiave

### Modificatore Difesa

```python
1. Calcola media voti base difensori
2. Lookup in tabella:
   - <5.00: +4, 5.00-5.24: +3, ..., >=7.00: -5
3. Correzione modulo:
   - 3 difensori: +1
   - 4 difensori: 0
   - 5 difensori: -1
4. Penalità difensori extra:
   - Per ogni difensore oltre il 4°: -1
5. IMPORTANTE: Modificatore si applica all'avversario
```

### Modificatore Centrocampo

```python
1. Confronta numero centrocampisti
2. Se diverso: aggiungi voti 5.0 d'ufficio al team con meno
3. Calcola somma voti per team
4. Differenza = |somma_casa - somma_trasferta|
5. Lookup in tabella:
   - <1: 0, 1-1.99: 0.5, 2-2.99: 1.0, ..., >=8: 4.0
6. Positivo a chi ha somma maggiore, negativo all'altro
```

### Modificatore Attacco

```python
1. Per ogni attaccante:
   2. Se bonus_malus_totale == 0:
      3. Se 6.50 <= voto_base < 7.00: +0.5
      4. Se 7.00 <= voto_base < 7.50: +1.0
      5. Se voto_base >= 7.50: +1.5
5. Somma tutti i contributi
```

### Conversione Punteggio -> Gol

```python
if punteggio < 66: 0 gol
elif punteggio < 72: 1 gol
elif punteggio < 77: 2 gol
elif punteggio < 81: 3 gol
elif punteggio < 85: 4 gol
else: 4 + floor((punteggio - 85) / 4) gol
```

## Pattern di Progettazione

### 1. Repository Pattern
`DatabaseManager` astrae l'accesso ai dati, isolando la logica di persistenza.

### 2. Pure Functions
Tutte le funzioni in `calc.py` sono pure: nessun side effect, output deterministico per stesso input.

### 3. Dependency Injection
`app.py` usa il DatabaseManager attraverso un singleton cached.

### 4. Separation of Concerns
- **UI**: `app.py` (Streamlit)
- **Logic**: `calc.py` (funzioni pure)
- **Data**: `db.py` (SQLAlchemy)
- **I/O**: `excel_import.py` (pandas)

## Testing

### Test Unitari

```bash
python test_calc.py
```

**Coverage**:
- ✅ Bonus/Malus da eventi
- ✅ Modificatori (difesa, centro, attacco)
- ✅ Conversione punteggio -> gol
- ✅ Calcolo partita completa

### Test Manuali UI

1. Crea giornata
2. Crea partita
3. Inserisci formazioni
4. Importa Excel
5. Verifica calcoli
6. Verifica persistenza

## Performance

### Ottimizzazioni

1. **Database**:
   - Indici su chiavi esterne
   - Lazy loading relationships
   - Cascade delete configurato

2. **Caching**:
   - `@st.cache_resource` per DatabaseManager
   - Session state per navigazione

3. **Queries**:
   - Eager loading quando necessario
   - Batch operations per formazioni

### Scalabilità

**Limiti SQLite**:
- ~1000 concorrenti max
- Lock su scritture

**Soluzione produzione**:
- Migrare a PostgreSQL
- Connection pooling
- Redis per caching

## Sicurezza

### Best Practices Implementate

1. **SQL Injection**: Prevenuto da SQLAlchemy ORM
2. **Input Validation**: Validazione ruoli, voti, numeri
3. **Type Safety**: Type hints in tutto il codice

### Considerazioni Produzione

- [ ] Autenticazione utenti
- [ ] HTTPS/SSL
- [ ] Rate limiting
- [ ] Sanitizzazione input file
- [ ] Backup automatici database

## Estensioni Future

### Feature da Aggiungere

1. **Multi-utente**:
   - Sistema di login
   - Leghe private
   - Permessi

2. **Analytics**:
   - Statistiche giocatori
   - Trend performance
   - Grafici interattivi

3. **Export**:
   - PDF report
   - Excel risultati
   - Condivisione social

4. **Notifiche**:
   - Email risultati
   - Push notifications
   - Reminder inserimento voti

5. **Mobile**:
   - App nativa
   - PWA
   - Responsive design migliorato

## Troubleshooting

### Errori Comuni

**1. Database locked**
```python
# Soluzione: usa autoflush
session = Session(autoflush=True)
```

**2. Import Excel fallisce**
```python
# Verifica encoding
df = pd.read_excel(file, encoding='utf-8')
```

**3. Voti non aggiornati**
```python
# Usa st.rerun() dopo update
db.update_voto(...)
st.rerun()
```

## Glossario Tecnico

- **ORM**: Object-Relational Mapping (SQLAlchemy)
- **CRUD**: Create, Read, Update, Delete
- **Pure Function**: Funzione senza side effects
- **Session State**: Stato persistente tra reruns Streamlit
- **Cascade**: Operazioni propagate su relazioni
- **Lazy Loading**: Caricamento dati on-demand

---

**Autore**: Sistema Fantacalcio Manager  
**Versione**: 1.0  
**Data**: 2025
