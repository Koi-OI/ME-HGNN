import pandas as pd


df = pd.read_csv('data/IMDB/movie_metadata.csv')
df.dropna(subset=['movie_title', 'director_name', 'actor_1_name'], inplace=True)
f1 = open('data/IMDB/md.txt', 'w')
f2 = open('data/IMDB/ma.txt', 'w')
for i in range(len(df)):
    f1.write(f'{df["movie_title"].iloc[i].strip().lower()}###{df["director_name"].iloc[i].strip().lower()}\n')
    f2.write(f'{df["movie_title"].iloc[i].strip().lower()}###{df["actor_1_name"].iloc[i].strip().lower()}\n')
    if not pd.isna(df["actor_2_name"].iloc[i]):
        f2.write(f'{df["movie_title"].iloc[i].strip().lower()}###{df["actor_2_name"].iloc[i].strip().lower()}\n')
    if not pd.isna(df["actor_3_name"].iloc[i]):
        f2.write(f'{df["movie_title"].iloc[i].strip().lower()}###{df["actor_3_name"].iloc[i].strip().lower()}\n')
