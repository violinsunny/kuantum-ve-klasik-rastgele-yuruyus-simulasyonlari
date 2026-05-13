import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def classic_random_walk(steps):
    positions = np.arange(-steps, steps + 1)
    probs = np.zeros(len(positions))
    # Binom dağılımı klasik yürüyüşün sonucudur
    from scipy.stats import binom
    for i, pos in enumerate(positions):
        if (steps + pos) % 2 == 0:
            probs[i] = binom.pmf((steps + pos) // 2, steps, 0.5)
    return positions, probs

def quantum_random_walk(steps):
    # Başlangıç durumu: |0> konumu ve spin yukarı/aşağı süperpozisyonu
    size = 2 * steps + 1
    state = np.zeros((size, 2), dtype=complex)
    state[steps, 0] = 1/np.sqrt(2)
    state[steps, 1] = 1j/np.sqrt(2)

    # Hadamard Operatörü
    H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)

    for _ in range(steps):
        # 1. Paratlacık (Coin) Adımı: Hadamard uygula
        new_state = np.zeros_like(state)
        for i in range(size):
            state[i] = np.dot(H, state[i])
        
        # 2. Kaydırma (Shift) Adımı
        for i in range(size):
            if i > 0:
                new_state[i-1, 0] += state[i, 0] # Sola kaydır
            if i < size - 1:
                new_state[i+1, 1] += state[i, 1] # Sağa kaydır
        state = new_state

    probabilities = np.abs(state[:, 0])**2 + np.abs(state[:, 1])**2
    return np.arange(-steps, steps + 1), probabilities

# Streamlit Arayüzü
st.set_page_config(page_title="QRW vs CRW Visualizer", layout="wide")
st.title("🚶‍♂️ Rastgele Yürüyüşler: Kuantum vs Klasik")

st.sidebar.header("Parametreler")
steps = st.sidebar.slider("Adım Sayısı (N)", min_value=10, max_value=200, value=50)

col1, col2 = st.columns(2)

# Hesaplamalar
pos_c, prob_c = classic_random_walk(steps)
pos_q, prob_q = quantum_random_walk(steps)

with col1:
    st.subheader("Klasik Rastgele Yürüyüş (CRW)")
    fig_c, ax_c = plt.subplots()
    ax_c.bar(pos_c, prob_c, color='gray', alpha=0.7)
    ax_c.set_title(f"Gauss Dağılımı ({steps} Adım)")
    ax_c.set_xlabel("Konum")
    ax_c.set_ylabel("Olasılık")
    st.pyplot(fig_c)
    st.info("Klasik yürüyüşte parçacık merkezde toplanma eğilimindedir.")

with col2:
    st.subheader("Kuantum Rastgele Yürüyüş (QRW)")
    fig_q, ax_q = plt.subplots()
    ax_q.plot(pos_q, prob_q, color='#00FFAA', linewidth=2)
    ax_q.fill_between(pos_q, prob_q, color='#00FFAA', alpha=0.3)
    ax_q.set_title(f"Kuantum Yayılımı ({steps} Adım)")
    ax_q.set_xlabel("Konum")
    ax_q.set_ylabel("Olasılık")
    st.pyplot(fig_q)
    st.success("Kuantum yürüyüşünde 'girişim' nedeniyle uçlara doğru hızlı bir yayılım görülür.")

st.divider()
st.markdown(f"""
### Temel Farklar:
*   **Hız:** Klasik yürüyüşte yayılım $O(\sqrt{N})$ iken, Kuantumda $O(N)$'dir. 
*   **Şekil:** Klasik dağılım bir **Çan Eğrisi (Normal Dağılım)** oluşturur. Kuantum dağılımı ise uçlarda yüksek zirveler yapan asimetrik veya balistik bir yapı sunar.
""")
