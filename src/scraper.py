import requests
from datetime import date, timedelta
from calendar import monthrange
from Insert import *
from date_treatment import *
from Db_connection import *

conn = get_connection();
cursor = conn.cursor();

try:
    yesterday = (datetime.now() - timedelta(days=1)).date()
    data_str = yesterday.strftime("%m-%d-%Y")

    url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao=%27{data_str}%27&$top=100&$format=json";

    response = requests.get(url, timeout=10);
    response.raise_for_status()
    data = response.json();

    if not data["value"]:
        raise RuntimeError(f"PTAX sem dados para {data_str}")

    else:
        info = data["value"][0]
        purchase_value = info["cotacaoCompra"];
        selling_value = info["cotacaoVenda"];
        date_time = info["dataHoraCotacao"];
        date_time = date_treat(date_time);
        insert_row(cursor, date_time, purchase_value, selling_value);

except Exception as e:
    conn.rollback()
    print("Erro:", e)

finally:
    cursor.close()
    conn.close()