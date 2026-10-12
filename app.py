import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Tiêu đề ứng dụng
st.title('QUẢN LÝ ĐIỂM SINH VIÊN')

# Dữ liệu và tính toán
data = {
    'Họ và tên': [
        'An',
        'Bình',
        'Chi',
        'Dũng',
        'Hà',
        'Lan',
        'Minh',
        'Nam',
        'Phúc',
        'Trang',
    ],
    'Chuyên cần': [8.0, 9.0, 7.5, 8.5, 6.0, 7.0, 9.5, 6.5, 8.0, 9.0],
    'Giữa kỳ': [7.0, 8.0, 6.5, 7.5, 5.0, 6.5, 8.5, 6.0, 7.5, 8.0],
    'Cuối kỳ': [7.5, 8.5, 7.0, 8.0, 5.5, 6.0, 9.0, 6.5, 8.0, 8.5],
}
df = pd.DataFrame(data)

df['Tong_ket'] = (
    df['Chuyên cần'] * 0.2 + df['Giữa kỳ'] * 0.3 + df['Cuối kỳ'] * 0.5
)
df['Tong_ket'] = df['Tong_ket'].round(2)


def xep_loai(dtk):
  if dtk >= 8.5:
    return 'Giỏi'
  elif dtk >= 7.0:
    return 'Khá'
  elif dtk >= 5.0:
    return 'Trung bình'
  else:
    return 'Yếu'


df['Xep_loai'] = df['Tong_ket'].apply(xep_loai)

# 1. Hiển thị bảng điểm tổng hợp
st.subheader('Bảng điểm tổng hợp của 10 sinh viên')
st.dataframe(df, use_container_width=True)

# 2. Thống kê lớp học
st.subheader('Thống kê lớp học')
dtb_lop = df['Tong_ket'].mean()
max_sv = df.loc[df['Tong_ket'].idxmax()]
min_sv = df.loc[df['Tong_ket'].idxmin()]
so_sv_dat = (df['Tong_ket'] >= 5.0).sum()

st.write(f'- **Điểm tổng kết trung bình của lớp:** `{dtb_lop:.2f}`')
st.write(
    f'- **Sinh viên điểm tổng kết cao nhất:** `{max_sv["Họ y tên"] if "Họ y tên" in max_sv else max_sv["Họ và tên"]}`'
    f' ({max_sv["Tong_ket"]})'
)
st.write(
    f'- **Sinh viên điểm tổng kết thấp nhất:** `{min_sv["Họ và tên"]}`'
    f' ({min_sv["Tong_ket"]})'
)
st.write(f'- **Số sinh viên đạt (>= 5.0):** `{so_sv_dat}`')

# 3. Tra cứu chi tiết theo sinh viên (Selectbox)
st.subheader('Tra cứu chi tiết theo sinh viên')
selected_name = st.selectbox('Chọn tên sinh viên:', df['Họ và tên'].values)
selected_row = df[df['Họ và tên'] == selected_name].iloc[0]

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric('Chuyên cần', selected_row['Chuyên cần'])
col2.metric('Giữa kỳ', selected_row['Giữa kỳ'])
col3.metric('Cuối kỳ', selected_row['Cuối kỳ'])
col4.metric('Tổng kết', selected_row['Tong_ket'])
col5.metric('Xếp loại', selected_row['Xep_loai'])

# 4. Biểu đồ cột điểm tổng kết
st.subheader('Biểu đồ cột điểm tổng kết')
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(df['Họ và tên'], df['Tong_ket'], color='skyblue')
ax.set_xlabel('Họ và tên sinh viên')
ax.set_ylabel('Điểm tổng kết')
ax.set_title('Biểu đồ điểm tổng kết của 10 sinh viên')
ax.set_ylim(0, 10)
st.pyplot(fig)

# 5. Hiển thị họ tên và MSSV ở cuối trang
st.markdown('---')
st.markdown(
    '<p style="text-align: center; color: gray; font-size: 12px;">Họ và tên:'
    ' [Họ tên của bạn] - MSSV: [MSSV của bạn]</p>',
    unsafe_allow_html=True,
)