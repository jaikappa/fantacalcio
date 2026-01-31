"""
Test per il motore di calcolo.
Verifica il corretto funzionamento di tutte le regole.
"""

from calc import (
    calcola_bonus_malus_da_eventi,
    calcola_voto_totale,
    calcola_voto_totale_squadra,
    calcola_modificatore_difesa,
    calcola_modificatore_centrocampo,
    calcola_modificatore_attacco,
    calcola_gol_da_punteggio,
    calcola_risultato_partita
)


def test_bonus_malus_da_eventi():
    """Test calcolo bonus/malus da eventi"""
    
    print("Test 1: Attaccante con 2 gol e 1 assist")
    bonus = calcola_bonus_malus_da_eventi(
        gol_fatti=2,
        assist=1,
        ruolo='A'
    )
    assert bonus == 7.0, f"Atteso 7.0, ottenuto {bonus}"
    print(f"✓ Bonus calcolato: {bonus}")
    
    print("\nTest 2: Centrocampista con 1 gol, 1 ammonizione, 1 espulsione")
    bonus = calcola_bonus_malus_da_eventi(
        gol_fatti=1,
        ammonizioni=1,
        espulsioni=1,
        ruolo='C'
    )
    assert bonus == 1.5, f"Atteso 1.5, ottenuto {bonus}"
    print(f"✓ Bonus calcolato: {bonus}")
    
    print("\nTest 3: Portiere con 2 gol subiti (nessun bonus porta inviolata)")
    bonus = calcola_bonus_malus_da_eventi(
        gol_subiti=2,
        ruolo='P'
    )
    assert bonus == -2.0, f"Atteso -2.0, ottenuto {bonus}"
    print(f"✓ Bonus calcolato: {bonus}")
    
    print("\nTest 4: Portiere con porta inviolata e 1 rigore parato")
    bonus = calcola_bonus_malus_da_eventi(
        gol_subiti=0,
        rigori_parati=1,
        ruolo='P'
    )
    assert bonus == 4.0, f"Atteso 4.0, ottenuto {bonus}"
    print(f"✓ Bonus calcolato: {bonus}")
    
    print("\nTest 5: Difensore con autogol e rigore sbagliato")
    bonus = calcola_bonus_malus_da_eventi(
        autogol=1,
        rigori_sbagliati=1,
        ruolo='D'
    )
    assert bonus == -5.0, f"Atteso -5.0, ottenuto {bonus}"
    print(f"✓ Bonus calcolato: {bonus}")


def test_modificatore_difesa():
    """Test calcolo modificatore difesa"""
    
    print("\n\nTest Modificatore Difesa:")
    
    print("\nTest 1: 4 difensori con media 6.25 (mod base -2, nessuna correzione)")
    mod = calcola_modificatore_difesa([6.0, 6.5, 6.5, 6.0], 4)
    assert mod == -2.0, f"Atteso -2.0, ottenuto {mod}"
    print(f"✓ Modificatore: {mod}")
    
    print("\nTest 2: 3 difensori con media 5.50 (mod base +1, +1 per difesa a 3)")
    mod = calcola_modificatore_difesa([5.5, 5.5, 5.5], 3)
    assert mod == 2.0, f"Atteso 2.0, ottenuto {mod}"
    print(f"✓ Modificatore: {mod}")
    
    print("\nTest 3: 5 difensori con media 7.0 (mod base -5, -1 per difesa a 5, -1 per 5° difensore)")
    mod = calcola_modificatore_difesa([7.0, 7.0, 7.0, 7.0, 7.0], 5)
    assert mod == -7.0, f"Atteso -7.0, ottenuto {mod}"
    print(f"✓ Modificatore: {mod}")


def test_modificatore_centrocampo():
    """Test calcolo modificatore centrocampo"""
    
    print("\n\nTest Modificatore Centrocampo:")
    
    print("\nTest 1: Stessi centrocampisti (5 vs 5), somma uguale")
    mod_casa, mod_trasferta = calcola_modificatore_centrocampo(
        [6.0, 6.0, 6.0, 6.0, 6.0],
        [6.0, 6.0, 6.0, 6.0, 6.0]
    )
    assert mod_casa == 0.0 and mod_trasferta == 0.0
    print(f"✓ Casa: {mod_casa}, Trasferta: {mod_trasferta}")
    
    print("\nTest 2: Casa 4 centrocampisti (somma 24), Trasferta 5 (somma 30)")
    print("       Casa riceve +5 d'ufficio, somma diventa 29 vs 30, diff=1")
    mod_casa, mod_trasferta = calcola_modificatore_centrocampo(
        [6.0, 6.0, 6.0, 6.0],
        [6.0, 6.0, 6.0, 6.0, 6.0]
    )
    # Differenza 1 -> mod 0.5
    assert mod_trasferta == 0.5 and mod_casa == -0.5
    print(f"✓ Casa: {mod_casa}, Trasferta: {mod_trasferta}")
    
    print("\nTest 3: Casa somma 35, Trasferta somma 25, diff=10 (mod 4.0)")
    mod_casa, mod_trasferta = calcola_modificatore_centrocampo(
        [7.0, 7.0, 7.0, 7.0, 7.0],
        [5.0, 5.0, 5.0, 5.0, 5.0]
    )
    assert mod_casa == 4.0 and mod_trasferta == -4.0
    print(f"✓ Casa: {mod_casa}, Trasferta: {mod_trasferta}")


