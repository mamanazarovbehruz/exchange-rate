import json
import requests
import datetime as dt
from colorama import Fore
from matplotlib import pyplot as plt
import xlsxwriter


def valyuta_kursi():
    ins = 1
    for name in valyuta:
        print(ins,'.', name['CcyNm_UZ'], sep='', end=' ')
        ins1 = 0
        while ins1 < (30 - len(name['CcyNm_UZ'])):
            print('-', end='')
            ins1 += 1
        print(f' 1 {name["Ccy"]} = {name["Rate"]} so\'m')
        ins += 1


def main():
    global valyuta
    sikl = 'ha'
    while sikl == 'ha':
        print('1.Valyuta kurslari')
        print('2.Valyuta konverter')
        print('3.Valyutalar kurslari arxivi')
        print('4.Valyuta kurslar diogrammasi')
        nomer = int(input('Nomer kiriting : '))
        if nomer == 1:
            valyuta_kursi()
        elif nomer == 2:
            ins = 1
            for name in valyuta:
                print(ins, '.', name['CcyNm_UZ'], sep='')
                ins += 1
            nomer = int(input('Nomer kiriting : '))
            name = valyuta[nomer - 1]
            sikl = 'ha'
            while sikl == 'ha':
                print(f'1. {name["Ccy"]} --> UZS')
                print(f'2. UZS --> {name["Ccy"]}')
                nomer = int(input('Nomer kiriting : '))
                if nomer == 1:
                    miqdor_boshqa = int(input(f'{name["Ccy"]} miqdorini kiriting : '))
                    uzs = float(name['Rate']) * miqdor_boshqa
                    print(f'UZB = {uzs} so\'m ')
                    sikl = 'yoq'
                elif nomer == 2:
                    miqdor_uzs = int(input('UZS miqdorini kiriting : '))
                    miqdor_boshqa = round(float(miqdor_uzs / float(name['Rate'])), 2)
                    print(f'{name["Ccy"]} = {miqdor_boshqa} {name["CcyNm_UZ"]}')
                    sikl = 'yoq'
                else:
                    print('bunday amal yoq.')
                    sikl = 'ha'
        elif nomer == 3:
            sikl = 'ha'
            while sikl == 'ha':
                try:
                    sana = input('Sana kiriting (yil - oy - kun) : ')
                    kurs = requests.post(f'https://cbu.uz/ru/arkhiv-kursov-valyut/json/all/{sana}/')
                    valyuta = kurs.json()
                    valyuta_kursi()
                except:
                    with open('valyuta.json') as file:
                        valyuta = json.load(file)
                        sana1 = valyuta[0]['Date']
                        if sana == f'{sana1[6:10]}-{sana1[3:5]}-{sana1[0:2]}':
                            valyuta_kursi()
                        else:
                            print(Fore.RED, 'Internet aloqasi yoq', Fore.RESET)
                            break
                sikl = input('Boshqa sanadagi kursni ko\'rasizmi ha/yoq : ')
        elif nomer == 4:
            sikl = 'ha'
            while sikl == 'ha':
                print('Qaysi valyuta diogrammasini ko\'rmoqchisiz.')
                ins = 1
                for name in valyuta:
                    print(ins, '.', name['CcyNm_UZ'], sep='')
                    ins += 1
                nomer = int(input('Nomer kiriting : '))
                print('Vaqt oralig\'ni kiriting.')
                sana1 = input('Boshlanish sanani kiriting (yil - oy - kun) : ')
                sana2 = input('Tugash sanani kiriting (yil - oy - kun) : ')
                kun1 = int(sana1[8:10])
                kun2 = int(sana2[8:10])
                x = []
                y = []
                data = []
                try:
                    while kun1 <= kun2:
                        sana = f'{sana1[0:4]}-{sana1[5:7]}-{kun1}'
                        kurs = requests.post(f'https://cbu.uz/ru/arkhiv-kursov-valyut/json/all/{sana}/')
                        valyuta = kurs.json()
                        name = valyuta[nomer - 1]
                        x.append(sana[8:10])
                        y.append(float(name['Rate']))
                        data.append(sana)
                        kun1 += 1
                    plt.plot(x, y)
                    plt.title(name['CcyNm_UZ'])
                    plt.xlabel(f'Sana ({sana[0:7]})')
                    plt.ylabel('Kurs')
                    plt.show()
                    workbook = xlsxwriter.Workbook('valyuta.xlsx')
                    worksheet = workbook.add_worksheet()
                    worksheet.write(1, 0, name['CcyNm_UZ'])
                    col = 1
                    for x in data:
                        worksheet.write(0, col, x)
                        col += 1
                    col = 1
                    for x in y:
                        worksheet.write(1, col, x)
                        col += 1
                    workbook.close()
                    sikl = input('Yana boshqa valyuta diogrammasini ko\'rasizmi ha/yoq : ')
                except:
                    print(Fore.RED, 'Internet yoq', Fore.RESET)
                    sikl = 'yoq'
        else:
            print('Bunday amal yoq.')
        sikl = input('Menyuga qaytasizmi ha/yoq : ')
    else:
        print('Bizning saytimizni kuzatib boring !!!')


def run():
    global valyuta
    try:
        sana = dt.datetime.now()
        sana = sana.date()
        kurs = requests.post(f'https://cbu.uz/ru/arkhiv-kursov-valyut/json/all/{sana}/')
        valyuta = kurs.json()
        with open('valyuta.json', 'w') as file:
            json.dump(valyuta, file)
        main()
    except:
        try:
            with open('valyuta.json') as file:
                valyuta = json.load(file)
            print(Fore.RED, 'Internet aloqasi yoq (Oflyndasiz)', Fore.RESET)
            print(f'Internet yoqligi sababli {valyuta[0]["Date"]} sanadagi valyutalarni ko\'ra olasiz.')
            main()
        except:
            print(Fore.RED, 'Internet aloqasi yoq bazada fayl ham topilmadi.', Fore.RESET)


if __name__ == '__main__':
    run()