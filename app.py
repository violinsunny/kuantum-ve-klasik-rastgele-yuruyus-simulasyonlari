import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import binom

st.set_page_config(page_title="Kuantum Deney Laboratuvarı", layout="wide")

# Akıcılık için CSS
st.markdown("""
    <style>
    .stPlotlyChart { margin-bottom: -50px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔬 Akıcı Kuantum Yürüyüş Simülasyonu")
st.write("Hesaplama tamamlandıktan sonra aşağıdaki 'Oynat' butonuna basarak deneyi izleyebilirsiniz.")

# --- Ayarlar ---
with st.sidebar:
    steps = st.slider("Adım Sayısı", 20, 100, 50)
    st.info("Kasmayı önlemek için adımlar önceden hesaplanır ve tarayıcıda akıcı bir şekilde oynatılır.")

# --- Hesaplama Fonksiyonu ---
@st.cache_data
def calculate_frames(steps):
    frames_c = []
    frames_q = []
    x = np.arange(-steps, steps + 1)
    
    # Kuantum Başlangıç
    H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
    psi = np.zeros((2 * steps + 1, 2), dtype=complex)
    psi[steps, 0] = 1/np.sqrt(2)
    psi[steps, 1] = 1j/np.sqrt(2)

    for t in range(1, steps + 1):
        # Klasik
        y_c = np.array([binom.pmf((steps + i)//2, t, 0.5) if (t + i) % 2 == 0 else 0 for i in x])
        frames_c.append(y_c)
        
        # Kuantum
        new_psi = np.zeros_like(psi)
        for j in range(len(psi)):
            if abs(psi[j,0]) > 0 or abs(psi[j,1]) > 0:
                coin = H @ psi[j]
                if j > 0: new_psi[j-1, 0] += coin[0]
                if j < len(psi) - 1: new_psi[j+1, 1] += coin[1]
        psi = new_psi
        frames_q.append(np.sum(np.abs(psi)**2, axis=1))
        
    return x, frames_c, frames_q

x_axis, classic_data, quantum_data = calculate_frames(steps)

def create_animated_plot(x, data_frames, title, color):
    # Animasyonlu Plotly Figürü
    fig = go.Figure(
        data=[go.Scatter(x=x, y=[0]*len(x), mode='markers', 
             marker=dict(size=10, color=color, opacity=0.8, line=dict(width=1, color='white')))],
        layout=go.Layout(
            title=title,
            xaxis=dict(range=[-steps-2, steps+2], showgrid=False, zeroline=True),
            yaxis=dict(range=[-0.1, 0.5], showgrid=False, showticklabels=False),
            template="plotly_dark",
            updatemenus=[dict(type="buttons", buttons=[dict(label="Deneyi Başlat/Oynat", method="animate", args=[None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True}])])]
        ),
        frames=[go.Frame(data=[go.Scatter(x=x, y=frame_y, mode='markers', 
                marker=dict(size=frame_y*400 + 5, color=color))]) for frame_y in data_frames]
    )
    return fig

# --- Ekran Düzeni ---
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(create_animated_plot(x_axis, classic_data, "🟠 KLASİK DENEY (Normal Dağılım)", "#FFA500"), use_container_width=True)

with col2:
    st.plotly_chart(create_animated_plot(x_axis, quantum_data, "🔵 KUANTUM DENEY (Girişim)", "#00FFFF"), use_container_width=True)

st.markdown("""
### 💡 Neden Artık Kasmıyor?
Önceki yöntemde Python her adımda internet üzerinden tarayıcıya yeni bir resim gönderiyordu. 
Şimdi ise tüm veriyi bir kerede gönderdik ve animasyon işlemini **sizin tarayıcınız (GPU)** üstleniyor. 
Bu sayede parçacıkların büyümesini ve yayılmasını çok daha akıcı görebilirsiniz.
""")
