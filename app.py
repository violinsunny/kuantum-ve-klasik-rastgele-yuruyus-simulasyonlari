import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import binom

# Sayfa Ayarları
st.set_page_config(page_title="Kuantum vs Klasik Yürüyüş", layout="wide")

st.title("🚶‍♂️ Rastgele Yürüyüş Simülasyonu")
st.write("Klasik ve Kuantum dünyasındaki olasılık farklarını keşfedin.")

# Parametreler
st.sidebar.header("Ayarlar")
steps = st.sidebar.slider("Adım Sayısı", 10, 200, 60)

# Matematiksel Mantık
def run_simulation(steps):
    # Klasik Hesaplama
    x_c = np.arange(-steps, steps + 1)
    y_c = np.zeros(len(x_c))
    for i, pos in enumerate(x_c):
        if (steps + pos) % 2 == 0:
            y_c[i] = binom.pmf((steps + pos) // 2, steps, 0.5)
            
    # Kuantum Hesaplama (Hadamard Walk)
    H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
    psi = np.zeros((2 * steps + 1, 2), dtype=complex)
    psi[steps, 0] = 1/np.sqrt(2)
    psi[steps, 1] = 1j/np.sqrt(2)
    
    for _ in range(steps):
        new_psi = np.zeros_like(psi)
        for x in range(len(psi)):
            if abs(psi[x,0]) > 0 or abs(psi[x,1]) > 0:
                coin = H @ psi[x]
                if x > 0: new_psi[x-1, 0] += coin[0]
                if x < len(psi) - 1: new_psi[x+1, 1] += coin[1]
        psi = new_psi
    y_q = np.sum(np.abs(psi)**2, axis=1)
    
    return x_c, y_c, y_q

x, y_class, y_quant = run_simulation(steps)

# Görselleştirme
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y_class, name="Klasik (Normal Dağılım)", line=dict(color='#FFA500', width=3)))
fig.add_trace(go.Scatter(x=x, y=y_quant, name="Kuantum (Girişim)", line=dict(color='#00FFFF', width=3)))

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Konum (0 = Başlangıç)",
    yaxis_title="Bulunma Olasılığı",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.info("💡 Not: Klasik yürüyüşte parçacık merkezde toplanırken, Kuantum yürüyüşte girişim (interference) nedeniyle uçlara doğru yayılır.")
