#!/bin/bash

# Script di avvio per Fantacalcio Manager

echo "========================================="
echo "  ⚽ Fantacalcio Manager - Avvio  "
echo "========================================="
echo ""

# Verifica se Python è installato
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trovato. Installa Python 3.8 o superiore."
    exit 1
fi

echo "✓ Python trovato: $(python3 --version)"
echo ""

# Verifica se le dipendenze sono installate
echo "Controllo dipendenze..."

if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "⚠️  Dipendenze mancanti. Installazione in corso..."
    pip install -r requirements.txt
    echo "✅ Dipendenze installate!"
else
    echo "✅ Dipendenze già installate"
fi

echo ""
echo "========================================="
echo "Avvio dell'applicazione..."
echo "========================================="
echo ""
echo "📱 L'applicazione si aprirà nel browser"
echo "🔗 URL: http://localhost:8501"
echo ""
echo "Per interrompere l'applicazione: CTRL+C"
echo ""

# Avvia Streamlit
streamlit run app.py
