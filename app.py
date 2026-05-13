import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Parametreler ---
STEPS = 40
size = 2 * STEPS + 1
x = np.arange(-STEPS, STEPS + 1)

# --- Kuantum Yürüyüş Hazırlığı ---
# Başlangıç durumu: Merkezde, süperpozisyon halinde bir 'para'
q_state = np.zeros((2, size), dtype=complex)
q_state[0, STEPS] = 1 / np.sqrt(2)
q_state[1, STEPS] = 1j / np.sqrt(2)
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])

# --- Klasik Yürüyüş Hazırlığı ---
c_pos = STEPS  # Başlangıç indeksi (0 noktası)
c_history = np.zeros(size)
c_history[c_pos] = 1

# --- Görselleştirme Hazırlığı ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
plt.subplots_adjust(hspace=0.4)

# Klasik Grafik Ayarları
ax1.set_xlim(-STEPS, STEPS)
ax1.set_ylim(0, 1.1)
ax1.set_title("Klasik Rastgele Yürüyüş (Tek Bir Kesin Nokta)")
classic_point, = ax1.plot([], [], 'ro', ms=10, label="Parçacık")
classic_bar = ax1.bar(x, np.zeros(size), color='red', alpha=0.3)

# Kuantum Grafik Ayarları
ax2.set_xlim(-STEPS, STEPS)
ax2.set_ylim(0, 0.2) # Olasılıklar yayıldığı için limit daha düşük
ax2.set_title("Kuantum Rastgele Yürüyüş (Süperpozisyon ve Girişim)")
quantum_line, = ax2.plot([], [], color='#1E88E5', lw=2, label="Olasılık Dalgası")
quantum_fill = ax2.fill_between(x, 0, 0, color='#1E88E5', alpha=0.3)

def animate(frame):
    global q_state, c_pos, quantum_fill
    
    if frame == 0: return classic_point, quantum_line

    # 1. Klasik Adım: Yazı/Tura at ve hareket et
    move = np.random.choice([-1, 1])
    c_pos += move
    
    # 2. Kuantum Adımı: Hadamard + Shift
    new_q_state = np.zeros_like(q_state)
    # Hadamard (Para atışı)
    for i in range(size):
        q_state[:, i] = np.dot(H, q_state[:, i])
    # Shift (Hareket)
    new_q_state[0, :-1] = q_state[0, 1:]
    new_q_state[1, 1:] = q_state[1, :-1]
    q_state = new_q_state
    
    # Kuantum olasılık hesapla
    q_probs = np.abs(q_state[0, :])**2 + np.abs(q_state[1, :])**2

    # --- Güncelleme ---
    # Klasik nokta güncelleme
    classic_point.set_data([c_pos - STEPS], [0.5])
    
    # Kuantum çizgi ve dolgu güncelleme
    quantum_line.set_data(x, q_probs)
    # Dolgu efektini güncellemek için eskiyi silip yeniyi ekliyoruz
    ax2.collections.clear()
    quantum_fill = ax2.fill_between(x, 0, q_probs, color='#1E88E5', alpha=0.3)

    return classic_point, quantum_line

ani = FuncAnimation(fig, animate, frames=STEPS, interval=200, blit=False, repeat=False)
plt.show()
