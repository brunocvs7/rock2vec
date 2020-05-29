#import libs
import os
import re


import pandas as pd


from make_data.legiao_lyrics import LyricsText, LyricsLink
 

#constantes
URL_SITE = 'https://www.letras.mus.br'
GROUP = '/legiao-urbana'
LYRICS_NAME = 'song-name'
TITLE_CLASS = 'cnt-head_title'
LYRICS_CLASS = 'cnt-letra p402_premium'
DATA_OUTPUT_PATH = 'src/data'
DATA_OUTPUT_SUB_PATH = '/raw'
DATA_OUTPUT_NAME = '/lyrics.csv'

#recuperando os links de onde estão as letras das músicas
ll = LyricsLink(website = URL_SITE+GROUP, lyrics_class = LYRICS_NAME)

# retornando lista de links
list_links_lyrics = ll.get_links()

#loop que varre os links na lista list_links_lyrics e  então carrega a página e captura o campo de texto, que é a letra da música
# No final teremos um dicionário com as chaves sendo os títulos das músicas e os valores sendro strings contendo a letra das músicas
lyrics = {}
for lyrics_url in list_links_lyrics:
    lt = LyricsText(lyrics_url = URL_SITE+lyrics_url, title_class = TITLE_CLASS, lyrics_class = LYRICS_CLASS)
    lyrics[lt.get_title()] = lt.get_lyrics_text()

#salvando dados
data_frame_lyrics = pd.DataFrame.from_dict(lyrics, orient='index',columns=['lyrics']) \
                                .reset_index(inplace = True) \
                                .rename(columns = {'index':'title'}, inplace = True) \
                                .to_csv(DATA_OUTPUT_PATH+DATA_OUTPUT_SUB_PATH+DATA_OUTPUT_NAME, index = False)
