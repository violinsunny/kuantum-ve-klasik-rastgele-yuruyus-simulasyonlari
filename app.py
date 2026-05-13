import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import binom

st.set_page_config(page_title="Kuantum Deney Laboratuvarı", layout="wide")

st.title("🔬 Sakin Kuantum ve Klasik Yürüyüş Deneyi")
st.markdown("""
Bu simülasyon, verileri önceden hesaplar ve tarayıcınızda akıcı bir şekilde oynatır. 
**'Oynat'** butonuna bastığınızda, kuantum dalgasının sakin yayılımını izleyebilirsiniz.
""")

# --- Sidebar Parametreleri ---
with st.sidebar:
    st.header("⚙️ Deney Ayarları")
    steps = st.slider("Toplam Adım (Zaman)", 20, 100, 60)
    frame_duration = st.slider("Adım Hızı (ms)", 20, 500, 100)
    st.info("Düşük ms değeri daha hızlı, yüksek ms değeri daha sakin bir animasyon sağlar.")

# --- Hesaplama Motoru (Önbellekli) ---
@st.cache_data
def calculate_experiment(steps):
    x = np.arange(-steps, steps + 1)
    classic_frames = []
    quantum_frames = []
    
    # Kuantum Başlangıç Durumu
    H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
    psi = np.zeros((2 * steps + 1, 2), dtype=complex)
    psi[steps, 0] = 1/np.sqrt(2) # Başlangıç konumu: Merkez
    psi[steps, 1] = 1j/np.sqrt(2) # Simetri için karmaşık faz

    for t in range(1, steps + 1):
        # 1. Klasik Hesaplama
        y_c = np.array([binom.pmf((steps + i)//2, t, 0.5) if (t + i) % 2 == 0 else 0 for i in x])
        classic_frames.append(y_c)
        
        # 2. Kuantum Hesaplama
        new_psi = np.zeros_like(psi)
        for j in range(len(psi)):
            if abs(psi[j,0]) > 0 or abs(psi[j,1]) > 0:
                coin = H @ psi[j]
                if j > 0: new_psi[j-1, 0] += coin[0]
                if j < len(psi) - 1: new_psi[j+1, 1] += coin[1]
        psi = new_psi
        quantum_frames.append(np.sum(np.abs(psi)**2, axis=1))
        
    return x, classic_frames, quantum_frames

x_axis, classic_data, quantum_data = calculate_experiment(steps)

def create_smooth_animation(x, data_frames, title, color):
    # Ana Figür
    fig = go.Figure(
        data=[go.Scatter(x=x, y=[0]*len(x), mode='markers', 
             marker=dict(size=5, color=color, opacity=0.8))],
        layout=go.Layout(
            title=title,
            xaxis=dict(range=[-steps-2, steps+2], showgrid=False, zeroline=True, zerolinecolor="gray"),
            yaxis=dict(range=[-0.05, 0.5], showgrid=False, showticklabels=False),
            template="plotly_dark",
            height=300,
            updatemenus=[{
                "type": "buttons",
                "buttons": [{
                    "label": "▶ Deneyi Başlat",
                    "method": "animate",
                    "args": [None, {"frame": {"duration": frame_duration, "redraw": False}, "fromcurrent": True, "transition": {"duration": frame_duration//2, "easing": "quadratic-in-out"}}]
                }]
            }]
        ),
        # Her bir adım için frame (kare) ekleme
        frames=[go.Frame(data=[go.Scatter(x=x, y=frame_y, mode='markers', 
                marker=dict(size=frame_y*350 + 4, color=color))]) for frame_y in data_frames]
    )
    return fig

# --- Görselleştirme ---
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(create_smooth_animation(x_axis, classic_data, "🟠 Klasik: Belirli Bir Konum", "#FFA500"), use_container_width=True)

with col2:
    st.plotly_chart(create_smooth_animation(x_axis, quantum_data, "🔵 Kuantum: Olasılık Bulutu", "#00FFFF"), use_container_width=True)

st.markdown("""
---
### 🧪 Deney Gözlemi
*   **Klasik:** Toplar rastgele dağılır ama istatistiksel olarak merkezde "yığılır".
*   **Kuantum:** Parçacık tek bir yerde olmak yerine bir **bulut (süperpozisyon)** gibi yayılır. Uçlardaki parlamalar, kuantum girişiminin (interferans) parçacığı ne kadar uzağa taşıyabildiğini gösterir.
""")
