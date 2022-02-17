import pandas as pd
import string
import re
import pickle
from nltk import word_tokenize, PorterStemmer


def preProcess(s):
    ps = PorterStemmer()
    s = word_tokenize(s)
    # stopwords_set = set(stopwords.words())
    # stop_dict = {s: 1 for s in stopwords_set}
    # s = [w for w in s if w not in stop_dict]
    s = [ps.stem(w) for w in s]
    s = ' '.join(s)
    s = s.translate(str.maketrans('', '', string.punctuation + u'\xa0'))
    return s

def get_and_clean_data():
    # Lyrics DataFrame
    df_lyrics = pd.read_csv('assets/lyrics-data.csv')
    df_lyrics = df_lyrics[df_lyrics['Idiom'] == 'ENGLISH']
    df_lyrics = df_lyrics.drop_duplicates(subset='SLink')
    # Artist DataFrame
    df_artists = pd.read_csv('assets/artists-data.csv')
    df_artists = df_artists.drop_duplicates(subset='Link')
    # Merge
    df = pd.DataFrame.merge(df_lyrics, df_artists, how='inner', left_on='ALink', right_on='Link')
    # Drop columns and duplicate(['Artist', 'SName', 'Lyric'])
    df = df.drop(columns=['ALink', 'SLink', 'Idiom', 'Songs', 'Popularity', 'Link', 'Genre', 'Genres'], axis=1)
    df = df.drop_duplicates(subset=['Artist', 'SName', 'Lyric'])
    df = df.rename({'SName': 'song', 'Lyric': 'lyric', 'Artist': 'artist'}, axis='columns')
    df = df[['artist', 'song', 'lyric']]

    # clean lyric
    cleaned_lyric = df['lyric']
    cleaned_lyric = cleaned_lyric.apply(lambda s: re.sub(r'[\(\[].*?[\)\]]', '', s.lower()))
    cleaned_lyric = cleaned_lyric.apply(lambda s: s.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    cleaned_lyric = cleaned_lyric.apply(lambda s: re.sub("\s+", " ", s.strip()))
    cleaned_lyric = cleaned_lyric.apply(
        lambda s: s.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), '')))
    df['lyric'] = cleaned_lyric
    df['artist'] = df['artist'].apply(lambda s: s.lower())
    df['song'] = df['song'].apply(lambda s: s.lower())
    pickle.dump(df, open('assets/parsed_data.pkl' ,'wb'))
    return df


def clean_data_wiki():
    f = open("C:/Users/Bungkai/Documents/953481 IR/953481-midterm-project/assets/eng-simple_wikipedia_2021_100K-sentences.txt", "r", encoding='utf8')
    text = f.read()
    text = re.sub('[^A-za-z]', ' ', text.lower() )
    text = re.sub('\s+', ',', text)
    text = text.split(',')
    text = [w for w in text if len(w)>2]
    text = list(set(text))
    text = ' '.join(text)
    save_text = open('assets/clean_wiki_100k.txt', 'w')
    save_text.write(text)
    return text

if __name__ == '__main__':
    get_and_clean_data()
    clean_data_wiki()