import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

print("   SOTM UYDU HEDEF GİRİŞ PANELİ")
target_az = float(input("Hedef Azimuth (Yatay Dönüş Açısı):"))
target_el = float(input("Hedef Elevation (Yukarı Bakış Açısı): "))

az_rad = np.radians(target_az)
el_rad = np.radians(target_el)
v_sat = np.array([
    np.cos(el_rad) * np.cos(az_rad),  
    np.cos(el_rad) * np.sin(az_rad),  
    np.sin(el_rad)                    
])

fig = plt.figure(figsize=(8, 7))
ax = fig.add_subplot(111, projection='3d')

def update(frame):
    ax.cla()
    
    roll = 15.0 * np.sin(np.radians(frame * 3))
    pitch = 10.0 * np.cos(np.radians(frame * 2))
    yaw = 20.0 * np.sin(np.radians(frame * 1))
    
    r = np.radians(roll)
    p = np.radians(pitch)
    y = np.radians(yaw)
    
    Rx = np.array([[1, 0, 0], [0, np.cos(r), -np.sin(r)], [0, np.sin(r), np.cos(r)]])
    Ry = np.array([[np.cos(p), 0, np.sin(p)], [0, 1, 0], [-np.sin(p), 0, np.cos(p)]])
    Rz = np.array([[np.cos(y), -np.sin(y), 0], [np.sin(y), np.cos(y), 0], [0, 0, 1]])
    R_car = Rz @ Ry @ Rx
    
    plate = np.array([[-0.5, -0.5, 0], [0.5, -0.5, 0], [0.5, 0.5, 0], [-0.5, 0.5, 0], [-0.5, -0.5, 0]])
    rotated_plate = (R_car @ plate.T).T
    ax.plot(rotated_plate[:, 0], rotated_plate[:, 1], rotated_plate[:, 2], 'r-', linewidth=2, label="Araç Tavanı (Sallanan)")
    
    ax.quiver(0, 0, 0, v_sat[0], v_sat[1], v_sat[2], color='blue', linestyle='--', length=1.2, arrow_length_ratio=0.1, label="Sabit Uydu Yönü")
    
    ax.quiver(0, 0, 0, v_sat[0], v_sat[1], v_sat[2], color='green', linewidth=3, length=1.0, arrow_length_ratio=0.15, label="Anten Doğrultusu (Kilitli)")
    
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-0.2, 1.2])
    ax.set_xlabel('Kuzey / Güney')
    ax.set_ylabel('Doğu / Batı')
    ax.set_zlabel('Yükseklik')
    ax.set_title(f"SOTM Stabilizasyon Simülasyonu\nHedef: Az={target_az}°, El={target_el}°\nAraç: Roll={roll:.1f}°, Pitch={pitch:.1f}°, Yaw={yaw:.1f}°")
    ax.legend(loc='upper left')

ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=50)
plt.show()