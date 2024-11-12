import os
import urllib.parse
import pandas as pd
from datetime import datetime

# 이미지 확장자 목록
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']

# 3MB를 바이트로 변환 (1MB = 1024 * 1024 바이트)
SIZE_LIMIT = 3 * 1024 * 1024  # 3MB

# 서버 URL
SERVER_URL = "https://"

def bytes_to_mb(byte_size):
    """바이트를 MB로 변환하는 함수"""
    return byte_size / (1024 * 1024)

def find_large_images(directory):
    large_images = []
    total_images = 0  # 이미지 파일의 총 개수 카운트

    # 디렉토리 내 모든 파일 탐색
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 파일의 확장자가 이미지인지 확인
            if any(file.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                total_images += 1  # 이미지 개수 증가
                file_path = os.path.join(root, file)

                # URL 인코딩된 경로 디코딩
                decoded_path = urllib.parse.unquote(file_path)

                # 디코딩된 경로가 실제 존재하는지 확인
                if os.path.exists(decoded_path):
                    # 파일 크기가 3MB 이상인지 확인
                    file_size = os.path.getsize(decoded_path)
                    file_size_mb = bytes_to_mb(file_size)
                    
                    if file_size > SIZE_LIMIT:                   
                        # 서버 URL과 합쳐서 전체 URL 생성
                        server_path = SERVER_URL + decoded_path.replace(os.sep, '/')
                        
                        # 경로, 파일명, 용량, 서버 URL을 리스트로 추가
                        large_images.append((decoded_path, file, round(file_size_mb, 1), server_path))
                else:
                    print(f"파일이 존재하지 않습니다: {decoded_path}")

    return large_images, total_images

def save_to_excel(large_images):
    # 결과를 데이터프레임으로 변환
    df = pd.DataFrame(large_images, columns=["이미지 주소", "이미지 명", "이미지 크기(MB)", "이미지 서버주소"])

    # 현재 날짜와 시간을 기반으로 고유한 파일 이름 생성
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"large_images_{current_time}.xlsx"
    # result 폴더 경로를 지정
    result_folder = "D:/ImgSizeFinder/result"  # 결과값이 저장되는 폴더 
    
    # result 폴더가 없으면 생성
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)
    
    # 엑셀 파일 경로
    file_path = os.path.join(result_folder, file_name)
        
    # 엑셀 파일로 저장
    df.to_excel(file_path, index=False, engine='openpyxl')

    print(f"결과가 '{file_path}' 파일에 저장되었습니다.")

def main():
    # 사용자로부터 검색할 디렉토리 경로를 입력받음
    directory = input("이미지 파일을 검색할 폴더 경로를 입력하세요: ")

    if os.path.isdir(directory):
        print(f"'{directory}' 디렉토리에서 3MB 이상인 이미지 파일을 검색합니다...\n")
        large_images, total_images = find_large_images(directory)

        if large_images:
            print(f"3MB 이상의 이미지 파일 목록 ({len(large_images)}개):")
            for image, name, size, server_url in large_images:
                print(f"{image} - {size:.1f} MB - {server_url}")
            
            # 엑셀에 저장
            save_to_excel(large_images)
        else:
            print("3MB 이상의 이미지 파일을 찾을 수 없습니다.")

        # 총 이미지 개수 출력
        print(f"\n전체 이미지 파일 개수: {total_images}개")
    else:
        print("유효한 디렉토리가 아닙니다.")

if __name__ == "__main__":
    main()
