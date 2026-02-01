"""
Modulo per la gestione del database SQLite.
Gestisce la persistenza di giornate, partite, formazioni e voti.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()


class Giornata(Base):
    """Rappresenta una giornata di campionato"""
    __tablename__ = 'giornate'
    
    id = Column(Integer, primary_key=True)
    numero = Column(Integer, nullable=False, unique=True)
    descrizione = Column(String(200))
    data_creazione = Column(DateTime, default=datetime.now)
    
    # Relazione con le partite
    partite = relationship("Partita", back_populates="giornata", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Giornata {self.numero}: {self.descrizione}>"


class Partita(Base):
    """Rappresenta una partita tra due squadre"""
    __tablename__ = 'partite'
    
    id = Column(Integer, primary_key=True)
    giornata_id = Column(Integer, ForeignKey('giornate.id'), nullable=False)
    squadra_casa = Column(String(100), nullable=False)
    squadra_trasferta = Column(String(100), nullable=False)
    
    # Relazioni
    giornata = relationship("Giornata", back_populates="partite")
    formazioni = relationship("Formazione", back_populates="partita", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Partita {self.squadra_casa} vs {self.squadra_trasferta}>"


class Formazione(Base):
    """Rappresenta la formazione di una squadra in una partita"""
    __tablename__ = 'formazioni'
    
    id = Column(Integer, primary_key=True)
    partita_id = Column(Integer, ForeignKey('partite.id'), nullable=False)
    squadra = Column(String(100), nullable=False)  # casa o trasferta
    giocatore = Column(String(100), nullable=False)
    ruolo = Column(String(1), nullable=False)  # P, D, C, A
    posizione = Column(Integer, nullable=False)  # 1-11 per ordine titolari
    
    # Relazioni
    partita = relationship("Partita", back_populates="formazioni")
    voto = relationship("Voto", back_populates="formazione", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Formazione {self.giocatore} ({self.ruolo})>"


class Voto(Base):
    """Rappresenta il voto e i bonus/malus di un giocatore"""
    __tablename__ = 'voti'
    
    id = Column(Integer, primary_key=True)
    formazione_id = Column(Integer, ForeignKey('formazioni.id'), nullable=False)
    
    # Voto base
    voto_base = Column(Float, nullable=False, default=6.0)
    
    # Eventi da Excel
    gol_fatti = Column(Integer, default=0)
    gol_subiti = Column(Integer, default=0)
    rigori_parati = Column(Integer, default=0)
    rigori_fatti = Column(Integer, default=0)
    rigori_sbagliati = Column(Integer, default=0)
    autogol = Column(Integer, default=0)
    ammonizioni = Column(Integer, default=0)
    espulsioni = Column(Integer, default=0)
    assist = Column(Integer, default=0)
    
    # Bonus/malus totale (calcolato o inserito manualmente)
    bonus_malus_totale = Column(Float, default=0.0)
    
    # Override manuale
    is_manual_override = Column(Boolean, default=False)
    
    # Note (es. SV)
    note = Column(String(50), default="")
    
    # Relazione
    formazione = relationship("Formazione", back_populates="voto")
    
    def __repr__(self):
        return f"<Voto {self.voto_base} + {self.bonus_malus_totale}>"


class DatabaseManager:
    """Gestisce le operazioni sul database"""
    
    def __init__(self, db_path='fantacalcio.db'):
        """
        Inizializza la connessione al database.
        Su Streamlit Cloud usa directory persistente per evitare perdita dati.
        """
        # Su Streamlit Cloud, usa directory persistente
        if os.path.exists('/mount/data'):
            # Directory persistente di Streamlit Cloud
            db_path = f'/mount/data/{db_path}'
        elif not db_path.startswith('/'):
            # Locale: crea directory data se non esiste
            os.makedirs('data', exist_ok=True)
            db_path = f'data/{db_path}'
        
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def get_session(self):
        """Restituisce la sessione del database"""
        return self.session
    
    def backup_database(self, backup_path=None):
        """
        Crea un backup del database.
        
        Args:
            backup_path: percorso dove salvare il backup (default: data/backup_YYYYMMDD_HHMMSS.db)
        
        Returns:
            str: percorso del file di backup creato
        """
        import shutil
        from datetime import datetime
        
        if backup_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            os.makedirs('data/backups', exist_ok=True)
            backup_path = f'data/backups/fantacalcio_backup_{timestamp}.db'
        
        # Chiudi e riapri la connessione per assicurare flush
        self.session.close()
        
        # Copia il file database
        shutil.copy2(self.db_path, backup_path)
        
        # Riapri la sessione
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        return backup_path
    
    def restore_database(self, backup_path):
        """
        Ripristina il database da un backup.
        
        Args:
            backup_path: percorso del file di backup
        
        Returns:
            bool: True se il ripristino è riuscito
        """
        import shutil
        
        if not os.path.exists(backup_path):
            return False
        
        # Chiudi la connessione
        self.session.close()
        self.engine.dispose()
        
        # Ripristina il database
        shutil.copy2(backup_path, self.db_path)
        
        # Riapri la connessione
        self.engine = create_engine(f'sqlite:///{self.db_path}')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        return True
    
    def export_to_json(self, filepath='data/fantacalcio_export.json'):
        """
        Esporta tutto il database in formato JSON.
        
        Args:
            filepath: percorso dove salvare il JSON
        
        Returns:
            str: percorso del file esportato
        """
        import json
        
        export_data = {
            'giornate': [],
            'export_date': datetime.now().isoformat()
        }
        
        # Esporta tutte le giornate con partite, formazioni e voti
        giornate = self.get_all_giornate()
        
        for g in giornate:
            giornata_data = {
                'numero': g.numero,
                'descrizione': g.descrizione,
                'partite': []
            }
            
            for p in g.partite:
                partita_data = {
                    'squadra_casa': p.squadra_casa,
                    'squadra_trasferta': p.squadra_trasferta,
                    'formazioni': {'casa': [], 'trasferta': []}
                }
                
                for tipo in ['casa', 'trasferta']:
                    formazioni = self.get_formazione_partita(p.id, tipo)
                    for f in formazioni:
                        voto = self.get_voto(f.id)
                        form_data = {
                            'giocatore': f.giocatore,
                            'ruolo': f.ruolo,
                            'posizione': f.posizione,
                            'voto': {
                                'voto_base': voto.voto_base if voto else None,
                                'bonus_malus': voto.bonus_malus_totale if voto else None,
                                'note': voto.note if voto else None
                            } if voto else None
                        }
                        partita_data['formazioni'][tipo].append(form_data)
                
                giornata_data['partite'].append(partita_data)
            
            export_data['giornate'].append(giornata_data)
        
        # Salva in JSON
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def create_giornata(self, numero, descrizione=""):
        """Crea una nuova giornata"""
        giornata = Giornata(numero=numero, descrizione=descrizione)
        self.session.add(giornata)
        self.session.commit()
        return giornata
    
    def get_all_giornate(self):
        """Restituisce tutte le giornate ordinate per numero"""
        return self.session.query(Giornata).order_by(Giornata.numero).all()
    
    def get_giornata(self, giornata_id):
        """Restituisce una giornata per ID"""
        return self.session.query(Giornata).filter_by(id=giornata_id).first()
    
    def create_partita(self, giornata_id, squadra_casa, squadra_trasferta):
        """Crea una nuova partita"""
        partita = Partita(
            giornata_id=giornata_id,
            squadra_casa=squadra_casa,
            squadra_trasferta=squadra_trasferta
        )
        self.session.add(partita)
        self.session.commit()
        return partita
    
    def get_partite_giornata(self, giornata_id):
        """Restituisce tutte le partite di una giornata"""
        return self.session.query(Partita).filter_by(giornata_id=giornata_id).all()
    
    def get_partita(self, partita_id):
        """Restituisce una partita per ID"""
        return self.session.query(Partita).filter_by(id=partita_id).first()
    
    def add_formazione(self, partita_id, squadra, giocatore, ruolo, posizione):
        """Aggiunge un giocatore alla formazione"""
        formazione = Formazione(
            partita_id=partita_id,
            squadra=squadra,
            giocatore=giocatore,
            ruolo=ruolo,
            posizione=posizione
        )
        self.session.add(formazione)
        
        # Crea automaticamente un voto associato
        voto = Voto(formazione=formazione)
        self.session.add(voto)
        
        self.session.commit()
        return formazione
    
    def get_formazione_partita(self, partita_id, squadra):
        """Restituisce la formazione di una squadra in una partita"""
        return self.session.query(Formazione).filter_by(
            partita_id=partita_id,
            squadra=squadra
        ).order_by(Formazione.posizione).all()
    
    def update_voto(self, formazione_id, voto_base=None, bonus_malus=None, 
                    gol_fatti=None, gol_subiti=None, rigori_parati=None,
                    rigori_fatti=None, rigori_sbagliati=None, autogol=None,
                    ammonizioni=None, espulsioni=None, assist=None, note=None,
                    is_manual=False):
        """Aggiorna il voto di un giocatore"""
        formazione = self.session.query(Formazione).filter_by(id=formazione_id).first()
        if not formazione:
            return None
        
        if not formazione.voto:
            voto = Voto(formazione_id=formazione_id)
            self.session.add(voto)
        else:
            voto = formazione.voto
        
        if voto_base is not None:
            voto.voto_base = voto_base
        if bonus_malus is not None:
            voto.bonus_malus_totale = bonus_malus
        if gol_fatti is not None:
            voto.gol_fatti = gol_fatti
        if gol_subiti is not None:
            voto.gol_subiti = gol_subiti
        if rigori_parati is not None:
            voto.rigori_parati = rigori_parati
        if rigori_fatti is not None:
            voto.rigori_fatti = rigori_fatti
        if rigori_sbagliati is not None:
            voto.rigori_sbagliati = rigori_sbagliati
        if autogol is not None:
            voto.autogol = autogol
        if ammonizioni is not None:
            voto.ammonizioni = ammonizioni
        if espulsioni is not None:
            voto.espulsioni = espulsioni
        if assist is not None:
            voto.assist = assist
        if note is not None:
            voto.note = note
        
        voto.is_manual_override = is_manual
        
        self.session.commit()
        return voto
    
    def delete_giornata(self, giornata_id):
        """Elimina una giornata e tutte le partite associate"""
        giornata = self.get_giornata(giornata_id)
        if giornata:
            self.session.delete(giornata)
            self.session.commit()
            return True
        return False
    
    def delete_partita(self, partita_id):
        """Elimina una partita"""
        partita = self.get_partita(partita_id)
        if partita:
            self.session.delete(partita)
            self.session.commit()
            return True
        return False
    
    def clear_formazione(self, partita_id, squadra):
        """Elimina tutti i giocatori di una formazione"""
        formazioni = self.get_formazione_partita(partita_id, squadra)
        for f in formazioni:
            self.session.delete(f)
        self.session.commit()
    
    def close(self):
        """Chiude la connessione al database"""
        self.session.close()
