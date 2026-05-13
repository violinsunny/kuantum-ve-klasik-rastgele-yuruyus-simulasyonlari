import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Sayfa yapılandırması
st.set_page_config(page_title="Kuantum vs Klasik Rastgele Yürüyüş", layout="wide")

def classical_walk(steps):
    size = 2 * steps + 1
    positions = np.zeros(size)
    positions[steps] = 1.0
    for _ in range(steps):
        new_positions = np.zeros_like(positions)
        for i in range(1, size - 1):
            if positions[i] > 0:
                new_positions[i-1] += positions[i] * 0.5
                new_positions[i+1] += positions[i] * 0.5
        positions = new_positions
    return positions

def quantum_walk(steps):
    size = 2 * steps + 1
    state = np.zeros((2, size), dtype=complex)
    # Simetrik başlangıç durumu
    state[0, steps] = 1 / np.sqrt(2)
    state[1, steps] = 1j / np.sqrt(2)
    
    H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    
    for _ in range(steps):
        # Coin Toss
        new_state = np.zeros_like(state)
        for i in range(size):
            res = H @ state[:, i]
            new_state[0, i] = res[0]
            new_state[1, i] = res[1]
        # Shift
        final_state = np.zeros_like(new_state)
        final_state[0, :-1] = new_state[0, 1:]
        final_state[1, 1:] = new_state[1, :-1]
        state = final_state
        
    return np.abs(state[0, :])**2 + np.abs(state[1, :])**2

# --- Arayüz (UI) Tasarımı ---
st.title("🚶‍♂️ Rastgele Yürüyüş Simülasyonu")
st.markdown("""
Klasik ve Kuantum rastgele yürüyüş arasındaki temel farkı gözlemleyin. 
**Klasik** yürüyüşte olasılık merkezde toplanırken, **Kuantum** yürüyüşünde girişim (interference) nedeniyle olasılık uçlara yayılır.
""")

with st.sidebar:
    st.header("Parametreler")
    steps = st.slider("Adım Sayısı", min_value=10, max_value=200, value=50, step=10)
    show_classical = st.checkbox("Klasik Yürüyüşü Göster", value=True)
    show_quantum = st.checkbox("Kuantum Yürüyüşü Göster", value=True)

# Hesaplamalar
x = np.arange(-steps, steps + 1)
c_probs = classical_walk(steps)
q_probs = quantum_walk(steps)

# Grafik Oluşturma
fig, ax = plt.subplots(figsize=(10, 5))

if show_classical:
    ax.plot(x, c_probs, label='Klasik (Normal Dağılım)', color='gray', linestyle='--', alpha=0.7)
    ax.fill_between(x, c_probs, color='gray', alpha=0.1)

if show_quantum:
    ax.plot(x, q_probs, label='Kuantum (Ballistic Yayılım)', color='#00d1b2', linewidth=2)
    ax.fill_between(x, q_probs, color='#00d1b2', alpha=0.2)

ax.set_title(f"{steps} Adım Sonundaki Durum")
ax.set_xlabel("Pozisyon")
ax.set_ylabel("Olasılık")
ax.legend()
ax.grid(True, which='both', linestyle='--', alpha=0.5)

st.pyplot(fig)

# Bilgi Notu
st.info(f"💡 Kuantum yürüyüşü klasik yürüyüşe göre yaklaşık **{steps} kat** daha geniş bir alana yayılmıştır. Bu özellik, kuantum arama algoritmalarının temelini oluşturur.")
