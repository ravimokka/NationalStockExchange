from django.shortcuts import render
from django.views import View
import requests
import io
import zipfile
import pandas as pd
import datetime
from pandas.tseries.offsets import BDay
from nsepy import get_history
import matplotlib.pyplot as plt



class nseDataDownload(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        start_date = pd.datetime.today() - BDay(30)
        date = start_date.strftime("%d")
        month = start_date.strftime("%b").upper()
        year = start_date.strftime("%Y")
        url = 'https://archives.nseindia.com/content/historical/EQUITIES/{2}/{1}/cm{0}{1}{2}bhav.csv.zip'.format(date,
                                                                                                                 month,
                                                                                                                 year)
        response = requests.get(url)
        with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
            for zipinfo in thezip.infolist():
                with thezip.open(zipinfo) as stackData_CSV:
                    df = pd.read_csv(stackData_CSV, encoding="Latin-1")
                    headers = df.columns.to_list()
                    symbols = df[headers[0]].values
                    html_table = df.to_html()
                    return render(request, 'stackData.html',
                                  {'stack_data': html_table, 'columns': symbols, "symbolName": "",
                                   'symbol_stack_data': '', 'symbolData': 'false'})


class symbolDataAnalysis(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        start_date = pd.datetime.today() - BDay(30)
        date = start_date.strftime("%d")
        month = start_date.strftime("%b").upper()
        year = start_date.strftime("%Y")
        url = 'https://archives.nseindia.com/content/historical/EQUITIES/{2}/{1}/cm{0}{1}{2}bhav.csv.zip'.format(date,
                                                                                                                 month,
                                                                                                                 year)
        response = requests.get(url)
        with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
            for zipinfo in thezip.infolist():
                with thezip.open(zipinfo) as stackData_CSV:
                    df = pd.read_csv(stackData_CSV, encoding="Latin-1")
                    headers = df.columns.to_list()
                    symbols = df[headers[0]].values
                    html_table = df.to_html()
        start_date = pd.datetime.today() - BDay(30)
        end_date = datetime.datetime.now()

        symbol_val = request.POST['symbol']
        symbol_df = get_history(symbol=symbol_val, start=start_date, end=end_date)
        symbol_html_table = symbol_df.to_html()
        symbol_df.plot.area()
        plt.savefig('media/symbol_data.png')
        return render(request, 'stackData.html',
                      {'stack_data': html_table, 'columns': symbols, "symbolName": symbol_val,
                       'symbol_stack_data': symbol_html_table, 'symbolData': 'true'})
