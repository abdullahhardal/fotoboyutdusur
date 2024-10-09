from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog

def compress_image(input_path, output_path, target_size_kb):
    # Fotoğrafı aç
    img = Image.open(input_path)
    
    # Kaliteyi kademeli olarak azaltarak ve fotoğrafı yeniden boyutlandırarak sıkıştırma işlemi
    quality = 95
    while True:
        # Geçici bir dosyaya fotoğrafı kaydet
        img.save(output_path, 'JPEG', quality=quality)
        
        # Dosya boyutunu kontrol et
        file_size = os.path.getsize(output_path) / 1024  # KB cinsinden
        
        # Dosya boyutu 500 KB'nin altına düştüyse veya kalite çok düşük seviyeye geldiyse döngüden çık
        if file_size <= target_size_kb or quality < 10:
            break
        
        # Kaliteyi azalt
        quality -= 5

    # Yeniden boyutlandırma gerekirse, boyutu kontrol et ve uygula
    if file_size > target_size_kb:
        width, height = img.size
        scaling_factor = (target_size_kb / file_size) ** 0.5
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        img = img.resize(new_size, Image.ANTIALIAS)
        img.save(output_path, 'JPEG', quality=quality)

    print(f"Son boyut: {os.path.getsize(output_path) / 1024:.2f} KB")

# Ana program
def main():
    # Tkinter'i başlat ve dosya seçici aç
    root = tk.Tk()
    root.withdraw()  # Ana pencereyi gizler

    # Kullanıcıdan bir dosya seçmesini iste
    input_image_path = filedialog.askopenfilename(title="Bir resim dosyası seçin", 
                                                  filetypes=[("JPEG Files", "*.jpg;*.jpeg")])
    
    if not input_image_path:
        print("Dosya seçilmedi.")
        return

    # Çıktı dosyasının kaydedileceği yol
    output_image_path = filedialog.asksaveasfilename(defaultextension=".jpg", 
                                                     filetypes=[("JPEG Files", "*.jpg;*.jpeg")],
                                                     title="Sıkıştırılmış resmi kaydetmek için bir yer seçin")
    if not output_image_path:
        print("Çıktı dosyası yolu belirtilmedi.")
        return

    # Sıkıştırma işlemi
    compress_image(input_image_path, output_image_path, 500)

if __name__ == "__main__":
    main()
