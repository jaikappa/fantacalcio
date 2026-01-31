"""
Motore di calcolo del Fantacalcio.
Implementa tutte le regole di calcolo con funzioni pure e testabili.
"""

from typing import List, Dict, Tuple


def calcola_bonus_malus_da_eventi(
    gol_fatti: int = 0,
    gol_subiti: int = 0,
    rigori_parati: int = 0,
    rigori_fatti: int = 0,
    rigori_sbagliati: int = 0,
    autogol: int = 0,
    ammonizioni: int = 0,
    espulsioni: int = 0,
    assist: int = 0,
    ruolo: str = ""
) -> float:
    """
    Calcola il bonus/malus totale da eventi secondo il regolamento B.
    
    Args:
        gol_fatti: numero di gol segnati
        gol_subiti: numero di gol subiti (solo per portieri)
        rigori_parati: numero di rigori parati
        rigori_fatti: numero di rigori segnati
        rigori_sbagliati: numero di rigori sbagliati
        autogol: numero di autogol
        ammonizioni: numero di ammonizioni
        espulsioni: numero di espulsioni
        assist: numero di assist
        ruolo: ruolo del giocatore (P, D, C, A)
    
    Returns:
        float: bonus/malus totale
    """
    bonus_malus = 0.0
    
    # +3 per gol fatto
    bonus_malus += gol_fatti * 3
    
    # +1 per assist
    bonus_malus += assist * 1
    
    # +3 per rigore segnato
    bonus_malus += rigori_fatti * 3
    
    # +3 per rigore parato
    bonus_malus += rigori_parati * 3
    
    # -3 per rigore sbagliato
    bonus_malus -= rigori_sbagliati * 3
    
    # -2 per autogol
    bonus_malus -= autogol * 2
    
    # -0.5 per ammonizione
    bonus_malus -= ammonizioni * 0.5
    
    # -1 per espulsione
    bonus_malus -= espulsioni * 1
    
    # Bonus/malus specifici per portiere
    if ruolo == 'P':
        # -1 per ogni gol subito
        bonus_malus -= gol_subiti * 1
        
        # +1 porta inviolata se gol subiti = 0
        if gol_subiti == 0:
            bonus_malus += 1
    
    return bonus_malus


def calcola_voto_totale(voto_base: float, bonus_malus: float) -> float:
    """
    Calcola il voto totale di un giocatore secondo regolamento A.
    
    Args:
        voto_base: voto base del giocatore
        bonus_malus: bonus/malus totale
    
    Returns:
        float: voto totale
    """
    return voto_base + bonus_malus


def calcola_voto_totale_squadra(voti_giocatori: List[float]) -> float:
    """
    Calcola il voto totale di una squadra secondo regolamento C.
    Somma dei voti totali degli 11 titolari.
    
    Args:
        voti_giocatori: lista dei voti totali degli 11 giocatori
    
    Returns:
        float: voto totale della squadra
    """
    return sum(voti_giocatori)


def calcola_modificatore_difesa(
    voti_base_difensori: List[float],
    numero_difensori: int
) -> float:
    """
    Calcola il modificatore difesa secondo regolamento D.
    
    Args:
        voti_base_difensori: voti base dei difensori titolari
        numero_difensori: numero di difensori schierati
    
    Returns:
        float: modificatore difesa (da applicare alla squadra avversaria)
    """
    if not voti_base_difensori:
        return 0.0
    
    # Calcola la media dei voti base dei difensori
    media = sum(voti_base_difensori) / len(voti_base_difensori)
    
    # Tabella del modificatore base
    if media < 5.00:
        modificatore = 4
    elif media < 5.25:
        modificatore = 3
    elif media < 5.50:
        modificatore = 2
    elif media < 5.75:
        modificatore = 1
    elif media < 6.00:
        modificatore = 0
    elif media < 6.25:
        modificatore = -1
    elif media < 6.50:
        modificatore = -2
    elif media < 6.75:
        modificatore = -3
    elif media < 7.00:
        modificatore = -4
    else:
        modificatore = -5
    
    # Correzioni in base al numero di difensori
    if numero_difensori == 3:
        modificatore += 1
    elif numero_difensori == 4:
        modificatore += 0
    elif numero_difensori == 5:
        modificatore -= 1
    
    # Penalità per difensori oltre il quarto
    if numero_difensori > 4:
        difensori_extra = numero_difensori - 4
        modificatore -= difensori_extra
    
    return float(modificatore)


