# 📋 Guida Import Formazioni via Copia/Incolla

## Formati Supportati

L'applicazione supporta diversi formati per incollare le formazioni. Scegli quello più comodo per te!

---

## ✅ Formato 1: Ruolo + Nome (Raccomandato)

Il più semplice e affidabile.

```
P Maignan
D Calabria
D Tomori
D Thiaw
D Hernandez
C Bennacer
C Reijnders
C Pulisic
C Leao
A Giroud
A Chukwueze
```

**Vantaggi:**
- ✅ Chiaro e preciso
- ✅ Facile da scrivere
- ✅ Nessuna ambiguità

---

## ✅ Formato 2: Nome (Ruolo)

Nome seguito dal ruolo tra parentesi.

```
Maignan (P)
Calabria (D)
Tomori (D)
Thiaw (D)
Hernandez (D)
Bennacer (C)
Reijnders (C)
Pulisic (C)
Leao (C)
Giroud (A)
Chukwueze (A)
```

---

## ✅ Formato 3: Ruolo Esteso

Usa i nomi completi dei ruoli.

```
Portiere: Maignan
Difensore: Calabria
Difensore: Tomori
Difensore: Thiaw
Difensore: Hernandez
Centrocampista: Bennacer
Centrocampista: Reijnders
Centrocampista: Pulisic
Centrocampista: Leao
Attaccante: Giroud
Attaccante: Chukwueze
```

**Varianti supportate:**
- `Portiere` / `Por`
- `Difensore` / `Dif`
- `Centrocampista` / `Centro` / `Cen`
- `Attaccante` / `Att`

---

## ⚠️ Formato 4: Solo Nomi (con Deduzione Automatica)

Se incolli solo i nomi senza ruoli, il sistema prova a dedurli automaticamente:

```
Maignan
Calabria
Tomori
Thiaw
Hernandez
Bennacer
Reijnders
Pulisic
Leao
Giroud
Chukwueze
```

**Regole di deduzione:**
1. Primo giocatore → Portiere (P)
2. Giocatori 2-5 → Difensori (D)
3. Giocatori 6-9 → Centrocampisti (C)
4. Ultimi 2 → Attaccanti (A)

**Nota:** Questo metodo è meno preciso, meglio specificare sempre i ruoli!

---

## 📄 Esempi da Siti Reali

### Da NEW fantageneration ⚡ (NUOVO!)

**Formato esatto dal sito:**

Quando copi dal sito NEW fantageneration, il formato è compatto tutto su una riga:

```
(P) Sommer(D) Bastoni(D) Cambiaso(D) Coco(D) Bisseck(C) Pulisic(C) Odgaard(C) Perrone(A) David(A) Rodriguez Je.(A) Adams C.
```

✅ **Funziona perfettamente!** Il sistema riconosce automaticamente il pattern `(Ruolo) Nome` anche tutto attaccato.

**Come usare:**
1. Copia la riga "GiocatoreVoto..." dal sito (quella che inizia con "(P) NomePortiere...")
2. Incolla nel campo
3. Clicca "Elabora"
4. Verifica l'anteprima → Conferma!

**Esempio completo da NEW fantageneration:**

```
Bundesfiga : Giornata n.21
 JK Team : gol - modulo : 4-3-3
(P) Sommer(D) Bastoni(D) Cambiaso(D) Coco(D) Bisseck(C) Pulisic(C) Odgaard(C) Perrone(A) David(A) Rodriguez Je.(A) Adams C.
```

Puoi copiare **tutta la riga** o solo la parte con i giocatori → Funziona lo stesso! ✨

**Il parser riconosce:**
- ✅ `(P) Sommer` → Portiere: Sommer
- ✅ `(D) Bastoni` → Difensore: Bastoni
- ✅ `(C) Pulisic` → Centrocampista: Pulisic
- ✅ `(A) David` → Attaccante: David

**Anche con nomi doppi:**
- ✅ `(A) Rodriguez Je.` → Attaccante: Rodriguez Je.
- ✅ `(C) Ederson D.S.` → Centrocampista: Ederson D.S.

---

### Da Fantacalcio.it

Se copi da Fantacalcio.it, il formato è di solito:

