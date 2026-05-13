%%writefile app.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import binom

# Sayfa Genişliği ve Tasarımı
st.set_page_config(page_title="Rastgele Yürüyüş Deneyi", layout="wide")

# --- CSS: Şık Görünüm ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- BAŞLIK VE GİRİŞ ---
st.title("🔬 Rastgele Yürüyüş Deneyi: Somut Bir Görselleştirme")
st.markdown("""
Bu simülasyon, bir parçacığın (makro dünyada bir insan veya atom altı seviyede bir kuantum parçacığı) hareketini somut bir görsel deney olarak sunar.
Bu deneyde, "rastgeleliğin" klasik ve kuantum dünyalarında nasıl farklı sonuçlar doğurduğunu gözlemleyebilirsiniz.
""")

# --- YAN MENÜ (KONTROL PANELİ) ---
with st.sidebar:
    st.header("⚙️ Deney Parametreleri")
    steps = st.slider("Adım Sayısı (Zaman)", min_value=10, max_value=200, value=100)
    st.info("Adım sayısını artırarak klasik ve kuantum arasındaki farkın nasıl derinleştiğini gözlemleyebilirsiniz.")

# --- ANALİZ VE HESAPLAMA ---
def get_data(steps):
    x = np.arange(-steps, steps + 1)
    
    # 1. Klasik Yürüyüş (Binom/Normal Dağılım)
    y_classic = np.zeros(len(x))
    for i, pos in enumerate(x):
        if (steps + pos) % 2 == 0:
            y_classic[i] = binom.pmf((steps + pos) // 2, steps, 0.5)
            
    # 2. Kuantum Yürüyüş (Hadamard Walk)
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

# --- SOMUT GÖRSEL DENEY ---
st.subheader("📊 Rastgele Yürüyüş Deneyi")

# Klasik Yürüyüş Deneyimi
st.markdown("### 🟠 Klasik Yürüyüş Deneyi")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
        Bu deneyde, bir insan gözleri kapalı bir şekilde düz bir çizgide ilerler. Her adımda yazı-tura atar.
        Yazı gelirse sağa, tura gelirse sola gider.
    """)
with col2:
    fig_classic = go.Figure()
    fig_classic.add_trace(go.Bar(
        x=x, y=y_c,
        name="Klasik (Sarhoş Yürüyüşü)",
        marker_color='#FFA500',
        opacity=0.6
    ))
    fig_classic.update_layout(
        template="plotly_dark",
        xaxis=dict(title="Konum", range=[-steps, steps]),
        yaxis=dict(title="Parçacığın Orada Bulunma İhtimali"),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_classic, use_container_width=True)

# Kuantum Yürüyüş Deneyimi
st.markdown("### 🔵 Kuantum Yürüyüş Deneyi")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
        Bu deneyde, bir kuantum parçacığı düz bir çizgide ilerler. Her adımda "süperpozisyon" halindedir; 
        yani aynı anda hem sağa hem sola gider. Bu dalgalar birbirleriyle etkileşime girer.
    """)
with col2:
    fig_quantum = go.Figure()
    fig_quantum.add_trace(go.Scatter(
        x=x, y=y_q,
        name="Kuantum (Dalga Fonksiyonu)",
        line=dict(color='#00FFFF', width=3),
        mode='lines+markers',
        fill='tozeroy'
    ))
    fig_quantum.update_layout(
        template="plotly_dark",
        xaxis=dict(title="Konum", range=[-steps, steps]),
        yaxis=dict(title="Parçacığın Orada Bulunma İhtimali"),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_quantum, use_container_width=True)

# --- BİLGİ KARTLARI (ANALİZ KISMI) ---
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟠 Klasik Analiz")
    st.write("""
    Klasik yürüyüşte, parçacık merkezde toplanma eğilimindedir. Bu bir Normal (Gauss) Dağılımıdır.
    Aynı anda sadece bir konumda bulunabilir.
    """)

with col2:
    st.subheader("🔵 Kuantum Analiz")
    st.write("""
    Kuantum yürüyüşte parçacıklar birbirini yok edebilir veya güçlendirebilir (Girişim).
    Bu yüzden uçlara doğru hızla yayılırlar. Kuantum arama algoritmalarının klasik olanlardan 
    çok daha hızlı olmasının temel sebebi bu yayılma hızıdır ($t$ ile orantılı).
    """)

# --- SOMUTLAŞTIRMA ÖRNEĞİ ---
st.success(f"🔍 **Deney Sonucu:** Şu an {steps} adım attınız. Klasik parçacık hala merkeze yakınken, Kuantum parçacığı çoktan {int(steps*0.7)} birim uzağa ulaşma şansını yakaladı!")
