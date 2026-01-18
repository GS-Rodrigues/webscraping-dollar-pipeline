import requests
from Insert import *
from datetime import date
from date_treatment import *
from Db_connection import *
from calendar import monthrange

conn = get_connection();
cursor = conn.cursor();

try:
    for j in range(date.today().year-1, date.today().year+1):
        for i in range(1, 13):
            for k in range(1, monthrange(j, i)[1]()[1]):
                if j == date.today().year and i == date.today().month and k >= date.today().day :
                    continue;

                url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao=%27{i}-{k}-{j}%27&$top=100&$format=json";
                response = requests.get(url, timeout=10);

                data = response.json();
                try:
                    purchase_value = data["value"][0]["cotacaoCompra"];
                    selling_value = data["value"][0]["cotacaoVenda"];
                    date_time = data["value"][0]["dataHoraCotacao"];
                    date_time = date_treat(date_time);
                    insert_row(cursor, date_time, purchase_value, selling_value);
                except ValueError:
                    continue
    conn.commit();

finally:
        if cursor is not None:
            cursor.close();
        if conn is not None:
            conn.close();
