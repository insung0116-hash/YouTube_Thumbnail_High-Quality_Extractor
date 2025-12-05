# app.py

import streamlit as st
import re
import requests
from io import BytesIO
from PIL import Image

# --- 페이지 설정 ---
st.set_page_config(
    page_title="유튜브 썸네일 추출기",
    page_icon="🎬",
    layout="centered"
)

# --- 제목 및 설명 ---
st.title("🎬 유튜브 썸네일 고화질 추출기")
st.markdown(
    """
    유튜브 영상의 링크를 입력하면 **가장 고화질(Max Resolution)**의 썸네일을 찾아줍니다.
    썸네일이 필요한 블로그 포스팅이나 디자인 작업에 활용해보세요!
    """
)

# --- 함수: 유튜브 ID 추출 ---
def get_video_id(url):
    """
    다양한 형태의 유튜브 URL에서 영상 ID(11자리)를 추출합니다.
    예: https://youtu.be/VIDEO_ID, https://www.youtube.com/watch?v=VIDEO_ID 등
    """
    # 정규표현식을 사용하여 ID 추출
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

# --- UI 구성 ---
video_url = st.text_input("👇 여기에 유튜브 영상 링크를 붙여넣으세요:")

if st.button("썸네일 가져오기"):
    if not video_url:
        st.warning("링크를 입력해주세요!")
    else:
        video_id = get_video_id(video_url)
        
        if video_id:
            # 썸네일 주소 생성 (maxresdefault: 최대 해상도)
            img_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            
            # 이미지 데이터 가져오기
            response = requests.get(img_url)
            
            # 만약 최대 해상도 이미지가 없다면 (404 에러), 고화질(hqdefault)로 대체
            if response.status_code != 200:
                img_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                response = requests.get(img_url)

            if response.status_code == 200:
                # 바이트 데이터를 이미지로 변환
                image = Image.open(BytesIO(response.content))
                
                st.success(f"✅ 썸네일을 찾았습니다! (ID: {video_id})")
                
                # 이미지 화면 표시
                st.image(image, caption="추출된 썸네일", use_column_width=True)
                
                # 다운로드 버튼
                # BytesIO를 사용하여 메모리에 있는 이미지를 바로 다운로드 가능하게 함
                buf = BytesIO()
                image.save(buf, format="JPEG")
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="📥 이미지 다운로드 (JPG)",
                    data=byte_im,
                    file_name=f"thumbnail_{video_id}.jpg",
                    mime="image/jpeg"
                )
            else:
                st.error("썸네일 이미지를 찾을 수 없습니다. 영상이 비공개이거나 삭제되었는지 확인해주세요.")
        else:
            st.error("올바르지 않은 유튜브 링크입니다. 다시 확인해주세요.")

# --- 부가 정보 ---
st.markdown("---")
st.caption("Created with Streamlit & Python")
