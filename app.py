import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

# Sayfa yapılandırması
st.set_page_config(page_title="Kuantum vs Klasik Rastgele Yürüyüş", layout="wide")

st.title("🚶‍♂️ Rastgele Yürüyüş Simülasyonu")
st.markdown("""
Bu uygulama, **Klasik Rastgele Yürüyüş** (Yazı-Tura) ile **Kuantum Rastgele Yürüyüş** arasındaki farkı görselleştirir.
Kuantum yürüyüşlerdeki 'boynuz' şeklindeki yayılımın, klasik 'çan eğrisi'nden ne kadar farklı olduğuna dikkat edin.
""")

# Yan panel kontrolleri
st.sidebar.header("Parametreler")
steps = st.sidebar.slider("Adım Sayısı (Steps)", min_value=10, max_value=200, value=100)

def run_quantum_walk(steps):
    size = 2 * steps + 1
    pos = np.zeros((2, size), dtype=complex)
    
    # Başlangıç durumu (Süperpozisyon)
    pos[0, steps] = 1 / np.sqrt(2)
    pos[1, steps] = 1j / np.sqrt(2)

    # Hadamard Operatörü
    H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])

    for _ in range(steps):
        # Para atışı (Coin flip)
        temp_pos = np.zeros_like(pos)
        for i in range(size):
            pos[:, i] = np.dot(H, pos[:, i])
            
        # Hareket (Shift)
        temp_pos[0, :-1] = pos[0, 1:]
        temp_pos[1, 1:] = pos[1, :-1]
        pos = temp_pos

    return np.abs(pos[0, :])**2 + np.abs(pos[1, :])**2

def run_classic_walk(steps):
    k = np.arange(0, steps + 1)
    probs_raw = binom.pmf(k, steps, 0.5)
    
    x_classic = 2 * k - steps
    full_x = np.arange(-steps, steps + 1)
    full_probs = np.zeros(len(full_x))
    
    # İndis eşleme
    indices = x_classic + steps
    full_probs[indices] = probs_raw
    return full_probs

# Hesaplamaları yap
x_axis = np.arange(-steps, steps + 1)
q_probs = run_quantum_walk(steps)
c_probs = run_classic_walk(steps)

# Görselleştirme
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x_axis, q_probs, label='Kuantum Yürüyüş', color='#1E88E5', lw=2)
ax.fill_between(x_axis, q_probs, color='#1E88E5', alpha=0.2)

ax.plot(x_axis, c_probs, label='Klasik Yürüyüş', color='#D81B60', lw=2, linestyle='--')
ax.fill_between(x_axis, c_probs, color='#D81B60', alpha=0.1)

ax.set_title(f"{steps} Adım Sonunda Olasılık Dağılımı")
ax.set_xlabel("Konum")
ax.set_ylabel("Bulunma Olasılığı")
ax.legend()
ax.grid(axis='y', alpha=0.3)

st.pyplot(fig)

# Bilgi kutuları
col1, col2
