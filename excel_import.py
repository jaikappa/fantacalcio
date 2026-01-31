"""
Modulo per l'import dei voti da file Excel.
Gestisce il parsing del file e il calcolo automatico dei bonus/malus.
"""

import pandas as pd
from typing import Dict, List
from calc import calcola_bonus_malus_da_eventi


def parse_voto_excel(voto_str) -> tuple:
    """
    Parsa il voto dal formato Excel.
    Gestisce casi come "6*" che indica voto 6 con nota SV.
    
    Args:
        voto_str: stringa del voto (es. "6.5", "6*", "7")
    
    Returns:
        tuple: (voto_float, nota_str)
    """
    if pd.isna(voto_str):
        return (6.0, "SV")
    
    voto_str = str(voto_str).strip()
    
    # Gestione "6*" o simili
    if '*' in voto_str:
        # Rimuovi l'asterisco e considera SV
        voto_str = voto_str.replace('*', '')
        nota = "SV"
    else:
        nota = ""
    
    # Converti in float
    try:
        voto = float(voto_str)
    except (ValueError, TypeError):
        # Se non è convertibile, considera come SV
        voto = 6.0
        nota = "SV"
    
    return (voto, nota)


def leggi_excel_voti(filepath: str) -> pd.DataFrame:
    """
    Legge un file Excel con i voti dei giocatori.
    
    Colonne attese:
    - Ruolo (P, D, C, A)
    - Nome (nome del giocatore)
    - Voto (voto base, può contenere asterisco)
    - Gf (gol fatti)
    - Gs (gol subiti)
    - Rp (rigori parati)
    - Rf (rigori fatti)
    - Rs (rigori sbagliati)
    - Au (autogol)
    - Amm (ammonizioni)
    - Esp (espulsioni)
    - Ass (assist)
    
    Args:
        filepath: percorso del file Excel
    
    Returns:
        pd.DataFrame: DataFrame con i dati processati
    """
    # Leggi il file Excel
    df = pd.read_excel(filepath)
    
    # Normalizza i nomi delle colonne (rimuovi spazi, converti in minuscolo)
    df.columns = df.columns.str.strip().str.lower()
    
    # Colonne richieste
    required_cols = ['ruolo', 'nome', 'voto']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Colonna obbligatoria '{col}' non trovata nel file Excel")
    
    # Colonne opzionali (se non presenti, usa 0)
    optional_cols = {
        'gf': 0,
        'gs': 0,
        'rp': 0,
        'rf': 0,
        'rs': 0,
        'au': 0,
        'amm': 0,
        'esp': 0,
        'ass': 0
    }
    
    for col, default in optional_cols.items():
        if col not in df.columns:
            df[col] = default
    
    # Converti le colonne numeriche
    numeric_cols = ['gf', 'gs', 'rp', 'rf', 'rs', 'au', 'amm', 'esp', 'ass']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    
    # Parsa i voti
    df[['voto_base', 'nota']] = df['voto'].apply(
        lambda x: pd.Series(parse_voto_excel(x))
    )
    
    # Normalizza ruolo (maiuscolo, solo prima lettera)
    df['ruolo'] = df['ruolo'].str.strip().str.upper().str[0]
    
    # Normalizza nome
    df['nome'] = df['nome'].str.strip()
    
    return df


def calcola_bonus_malus_excel(row: pd.Series) -> float:
    """
    Calcola il bonus/malus per una riga del DataFrame Excel.
    
    Args:
        row: riga del DataFrame con le colonne degli eventi
    
    Returns:
        float: bonus/malus totale
    """
    return calcola_bonus_malus_da_eventi(
        gol_fatti=int(row.get('gf', 0)),
        gol_subiti=int(row.get('gs', 0)),
        rigori_parati=int(row.get('rp', 0)),
        rigori_fatti=int(row.get('rf', 0)),
        rigori_sbagliati=int(row.get('rs', 0)),
        autogol=int(row.get('au', 0)),
        ammonizioni=int(row.get('amm', 0)),
        espulsioni=int(row.get('esp', 0)),
        assist=int(row.get('ass', 0)),
        ruolo=row.get('ruolo', '')
    )