def test_modificatore_attacco():
    """Test calcolo modificatore attacco"""
    
    print("\n\nTest Modificatore Attacco:")
    
    print("\nTest 1: Attaccante con voto 7.0 e bonus/malus 0")
    attaccanti = [{'voto_base': 7.0, 'bonus_malus': 0.0}]
    mod = calcola_modificatore_attacco(attaccanti)
    assert mod == 1.0, f"Atteso 1.0, ottenuto {mod}"
    print(f"✓ Modificatore: {mod}")
    
    print("\nTest 2: Attaccante con voto 6.5 e bonus/malus 0")
    attaccanti = [{'voto_base': 6.5, 'bonus_malus': 0.0}]
    mod = calcola_modificatore_attacco(attaccanti)
    assert mod == 0.5, f"Atteso 0.5, ottenuto {mod}"
    print(f"✓ Modificatore: {mod}")
    
    print("\nTest 3: Attaccante con voto 7.5 e bonus/malus diverso da 0 (NON conta)")
    attaccanti = [{'voto_base': 7.5, 'bonus_malus': 3.0}]
    mod = calcola_modificatore_attacco(attaccanti)
    assert mod == 0.0, f"Atteso 0.0, ottenuto {mod}"
    print(f"✓ Modificatore: {mod}")
    
    print("\nTest 4: Due attaccanti, uno 7.5 senza bonus, uno 6.0 con bonus")
    attaccanti = [
        {'voto_base': 7.5, 'bonus_malus': 0.0},
        {'voto_base': 6.0, 'bonus_malus': 3.0}
    ]
    mod = calcola_modificatore_attacco(attaccanti)
    assert mod == 1.5, f"Atteso 1.5, ottenuto {mod}"
    print(f"✓ Modificatore: {mod}")


def test_gol_da_punteggio():
    """Test conversione punteggio in gol"""
    
    print("\n\nTest Conversione Punteggio -> Gol:")
    
    test_cases = [
        (65.99, 0),
        (66.0, 1),
        (71.99, 1),
        (72.0, 2),
        (76.99, 2),
        (77.0, 3),
        (80.99, 3),
        (81.0, 4),
        (84.99, 4),
        (85.0, 4),
        (89.0, 5),  # 85 + 4 = 89
        (93.0, 6),  # 85 + 8 = 93
    ]
    
    for punteggio, gol_attesi in test_cases:
        gol = calcola_gol_da_punteggio(punteggio)
        assert gol == gol_attesi, f"Punteggio {punteggio}: attesi {gol_attesi} gol, ottenuti {gol}"
        print(f"✓ Punteggio {punteggio:.2f} -> {gol} gol")


