#from src.load_data.call_api import retrieve_tgvmax_at_date

def test_retrieve_tgvmax_at_date():
    a = retrieve_tgvmax_at_date()
    a.head()