def calcola_modificatore_centrocampo(
    voti_base_centrocampisti_casa: List[float],
    voti_base_centrocampisti_trasferta: List[float]
) -> Tuple[float, float]:
    """
    Calcola il modificatore centrocampo secondo regolamento E.
    
    Args:
        voti_base_centrocampisti_casa: voti base centrocampisti squadra casa
        voti_base_centrocampisti_trasferta: voti base centrocampisti trasferta
    
    Returns:
        Tuple[float, float]: (modificatore casa, modificatore trasferta)
    """
    num_casa = len(voti_base_centrocampisti_casa)
    num_trasferta = len(voti_base_centrocampisti_trasferta)
    
    # Se numero diverso, aggiungi 5 d'ufficio
    voti_casa = voti_base_centrocampisti_casa.copy()
    voti_trasferta = voti_base_centrocampisti_trasferta.copy()
    
    if num_casa < num_trasferta:
        diff = num_trasferta - num_casa
        voti_casa.extend([5.0] * diff)
    elif num_trasferta < num_casa:
        diff = num_casa - num_trasferta
        voti_trasferta.extend([5.0] * diff)
    
    # Calcola somme
    somma_casa = sum(voti_casa)
    somma_trasferta = sum(voti_trasferta)
    
    # Calcola differenza assoluta
    differenza = abs(somma_casa - somma_trasferta)
    
    # Tabella del modificatore
    if differenza < 1:
        mod_value = 0.0
    elif differenza < 2:
        mod_value = 0.5
    elif differenza < 3:
        mod_value = 1.0
    elif differenza < 4:
        mod_value = 1.5
    elif differenza < 5:
        mod_value = 2.0
    elif differenza < 6:
        mod_value = 2.5
    elif differenza < 7:
        mod_value = 3.0
    elif differenza < 8:
        mod_value = 3.5
    else:
        mod_value = 4.0
    
    # Applica positivo a chi ha somma maggiore, negativo all'altro
    if somma_casa > somma_trasferta:
        return (mod_value, -mod_value)
    elif somma_trasferta > somma_casa:
        return (-mod_value, mod_value)
    else:
        return (0.0, 0.0)


def calcola_modificatore_attacco(
    attaccanti: List[Dict[str, float]]
) -> float:
    """
    Calcola il modificatore attacco secondo regolamento F.
    
    Args:
        attaccanti: lista di dict con 'voto_base' e 'bonus_malus' per ogni attaccante
    
    Returns:
        float: modificatore attacco
    """
    modificatore = 0.0
    
    for att in attaccanti:
        voto_base = att.get('voto_base', 6.0)
        bonus_malus = att.get('bonus_malus', 0.0)
        
        # Solo se bonus_malus totale = 0
        if bonus_malus == 0:
            if 6.50 <= voto_base < 7.00:
                modificatore += 0.5
            elif 7.00 <= voto_base < 7.50:
                modificatore += 1.0
            elif voto_base >= 7.50:
                modificatore += 1.5
    
    return modificatore


def calcola_gol_da_punteggio(punteggio: float) -> int:
    """
    Calcola i gol segnati in base al punteggio totale secondo regolamento H.
    
    Args:
        punteggio: punteggio totale della squadra
    
    Returns:
        int: numero di gol segnati
    """
    if punteggio < 66:
        return 0
    elif punteggio < 72:
        return 1
    elif punteggio < 77:
        return 2
    elif punteggio < 81:
        return 3
    elif punteggio < 85:
        return 4
    else:
        # Oltre 85: +1 gol ogni 4 punti aggiuntivi
        punti_extra = punteggio - 85
        gol_extra = int(punti_extra / 4)
        return 4 + gol_extra


