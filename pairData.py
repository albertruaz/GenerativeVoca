import pandas as pd
import os
from collections import deque

# 폴더 경로 설정
input_folder = 'organizedData'
output_folder = 'pairedData'
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
            # NN인 경우 큐에 추가
            if vb_jj_queue:
                # VB/JJ가 큐에 있으면 즉시 쌍으로 만듦
                vb_jj_meaning, vb_jj_word, vb_jj_pos = vb_jj_queue.popleft()
                paired_data.append({
                    '뜻1': meaning, '단어1': word, '품사1': 'NN',
                    '뜻2': vb_jj_meaning, '단어2': vb_jj_word, '품사2': vb_jj_pos
                })
            else:
                nn_queue.append((meaning, word))
        
        elif pos in ('VB', 'JJ'):
            # VB 또는 JJ인 경우
            if nn_queue:
                # NN이 큐에 있으면 즉시 쌍으로 만듦
                nn_meaning, nn_word = nn_queue.popleft()
                paired_data.append({
                    '뜻1': nn_meaning, '단어1': nn_word, '품사1': 'NN',
                    '뜻2': meaning, '단어2': word, '품사2': pos
                })
            else:
                vb_jj_queue.append((meaning, word, pos))
    
    # 남은 nn_queue와 vb_jj_queue의 단어들을 remaining_data에 추가
    while nn_queue:
        nn_meaning, nn_word = nn_queue.popleft()
        remaining_data.append({
            '뜻1': nn_meaning, '단어1': nn_word, '품사1': 'NN',
            '뜻2': '', '단어2': '', '품사2': ''
        })
    
    while vb_jj_queue:
        vb_jj_meaning, vb_jj_word, vb_jj_pos = vb_jj_queue.popleft()
        remaining_data.append({
            '뜻1': '', '단어1': '', '품사1': '',
            '뜻2': vb_jj_meaning, '단어2': vb_jj_word, '품사2': vb_jj_pos
        })
    
    # 최종 데이터를 DataFrame으로 변환하고 저장
    all_data = paired_data + remaining_data
    paired_df = pd.DataFrame(all_data)
    paired_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Paired data for '{input_file}' has been saved to '{output_path}'")
