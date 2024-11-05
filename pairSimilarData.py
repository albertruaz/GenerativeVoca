import pandas as pd
import os
from collections import deque

# 폴더 경로 설정
input_folder = 'organizedData'
output_folder = 'pairedSimilarData'
os.makedirs(output_folder, exist_ok=True)

# 파일 목록 정의
file_paths = {
    'level1_voca.csv': 'level1_paired_voca.csv',
    'level2_voca.csv': 'level2_paired_voca.csv',
    'level3_voca.csv': 'level3_paired_voca.csv'
}

# CSV 파일 순회 및 (NN, VB), (NN, JJ) 쌍 만들기
for input_file, output_file in file_paths.items():
    input_path = os.path.join(input_folder, input_file)
    output_path = os.path.join(output_folder, output_file)
    
    df = pd.read_csv(input_path)
    nn_queue = deque()  # 각 파일에 대해 별도의 NN 큐 생성
    vb_jj_queue = deque()  # 각 파일에 대해 VB/JJ 큐 생성
    paired_data = []  # 각 파일에 대해 쌍 리스트
    remaining_data = []  # 쌍을 이루지 못한 단어들을 저장
    
    for _, row in df.iterrows():
        meaning, word, pos = row['뜻'], row['단어'], row['품사']
        
        if pos == 'NN':
            nn_queue.append((meaning, word))
        
        elif pos in ('VB', 'JJ'):
            vb_jj_queue.append((meaning, word, pos))
    
    # 유사성 비교

    # 쌍 만들기

    all_data = paired_data + remaining_data
    paired_df = pd.DataFrame(all_data)
    paired_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Paired data for '{input_file}' has been saved to '{output_path}'")
