# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 20:38:29 2020

@author: Akirawisnu
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from io import StringIO

path = "C:/Users/Akirawisnu/Documents/work/faskes"
os.chdir(path)

def cleansing(string):
    #rapihin string
        #a = (string.encode("ascii", 'ignore')).replace('\t','')
        a = string.replace('\t','')
        b = a.replace('\r\n','')
        c = b.replace('({','')
        d = c.replace('});','')
        e = d.replace('#map','')
        f = e.replace("'",'')
        g = f.split('content:')
        h = g[0].split(',')

        #process lat
        lat = h[0].split(':')
        lat = lat[1].replace(' ','')
        

        #process lng
        lng = h[1].split(':')
        lng = lng[1].replace(' ','')

        #process title
        title = h[2].split(':')
        title = title[1]
        title = title.replace(' "','')
        title = title.replace('"','')
        title = title.replace('\\','')

        #get content
        content = g[1].replace('<div><table border=1><tr><td>','')
        content = content.replace('\\','')
        content = content.replace('<td>','')
        content = content.replace('</td>','')
        content = content.replace(';','')
        content = content.replace('<tr>',';')
        content = content.replace('</tr>','')
        content = content.replace('<br/>',';')
        content = content.split(';')

        #process kode unit
        kode_unit = content[0].split(':')
        kode_unit = kode_unit[1]

        #process nama unit
        nama_unit = content[1].split(':')
        nama_unit = nama_unit[1]

        #process alamat
        alamat = content[2].split(':')
        alamat = alamat[1]

        #process medis
        medis = content[3].split(':')
        medis = medis[1]

        #process psikolohi klinis
        psikologi_klinis = content[4].split(' ')
        psikologi_klinis = psikologi_klinis[0]

        #process perawat
        perawat = content[5].split(' ')
        perawat = perawat[0]

        #process bidan
        bidan = content[6].split(' ')
        bidan = bidan[0]
       
        #process Farmasi
        farmasi = content[7].split(' ')
        farmasi = farmasi[0]

        #process Kesmas
        kesmas = content[8].split(' ')
        kesmas = kesmas[0]

        #process kesling
        kesling = content[9].split(' ')
        kesling = kesling[0]
        
        # proses gizi
        gizi = content[10].split(' ')
        gizi = gizi[0]
        
        # keterapian fisik
        terapi_fisik = content[11].split(' ')
        terapi_fisik = terapi_fisik[0]
        
        # teknisi medis
        teknisi_medis = content[12].split(' ')
        teknisi_medis = teknisi_medis[0]
        
        # teknik biomedika
        teknik_biomed = content[13].split(' ')
        teknik_biomed = teknik_biomed[0]
        
        # kes tradisional
        kes_tradisional = content[14].split(' ')
        kes_tradisional = kes_tradisional[0]
        
        #nakes lain
        nakes_lain = content[15].split(' ')
        nakes_lain = nakes_lain[0]
        
        # penunjang
        penunjang = content[16].split(' ')
        penunjang = penunjang[0]

        return lat,lng,title,kode_unit,nama_unit,alamat,medis,psikologi_klinis,perawat,bidan,farmasi,kesmas,kesling,gizi,terapi_fisik,teknisi_medis,teknik_biomed,kes_tradisional,nakes_lain,penunjang


def get_map(kode_prov):
    endpoint = 'http://bppsdmk.kemkes.go.id/info_sdmk/peta?prov='
    kode_prov = kode_prov
    r = requests.get(endpoint+kode_prov)
    content = r.text
    soup = BeautifulSoup(content,'lxml')
    script = soup.find_all('script')
    df=[]

    map = (script[len(script)-38].string).split('map.addMarker')
    i = len(map)
    while i>1:
        i -= 1
        #print(i,kode_prov)

        clean=cleansing(map[i])

        query = "%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" \
        %(kode_prov,clean[0],clean[1],clean[2],clean[3],clean[4],clean[5],clean[6],clean[7],clean[8],clean[9],clean[10],clean[11],clean[12],clean[13],clean[14],clean[15],clean[16],clean[17],clean[18],clean[19])
        query = StringIO(query)
        qf=pd.read_csv(query, sep=",")
        df.append(qf)
    
    df=pd.DataFrame(df)    
    print(df)
    lst = list(df)
    df[lst] = df[lst].astype(str)
    df.to_stata("data_{}.dta".format(kode_prov), version=117, convert_strl=['_0'])
        
def kode_prov():
    endpoint = 'http://bppsdmk.kemkes.go.id/info_sdmk/peta?prov=34'
    r = requests.get(endpoint)
    content = r.text
    soup = BeautifulSoup(content,'lxml')
    form = soup.find_all('form')
    option = form[1].find_all('option')
    for value in option:
        kode_prov = value.get('value')
        print(kode_prov)
        get_map(kode_prov)

def main():
    kode_prov()

main()