def test_partita_completa():
    """Test calcolo completo di una partita"""
    
    print("\n\nTest Partita Completa:")
    
    # Formazione Casa: 1P, 4D, 4C, 2A
    formazione_casa = [
        {'nome': 'Portiere', 'ruolo': 'P', 'voto_base': 6.0, 'bonus_malus': 1.0},  # Porta inviolata
        {'nome': 'Difensore 1', 'ruolo': 'D', 'voto_base': 6.0, 'bonus_malus': 0.0},
        {'nome': 'Difensore 2', 'ruolo': 'D', 'voto_base': 6.5, 'bonus_malus': 0.0},
        {'nome': 'Difensore 3', 'ruolo': 'D', 'voto_base': 6.0, 'bonus_malus': 0.0},
        {'nome': 'Difensore 4', 'ruolo': 'D', 'voto_base': 6.5, 'bonus_malus': 0.0},
        {'nome': 'Centrocampista 1', 'ruolo': 'C', 'voto_base': 6.0, 'bonus_malus': 0.0},
        {'nome': 'Centrocampista 2', 'ruolo': 'C', 'voto_base': 6.5, 'bonus_malus': 0.0},
        {'nome': 'Centrocampista 3', 'ruolo': 'C', 'voto_base': 6.0, 'bonus_malus': 0.0},
        {'nome': 'Centrocampista 4', 'ruolo': 'C', 'voto_base': 6.5, 'bonus_malus': 0.0},
        {'nome': 'Attaccante 1', 'ruolo': 'A', 'voto_base': 7.0, 'bonus_malus': 3.0},  # 1 gol
        {'nome': 'Attaccante 2', 'ruolo': 'A', 'voto_base': 6.5, 'bonus_malus': 0.0},  # Senza bonus
    ]
    
    # Formazione Trasferta: 1P, 4D, 3C, 3A
    formazione_trasferta = [
        {'nome': 'Portiere T', 'ruolo': 'P', 'voto_base': 6.0, 'bonus_malus': -2.0},  # 2 gol subiti
        {'nome': 'Difensore T1', 'ruolo': 'D', 'voto_base': 6.0, 'bonus_malus': 0.0},
        {'nome': 'Difensore T2', 'ruolo': 'D', 'voto_base': 6.0, 'bonus_malus': 0.0},
        {'nome': 'Difensore T3', 'ruolo': 'D', 'voto_base': 5.5, 'bonus_malus': 0.0},
        {'nome': 'Difensore T4', 'ruolo': 'D', 'voto_base': 6.0, 'bonus_malus': 0.0},
        {'nome': 'Centrocampista T1', 'ruolo': 'C', 'voto_base': 6.0, 'bonus_malus': 0.0},
        {'nome': 'Centrocampista T2', 'ruolo': 'C', 'voto_base': 6.0, 'bonus_malus': 0.0},
        {'nome': 'Centrocampista T3', 'ruolo': 'C', 'voto_base': 5.5, 'bonus_malus': 0.0},
        {'nome': 'Attaccante T1', 'ruolo': 'A', 'voto_base': 7.0, 'bonus_malus': 0.0},  # Senza bonus
        {'nome': 'Attaccante T2', 'ruolo': 'A', 'voto_base': 6.0, 'bonus_malus': 0.0},
        {'nome': 'Attaccante T3', 'ruolo': 'A', 'voto_base': 6.0, 'bonus_malus': 3.0},  # 1 gol
    ]
    
    risultato = calcola_risultato_partita(formazione_casa, formazione_trasferta)
    
    print(f"\n{'='*60}")
    print(f"SQUADRA CASA")
    print(f"{'='*60}")
    print(f"Voto squadra: {risultato['casa']['voto_squadra']}")
    print(f"Modulo: {risultato['casa']['num_difensori']}-{risultato['casa']['num_centrocampisti']}-{risultato['casa']['num_attaccanti']}")
    print(f"Modificatore difesa generato: {risultato['casa']['modificatore_difesa_generato']:+.2f}")
    print(f"Modificatore difesa subito: {risultato['casa']['modificatore_difesa_subito']:+.2f}")
    print(f"Modificatore centrocampo: {risultato['casa']['modificatore_centrocampo']:+.2f}")
    print(f"Modificatore attacco: {risultato['casa']['modificatore_attacco']:+.2f}")
    print(f"Vantaggio casa: {risultato['casa']['vantaggio_casa']:+.2f}")
    print(f"Punteggio totale: {risultato['casa']['punteggio_totale']:.2f}")
    print(f"Gol: {risultato['casa']['gol']}")
    
    print(f"\n{'='*60}")
    print(f"SQUADRA TRASFERTA")
    print(f"{'='*60}")
    print(f"Voto squadra: {risultato['trasferta']['voto_squadra']}")
    print(f"Modulo: {risultato['trasferta']['num_difensori']}-{risultato['trasferta']['num_centrocampisti']}-{risultato['trasferta']['num_attaccanti']}")
    print(f"Modificatore difesa generato: {risultato['trasferta']['modificatore_difesa_generato']:+.2f}")
    print(f"Modificatore difesa subito: {risultato['trasferta']['modificatore_difesa_subito']:+.2f}")
    print(f"Modificatore centrocampo: {risultato['trasferta']['modificatore_centrocampo']:+.2f}")
    print(f"Modificatore attacco: {risultato['trasferta']['modificatore_attacco']:+.2f}")
    print(f"Vantaggio casa: {risultato['trasferta']['vantaggio_casa']:+.2f}")
    print(f"Punteggio totale: {risultato['trasferta']['punteggio_totale']:.2f}")
    print(f"Gol: {risultato['trasferta']['gol']}")
    
    print(f"\n{'='*60}")
    print(f"RISULTATO FINALE: {risultato['risultato_finale']}")
    print(f"{'='*60}")


if __name__ == "__main__":
    print("="*60)
    print("TEST MOTORE DI CALCOLO FANTACALCIO")
    print("="*60)
    
    test_bonus_malus_da_eventi()
    test_modificatore_difesa()
    test_modificatore_centrocampo()
    test_modificatore_attacco()
    test_gol_da_punteggio()
    test_partita_completa()
    
    print("\n" + "="*60)
    print("✅ TUTTI I TEST COMPLETATI CON SUCCESSO!")
    print("="*60)
