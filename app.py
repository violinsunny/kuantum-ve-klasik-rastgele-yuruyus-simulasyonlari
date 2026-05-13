import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Canlı Kuantum Yürüyüş", layout="wide")

st.title("🎲 Klasik vs Kuantum: Adım Adım Simülasyon")
st.sidebar.header("Ayarlar")
steps_limit = st.sidebar.slider("Toplam Adım", 10, 100, 40)
speed = st.sidebar.slider("Simülasyon Hızı", 0.01, 0.5, 0.1)

if st.sidebar.button("Simülasyonu Başlat"):
    # Hazırlık
    size = 2 * steps_limit + 1
    x = np.arange(-steps_limit, steps_limit + 1)
    
    # Kuantum Durumu
    q_state = np.zeros((2, size), dtype=complex)
    q_state[0, steps_limit] = 1 / np.sqrt(2)
    q_state[1, steps_limit] = 1j / np.sqrt(2)
    H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])
    
    # Klasik Durum
    c_pos = steps_limit
    
    # Görselleştirme alanı
    plot_spot = st.empty()

    for t in range(steps_limit):
        # --- KLASİK HESAP ---
        c_pos += np.random.choice([-1, 1])
        
        # --- KUANTUM HESAP ---
        # Para Atışı (Hadamard)
        for i in range(size):
            q_state[:, i] = np.dot(H, q_state[:, i])
        # Hareket (Shift)
        new_q = np.zeros_like(q_state)
        new_q[0, :-1] = q_state[0, 1:]
        new_q[1, 1:] = q_state[1, :-1]
        q_state = new_q
        
        q_probs = np.abs(q_state[0, :])**2 + np.abs(q_state[1, :])**2

        # --- ÇİZİM ---
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
        
        # Üst: Klasik (Para Atma Sonucu)
        ax1.set_xlim(-steps_limit, steps_limit)
        ax1.set_ylim(-0.5, 1.5)
        ax1.set_title(f"Adım {t}: Klasik Parçacık (Yazı-Tura)")
        ax1.scatter([c_pos - steps_limit], [0.5], color='red', s=200, label="Şu anki Konum")
        ax1.axvline(0, color='black', alpha=0.2, linestyle='--')
        ax1.legend()

        # Alt: Kuantum (Süperpozisyon)
        ax2.set_xlim(-steps_limit, steps_limit)
        ax2.set_ylim(0, 0.3)
        ax2.set_title(f"Adım {t}: Kuantum Dalga Fonksiyonu (Süperpozisyon)")
        ax2.plot(x, q_probs, color='#1E88E5', lw=2)
        ax2.fill_between(x, 0, q_probs, color='#1E88E5', alpha=0.3)
        
        # Grafiği ekrana bas
        plot_spot.pyplot(fig)
        plt.close(fig) # Belleği temizle
        
        time.sleep(speed)

else:
    st.info("Simülasyonu başlatmak için sol paneldeki butona tıklayın.")
