# 🚀 Guida al Deployment

Questa guida spiega come deployare l'applicazione Fantacalcio Manager su diverse piattaforme.

## 📦 Preparazione

Prima del deployment, assicurati di avere:
- Tutti i file del progetto
- Il file `requirements.txt` aggiornato
- Python 3.8 o superiore installato localmente per test

## 🌐 Opzioni di Deployment

### 1. Streamlit Cloud (Consigliato - GRATUITO)

**Vantaggi**: Gratuito, facile, ottimizzato per Streamlit

**Procedura**:

1. Crea un repository su GitHub con il progetto
2. Vai su [share.streamlit.io](https://share.streamlit.io)
3. Connetti il tuo account GitHub
4. Seleziona il repository e il file `app.py`
5. Clicca "Deploy"

**Configurazione**:
- Non servono file di configurazione aggiuntivi
- Il database SQLite viene creato automaticamente
- NOTA: Su Streamlit Cloud il database viene resettato ad ogni riavvio (usa per demo)

### 2. Heroku

**Vantaggi**: Scalabile, supporto database PostgreSQL

**Procedura**:

1. Crea un account su [heroku.com](https://heroku.com)
2. Installa Heroku CLI: `curl https://cli-assets.heroku.com/install.sh | sh`
3. Nel progetto, crea un file `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

4. Crea un file `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

5. Deploy:
```bash
heroku login
heroku create fantacalcio-app
git push heroku main
```

### 3. Railway (GRATUITO)

**Vantaggi**: Deploy facile, gratuito fino a $5/mese di utilizzo

**Procedura**:

1. Vai su [railway.app](https://railway.app)
2. Connetti il repository GitHub
3. Railway rileva automaticamente che è un'app Python
4. Deploy automatico!

**Configurazione**:
Crea un file `railway.json`:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 4. Render (GRATUITO)

**Vantaggi**: Facile, gratuito, supporto database persistente

**Procedura**:

1. Vai su [render.com](https://render.com)
2. Crea un "New Web Service"
3. Connetti il repository GitHub
4. Configura:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. Deploy!

### 5. PythonAnywhere

**Vantaggi**: Hosting Python dedicato, facile configurazione

**Procedura**:

1. Crea account su [pythonanywhere.com](https://pythonanywhere.com)
2. Carica i file via web interface o Git
3. Crea una web app Flask/Django
4. Configura WSGI per servire Streamlit
5. Usa `streamlit run app.py` in una Bash console

### 6. DigitalOcean / AWS / Google Cloud

**Vantaggi**: Controllo completo, scalabilità

**Procedura**:

1. Crea un droplet/istanza con Ubuntu
2. Installa Python e dipendenze:
```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install -r requirements.txt
```

3. Configura Nginx come reverse proxy:
```nginx
server {
    listen 80;
    server_name tuo-dominio.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

4. Usa systemd per mantenere l'app attiva:
```ini
[Unit]
Description=Fantacalcio Streamlit App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/fantacalcio
ExecStart=/usr/local/bin/streamlit run app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

5. Avvia il servizio:
```bash
sudo systemctl start fantacalcio
sudo systemctl enable fantacalcio
```

## 🗄️ Database Persistente

### SQLite (Deployment locale o VPS)
- Il database `fantacalcio.db` viene creato automaticamente
- Su piattaforme cloud gratuite, il database può essere resettato
- Per persistenza, usa un volume o storage esterno

### PostgreSQL (Per produzione)
Se vuoi usare PostgreSQL invece di SQLite:

1. Modifica `db.py`:
```python
# Invece di:
self.engine = create_engine(f'sqlite:///{db_path}')

# Usa:
DATABASE_URL = os.environ.get('DATABASE_URL')
self.engine = create_engine(DATABASE_URL)
```

2. Aggiungi `psycopg2-binary` a `requirements.txt`
3. Configura la variabile d'ambiente `DATABASE_URL` sulla piattaforma

## 🔒 Variabili d'Ambiente

Se necessario, configura variabili d'ambiente:

```bash
export DATABASE_URL="postgresql://user:pass@host:5432/dbname"
export SECRET_KEY="your-secret-key"
```

Su piattaforme cloud, usa la loro interfaccia per le env variables.

## 📊 Monitoring e Logs

### Streamlit Cloud
- Logs disponibili nel dashboard
- Monitoring automatico

### Heroku
```bash
heroku logs --tail
```

### Railway/Render
- Interfaccia web con logs in tempo reale

### VPS
```bash
journalctl -u fantacalcio -f  # Segui i logs
```

## 🔧 Troubleshooting

### Errore "Port already in use"
Streamlit usa la porta 8501 di default. Cambiala:
```bash
streamlit run app.py --server.port=8080
```

### Database locked
Su SQLite, se hai errori di lock:
- Usa PostgreSQL per ambienti multi-utente
- Configura connection pooling

### Memory limit exceeded
Su piattaforme gratuite con limiti di memoria:
- Ottimizza le query al database
- Usa paginazione per grandi dataset

## 🚀 Best Practices

1. **Usa Git**: Versiona sempre il codice
2. **Environment Variables**: Non hardcodare credenziali
3. **Backup Database**: Esporta regolarmente i dati
4. **Monitoring**: Configura alert per errori
5. **HTTPS**: Usa sempre SSL in produzione
6. **Firewall**: Limita gli accessi se necessario

## 📝 Checklist Pre-Deployment

- [ ] Test locali completati
- [ ] Requirements.txt aggiornato
- [ ] .gitignore configurato
- [ ] Database funzionante
- [ ] Variabili d'ambiente configurate
- [ ] File di configurazione piattaforma creati
- [ ] Backup del database locale

## 🆘 Supporto

Per problemi di deployment:
- Streamlit: [docs.streamlit.io](https://docs.streamlit.io)
- Heroku: [devcenter.heroku.com](https://devcenter.heroku.com)
- Railway: [docs.railway.app](https://docs.railway.app)
- Render: [render.com/docs](https://render.com/docs)

---

**Buon deployment! 🎉**
