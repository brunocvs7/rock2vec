#import libs
import re
import os
from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup

class LyricsLink:
    """
    Essa classe retorna todos os links de letras de músicas de um grupo musical

    """
    def __init__(self, website, lyrics_class):
        """
        Attributes:
            website (str): Link da página da banda com a lista de todas as músicas.
            lyrics_class (str): Tag html que se referem as letras das músicas da banda.
        """
        self._website = website
        self._lyrics_class = lyrics_class

    def get_links(self):

        """
        Returns: 
            list_links_lyrics: Lista contendo todos os links para todas as letras de músicas da banda.
        """
        list_links_lyrics = []
        html_page = urlopen(self._website)
        bs = BeautifulSoup(html_page, 'lxml')
        links =  bs.findAll('a', {'class':self._lyrics_class})
        for link in links:
            list_links_lyrics.append(link['href'])

        return list_links_lyrics


class LyricsText:

    """
    Essa classe retorna a letra e o título de uma música dentro de um dado link.
    """
 
    def __init__(self, lyrics_url, title_class, lyrics_class):
        """
        Attributes:
            lyrics_url (str): Link da página da música.
            title_class (str): Tag html que referencia o título da música.
            lyrics_class (str): Tag html que referencia o texto da música.
        """
        self._lyric_url = lyrics_url
        self._title_class = title_class
        self._lyrics_class = lyrics_class

    def get_lyrics_text(self):
        """
        Returns:
            lyrics_text: String contendo o conteúdo da letra da música.
        """
        html_page = urlopen(self._lyric_url)

        bs = BeautifulSoup(html_page, 'lxml')

        lyrics_text = ''

        lyrics = bs.find('div', {'class':self._lyrics_class}).findAll('p')
        
        for text in lyrics:
            lyrics_text += ' ' + ' '.join(text.findAll(text = True))

        return lyrics_text

    def get_title(self):
        """
        Returns:
            titulo: String com o título da música.
        """
        html_page = urlopen(self._lyric_url)
        bs = BeautifulSoup(html_page, 'lxml')
        titulo = bs.find('div', {'class':self._title_class}).h1.text

        return titulo