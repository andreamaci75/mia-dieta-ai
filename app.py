import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go

# Configurazione Gemini
genai.configure(api_key="LA_TUA_CHIAVE_QUI")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AI Diet Coach", page_icon="🍎")

# --- STILE CSS PER SEMBRARE UN'APP IOS ---
st.markdown("""
    <style>
    .stApp { background-color: #f2f2f7; }
    .main-card { background: white; padding: 20px; border-radius: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA ONBOARDING ---
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.user_data = {}

if st.session_state.step == 1:
    st.title("Ciao! Sono la tua Mascotte 🤖")
    st.write("Aiutami a conoscerti per sgonfiare la pancia insieme!")
    nome = st.text_input("Come ti chiami?")
    obiettivo = st.selectbox("Qual è il tuo obiettivo?", ["Dimagrire", "Tonificare", "Mantenimento"])
    if st.button("Avanti"):
        st.session_state.user_data['nome'] = nome
        st.session_state.user_data['obiettivo'] = obiettivo
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.title("Il tuo stile di vita 🏃‍♂️")
    lavoro = st.radio("Che tipo di lavoro fai?", ["Sedentario", "Attivo", "Molto Attivo"])
    cibo_top = st.text_input("Cosa ami mangiare?")
    if st.button("Inizia la dieta"):
        st.session_state.step = 3
        st.rerun()

# --- DASHBOARD PRINCIPALE ---
else:
    st.title(f"Bentornato, {st.session_state.user_data['nome']}! ✨")
    
    # Grafico a Cerchio (Anello iOS)
    fig = go.Figure(go.Pie(
        values=[1200, 500, 300], 
        labels=['Assunte', 'Bruciate', 'Rimanenti'],
        hole=.7,
        marker_colors=['#ff9500', '#007aff', '#4cd964']
    ))
    fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=250)
    st.plotly_chart(fig, use_container_width=True)

    # Mascotte e Supporto Morale
    st.info("💡 **Messaggio del Coach:** Oggi hai fatto un ottimo lavoro con i passi! Ricorda che quel piatto di pasta che ami può essere bilanciato con una cena leggera.")

    # Inserimento Cibo
    pasto = st.text_input("Cosa hai mangiato?")
    if pasto:
        prompt = f"L'utente ha mangiato {pasto}. Calcola calorie approssimative, benefici per {st.session_state.user_data['obiettivo']} e dai un consiglio morale come un coach empatico."
        response = model.generate_content(prompt)
        st.write(response.text)
