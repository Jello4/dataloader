from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
# Create your views here.
import pandas as pd
from django.db import connection
from .utils import azure_sql_connector as az

def index(request):
    return render(request, "home.html")


def upload_file(request):
    # cursor = connection.cursor()
    # cursor.execute('''SELECT * FROM [social-development-bank-loans1]''')
    # row = cursor.fetchall()
    # print(row)
    # if request.method == 'POST':
    #     print(request.FILES)
    #     file_df = pd.read_excel(request.FILES.get('file'),engine='openpyxl')
    #     print(file_df)
    df = az.main(request.FILES.get('file'))
    return HttpResponse(df.to_html())