#import libs
import re
import os
from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup

class LyricsLink:

    def __init__(self, website, lyrics_class):

        self._website = website
        self._lyrics_class = lyrics_class

    def get_links(self):

        list_links_lyrics = []
        html_page = urlopen(self._website)
        bs = BeautifulSoup(html_page, 'lxml')
        # Precisamos fazer um programa para iterar na pagina principal
        links =  bs.findAll('a', {'class':self._lyrics_class})
        for link in links:
            list_links_lyrics.append(link['href'])

        return list_links_lyrics



class LyricsText:
    
    def __init__(self, lyrics_url, title_class, lyrics_class):

        self._lyric_url = lyrics_url
        self._title_class = title_class
        self._lyrics_class = lyrics_class

    def get_lyrics_text(self):
        #carregando letra da musica
        html_page = urlopen(self._lyric_url)

        bs = BeautifulSoup(html_page, 'lxml')

        lyrics_text = ''

        lyrics = bs.find('div', {'class':self._lyrics_class}).findAll('p')
        
        for text in lyrics:
            lyrics_text += ' ' + ' '.join(text.findAll(text = True))

        return lyrics_text

    def get_title(self):
        
        html_page = urlopen(self._lyric_url)

        bs = BeautifulSoup(html_page, 'lxml')
        titulo = bs.find('div', class_= self._title_class).h1.text

        return titulo