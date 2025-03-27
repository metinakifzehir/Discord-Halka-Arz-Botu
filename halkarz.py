import requests
from bs4 import BeautifulSoup as bs
import math
from datetime import datetime, timedelta


def link_cek(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    links = []
    if response.status_code == 200:
        soup = bs(response.text, 'html.parser')
        basliklar = soup.find('ul', class_="halka-arz-list").find_all('h3')
        tarihler = soup.find('ul', class_="halka-arz-list").find_all('time')
        i = 0
        for baslik in basliklar:
            baslik = baslik.text
            if baslik.startswith("("):
                baslik = baslik[baslik.find(")")+1:]
            yenibaslik = baslik[0]
            baslik = baslik.replace('(', '')
            baslik = baslik.replace(')', '')
            baslik = baslik.replace('.', ' ')
            for harf in baslik[1:]:
                if harf.isupper():
                    yenibaslik += " " + harf
                else:
                    yenibaslik += harf
            baslik = yenibaslik
            baslik = baslik.replace('İ', 'i')
            baslik = baslik.replace('Ş', 's')
            baslik = baslik.replace('Ğ', 'g')
            baslik = baslik.replace('Ü', 'u')
            baslik = baslik.replace('Ç', 'c')
            baslik = baslik.replace('Ö', 'o')
            baslik = baslik.replace('ı', 'i')
            baslik = baslik.replace('ş', 's')
            baslik = baslik.replace('ğ', 'g')
            baslik = baslik.replace('ü', 'u')
            baslik = baslik.replace('ç', 'c')
            baslik = baslik.replace('ö', 'o')
            baslik = ' '.join(baslik.split())
            baslik = baslik.replace(' ', '-')
            baslik = "https://halkarz.com/" + baslik
            tarih = tarihler[i].text
            i += 1
            links.append([baslik.lower(), tarih])
    return links


def tarih_kontrol(links):
    temp_links = []
    for link in links:
        tarih = link[1]
        if "Hazırlanıyor" in tarih:
            temp_links.append(link)
        else:
            index = tarih.rfind("-")
            tarih = tarih[index+1:].strip()
            tarih = tarih.replace("Ocak", "1").replace("Şubat", "2").replace("Mart", "3").replace("Nisan", "4")
            tarih = tarih.replace("Mayıs", "5").replace("Haziran", "6").replace("Temmuz", "7").replace("Ağustos", "8")
            tarih = tarih.replace("Eylül", "9").replace("Ekim", "10").replace("Kasım", "11").replace("Aralık", "12")
            tarih = datetime.strptime(tarih, "%d %m %Y")
            today = datetime.today()
            if tarih >= today:
                temp_links.append(link)
    return temp_links


def print_data(link):
    url = link[0]
    tarih = link[1]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = bs(response.text, 'html.parser')
        isim = soup.find('div', class_="il-content")
        lot_fiyat = soup.find('table', class_="sp-table").find('strong', class_="f700").text
        lot_fiyat = float(lot_fiyat.replace(",", ".").replace(" TL", ""))
        if isim.find('h2').text.replace("\n", "").replace(" ", "").isalnum():
            isim = isim.find('h2').text.replace("\n", "").replace(" ", "")
        else:
            isim = isim.find('h1').text

        detaylar = 1
        tahmini = 0
        sptable = soup.find('table', class_="sp-table").text
        toplam_lot = sptable[:sptable.find(" Lot")]
        toplam_lot = toplam_lot[toplam_lot.rfind("\n"):]
        toplam_lot = toplam_lot.replace(",", "")
        toplam_lot = int(toplam_lot)

        bilgiler = soup.find('ul', class_="aex-in").text
        if ("Yurt İçi Bireysel" or "Tamamı Eşit Dağıtım" or "T1-T2 Uygun") in bilgiler:
            yuzde = bilgiler[:bilgiler.find("Yurt İçi Bireysel")]
            yuzde = yuzde[yuzde.rfind("%")+1:yuzde.rfind(")")]
            
            if yuzde.replace(',', '.').isdecimal():
                yuzde = float(yuzde.replace(',', '.'))
            else:
                yuzde = 75
                tahmini = 1
        else:
            if "Yoktur" in bilgiler:
                yuzde = 100
            else:
                tahmini = 1
                yuzde = 75
        print(isim)
        return [isim, tarih, lot_fiyat, toplam_lot, yuzde, tahmini]


def colored_text(lines):
    halkarz = open("halkarz.txt", "w", encoding="utf-8")
    for line in lines:
        line = str(line)
        line = line.replace("^", "[0m").replace("bold", "[1;2m").replace("red", "[2;31m")
        line = line.replace("line", "[4;2m").replace("yellow", "[2;32m")
        halkarz.write(line + "\n")


site = "https://halkarz.com"
linkler = link_cek(site)
linkler = tarih_kontrol(linkler)
lines = []
for link in linkler:
    isim, tarih, lot_fiyat, toplam_lot, yuzde, tahmini = print_data(link)
    lines.append("• bold" + isim + "^")
    lines.append("• Lot Tutarı: bold" + str(lot_fiyat) + "^" + "₺")
    katilimci_sayilari = [500000, 1000000, 1500000]
    lot = []
    for katilimci in katilimci_sayilari:
        lot_miktari = round(toplam_lot * yuzde / 100 / katilimci)
        lot.append([lot_miktari, round(lot_miktari * lot_fiyat, 2)])
    lines.append("  ⚬ red" + str(lot[0][0]) + "^ Lot (red" + str(lot[0][1]) + "^₺) -yellow" + str(katilimci_sayilari[0]/1000000) + "M^ katılımcı")
    lines.append("  ⚬ red" + str(lot[1][0]) + "^ Lot (red" + str(lot[1][1]) + "^₺) -yellow" + str(katilimci_sayilari[1]/1000000) + "M^ katılımcı")
    lines.append("  ⚬ red" + str(lot[2][0]) + "^ Lot (red" + str(lot[2][1]) + "^₺) -yellow" + str(katilimci_sayilari[2]/1000000) + "M^ katılımcı")
    if yuzde == 100:
        lines.append("• HİSSE ALIŞ MENÜSÜ bold(10:30-13:00)^")
    else:
        lines.append("• HALKA ARZ MENÜSÜ")
    lines.append("• " + tarih)
    if tahmini == 1:
        lines.append("(linetahmini^)")
    lines.append("\n\n")
colored_text(lines)