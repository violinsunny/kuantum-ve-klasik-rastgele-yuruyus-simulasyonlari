%%writefile app.py
import streamlit as st
import numpy as np
import time

st.set_page_config(page_title="Kuantum Deney Alanı", layout="wide")

st.title("🔬 Somut Rastgele Yürüyüş Deneyi")
st.markdown("""
Aşağıdaki iki panelde, parçacıkların (atomların veya insanların) nasıl yol aldığını **canlı** olarak izleyin.
*   **Üst Panel:** Yazı-tura atan bir insan (Klasik).
*   **Alt Panel:** Aynı anda her yerde olan bir kuantum dalgası.
""")

# --- Ayarlar ---
steps = st.sidebar.slider("Adım Sayısı", 10, 100, 50)
speed = st.sidebar.slider("Simülasyon Hızı", 0.01, 0.5, 0.1)
start_button = st.button("Deneyi Başlat")

# --- Deney Alanları ---
classic_area = st.empty()
quantum_area = st.empty()

def render_experiment(positions, probs, title, color_hex):
    """Parçacıkları fiziksel noktalar olarak çizen fonksiyon"""
    # Normalize edilmiş olasılıklarla 'parçacık yoğunluğu' oluşturma
    # Yüksek olasılıklı yerlerde noktalar daha parlak ve büyük görünür
    
    # Plotly ile görsel bir 'piste' dönüştürelim
    import plotly.graph_objects as go
    
    fig = go.Figure()
    
    # Zemin çizgisi
    fig.add_shape(type="line", x0=-steps, y0=0, x1=steps, y1=0, line=dict(color="Gray", width=2))
    
    # Parçacıkların konumları (Somut topçuklar)
    fig.add_trace(go.Scatter(
        x=positions,
        y=[0] * len(positions),
        mode='markers',
        marker=dict(
            size=probs * 300,  # Olasılığa göre topun boyutu değişir
            color=color_hex,
            opacity=0.7,
            line=dict(width=2, color='white')
        ),
        name="Parçacık Bulutu"
    ))
    
    fig.update_layout(
        title=title,
        xaxis=dict(range=[-steps-5, steps+5], showgrid=False, zeroline=False),
        yaxis=dict(range=[-1, 1], showgrid=False, zeroline=False, showticklabels=False),
        height=250,
        template="plotly_dark",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

if start_button:
    # Kuantum hesaplama hazırlığı (Hadamard)
    H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
    psi = np.zeros((2 * steps + 1, 2), dtype=complex)
    psi[steps, 0] = 1/np.sqrt(2)
    psi[steps, 1] = 1j/np.sqrt(2)
    
    # Klasik için başlangıç
    pos_c = np.array([steps]) # Başlangıç noktası (merkez)
    
    for t in range(1, steps + 1):
        # --- KLASİK ADIM --- (Sarhoş yürüyüşü)
        from scipy.stats import binom
        x_c = np.arange(-steps, steps + 1)
        y_c = np.array([binom.pmf((steps + i)//2, t, 0.5) if (t + i) % 2 == 0 else 0 for i in x_c])
        
        # --- KUANTUM ADIM --- (Girişim)
        new_psi = np.zeros_like(psi)
        for j in range(len(psi)):
            if abs(psi[j,0]) > 0 or abs(psi[j,1]) > 0:
                coin = H @ psi[j]
                if j > 0: new_psi[j-1, 0] += coin[0]
                if j < len(psi) - 1: new_psi[j+1, 1] += coin[1]
        psi = new_psi
        y_q = np.sum(np.abs(psi)**2, axis=1)
        x_q = np.arange(-steps, steps + 1)

        # GÖRSELLEŞTİRME GÜNCELLEME
        classic_area.plotly_chart(render_experiment(x_c, y_c, "🟠 KLASİK DENEY: Parçacık merkezde hapsoluyor", "#FFA500"), use_container_width=True)
        quantum_area.plotly_chart(render_experiment(x_q, y_q, "🔵 KUANTUM DENEY: Parçacık dalga gibi iki yöne fırlıyor", "#00FFFF"), use_container_width=True)
        
        time.sleep(speed)

st.markdown("""
---
### 🧪 Neyi Gözlemliyoruz?
1.  **Klasik Parçacık (Turuncu):** Tek bir varlık gibi davranır. Sağa sola zıplasa da zamanla hep orta bölgede (0 civarı) bir yığın oluşturur.
2.  **Kuantum Parçacığı (Mavi):** Tek bir top gibi değil, bir **sis bulutu** gibi hareket eder. Bazı yerlerde sönümlenir (girişim), bazı yerlerde devleşir ve merkezin aksine uçlara doğru "ışınlanır" gibi yayılır.
""")
