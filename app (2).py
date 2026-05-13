import streamlit as st
import numpy as np
import time

# Sayfa Ayarları
st.set_page_config(page_title="Kuantum Rastgele Yürüyüş Analizi", layout="wide")

# Görsel Stil Ayarları
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button {
        background-color: #00d4ff;
        color: black;
        border-radius: 12px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("Kuantum ve Klasik Rastgele Yürüyüş Simülasyonları")
st.write("Sistemlerin evrimini 'olasılık dağılımı' ve 'dalga fonksiyonu' üzerinden analiz edin.")

col1, col2 = st.columns(2)

with col1:
    st.header("1) Klasik Yürüyüş")
    st.write("Sistem, her adımda **belirli** bir durumdadır.")
    steps_c = st.slider("İterasyon Sayısı (K)", 5, 30, 15)

    if st.button("Klasik Deneyi Başlat"):
        pos = 0
        display_area = st.empty()
        for i in range(steps_c):
            # Rastgele seçim: Bağımsız olaylar toplama ilkesi
            coin = np.random.choice([-1, 1])
            pos += coin

            viz = "".join(["🔴 " if j == pos else "▫️ " for j in range(-steps_c, steps_c + 1)])
            display_area.subheader(viz)
            time.sleep(0.2)
        st.success(f"Sistem Kararlı Durumu: Konum {pos}")

with col2:
    st.header("2) Kuantum Yürüyüşü")
    st.write("Sistem, durumların **süperpozisyonu** olarak evrilir.")
    steps_q = st.slider("İterasyon Sayısı (Q)", 5, 30, 15)

    if st.button("Kuantum Evrimini Başlat"):
        size = 2 * steps_q + 1
        # Başlangıç durumu (State Vector)
        state = np.zeros(size, dtype=complex)
        state[steps_q] = 1.0

        display_area_q = st.empty()

        for i in range(steps_q):
            # Kuantum yayılımı: Her konum bir dalga fonksiyonu genliği taşır
            new_state = np.zeros_like(state)
            for j in range(1, size-1):
                if abs(state[j]) > 0:
                    # Schrödinger benzeri yayılım: Faz korunumu ile her iki yöne geçiş
                    new_state[j-1] += state[j] * (1/np.sqrt(2))
                    new_state[j+1] += state[j] * (1j/np.sqrt(2)) # i fazı (hayali birim) ekleyerek girişim yaratılır

            state = new_state / np.linalg.norm(new_state) # Üniter koruma
            probs = np.abs(state)**2

            viz_q = "".join(["🔵 " if p > 0.05 else "🔹 " if p > 0.005 else "▫️ " for p in probs])
            display_area_q.subheader(viz_q)
            time.sleep(0.2)
        st.info("Sistem Koherent Durumu: Yayılım ve Girişim gözlemlendi.")

st.markdown("---")

# Orta Düzey Akademik Açıklama Paneli
st.markdown("""
### 🧠 Sistemsel Karşılaştırma ve Mekanikler

#### **Klasik Stokastik Süreç (Bernoulli)**
Klasik rastgele yürüyüşte sistem, **Merkezi Limit Teoremi**'ne göre hareket eder. Her adım bir önceki adımdan bağımsızdır.
*   **İstatistik:** Birçok deneme yapıldığında sonuçlar merkezde toplanarak bir **Gauss (Çan) eğrisi** oluşturur.
*   **Bilgi:** Parçacığın konumu her zaman kesin olarak tanımlıdır (Lokalite).

#### **Kuantum Üniter Evrim (Hadamard)**
Kuantum rastgele yürüyüşü, klasik olandan farklı olarak **Girişim (Interference)** fenomenine dayanır.
*   **Süperpozisyon:** Parçacık sadece sağa veya sola gitmez; her iki olasılık genliğini de aynı anda taşır. Animasyondaki mavi 'bulut' yayılımı, parçacığın **Dalga Fonksiyonu**'nun genişlemesini temsil eder.
*   **Girişim:** Farklı yollardan gelen olasılık genlikleri birbirini yok edebilir (yıkıcı) veya güçlendirebilir (yapıcı). Bu yüzden kuantum parçacığı klasik olandan **çok daha hızlı** bir şekilde uç noktalara yayılır.
*   **Hız:** Klasik yürüyüşte konum $ \sqrt{t} $ ile yayılırken, kuantum yürüyüşünde konum doğrudan $ t $ süresiyle orantılı yayılır.

> **Sonuç:** Klasik dünya bir 'nokta' takibiyken, kuantum dünyası bir 'dalga' dinamiğidir.
""")
