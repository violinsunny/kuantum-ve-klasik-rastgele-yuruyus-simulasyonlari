import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import binom

# Sayfa Genişliği ve Tasarımı
st.set_page_config(page_title="Kuantum Rastgele Yürüyüş Deneyi", layout="wide")

# --- CSS Düzeltmesi: unsafe_allow_html kullanıldı ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- BAŞLIK VE GİRİŞ ---
st.title("🔬 Kuantum ve Klasik Rastgele Yürüyüş Analizi")
st.markdown("""
Bu simülasyon, bir parçacığın hareket mantığını karşılaştırır. 
**Klasik** dünyada parçacık belirli bir yerdedir, **Kuantum** dünyasında ise bir dalga gibi yayılır ve kendisiyle girişim yapar.
""")

# --- YAN MENÜ ---
with st.sidebar:
    st.header("⚙️ Deney Parametreleri")
    steps = st.slider("Adım Sayısı (Zaman)", min_value=10, max_value=150, value=60)

# --- ANALİZ VE HESAPLAMA ---
def get_data(steps):
    x = np.arange(-steps, steps + 1)
    
    # 1. Klasik Yürüyüş
    y_classic = np.zeros(len(x))
    for i, pos in enumerate(x):
        if (steps + pos) % 2 == 0:
            y_classic[i] = binom.pmf((steps + pos) // 2, steps, 0.5)
            
    # 2. Kuantum Yürüyüş
    H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
    psi = np.zeros((2 * steps + 1, 2), dtype=complex)
    psi[steps, 0] = 1/np.sqrt(2)
    psi[steps, 1] = 1j/np.sqrt(2)
    
    for _ in range(steps):
        new_psi = np.zeros_like(psi)
        for j in range(len(psi)):
            if abs(psi[j,0]) > 0 or abs(psi[j,1]) > 0:
                coin = H @ psi[j]
                if j > 0: new_psi[j-1, 0] += coin[0]
                if j < len(psi) - 1: new_psi[j+1, 1] += coin[1]
        psi = new_psi
    y_quantum = np.sum(np.abs(psi)**2, axis=1)
    
    return x, y_classic, y_quantum

x, y_c, y_q = get_data(steps)

# --- GRAFİK ---
st.subheader("📊 Olasılık Yoğunluğu Analizi")
fig = go.Figure()

fig.add_trace(go.Bar(x=x, y=y_c, name="Klasik (Parçacık)", marker_color='#FFA500', opacity=0.6))
fig.add_trace(go.Scatter(x=x, y=y_q, name="Kuantum (Dalga)", line=dict(color='#00FFFF', width=3), fill='tozeroy'))

fig.update_layout(template="plotly_dark", xaxis_title="Konum", yaxis_title="Olasılık")
st.plotly_chart(fig, use_container_width=True)

# --- ANALİZ KISMI ---
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟠 Klasik Analiz")
    st.write("Parçacık bir noktada yoğunlaşır. Rastgele adımlar birbirini dengeler ve merkezde birikme olur (Normal Dağılım).")

with col2:
    st.subheader("🔵 Kuantum Analiz")
    st.write("Parçacık bir dalga gibi davranır. Yıkıcı girişim merkezi boşaltırken, yapıcı girişim parçacığı hızla dışarı iter.")
