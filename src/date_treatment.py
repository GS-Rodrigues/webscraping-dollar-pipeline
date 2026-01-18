import datetime

def date_treat(text):
    #text = "2026-01-16 13:04:26.486"
    dt = datetime.strptime(text, "%Y-%m-%d %H:%M:%S.%f")
    return(dt)
