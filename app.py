import streamlit as st
import pandas as pd

st.set_page_config(page_title="SPK Judul Skripsi", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    .main-title {
        font-size: 2.8rem;
        color: #1E88E5;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #616161;
        text-align: center;
        margin-bottom: 40px;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-size: 18px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1565C0;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# 3. SIDEBAR (Menu di samping kiri)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2941/2941120.png", width=120)
    st.header("⚙️ Panel Admin")
    st.write("Sistem Pendukung Keputusan Penentuan Judul Skripsi Teknik Informatika.")
    st.divider()
    st.info("💡 **Metode SAW**\nSistem ini menghitung nilai akademik dan membandingkannya dengan kriteria setiap bidang skripsi secara otomatis.")
    st.caption("© 2026 - TI Unpam")

# 4. HEADER WEB
st.markdown('<p class="main-title">🎓 Sistem Rekomendasi Judul Skripsi</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Penyelamat Mahasiswa Galau! Temukan topik skripsi paling pas berdasarkan nilai akademis kamu.</p>', unsafe_allow_html=True)

# 5. DATA DUMMY JUDUL (Ini nanti diganti dari Database)
data_topik = {
    'Topik Skripsi': ['Sistem Pakar / AI', 'Sistem Informasi Web', 'Jaringan Komputer / IoT', 'Data Science / Data Analyst'],
    'Min_AI': [85, 60, 60, 80],       
    'Min_Web': [60, 85, 60, 70],      
    'Min_Jaringan': [60, 60, 85, 60]  
}
df_topik = pd.DataFrame(data_topik)

# 6. FORM INPUT (Dibikin menyamping biar rapi)
st.markdown("### 📝 Masukkan Nilai Mata Kuliah Kamu")
st.write("Silakan isi nilai mata kuliah di bawah ini dari skala 0 - 100.")

# Membagi layar jadi 3 kolom
col1, col2, col3 = st.columns(3)

with col1:
    nilai_ai = st.number_input("🤖 Kecerdasan Buatan (AI)", min_value=0, max_value=100, value=75)
with col2:
    nilai_web = st.number_input("🌐 Pemrograman Web", min_value=0, max_value=100, value=75)
with col3:
    nilai_jaringan = st.number_input("📡 Jaringan Komputer", min_value=0, max_value=100, value=75)

st.write("") # Spasi kosong

# 7. TOMBOL PROSES (Penuh satu layar)
if st.button("🚀 Analisis Rekomendasi Judul", use_container_width=True):
    
    with st.spinner('Memproses algoritma Simple Additive Weighting (SAW)...'):
        
        # LOGIKA PERHITUNGAN SAW
        skor_akhir = []
        for index, row in df_topik.iterrows():
            # Bobot: AI 40%, Web 30%, Jaringan 30%
            skor = (
                ((nilai_ai / row['Min_AI']) * 0.4) +
                ((nilai_web / row['Min_Web']) * 0.3) +
                ((nilai_jaringan / row['Min_Jaringan']) * 0.3)
            ) * 100 
            
            # Batasi maksimal 100%
            skor = min(skor, 100.0)
            skor_akhir.append(round(skor, 2))
            
        df_topik['Skor Kecocokan (%)'] = skor_akhir
        df_hasil = df_topik[['Topik Skripsi', 'Skor Kecocokan (%)']].sort_values(by='Skor Kecocokan (%)', ascending=False)
        df_hasil.insert(0, 'Ranking', range(1, 1 + len(df_hasil)))
        
    # 8. TAMPILAN HASIL (Desain Dashboard)
    st.divider()
    st.success("🎉 Analisis Selesai! Berikut adalah rekomendasi terbaik untukmu:")
    
    res_col1, res_col2 = st.columns([1, 2]) # Kolom kiri kecil, kolom kanan besar
    
    # Kolom kiri: Menampilkan Juara 1 nya
    with res_col1:
        top_judul = df_hasil.iloc[0]['Topik Skripsi']
        top_skor = df_hasil.iloc[0]['Skor Kecocokan (%)']
        
        st.metric(label="🏆 Top Rekomendasi", value=top_judul, delta=f"{top_skor}% Cocok", delta_color="normal")
        st.info("Disarankan kamu segera menemui dosen pembimbing di bidang ini.")
        
    # Kolom kanan: Menampilkan Tabel lengkapnya
    with res_col2:
        # Menampilkan tabel interaktif yang warnanya disesuaikan
        st.dataframe(
            df_hasil.style.background_gradient(cmap='Blues', subset=['Skor Kecocokan (%)']),
            hide_index=True, 
            use_container_width=True
        )