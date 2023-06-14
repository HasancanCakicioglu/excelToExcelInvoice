data_map = {
    "001250": "ADANA İHTİSAS VERGİ DAİRESİ MÜDÜRLÜĞÜ",
    "001251": "5 OCAK VERGİ DAİRESİ MÜDÜRLÜĞÜ",
    "001252": "YÜREĞİR VERGİ DAİRESİ MÜDÜRLÜĞÜ",

}

print(data_map["001250"])
data_map["0"] = 123

print(data_map["0"])
import pandas as pd

# Excel dosyasını oku
df = pd.read_excel('C:\\Users\\Yonet\\Desktop\\folder\\exceller\\kısmet\\gelir\\Isletme_eFatura.xlsx', sheet_name='Vergi Dairesi')


#message = "My name is {} and I'm {} years old.".format(name, age)

for index, row in df.iterrows():

    print("'{}' : '{}',".format(row[1],row[0]))



