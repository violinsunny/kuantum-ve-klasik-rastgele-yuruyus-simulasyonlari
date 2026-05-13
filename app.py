import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Görsel Kuantum Yürüyüş", layout="centered")

st.title("🪙 Para Atma ve Kuantum Yayılımı")
st.write("Klasik dünyada para tektir, kuantumda ise para bir buluttur.")

# Yan Menü
steps_limit = st.sidebar.slider("Adım Sayısı", 5, 30, 15)
speed = st.sidebar.slider("Hız", 0.1, 1.0, 0.5)

if st.sidebar.button("Simülasyonu Başlat"):
    # Başlangıç Değerleri
    c_pos = 0
    q_probs = np.zeros(2 * steps_limit + 1)
    q_probs[steps_limit] = 1.0
    
    # Kuantum hesaplama için matris hazırlığı
    size = 2 * steps_limit + 1
    q_state = np.zeros((2, size), dtype=complex)
    q_state[0, steps_limit] = 1/np.sqrt(2)
    q_state[1, steps_limit] = 1j/np.sqrt(2)
    H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])

    # Görselleştirme Alanı
    display_area = st.empty()

    for t in range(steps_limit):
        # --- KLASİK MANTIK ---
        coin_flip = np.random.choice(["YAZI", "TURA"])
        move = 1 if coin_flip == "YAZI" else -1
        c_pos += move

        # --- KUANTUM MANTIK ---
        # Hadamard ve Kaydırma
        for i in range(size):
            q_state[:, i] = np.dot(H, q_state[:, i])
        new_q = np.zeros_like(q_state)
        new_q[0, :-1] = q_state[0, 1:]
        new_q[1, 1:] = q_state[1, :-1]
        q_state = new_q
        q_probs = np.abs(q_state[0, :])**2 + np.abs(q_state[1, :])**2

        # --- GÖRSEL ÇİZİM (MATPLOTLIB AMA İKONLARLA) ---
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), facecolor='#f0f2f6')
        
        # 1. KLASİK ALAN
        ax1.set_facecolor('#ffffff')
        ax1.set_xlim(-steps_limit-1, steps_limit+1)
        ax1.set_ylim(-1, 2)
        ax1.set_title(f"KLASİK: Para {coin_flip} geldi!", fontsize=14, fontweight='bold')
        
        # Para İkonu
        ax1.text(0, 1.2, "🪙", fontsize=40, ha='center') 
        # Yürüyen Adam İkonu
        ax1.text(c_pos, 0, "🚶", fontsize=35, ha='center')
        ax1.axhline(0, color='black', lw=1, alpha=0.3)
        ax1.set_xticks(range(-steps_limit, steps_limit + 1))

        # 2. KUANTUM ALAN
        ax2.set_facecolor('#e3f2fd')
        ax2.set_xlim(-steps_limit-1, steps_limit+1)
        ax2.set_ylim(0, 0.5)
        ax2.set_title("KUANTUM: Para süperpozisyonda (Her iki yöne yayılım)", fontsize=14, fontweight='bold')
        
        # Kuantum Para İkonu (Bulanık/Süperpoze)
        ax2.text(0, 0.4, "🌀", fontsize=40, ha='center', alpha=0.6)
        
        # Olasılık Dalgalarını Görsel Nesneler Olarak Çiz
        for idx, prob in enumerate(q_probs):
            if prob > 0.01:
                # Olasılığa göre boyutu değişen mavi halkalar
                ax2.scatter(idx - steps_limit, 0.1, s=prob*5000, color='#1E88E5', alpha=0.5, edgecolor='blue')
                ax2.text(idx - steps_limit, 0.2, "👻", fontsize=15, ha='center', alpha=prob*2)

        display_area.pyplot(fig)
        plt.close(fig)
        time.sleep(speed)

    st.balloons()
else:
    st.info("Simülasyonu başlatmak için butona bas. Klasik dünyada '🚶' göreceksin, kuantumda ise her yere yayılan '👻' hayaletleri!")
