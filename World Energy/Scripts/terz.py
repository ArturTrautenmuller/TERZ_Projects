import requests

def importDataFrame(dataframePath,reportid,user,password):
    url = "http://terzanalytics.com/api/Report/"+reportid+"/UploadDataFrame"

    payload = {'email': user,
               'password': password}
    files = [
        ('dataframe', (dataframePath.split('\\')[-1], open(dataframePath, 'rb'), 'text/csv'))
    ]
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload, files=files)

    print(response.text)