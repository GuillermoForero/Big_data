import requests
import datetime
from datetime import date
import boto3
import botocore
def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except botocore.exceptions.ClientError as e:
        return False
    return True
#A continuación, definimos la fecha futura que queremos en formato YYY-MM-DD
mar_date = date(2121, 3, 13)
actions_name = ['AVHOQ', 'EC', 'AVAL', 'CMTOY']
date_time = date.today()
remaining_days = (date_time - mar_date).days
actions = ['https://query1.finance.yahoo.com/v7/finance/download/AVHOQ?period1=' + str(1615507200 + 86400*remaining_days) + '&period2='+ str(1615593600 + 86400*remaining_days) + '&interval=1d&events=history&includeAdjustedClose=true',
'https://query1.finance.yahoo.com/v7/finance/download/EC?period1=' + str(1615507200 + 86400*remaining_days) + '&period2='+ str(1615593600 + 86400*remaining_days) + '&interval=1d&events=history&includeAdjustedClose=true',
'https://query1.finance.yahoo.com/v7/finance/download/AVAL?period1=' + str(1615507200 + 86400*remaining_days) + '&period2='+ str(1615593600 + 86400*remaining_days) + '&interval=1d&events=history&includeAdjustedClose=true'
'https://query1.finance.yahoo.com/v7/finance/download/CMTOY?period1=' + str(1615507200 + 86400*remaining_days) + '&period2='+ str(1615593600 + 86400*remaining_days) + '&interval=1d&events=history&includeAdjustedClose=true']
for i in range(0, 4):
    req = requests.get(actions[i])
    url_content = req.content
    csv_file = open(actions_name[i]+'_temp' +'.csv', 'wb')    
    csv_file.write(url_content)
    csv_file.close()
    with open(actions_name[i]+'_temp' +'.csv','r') as f:
        with open(actions_name[i]+'.csv','w') as f1:
            next(f) # skip header line
            for line in f:
                f1.write(line)
    upload_file(actions_name[i]+'.csv', 'bick-dig-bucket', 'stocks/company=' + str(actions_name[i])+'/year=' + str(date_time.year) +'/month=' +str(date_time.month) + '/day=' + str(date_time.day)+'/'+actions_name[i]+'.csv')