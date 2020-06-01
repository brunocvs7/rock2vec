#import libs
import os
import re
import time
from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup

from make_data.rock_lyrics import LyricsText, LyricsLink

"""
Inicialmente iremos parsear a lista de links (URL_PRINCIPAL) com as 20 
maiores bandas de rock segundo o próprio site.
A partir daí, iremos iterar através dessa lista e, aí sim, traremos todas 
as letras de música de todas as 20 bandas de rock.
"""
#constantes
#home page
URL_HOME = 'https://www.letras.mus.br'
#url principal
URL_PRINCIPAL = 'https://www.letras.mus.br/blog/bandas-de-rock-nacional/'
#link do grupo cujas musicas serão trazidas
URL_GROUP = None
#classe do html (tag) onde o os links de todas as musicas estão
LYRICS_NAME = 'song-name'
#classe (tag) onde achamos o título da música
TITLE_CLASS = 'cnt-head_title'
# classe (tag) onde temos o texto da música
LYRICS_CLASS = 'cnt-letra p402_premium'
# classe (tag) onde temos os links para as paginas principais
LINK_GROUP_CLASS = 'news-copy'
#classe (tag) onde temos o nome dos artistas
GROUP_NAME_CLASS = 'cnt-head_title'
#caminho para salvar os resultados
OUTPUT_PATH = 'src/data'
OUTPUT_SUB_PATH = '/raw'
DATA_OUTPUT_NAME = '/lyrics.csv'

##### Recuperando os links das páginas da bandas a partir a URL_PRINCIAL
list_groups_link = []
#abrindo a página
html_page = urlopen(URL_PRINCIPAL)
bs = BeautifulSoup(html_page, 'lxml')
#selecionando a div em que temos os links
div =  bs.findAll('div', {'class':LINK_GROUP_CLASS})
for link in div:
    links_groups = link.findAll('a')
    for a in links_groups:
        link = a['href']
        print(link)
        list_groups_link.append(link)

#alguns links não são exatamente das páginas das bandas
#então iremos utilizar um try:except e admitir que todas rejeitadas
#são links que não correspondem a essas páginas principais.
#inicialmente iremos salvar um dataframe vazio como csv e então ir 
#apendando diretamente no arquivo.

#Criação do csv file
df_rock_lyrics = pd.DataFrame(data = None, 
                              columns = ['group', 'lyrics_title',
                                         'lyrics_text'])
#Salvando o csv 
df_rock_lyrics.to_csv(OUTPUT_PATH+OUTPUT_SUB_PATH+DATA_OUTPUT_NAME, 
                      index = False)

##### Varrendo a lista de links 
#for para ir de link em link buscando a lista de músicas de cada banda
for URL_GROUP in list_groups_link:
    #Bloco try para verificar se link da lista da banda é válido
    try:
        html_page = urlopen(URL_GROUP)
        bs = BeautifulSoup(html_page, 'lxml')
        group_name = bs.find('div', {'class':GROUP_NAME_CLASS}).h1.text
        print(group_name)
        #recuperando os links de onde estão as letras das músicas
        ll = LyricsLink(website = URL_GROUP, lyrics_class = LYRICS_NAME)
        # retornando lista de links
        list_links_lyrics = ll.get_links()
        print(list_links_lyrics)
        """
        loop que varre os links na lista list_links_lyrics e  então 
        carrega a página e captura o campo de texto, que é a letra da 
        música. No final teremos um dicionário com as chaves sendo os 
        títulos das músicas e os valores sendro strings contendo a letra
        das músicas
        """
        lyrics = {}
        for lyrics_url in list_links_lyrics:
            print(lyrics_url)
            #Bloco try para verificar se temos um link de música valido
            try:
                lt = LyricsText(lyrics_url =  URL_HOME+lyrics_url, 
                            title_class = TITLE_CLASS, 
                            lyrics_class = LYRICS_CLASS)
                lyrics[lt.get_title()] = lt.get_lyrics_text()
            except:
                print('ERROR: Música não pode ser acessada')
                continue
        #salvando dados
        df_lyrics = pd.DataFrame.from_dict(lyrics, orient='index',\
                                             columns=['lyrics_text'])
        df_lyrics.reset_index(inplace = True) 
        df_lyrics.rename(columns = {'index':'lyrics_title'},\
                             inplace = True)
        df_lyrics['group'] = group_name
        df_lyrics = df_lyrics.loc[:, ['group',
                                      'lyrics_title', 
                                      'lyrics_text']]
        #apendando
        df_lyrics.to_csv(OUTPUT_PATH+OUTPUT_SUB_PATH+DATA_OUTPUT_NAME, 
                         index = False, mode='a', header=False)
    except:
        print('ERROR: Link não pode ser utilizado')
        print('Link: ', URL_GROUP)
        print('\n')