def calcola_risultato_partita(
    formazione_casa: List[Dict],
    formazione_trasferta: List[Dict]
) -> Dict:
    """
    Calcola il risultato completo di una partita.
    
    Args:
        formazione_casa: lista di giocatori casa con voto_base, bonus_malus, ruolo
        formazione_trasferta: lista di giocatori trasferta con voto_base, bonus_malus, ruolo
    
    Returns:
        Dict: risultato dettagliato con tutti i calcoli
    """
    
    # ===== CASA =====
    
    # Calcola voti totali giocatori casa
    voti_totali_casa = []
    voti_base_difensori_casa = []
    voti_base_centrocampisti_casa = []
    attaccanti_casa = []
    
    for giocatore in formazione_casa:
        voto_tot = calcola_voto_totale(
            giocatore['voto_base'],
            giocatore['bonus_malus']
        )
        voti_totali_casa.append(voto_tot)
        
        if giocatore['ruolo'] == 'D':
            voti_base_difensori_casa.append(giocatore['voto_base'])
        elif giocatore['ruolo'] == 'C':
            voti_base_centrocampisti_casa.append(giocatore['voto_base'])
        elif giocatore['ruolo'] == 'A':
            attaccanti_casa.append({
                'voto_base': giocatore['voto_base'],
                'bonus_malus': giocatore['bonus_malus']
            })
    
    # Voto totale squadra casa
    voto_squadra_casa = calcola_voto_totale_squadra(voti_totali_casa)
    
    # ===== TRASFERTA =====
    
    # Calcola voti totali giocatori trasferta
    voti_totali_trasferta = []
    voti_base_difensori_trasferta = []
    voti_base_centrocampisti_trasferta = []
    attaccanti_trasferta = []
    
    for giocatore in formazione_trasferta:
        voto_tot = calcola_voto_totale(
            giocatore['voto_base'],
            giocatore['bonus_malus']
        )
        voti_totali_trasferta.append(voto_tot)
        
        if giocatore['ruolo'] == 'D':
            voti_base_difensori_trasferta.append(giocatore['voto_base'])
        elif giocatore['ruolo'] == 'C':
            voti_base_centrocampisti_trasferta.append(giocatore['voto_base'])
        elif giocatore['ruolo'] == 'A':
            attaccanti_trasferta.append({
                'voto_base': giocatore['voto_base'],
                'bonus_malus': giocatore['bonus_malus']
            })
    
    # Voto totale squadra trasferta
    voto_squadra_trasferta = calcola_voto_totale_squadra(voti_totali_trasferta)
    
    # ===== MODIFICATORI =====
    
    # Modificatore difesa (si applica alla squadra avversaria)
    mod_difesa_casa = calcola_modificatore_difesa(
        voti_base_difensori_casa,
        len(voti_base_difensori_casa)
    )
    mod_difesa_trasferta = calcola_modificatore_difesa(
        voti_base_difensori_trasferta,
        len(voti_base_difensori_trasferta)
    )
    
    # Modificatore centrocampo
    mod_centro_casa, mod_centro_trasferta = calcola_modificatore_centrocampo(
        voti_base_centrocampisti_casa,
        voti_base_centrocampisti_trasferta
    )
    
    # Modificatore attacco
    mod_attacco_casa = calcola_modificatore_attacco(attaccanti_casa)
    mod_attacco_trasferta = calcola_modificatore_attacco(attaccanti_trasferta)
    
    # Vantaggio casa: +2 alla squadra di casa
    vantaggio_casa = 2.0
    vantaggio_trasferta = 0.0
    
    # ===== PUNTEGGI FINALI =====
    
    # Punteggio casa: voto squadra + mod difesa avversaria + mod centro + mod attacco + vantaggio
    punteggio_casa = (
        voto_squadra_casa +
        mod_difesa_trasferta +  # difesa avversaria
        mod_centro_casa +
        mod_attacco_casa +
        vantaggio_casa
    )
    
    # Punteggio trasferta: voto squadra + mod difesa avversaria + mod centro + mod attacco
    punteggio_trasferta = (
        voto_squadra_trasferta +
        mod_difesa_casa +  # difesa avversaria
        mod_centro_trasferta +
        mod_attacco_trasferta +
        vantaggio_trasferta
    )
    
    # Calcola gol
    gol_casa = calcola_gol_da_punteggio(punteggio_casa)
    gol_trasferta = calcola_gol_da_punteggio(punteggio_trasferta)
    
    # ===== RISULTATO =====
    
    return {
        'casa': {
            'voto_squadra': round(voto_squadra_casa, 2),
            'modificatore_difesa_generato': round(mod_difesa_casa, 2),
            'modificatore_difesa_subito': round(mod_difesa_trasferta, 2),
            'modificatore_centrocampo': round(mod_centro_casa, 2),
            'modificatore_attacco': round(mod_attacco_casa, 2),
            'vantaggio_casa': round(vantaggio_casa, 2),
            'punteggio_totale': round(punteggio_casa, 2),
            'gol': gol_casa,
            'num_difensori': len(voti_base_difensori_casa),
            'num_centrocampisti': len(voti_base_centrocampisti_casa),
            'num_attaccanti': len(attaccanti_casa)
        },
        'trasferta': {
            'voto_squadra': round(voto_squadra_trasferta, 2),
            'modificatore_difesa_generato': round(mod_difesa_trasferta, 2),
            'modificatore_difesa_subito': round(mod_difesa_casa, 2),
            'modificatore_centrocampo': round(mod_centro_trasferta, 2),
            'modificatore_attacco': round(mod_attacco_trasferta, 2),
            'vantaggio_casa': round(vantaggio_trasferta, 2),
            'punteggio_totale': round(punteggio_trasferta, 2),
            'gol': gol_trasferta,
            'num_difensori': len(voti_base_difensori_trasferta),
            'num_centrocampisti': len(voti_base_centrocampisti_trasferta),
            'num_attaccanti': len(attaccanti_trasferta)
        },
        'risultato_finale': f"{gol_casa} - {gol_trasferta}"
    }
