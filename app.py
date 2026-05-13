import numpy as np
import matplotlib.pyplot as plt

def quantum_walk(steps):
    # Başlangıç durumu: Konum 0, Para durumu (Süperpozisyon)
    # Konum sayısını adımlara göre belirliyoruz (2*steps + 1)
    size = 2 * steps + 1
    pos = np.zeros((2, size), dtype=complex)
    
    # Başlangıçta 0. konumda (merkezde) başla
    # Karmaşık bir başlangıç durumu simetriyi bozabilir veya sağlayabilir
    pos[0, steps] = 1 / np.sqrt(2)
    pos[1, steps] = 1j / np.sqrt(2)

    # Hadamard Operatörü
    H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])

    for _ in range(steps):
        # 1. Adım: Parayı at (Hadamard uygulayarak süperpozisyon oluştur)
        new_pos = np.zeros_like(pos)
        for i in range(size):
            res = np.dot(H, pos[:, i])
            pos[:, i] = res
            
        # 2. Adım: Hareket (Shift)
        # 0. indis sola (-1), 1. indis sağa (+1) kaydırır
        new_pos[0, :-1] = pos[0, 1:]
        new_pos[1, 1:] = pos[1, :-1]
        pos = new_pos

    # Olasılık yoğunluğunu hesapla (Genliklerin karesi)
    probabilities = np.abs(pos[0, :])**2 + np.abs(pos[1, :])**2
    return probabilities

# Parametreler
N_steps = 100
x = np.arange(-N_steps, N_steps + 1)

# Kuantum hesaplama
quantum_probs = quantum_walk(N_steps)

# Klasik Binom (Normal) Dağılımı (Karşılaştırma için)
from scipy.stats import binom
# Klasik yürüyüşte n adımda k sağa gitme olasılığı
k = np.arange(0, N_steps + 1)
classic_probs_raw = binom.pmf(k, N_steps, 0.5)
classic_x = 2 * k - N_steps
classic_probs = np.zeros(2 * N_steps + 1)
classic_probs[classic_x + N_steps] = classic_probs_raw

# Görselleştirme
plt.figure(figsize=(12, 6))
plt.plot(x, quantum_probs, label='Kuantum Rastgele Yürüyüş', color='blue', linewidth=2)
plt.plot(x, classic_probs, label='Klasik Rastgele Yürüyüş (Çan Eğrisi)', color='red', linestyle='--', alpha=0.7)
plt.title(f"{N_steps} Adım Sonunda Olasılık Dağılımı")
plt.xlabel("Konum")
plt.ylabel("Olasılık")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
