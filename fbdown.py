#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  fbdown.py
#  
#  Copyright 2019 Mario Zamora <mortasoftgmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import re
import sys
import time
import urllib.request
import requests as r
from slugify import slugify
import os.path

cantArchivos=0
archivoActual=1

def iniciar():
    f = open("listaVideos.txt", "r")
    for url in f:
        descargarVideo(url)


def contarArchivos():
    global cantArchivos
    f = open("listaVideos.txt", "r")
    for url in f:
        cantArchivos= cantArchivos+1

def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d segundos transcurridos" %
                     (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


def descargarVideo(url):
    try:
        global cantArchivos
        global archivoActual
        print("-----------------------------------------")
        print('Descargando el video: ' + url)
        html = r.get(url)
        video_url = re.search('hd_src:"(.+?)"', html.text).group(1)
        video_name = re.search('"og:title" content="(.+?)"', html.text).group(1)
        video_name = slugify(video_name)
        video_name = video_name+'.mp4'
        print('Archivo ' + str(archivoActual) + '/' + str(cantArchivos) + ' '+ video_name)
        if os.path.isfile(video_name):
            print('El archivo ya existe')
        else:
            urllib.request.urlretrieve(video_url, video_name, reporthook)
        archivoActual = archivoActual + 1
    except Exception as e:
        print('No se pudo descargar el archivo ' + str(e) + '. El video podria ser privado o no estar compartido como publico' )


contarArchivos()
iniciar()