import pandas as pd
import os
import nltk
nltk.download('averaged_perceptron_tagger_eng')

def get_part_of_speech(word):
    # 단어를 토큰화하여 리스트 형태로 만들고 품사 태깅
    pos_tagged = nltk.pos_tag([word])
    return pos_tagged[0][1]  # 품사 태그 반환

# CSV 파일 경로
file_path = 'data/어메이징토커-영단어-3000.csv'
df = pd.read_csv(file_path, header=2)

# '품사' 컬럼을 추가하기 위해 '단어' 컬럼에 대해 품사 태깅을 수행
df['품사'] = df['단어'].apply(get_part_of_speech)

# 저장할 폴더 경로 설정
output_folder = 'organizedData'
os.makedirs(output_folder, exist_ok=True)

# 단계별 필터링과 저장
levels = {'초등': 'level1_voca.csv', '중고': 'level2_voca.csv', '전문': 'level3_voca.csv'}

for 단계, filename in levels.items():
    # 해당 단계의 데이터만 필터링
    filtered_df = df[df['단계'] == 단계][['뜻', '단어', '품사']]
    
    # 저장 경로 설정
    output_path = os.path.join(output_folder, filename)
    
    # 결과를 CSV 파일로 저장
    filtered_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"'{단계}' 단계의 단어가 '{output_path}'에 저장되었습니다.")
