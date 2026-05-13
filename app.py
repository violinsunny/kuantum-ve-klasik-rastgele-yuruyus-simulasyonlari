%%writefile app.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import binom

# Sayfa Genişliği ve Tasarımı
st.set_page_config(page_title="Kuantum Rastgele Yürüyüş Deneyi", layout="wide")

# --- CSS: Daha Şık Bir Görünüm ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_base64=True)

# --- BAŞLIK VE GİRİŞ ---
st.title("🔬 Kuantum ve Klasik Rastgele Yürüyüş Analizi")
st.markdown("""
Bu simülasyon, bir parçacığın (atom altı seviyede veya makro dünyada) hareket mantığını karşılaştırır.
Çifte Yarık Deneyi'nde olduğu gibi, kuantum dünyasında parçacıklar sadece 'yol almaz', aynı zamanda birbiriyle etkileşime girer.
""")

# --- YAN MENÜ (KONTROL PANELİ) ---
with st.sidebar:
    st.header("⚙️ Deney Parametreleri")
    steps = st.slider("Adım Sayısı (Zaman)", min_value=10, max_value=150, value=60)
    st.info("Adım sayısını artırarak kuantum girişiminin (interferans) nasıl karmaşıklaştığını gözlemleyebilirsiniz.")

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

# --- GÖRSEL ANALİZ: SOMUTLAŞTIRILMIŞ GRAFİK ---
st.subheader("📊 Olasılık Yoğunluğu Analizi")

fig = go.Figure()

# Klasik Alan
fig.add_trace(go.Bar(
    x=x, y=y_c,
    name="Klasik (Sarhoş Yürüyüşü)",
    marker_color='#FFA500',
    opacity=0.6
))

# Kuantum Alan
fig.add_trace(go.Scatter(
    x=x, y=y_q,
    name="Kuantum (Dalga Fonksiyonu)",
    line=dict(color='#00FFFF', width=3),
    mode='lines+markers',
    fill='tozeroy'
))

fig.update_layout(
    template="plotly_dark",
    xaxis=dict(title="Konum (Merkezden Uzaklık)", range=[-steps, steps]),
    yaxis=dict(title="Parçacığın Orada Bulunma İhtimali"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# --- BİLGİ KARTLARI (ANALİZ KISMI) ---
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟠 Klasik Analiz")
    st.write("""
    **Örnek:** Sokakta gözü kapalı yürüyen bir insan.
    - **Davranış:** Her adımda yazı-tura atar. Yazı gelirse sağa, tura gelirse sola gider.
    - **Sonuç:** Zamanın çoğunda başladığı yere yakın kalır. 
    - **Matematik:** Dağılım bir **çan eğrisi** (Normal Dağılım) oluşturur. Uç noktalara gitme ihtimali neredeyse sıfırdır.
    """)

with col2:
    st.subheader("🔵 Kuantum Analiz")
    st.write("""
    **Örnek:** Aynı anda her yöne yayılan bir dalga.
    - **Davranış:** Parçacık 'süperpozisyon' halindedir. Yani aynı anda hem sağa hem sola gider.
    - **Girişim:** Dalgalar birbirini bazı noktalarda yok eder, bazı noktalarda güçlendirir.
    - **Sonuç:** Parçacık, merkezin aksine **hızla uçlara yayılır**. Bu, kuantum bilgisayarların veri tarama hızının temelidir.
    """)

# --- SOMUTLAŞTIRMA ÖRNEĞİ ---
st.success(f"🔍 **Analiz Notu:** Şu an {steps} adım attınız. Klasik parçacık hala merkeze yakınken, Kuantum parçacığı çoktan {int(steps*0.7)} birim uzağa ulaşma şansını yakaladı!")