def applica_voti_excel_a_formazione(
    df_excel: pd.DataFrame,
    formazione: List[Dict],
    use_fallback: bool = True
) -> List[Dict]:
    """
    Applica i voti da Excel a una formazione.
    
    Args:
        df_excel: DataFrame con i voti da Excel
        formazione: lista di giocatori della formazione
        use_fallback: se True, applica fallback per giocatori non trovati
    
    Returns:
        List[Dict]: formazione aggiornata con voti e bonus/malus
    """
    # Crea un dizionario nome -> dati per lookup veloce
    voti_dict = {}
    for _, row in df_excel.iterrows():
        nome = row['nome'].strip().lower()
        voti_dict[nome] = row
    
    # Aggiorna la formazione
    formazione_aggiornata = []
    
    for giocatore in formazione:
        nome_giocatore = giocatore['nome'].strip().lower()
        
        if nome_giocatore in voti_dict:
            # Giocatore trovato nel file Excel
            row = voti_dict[nome_giocatore]
            
            # Calcola bonus/malus
            bonus_malus = calcola_bonus_malus_excel(row)
            
            giocatore_aggiornato = giocatore.copy()
            giocatore_aggiornato['voto_base'] = float(row['voto_base'])
            giocatore_aggiornato['bonus_malus'] = bonus_malus
            giocatore_aggiornato['nota'] = row.get('nota', '')
            giocatore_aggiornato['from_excel'] = True
            
            # Salva anche gli eventi per trasparenza
            giocatore_aggiornato['eventi'] = {
                'gol_fatti': int(row.get('gf', 0)),
                'gol_subiti': int(row.get('gs', 0)),
                'rigori_parati': int(row.get('rp', 0)),
                'rigori_fatti': int(row.get('rf', 0)),
                'rigori_sbagliati': int(row.get('rs', 0)),
                'autogol': int(row.get('au', 0)),
                'ammonizioni': int(row.get('amm', 0)),
                'espulsioni': int(row.get('esp', 0)),
                'assist': int(row.get('ass', 0))
            }
            
            formazione_aggiornata.append(giocatore_aggiornato)
        else:
            # Giocatore non trovato
            if use_fallback:
                # Applica fallback: voto 6, bonus/malus 0, nota SV
                giocatore_aggiornato = giocatore.copy()
                giocatore_aggiornato['voto_base'] = 6.0
                giocatore_aggiornato['bonus_malus'] = 0.0
                giocatore_aggiornato['nota'] = 'SV'
                giocatore_aggiornato['from_excel'] = False
                giocatore_aggiornato['eventi'] = {}
                
                formazione_aggiornata.append(giocatore_aggiornato)
            else:
                # Non applicare fallback, mantieni i dati esistenti
                formazione_aggiornata.append(giocatore)
    
    return formazione_aggiornata


def importa_voti_excel(filepath: str) -> Dict[str, pd.DataFrame]:
    """
    Importa i voti da un file Excel e restituisce il DataFrame processato.
    
    Args:
        filepath: percorso del file Excel
    
    Returns:
        Dict con 'df' (DataFrame processato) e 'summary' (sommario)
    """
    try:
        # Leggi e processa il file
        df = leggi_excel_voti(filepath)
        
        # Calcola bonus/malus per ogni riga
        df['bonus_malus_calcolato'] = df.apply(calcola_bonus_malus_excel, axis=1)
        
        # Calcola voto totale
        df['voto_totale'] = df['voto_base'] + df['bonus_malus_calcolato']
        
        # Crea summary
        summary = {
            'totale_giocatori': len(df),
            'per_ruolo': df['ruolo'].value_counts().to_dict(),
            'giocatori_con_bonus': len(df[df['bonus_malus_calcolato'] > 0]),
            'giocatori_con_malus': len(df[df['bonus_malus_calcolato'] < 0]),
            'giocatori_sv': len(df[df['nota'] == 'SV'])
        }
        
        return {
            'df': df,
            'summary': summary,
            'success': True,
            'message': f"File importato con successo: {len(df)} giocatori"
        }
        
    except Exception as e:
        return {
            'df': None,
            'summary': None,
            'success': False,
            'message': f"Errore durante l'import: {str(e)}"
        }


def esporta_template_excel(filepath: str = "template_voti.xlsx"):
    """
    Crea un file Excel template con le colonne corrette.
    
    Args:
        filepath: percorso dove salvare il template
    """
    # Crea un DataFrame di esempio
    data = {
        'Ruolo': ['P', 'D', 'C', 'A'],
        'Nome': ['Esempio Portiere', 'Esempio Difensore', 'Esempio Centrocampista', 'Esempio Attaccante'],
        'Voto': [6.5, 7.0, 6.0, '6*'],
        'Gf': [0, 0, 1, 2],
        'Gs': [2, 0, 0, 0],
        'Rp': [0, 0, 0, 0],
        'Rf': [0, 0, 0, 0],
        'Rs': [0, 0, 0, 0],
        'Au': [0, 0, 0, 0],
        'Amm': [0, 1, 0, 0],
        'Esp': [0, 0, 0, 0],
        'Ass': [0, 0, 1, 0]
    }
    
    df = pd.DataFrame(data)
    df.to_excel(filepath, index=False)
    
    return filepath
