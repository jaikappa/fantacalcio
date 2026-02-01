"""
Applicazione Streamlit per il Fantacalcio.
Interfaccia web completa per gestire giornate, partite, formazioni e calcoli.
"""

import streamlit as st
import pandas as pd
import time
import re
from db import DatabaseManager, Formazione, Voto
from calc import calcola_risultato_partita, calcola_bonus_malus_da_eventi
from excel_import import importa_voti_excel, applica_voti_excel_a_formazione, esporta_template_excel
import os

# Configurazione pagina
st.set_page_config(
    page_title="Fantacalcio Manager",
    page_icon="⚽",
    layout="wide"
)

# Inizializza il database
@st.cache_resource
def get_db():
    return DatabaseManager('fantacalcio.db')

db = get_db()

# Inizializza session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_giornata' not in st.session_state:
    st.session_state.selected_giornata = None
if 'selected_partita' not in st.session_state:
    st.session_state.selected_partita = None

# ===== FUNZIONI DI UTILITÀ =====

def render_menu():
    """Renderizza il menu principale"""
    st.sidebar.title("⚽ Fantacalcio Manager")
    
    menu_options = {
        'home': '🏠 Home',
        'giornate': '📅 Gestione Giornate',
        'partite': '⚽ Gestione Partite',
        'formazioni': '👥 Inserimento Formazioni',
        'voti': '📝 Inserimento Voti',
        'excel': '📊 Import da Excel',
        'calcolo': '🧮 Calcolo Risultati',
        'backup': '💾 Backup/Restore'
    }
    
    for key, label in menu_options.items():
        if st.sidebar.button(label, key=f"menu_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()
    
    st.sidebar.divider()
    st.sidebar.info("Webapp Fantacalcio v1.2")


def render_home():
    """Pagina home con panoramica"""
    st.title("🏠 Fantacalcio Manager")
    st.write("Benvenuto nel sistema di gestione del Fantacalcio!")
    
    st.header("📊 Panoramica")
    
    giornate = db.get_all_giornate()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Giornate create", len(giornate))
    
    with col2:
        totale_partite = sum(len(g.partite) for g in giornate)
        st.metric("Partite totali", totale_partite)
    
    with col3:
        st.metric("Database", "✅ Connesso")
    
    st.divider()
    
    st.subheader("🚀 Per iniziare:")
    st.write("1. Crea una nuova giornata dalla sezione 'Gestione Giornate'")
    st.write("2. Aggiungi una partita alla giornata")
    st.write("3. Inserisci le formazioni delle due squadre")
    st.write("4. Importa i voti da Excel o inseriscili manualmente")
    st.write("5. Calcola il risultato della partita")
    
    if giornate:
        st.divider()
        st.subheader("📅 Ultime giornate")
        
        for g in giornate[-5:]:
            with st.expander(f"Giornata {g.numero}: {g.descrizione}"):
                st.write(f"Partite: {len(g.partite)}")
                for p in g.partite:
                    st.write(f"• {p.squadra_casa} vs {p.squadra_trasferta}")


def render_giornate():
    """Pagina gestione giornate"""
    st.title("📅 Gestione Giornate")
    
    tab1, tab2 = st.tabs(["Crea Nuova Giornata", "Giornate Esistenti"])
    
    with tab1:
        st.subheader("Crea una nuova giornata")
        
        # Usa session state per gestire i valori dei form
        if 'giornata_numero' not in st.session_state:
            st.session_state.giornata_numero = 1
        if 'giornata_descrizione' not in st.session_state:
            st.session_state.giornata_descrizione = ""
        
        col1, col2 = st.columns(2)
        
        with col1:
            numero = st.number_input(
                "Numero giornata", 
                min_value=1, 
                step=1, 
                value=st.session_state.giornata_numero,
                key="input_numero_giornata"
            )
        
        with col2:
            descrizione = st.text_input(
                "Descrizione (opzionale)", 
                placeholder="Es: Giornata di andata",
                value=st.session_state.giornata_descrizione,
                key="input_descrizione_giornata"
            )
        
        if st.button("✅ Crea Giornata", type="primary"):
            try:
                giornata = db.create_giornata(numero, descrizione)
                
                # Mostra messaggio di successo
                st.success(f"✅ Giornata {numero} creata con successo!")
                
                # Reset dei campi
                st.session_state.giornata_numero = numero + 1  # Incrementa automaticamente
                st.session_state.giornata_descrizione = ""
                
                # Piccolo delay per far vedere il messaggio
                time.sleep(1)
                
                st.rerun()
            except Exception as e:
                st.error(f"❌ Errore: {str(e)}")
    
    with tab2:
        st.subheader("Giornate esistenti")
        
        giornate = db.get_all_giornate()
        
        if not giornate:
            st.info("Nessuna giornata creata. Crea la prima giornata dalla tab precedente.")
        else:
            for giornata in giornate:
                with st.expander(f"🗓️ Giornata {giornata.numero}: {giornata.descrizione}"):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.write(f"**Partite:** {len(giornata.partite)}")
                    
                    with col2:
                        st.write(f"**Creata il:** {giornata.data_creazione.strftime('%d/%m/%Y')}")
                    
                    with col3:
                        if st.button("🗑️ Elimina", key=f"del_giornata_{giornata.id}"):
                            if db.delete_giornata(giornata.id):
                                st.success("Giornata eliminata!")
                                st.rerun()
                    
                    if giornata.partite:
                        st.write("**Partite:**")
                        for p in giornata.partite:
                            st.write(f"• {p.squadra_casa} vs {p.squadra_trasferta}")


def render_partite():
    """Pagina gestione partite"""
    st.title("⚽ Gestione Partite")
    
    giornate = db.get_all_giornate()
    
    if not giornate:
        st.warning("⚠️ Nessuna giornata disponibile. Crea prima una giornata.")
        return
    
    tab1, tab2 = st.tabs(["Crea Nuova Partita", "Partite Esistenti"])
    
    with tab1:
        st.subheader("Crea una nuova partita")
        
        # Seleziona giornata
        giornata_options = {g.id: f"Giornata {g.numero}: {g.descrizione}" for g in giornate}
        selected_giornata_id = st.selectbox(
            "Seleziona giornata",
            options=list(giornata_options.keys()),
            format_func=lambda x: giornata_options[x],
            key="select_giornata_partita"
        )
        
        # Usa form per reset automatico
        with st.form("form_nuova_partita", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                squadra_casa = st.text_input("Squadra di Casa", placeholder="Es: Team A")
            
            with col2:
                squadra_trasferta = st.text_input("Squadra in Trasferta", placeholder="Es: Team B")
            
            submitted = st.form_submit_button("✅ Crea Partita", type="primary", use_container_width=True)
            
            if submitted:
                if not squadra_casa or not squadra_trasferta:
                    st.error("❌ Inserisci entrambe le squadre")
                elif squadra_casa.strip().lower() == squadra_trasferta.strip().lower():
                    st.error("❌ Le squadre devono essere diverse")
                else:
                    try:
                        partita = db.create_partita(selected_giornata_id, squadra_casa, squadra_trasferta)
                        st.success(f"✅ Partita creata: {squadra_casa} vs {squadra_trasferta}! I campi sono stati resettati.")
                        time.sleep(1.5)
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Errore: {str(e)}")
    
    with tab2:
        st.subheader("Partite esistenti")
        
        for giornata in giornate:
            if giornata.partite:
                st.write(f"### Giornata {giornata.numero}")
                
                for partita in giornata.partite:
                    with st.expander(f"⚽ {partita.squadra_casa} vs {partita.squadra_trasferta}"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            # Mostra formazioni se presenti
                            form_casa = db.get_formazione_partita(partita.id, 'casa')
                            form_trasferta = db.get_formazione_partita(partita.id, 'trasferta')
                            
                            st.write(f"**{partita.squadra_casa} (Casa):** {len(form_casa)} giocatori")
                            st.write(f"**{partita.squadra_trasferta} (Trasferta):** {len(form_trasferta)} giocatori")
                        
                        with col2:
                            if st.button("🗑️ Elimina", key=f"del_partita_{partita.id}"):
                                if db.delete_partita(partita.id):
                                    st.success("Partita eliminata!")
                                    st.rerun()


def render_formazioni():
    """Pagina inserimento formazioni"""
    st.title("👥 Inserimento Formazioni")
    
    giornate = db.get_all_giornate()
    
    if not giornate:
        st.warning("⚠️ Nessuna giornata disponibile.")
        return
    
    # Seleziona giornata
    giornata_options = {g.id: f"Giornata {g.numero}: {g.descrizione}" for g in giornate}
    selected_giornata_id = st.selectbox(
        "Seleziona giornata",
        options=list(giornata_options.keys()),
        format_func=lambda x: giornata_options[x],
        key="form_giornata"
    )
    
    partite = db.get_partite_giornata(selected_giornata_id)
    
    if not partite:
        st.info("Nessuna partita in questa giornata. Crea prima una partita.")
        return
    
    # Seleziona partita
    partita_options = {p.id: f"{p.squadra_casa} vs {p.squadra_trasferta}" for p in partite}
    selected_partita_id = st.selectbox(
        "Seleziona partita",
        options=list(partita_options.keys()),
        format_func=lambda x: partita_options[x],
        key="form_partita"
    )
    
    partita = db.get_partita(selected_partita_id)
    
    st.divider()
    
    # Tab per le due squadre
    tab_casa, tab_trasferta = st.tabs([f"🏠 {partita.squadra_casa}", f"✈️ {partita.squadra_trasferta}"])
    
    with tab_casa:
        render_formazione_squadra(partita, 'casa', partita.squadra_casa)
    
    with tab_trasferta:
        render_formazione_squadra(partita, 'trasferta', partita.squadra_trasferta)


def render_formazione_squadra(partita, tipo_squadra, nome_squadra):
    """Renderizza il form per inserire la formazione di una squadra"""
    st.subheader(f"Formazione {nome_squadra}")
    
    # Mostra formazione esistente
    formazione_esistente = db.get_formazione_partita(partita.id, tipo_squadra)
    
    if formazione_esistente:
        st.write("**Formazione attuale:**")
        
        df_form = pd.DataFrame([
            {
                'Pos': f.posizione,
                'Ruolo': f.ruolo,
                'Giocatore': f.giocatore
            }
            for f in formazione_esistente
        ])
        
        st.dataframe(df_form, use_container_width=True, hide_index=True)
        
        if st.button(f"🗑️ Cancella formazione {nome_squadra}", key=f"clear_{tipo_squadra}"):
            db.clear_formazione(partita.id, tipo_squadra)
            st.success("Formazione cancellata!")
            st.rerun()
        
        st.divider()
    
    # Metodo di inserimento
    metodo = st.radio(
        "Metodo di inserimento",
        ["📝 Inserimento Manuale", "📋 Copia/Incolla"],
        key=f"metodo_{tipo_squadra}",
        horizontal=True
    )
    
    if metodo == "📋 Copia/Incolla":
        st.write("**Incolla la formazione:**")
        st.info("""
        **Formati supportati:**
        - `P Nome Cognome` (un giocatore per riga)
        - `Portiere: Nome Cognome` 
        - `Nome Cognome (P)`
        - **NEW fantageneration**: `(P) Sommer(D) Bastoni(C) Pulisic...` (tutto attaccato)
        - Solo nomi separati da virgola o a capo (rileverà automaticamente i ruoli)
        
        **Esempio NEW fantageneration:**
        ```
        (P) Sommer(D) Bastoni(D) Cambiaso(D) Coco(C) Pulisic(A) David
        ```
        
        **Esempio standard:**
        ```
        P Maignan
        D Calabria
        D Tomori
        C Bennacer
        A Giroud
        ```
        """)
        
        testo_formazione = st.text_area(
            "Incolla qui la formazione (11 giocatori)",
            height=300,
            placeholder="Incolla qui la lista dei giocatori...",
            key=f"paste_{tipo_squadra}"
        )
        
        # Session state per gestire il workflow
        preview_key = f"preview_{tipo_squadra}_{partita.id}"
        if preview_key not in st.session_state:
            st.session_state[preview_key] = None
        
        if st.button("🔄 Elabora e Inserisci", type="primary", key=f"parse_{tipo_squadra}"):
            giocatori_parsed = parse_formazione_da_testo(testo_formazione)
            
            if giocatori_parsed is None:
                st.error("❌ Formato non riconosciuto. Usa uno dei formati supportati.")
                st.session_state[preview_key] = None
            elif len(giocatori_parsed) != 11:
                st.error(f"❌ Trovati {len(giocatori_parsed)} giocatori, servono esattamente 11.")
                st.session_state[preview_key] = None
            else:
                # Salva in session state
                st.session_state[preview_key] = giocatori_parsed
                st.rerun()
        
        # Mostra anteprima se presente
        if st.session_state[preview_key] is not None:
            st.write("**Anteprima formazione rilevata:**")
            df_preview = pd.DataFrame(st.session_state[preview_key])
            st.dataframe(df_preview, use_container_width=True, hide_index=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ Conferma e Salva", type="primary", key=f"confirm_{tipo_squadra}", use_container_width=True):
                    # Cancella formazione esistente
                    db.clear_formazione(partita.id, tipo_squadra)
                    
                    # Inserisci nuova formazione
                    for i, g in enumerate(st.session_state[preview_key], 1):
                        db.add_formazione(
                            partita.id,
                            tipo_squadra,
                            g['nome'],
                            g['ruolo'],
                            i
                        )
                    
                    st.success(f"✅ Formazione {nome_squadra} salvata!")
                    # Pulisci session state
                    st.session_state[preview_key] = None
                    time.sleep(1)
                    st.rerun()
            
            with col2:
                if st.button("❌ Annulla", key=f"cancel_{tipo_squadra}", use_container_width=True):
                    st.session_state[preview_key] = None
                    st.rerun()
    
    else:  # Inserimento manuale
        st.write("**Inserisci formazione manualmente (11 titolari):**")
        
        ruoli = ['P', 'D', 'C', 'A']
        
        with st.form(f"form_{tipo_squadra}"):
            giocatori = []
            
            for i in range(11):
                col1, col2, col3 = st.columns([1, 2, 3])
                
                with col1:
                    st.write(f"**{i+1}**")
                
                with col2:
                    ruolo = st.selectbox(
                        f"Ruolo {i+1}",
                        options=ruoli,
                        key=f"ruolo_{tipo_squadra}_{i}",
                        label_visibility="collapsed"
                    )
                
                with col3:
                    nome = st.text_input(
                        f"Nome {i+1}",
                        placeholder=f"Nome giocatore {i+1}",
                        key=f"nome_{tipo_squadra}_{i}",
                        label_visibility="collapsed"
                    )
                
                giocatori.append({'ruolo': ruolo, 'nome': nome, 'posizione': i+1})
            
            submitted = st.form_submit_button("✅ Salva Formazione", type="primary")
            
            if submitted:
                # Verifica che tutti i nomi siano inseriti
                nomi_validi = [g for g in giocatori if g['nome'].strip()]
                
                if len(nomi_validi) != 11:
                    st.error("❌ Inserisci tutti gli 11 giocatori")
                else:
                    # Cancella formazione esistente
                    db.clear_formazione(partita.id, tipo_squadra)
                    
                    # Inserisci nuova formazione
                    for g in giocatori:
                        db.add_formazione(
                            partita.id,
                            tipo_squadra,
                            g['nome'].strip(),
                            g['ruolo'],
                            g['posizione']
                        )
                    
                    st.success(f"✅ Formazione {nome_squadra} salvata!")
                    time.sleep(1)
                    st.rerun()


def parse_formazione_da_testo(testo):
    """
    Parsa una formazione da testo incollato.
    Supporta vari formati incluso NEW fantageneration.
    
    Returns:
        List[dict] con 'ruolo' e 'nome', oppure None se parsing fallisce
    """
    if not testo or not testo.strip():
        return None
    
    # FORMATO NEW FANTAGENERATION
    # Cerca pattern: (P) Nome, (D) Nome, (C) Nome, (A) Nome
    # Esempio: "(P) Sommer(D) Bastoni(D) Cambiaso..."
    pattern_fantageneration = r'\(([PDCA])\)\s*([^(]+?)(?=\([PDCA]\)|$)'
    matches = re.findall(pattern_fantageneration, testo, re.IGNORECASE)
    
    if matches and len(matches) >= 11:
        giocatori = []
        for ruolo, nome in matches[:11]:  # Prendi solo i primi 11
            nome_pulito = nome.strip()
            # Rimuovi eventuali numeri/statistiche alla fine
            nome_pulito = re.sub(r'\d+\.?\d*\s*$', '', nome_pulito).strip()
            if nome_pulito:
                giocatori.append({
                    'ruolo': ruolo.upper(),
                    'nome': nome_pulito
                })
        
        if len(giocatori) == 11:
            return giocatori
    
    # FORMATO STANDARD: linee separate
    linee = [l.strip() for l in testo.strip().split('\n') if l.strip()]
    
    # Filtra linee che sono header/info (contengono "giornata", "modulo", "gol", ecc.)
    linee_filtrate = []
    for linea in linee:
        linea_lower = linea.lower()
        # Skippa header e info match
        if any(keyword in linea_lower for keyword in 
               ['giornata', 'modulo', 'gol -', 'bundesliga', 'serie a', 
                'giocatore', 'voto', 'team', ' : ', 'formazione']):
            continue
        linee_filtrate.append(linea)
    
    giocatori = []
    
    for linea in linee_filtrate:
        # Formato: "P Nome Cognome" o "P: Nome Cognome"
        match = re.match(r'^([PDCA])[:\s]+(.+)$', linea, re.IGNORECASE)
        if match:
            ruolo = match.group(1).upper()
            nome = match.group(2).strip()
            giocatori.append({'ruolo': ruolo, 'nome': nome})
            continue
        
        # Formato: "Nome Cognome (P)" o "Nome Cognome - P"
        match = re.match(r'^(.+?)[\s\-]+\(?([PDCA])\)?$', linea, re.IGNORECASE)
        if match:
            nome = match.group(1).strip()
            ruolo = match.group(2).upper()
            giocatori.append({'ruolo': ruolo, 'nome': nome})
            continue
        
        # Formato: "Portiere: Nome Cognome"
        ruoli_map = {
            'portiere': 'P', 'por': 'P',
            'difensore': 'D', 'dif': 'D',
            'centrocampista': 'C', 'centro': 'C', 'cen': 'C',
            'attaccante': 'A', 'att': 'A'
        }
        for ruolo_text, ruolo_code in ruoli_map.items():
            if linea.lower().startswith(ruolo_text):
                nome = linea[len(ruolo_text):].strip(' :').strip()
                if nome:
                    giocatori.append({'ruolo': ruolo_code, 'nome': nome})
                    break
        else:
            # Se non trova pattern, considera come nome semplice e prova a dedurre ruolo
            # Per ora lo skippiamo o lo mettiamo come centrocampista di default
            if linea and len(linea) > 2:
                # Deduzione semplice: primo giocatore = P, ultimi 2 = A, resto = D o C
                pos = len(giocatori)
                if pos == 0:
                    ruolo = 'P'
                elif pos >= 9:  # Ultimi 2
                    ruolo = 'A'
                elif pos <= 4:  # Primi difensori
                    ruolo = 'D'
                else:
                    ruolo = 'C'
                giocatori.append({'ruolo': ruolo, 'nome': linea.strip()})
    
    return giocatori if giocatori else None


def render_voti():
    """Pagina inserimento voti manuali"""
    st.title("📝 Inserimento Voti")
    
    giornate = db.get_all_giornate()
    
    if not giornate:
        st.warning("⚠️ Nessuna giornata disponibile.")
        return
    
    # Seleziona giornata
    giornata_options = {g.id: f"Giornata {g.numero}: {g.descrizione}" for g in giornate}
    selected_giornata_id = st.selectbox(
        "Seleziona giornata",
        options=list(giornata_options.keys()),
        format_func=lambda x: giornata_options[x],
        key="voti_giornata"
    )
    
    partite = db.get_partite_giornata(selected_giornata_id)
    
    if not partite:
        st.info("Nessuna partita in questa giornata.")
        return
    
    # Seleziona partita
    partita_options = {p.id: f"{p.squadra_casa} vs {p.squadra_trasferta}" for p in partite}
    selected_partita_id = st.selectbox(
        "Seleziona partita",
        options=list(partita_options.keys()),
        format_func=lambda x: partita_options[x],
        key="voti_partita"
    )
    
    partita = db.get_partita(selected_partita_id)
    
    st.divider()
    
    # Tab per le due squadre
    tab_casa, tab_trasferta = st.tabs([f"🏠 {partita.squadra_casa}", f"✈️ {partita.squadra_trasferta}"])
    
    with tab_casa:
        render_voti_squadra(partita, 'casa', partita.squadra_casa)
    
    with tab_trasferta:
        render_voti_squadra(partita, 'trasferta', partita.squadra_trasferta)


def render_voti_squadra(partita, tipo_squadra, nome_squadra):
    """Renderizza il form per inserire i voti di una squadra"""
    st.subheader(f"Voti {nome_squadra}")
    
    formazione = db.get_formazione_partita(partita.id, tipo_squadra)
    
    if not formazione:
        st.warning(f"⚠️ Nessuna formazione inserita per {nome_squadra}. Inserisci prima la formazione.")
        return
    
    for giocatore in formazione:
        with st.expander(f"{giocatore.posizione}. {giocatore.giocatore} ({giocatore.ruolo})"):
            col1, col2 = st.columns(2)
            
            voto_attuale = giocatore.voto
            
            with col1:
                voto_base = st.number_input(
                    "Voto base",
                    min_value=0.0,
                    max_value=10.0,
                    value=float(voto_attuale.voto_base) if voto_attuale else 6.0,
                    step=0.5,
                    key=f"voto_base_{giocatore.id}"
                )
            
            with col2:
                bonus_malus = st.number_input(
                    "Bonus/Malus totale",
                    min_value=-20.0,
                    max_value=20.0,
                    value=float(voto_attuale.bonus_malus_totale) if voto_attuale else 0.0,
                    step=0.5,
                    key=f"bonus_malus_{giocatore.id}"
                )
            
            note = st.text_input(
                "Note",
                value=voto_attuale.note if voto_attuale else "",
                placeholder="Es: SV",
                key=f"note_{giocatore.id}"
            )
            
            if st.button("💾 Salva voto", key=f"save_voto_{giocatore.id}"):
                db.update_voto(
                    giocatore.id,
                    voto_base=voto_base,
                    bonus_malus=bonus_malus,
                    note=note,
                    is_manual=True
                )
                st.success(f"✅ Voto salvato per {giocatore.giocatore}")
                st.rerun()
            
            # Mostra voto totale
            voto_totale = voto_base + bonus_malus
            st.metric("Voto totale", f"{voto_totale:.1f}")


def render_excel():
    """Pagina import da Excel"""
    st.title("📊 Import Voti da Excel")
    
    st.write("Carica un file Excel con i voti ufficiali per importarli automaticamente.")
    
    # Mostra formato richiesto
    with st.expander("ℹ️ Formato file Excel richiesto"):
        st.write("Il file Excel deve contenere le seguenti colonne:")
        st.code("""
Ruolo: P, D, C, A
Nome: Nome del giocatore
Voto: Voto base (può contenere asterisco per SV, es: 6*)
Gf: Gol fatti
Gs: Gol subiti
Rp: Rigori parati
Rf: Rigori fatti
Rs: Rigori sbagliati
Au: Autogol
Amm: Ammonizioni
Esp: Espulsioni
Ass: Assist
        """)
        
        st.write("**Download template:**")
        if st.button("📥 Scarica template Excel"):
            template_path = esporta_template_excel("template_voti.xlsx")
            with open(template_path, 'rb') as f:
                st.download_button(
                    "⬇️ Download template",
                    f,
                    file_name="template_voti.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    st.divider()
    
    # Upload file
    uploaded_file = st.file_uploader("Carica file Excel", type=['xlsx', 'xls'])
    
    if uploaded_file:
        # Salva il file temporaneamente
        temp_path = f"/tmp/{uploaded_file.name}"
        with open(temp_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        # Importa i voti
        result = importa_voti_excel(temp_path)
        
        if result['success']:
            st.success(f"✅ {result['message']}")
            
            # Mostra summary
            summary = result['summary']
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Totale giocatori", summary['totale_giocatori'])
            with col2:
                st.metric("Con bonus", summary['giocatori_con_bonus'])
            with col3:
                st.metric("Con malus", summary['giocatori_con_malus'])
            with col4:
                st.metric("Senza voto (SV)", summary['giocatori_sv'])
            
            # Mostra dati importati
            st.subheader("📋 Anteprima dati importati")
            df = result['df']
            
            # Seleziona colonne da mostrare
            cols_to_show = ['nome', 'ruolo', 'voto_base', 'bonus_malus_calcolato', 'voto_totale', 'nota']
            st.dataframe(df[cols_to_show], use_container_width=True, hide_index=True)
            
            st.divider()
            
            # Applica a una partita
            st.subheader("🎯 Applica voti a una partita")
            
            giornate = db.get_all_giornate()
            
            if giornate:
                giornata_options = {g.id: f"Giornata {g.numero}: {g.descrizione}" for g in giornate}
                selected_giornata_id = st.selectbox(
                    "Seleziona giornata",
                    options=list(giornata_options.keys()),
                    format_func=lambda x: giornata_options[x],
                    key="excel_giornata"
                )
                
                partite = db.get_partite_giornata(selected_giornata_id)
                
                if partite:
                    partita_options = {p.id: f"{p.squadra_casa} vs {p.squadra_trasferta}" for p in partite}
                    selected_partita_id = st.selectbox(
                        "Seleziona partita",
                        options=list(partita_options.keys()),
                        format_func=lambda x: partita_options[x],
                        key="excel_partita"
                    )
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("✅ Applica a Squadra Casa", type="primary"):
                            applica_voti_da_excel(selected_partita_id, 'casa', df)
                    
                    with col2:
                        if st.button("✅ Applica a Squadra Trasferta", type="primary"):
                            applica_voti_da_excel(selected_partita_id, 'trasferta', df)
        else:
            st.error(f"❌ {result['message']}")


def applica_voti_da_excel(partita_id, tipo_squadra, df_excel):
    """Applica i voti da Excel a una formazione"""
    partita = db.get_partita(partita_id)
    formazione = db.get_formazione_partita(partita_id, tipo_squadra)
    
    if not formazione:
        st.error("❌ Nessuna formazione trovata. Inserisci prima la formazione.")
        return
    
    # Crea dizionario nome -> dati
    voti_dict = {}
    for _, row in df_excel.iterrows():
        # Salta righe con nome vuoto o NaN
        if pd.isna(row.get('nome')) or not str(row.get('nome')).strip():
            continue
        
        nome = str(row['nome']).strip().lower()
        voti_dict[nome] = row
    
    # Applica voti
    trovati = 0
    non_trovati = []
    
    for giocatore in formazione:
        nome_giocatore = giocatore.giocatore.strip().lower()
        
        if nome_giocatore in voti_dict:
            row = voti_dict[nome_giocatore]
            
            # Calcola bonus/malus
            bonus_malus = calcola_bonus_malus_da_eventi(
                gol_fatti=int(row.get('gf', 0)),
                gol_subiti=int(row.get('gs', 0)),
                rigori_parati=int(row.get('rp', 0)),
                rigori_fatti=int(row.get('rf', 0)),
                rigori_sbagliati=int(row.get('rs', 0)),
                autogol=int(row.get('au', 0)),
                ammonizioni=int(row.get('amm', 0)),
                espulsioni=int(row.get('esp', 0)),
                assist=int(row.get('ass', 0)),
                ruolo=giocatore.ruolo
            )
            
            # Aggiorna voto
            db.update_voto(
                giocatore.id,
                voto_base=float(row['voto_base']),
                bonus_malus=bonus_malus,
                gol_fatti=int(row.get('gf', 0)),
                gol_subiti=int(row.get('gs', 0)),
                rigori_parati=int(row.get('rp', 0)),
                rigori_fatti=int(row.get('rf', 0)),
                rigori_sbagliati=int(row.get('rs', 0)),
                autogol=int(row.get('au', 0)),
                ammonizioni=int(row.get('amm', 0)),
                espulsioni=int(row.get('esp', 0)),
                assist=int(row.get('ass', 0)),
                note=row.get('nota', ''),
                is_manual=False
            )
            
            trovati += 1
        else:
            # Fallback: voto 6, bonus 0, nota SV
            db.update_voto(
                giocatore.id,
                voto_base=6.0,
                bonus_malus=0.0,
                note='SV',
                is_manual=False
            )
            non_trovati.append(giocatore.giocatore)
    
    nome_squadra = partita.squadra_casa if tipo_squadra == 'casa' else partita.squadra_trasferta
    st.success(f"✅ Voti applicati a {nome_squadra}: {trovati} giocatori trovati")
    
    if non_trovati:
        st.warning(f"⚠️ Giocatori non trovati (applicato fallback 6.0 SV): {', '.join(non_trovati)}")
    
    st.rerun()


def render_calcolo():
    """Pagina calcolo risultati"""
    st.title("🧮 Calcolo Risultati")
    
    giornate = db.get_all_giornate()
    
    if not giornate:
        st.warning("⚠️ Nessuna giornata disponibile.")
        return
    
    # Seleziona giornata
    giornata_options = {g.id: f"Giornata {g.numero}: {g.descrizione}" for g in giornate}
    selected_giornata_id = st.selectbox(
        "Seleziona giornata",
        options=list(giornata_options.keys()),
        format_func=lambda x: giornata_options[x],
        key="calc_giornata"
    )
    
    partite = db.get_partite_giornata(selected_giornata_id)
    
    if not partite:
        st.info("Nessuna partita in questa giornata.")
        return
    
    # Seleziona partita
    partita_options = {p.id: f"{p.squadra_casa} vs {p.squadra_trasferta}" for p in partite}
    selected_partita_id = st.selectbox(
        "Seleziona partita",
        options=list(partita_options.keys()),
        format_func=lambda x: partita_options[x],
        key="calc_partita"
    )
    
    partita = db.get_partita(selected_partita_id)
    
    st.divider()
    
    if st.button("🧮 Calcola Risultato", type="primary", use_container_width=True):
        calcola_e_mostra_risultato(partita)


def calcola_e_mostra_risultato(partita):
    """Calcola e mostra il risultato di una partita"""
    
    # Recupera formazioni
    formazione_casa = db.get_formazione_partita(partita.id, 'casa')
    formazione_trasferta = db.get_formazione_partita(partita.id, 'trasferta')
    
    if len(formazione_casa) != 11:
        st.error(f"❌ Formazione casa incompleta: {len(formazione_casa)}/11 giocatori")
        return
    
    if len(formazione_trasferta) != 11:
        st.error(f"❌ Formazione trasferta incompleta: {len(formazione_trasferta)}/11 giocatori")
        return
    
    # Prepara dati per il calcolo
    def prepara_formazione(formazione):
        return [
            {
                'nome': f.giocatore,
                'ruolo': f.ruolo,
                'voto_base': f.voto.voto_base if f.voto else 6.0,
                'bonus_malus': f.voto.bonus_malus_totale if f.voto else 0.0,
                'note': f.voto.note if f.voto else ''
            }
            for f in formazione
        ]
    
    form_casa = prepara_formazione(formazione_casa)
    form_trasferta = prepara_formazione(formazione_trasferta)
    
    # Calcola risultato
    risultato = calcola_risultato_partita(form_casa, form_trasferta)
    
    # Mostra risultato
    st.success("✅ Calcolo completato!")
    
    st.header("🏆 Risultato Finale")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.metric(partita.squadra_casa, risultato['casa']['gol'])
    
    with col2:
        st.markdown("<h2 style='text-align: center;'>VS</h2>", unsafe_allow_html=True)
    
    with col3:
        st.metric(partita.squadra_trasferta, risultato['trasferta']['gol'])
    
    st.divider()
    
    # Dettaglio squadre
    col_casa, col_trasferta = st.columns(2)
    
    with col_casa:
        st.subheader(f"🏠 {partita.squadra_casa}")
        mostra_dettaglio_squadra(formazione_casa, risultato['casa'])
    
    with col_trasferta:
        st.subheader(f"✈️ {partita.squadra_trasferta}")
        mostra_dettaglio_squadra(formazione_trasferta, risultato['trasferta'])


def mostra_dettaglio_squadra(formazione, risultato_squadra):
    """Mostra il dettaglio dei calcoli per una squadra"""
    
    # Rosa giocatori
    st.write("**Rosa titolare:**")
    
    data_giocatori = []
    for f in formazione:
        voto_base = f.voto.voto_base if f.voto else 6.0
        bonus_malus = f.voto.bonus_malus_totale if f.voto else 0.0
        voto_totale = voto_base + bonus_malus
        nota = f.voto.note if f.voto else ''
        
        data_giocatori.append({
            'Ruolo': f.ruolo,
            'Giocatore': f.giocatore,
            'Voto': f"{voto_base:.1f}",
            'Bonus/Malus': f"{bonus_malus:+.1f}" if bonus_malus != 0 else "0",
            'Totale': f"{voto_totale:.1f}",
            'Note': nota
        })
    
    df_giocatori = pd.DataFrame(data_giocatori)
    st.dataframe(df_giocatori, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Calcoli
    st.write("**Riepilogo calcoli:**")
    
    st.metric("Voto squadra (somma 11 titolari)", f"{risultato_squadra['voto_squadra']:.2f}")
    
    st.write(f"**Modulo:** {risultato_squadra['num_difensori']}:{risultato_squadra['num_centrocampisti']}:{risultato_squadra['num_attaccanti']}")
    
    st.write("**Modificatori:**")
    st.write(f"• Difesa generata: {risultato_squadra['modificatore_difesa_generato']:+.2f} (applicato all'avversario)")
    st.write(f"• Difesa subita: {risultato_squadra['modificatore_difesa_subito']:+.2f}")
    st.write(f"• Centrocampo: {risultato_squadra['modificatore_centrocampo']:+.2f}")
    st.write(f"• Attacco: {risultato_squadra['modificatore_attacco']:+.2f}")
    st.write(f"• Vantaggio casa: {risultato_squadra['vantaggio_casa']:+.2f}")
    
    st.divider()
    
    st.metric("🎯 Punteggio totale", f"{risultato_squadra['punteggio_totale']:.2f}")
    st.metric("⚽ Gol segnati", risultato_squadra['gol'])


def render_backup():
    """Pagina gestione backup e restore"""
    st.title("💾 Backup e Restore Database")
    
    st.info("""
    **Importante:** Su Streamlit Cloud, il database viene salvato in una directory persistente.
    Tuttavia, è consigliato fare backup periodici per sicurezza.
    """)
    
    tab1, tab2, tab3 = st.tabs(["📥 Backup", "📤 Restore", "📄 Export JSON"])
    
    with tab1:
        st.subheader("Crea Backup")
        st.write("Crea una copia di sicurezza del database completo.")
        
        if st.button("💾 Crea Backup Ora", type="primary"):
            try:
                backup_path = db.backup_database()
                st.success(f"✅ Backup creato con successo!")
                st.info(f"Percorso: `{backup_path}`")
                
                # Offri download del backup
                if os.path.exists(backup_path):
                    with open(backup_path, 'rb') as f:
                        st.download_button(
                            label="⬇️ Scarica Backup",
                            data=f,
                            file_name=os.path.basename(backup_path),
                            mime="application/octet-stream"
                        )
            except Exception as e:
                st.error(f"❌ Errore durante il backup: {str(e)}")
        
        st.divider()
        
        # Lista backup esistenti
        st.subheader("Backup Esistenti")
        backup_dir = 'data/backups'
        if os.path.exists(backup_dir):
            backups = [f for f in os.listdir(backup_dir) if f.endswith('.db')]
            if backups:
                for backup in sorted(backups, reverse=True):
                    backup_path = os.path.join(backup_dir, backup)
                    size = os.path.getsize(backup_path) / 1024  # KB
                    st.write(f"📁 `{backup}` ({size:.1f} KB)")
            else:
                st.info("Nessun backup trovato.")
        else:
            st.info("Nessun backup trovato.")
    
    with tab2:
        st.subheader("Ripristina da Backup")
        st.warning("⚠️ **Attenzione:** Il ripristino sovrascriverà tutti i dati attuali!")
        
        # Upload backup file
        uploaded_file = st.file_uploader(
            "Carica un file di backup (.db)",
            type=['db'],
            key="restore_upload"
        )
        
        if uploaded_file is not None:
            st.write(f"File caricato: `{uploaded_file.name}`")
            st.write(f"Dimensione: {uploaded_file.size / 1024:.1f} KB")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ Conferma Ripristino", type="primary"):
                    try:
                        # Salva il file caricato temporaneamente
                        temp_backup = 'data/temp_restore.db'
                        os.makedirs('data', exist_ok=True)
                        with open(temp_backup, 'wb') as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Ripristina
                        if db.restore_database(temp_backup):
                            st.success("✅ Database ripristinato con successo!")
                            st.info("Ricarica la pagina per vedere i dati ripristinati.")
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("❌ Errore durante il ripristino.")
                    except Exception as e:
                        st.error(f"❌ Errore: {str(e)}")
            
            with col2:
                if st.button("❌ Annulla"):
                    st.rerun()
    
    with tab3:
        st.subheader("Export JSON")
        st.write("Esporta tutti i dati in formato JSON leggibile.")
        
        if st.button("📄 Esporta in JSON", type="primary"):
            try:
                json_path = db.export_to_json()
                st.success(f"✅ Dati esportati in JSON!")
                
                # Offri download
                if os.path.exists(json_path):
                    with open(json_path, 'r', encoding='utf-8') as f:
                        st.download_button(
                            label="⬇️ Scarica JSON",
                            data=f.read(),
                            file_name="fantacalcio_export.json",
                            mime="application/json"
                        )
            except Exception as e:
                st.error(f"❌ Errore durante l'export: {str(e)}")


# ===== ROUTING =====

def main():
    """Funzione principale dell'applicazione"""
    
    render_menu()
    
    # Routing
    if st.session_state.page == 'home':
        render_home()
    elif st.session_state.page == 'giornate':
        render_giornate()
    elif st.session_state.page == 'partite':
        render_partite()
    elif st.session_state.page == 'formazioni':
        render_formazioni()
    elif st.session_state.page == 'voti':
        render_voti()
    elif st.session_state.page == 'excel':
        render_excel()
    elif st.session_state.page == 'calcolo':
        render_calcolo()
    elif st.session_state.page == 'backup':
        render_backup()


if __name__ == "__main__":
    main()