```
P - Maignan
D - Calabria  
D - Tomori
D - Thiaw
D - Hernandez
C - Bennacer
C - Reijnders
C - Pulisic
C - Leao
A - Giroud
A - Chukwueze
```

✅ **Funziona!** Il sistema rimuove automaticamente i trattini.

### Da Gazzetta dello Sport

```
Maignan (P)
Calabria (D)
Tomori (D)
...
```

✅ **Funziona!**

### Da Transfermarkt o altri siti

Se hai un formato diverso, **mandami un esempio** e lo aggiungo al parser!

---

## 🔧 Come Usare

1. **Copia** la formazione dal sito o dal tuo documento
2. Vai in **"👥 Inserimento Formazioni"**
3. Seleziona **"📋 Copia/Incolla"**
4. **Incolla** nel campo di testo
5. Clicca **"🔄 Elabora e Inserisci"**
6. Verifica l'**anteprima**
7. Clicca **"✅ Conferma e Salva"**

---

## ✏️ Regole Generali

- ✅ Un giocatore per riga
- ✅ Esattamente 11 giocatori
- ✅ Ruoli: P, D, C, A (maiuscoli o minuscoli)
- ✅ Spazi e trattini vengono ignorati
- ❌ Non usare caratteri speciali strani
- ❌ Non lasciare righe vuote tra i giocatori

---

## 🎯 Esempi Completi

### Milan vs Inter (Esempio Completo)

**Milan (Casa):**
```
P Maignan
D Calabria
D Tomori
D Thiaw
D Theo Hernandez
C Bennacer
C Reijnders
C Pulisic
C Leao
A Giroud
A Chukwueze
```

**Inter (Trasferta):**
```
P Sommer
D Pavard
D Acerbi
D Bastoni
D Dumfries
C Barella
C Calhanoglu
C Mkhitaryan
C Dimarco
A Lautaro Martinez
A Thuram
```

---

### Esempio NEW fantageneration (Formato Reale)

**JK Team vs MAFIA CAPITALE**

**JK Team (Casa) - Copia esattamente così:**
```
(P) Sommer(D) Bastoni(D) Cambiaso(D) Coco(D) Bisseck(C) Pulisic(C) Odgaard(C) Perrone(A) David(A) Rodriguez Je.(A) Adams C.
```

**MAFIA CAPITALE (Trasferta) - Copia esattamente così:**
```
(P) Meret(D) Di Lorenzo(D) Mancini(D) Zortea(D) Luperto(C) Calhanoglu(C) Ederson D.S.(C) Modric(A) De Ketelaere(A) Berardi(A) Douvikas
```

✅ **Risultato:** Entrambe le formazioni vengono riconosciute perfettamente anche se tutto è su una riga!

---

## 🐛 Problemi Comuni

### Errore: "Trovati X giocatori, servono 11"

**Causa:** Hai righe vuote o hai copiato meno/più di 11 nomi

**Soluzione:** 
- Conta i giocatori
- Rimuovi righe vuote
- Assicurati di avere esattamente 11 giocatori

### Errore: "Formato non riconosciuto"

**Causa:** Il formato è troppo particolare

**Soluzioni:**
1. Prova a formattare manualmente in formato `P Nome`
2. Usa il metodo "📝 Inserimento Manuale"
3. Contattami con un esempio del tuo formato

### I ruoli sono sbagliati

**Causa:** Hai usato solo i nomi senza specificare i ruoli

**Soluzione:** Specifica sempre i ruoli esplicitamente:
- ✅ `P Maignan` invece di solo `Maignan`

---

## 💡 Consigli Pro

1. **Usa sempre il formato `P Nome`**: È il più affidabile
2. **Controlla l'anteprima**: Prima di confermare, verifica che ruoli e nomi siano corretti
3. **Copia dal tuo editor**: Se hai dubbi, scrivi la formazione in Notepad/TextEdit prima
4. **Un nome per riga**: Mai mettere più giocatori sulla stessa riga

---

## 🆕 Vuoi un Nuovo Formato?

Se hai un sito da cui copi spesso le formazioni e il formato non è supportato:

1. Copia un esempio della formazione
2. Invialomelo
3. Aggiungerò il supporto nella prossima versione!

---

**Ultimo aggiornamento:** v1.1.0 - 31 Gennaio 2025
