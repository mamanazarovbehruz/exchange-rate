import pandas as pd
from matplotlib import pyplot as plt
import requests

# x = [1, 4, 8, 19]
# y = [1, 6, 2, 7]

# plt.plot(x, y)
# plt.title('Valyuta')
# plt.xlabel('sana')
# plt.ylabel('kurs')
# plt.show()


nomer = int(input('Nomer kiriting : '))
sana1 = input('Boshlanish sanani kiriting (yil - oy - kun) : ')
sana2 = input('Tugash sanani kiriting (yil - oy - kun) : ')
kun1 = int(sana1[8:10])
kun2 = int(sana2[8:10])
x = []
y = []
while kun1 <= kun2:
    sana = f'{sana1[0:4]}-{sana1[5:7]}-{kun1}'
    kurs = requests.post(f'https://cbu.uz/ru/arkhiv-kursov-valyut/json/all/{sana}/')
    valyuta = kurs.json()
    name = valyuta[nomer - 1]
    x.append(kun1)
    y.append(name['Rate'])
    kun1 += 1
plt.plot(x, y)
plt.title(name['CcyNm_UZ'])
plt.xlabel('Sana')
plt.ylabel('Kurs')
plt.show()