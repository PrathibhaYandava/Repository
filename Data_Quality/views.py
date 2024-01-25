from django.shortcuts import render
from Data_Quality.forms import OnpremiseForm,CloudForm
import oracledb
import requests
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('success_page')  # Redirect to success page
        else:
            error_message = 'Invalid credentials'

    return render(request, 'login_page.html', {'error': error_message})

def success_view(request):
    return render(request, 'success_page.html')
# Create your views here.
def home_view(request):
        return render(request,'Home.html')

def ReportForm(request):
        return render(request,'ReportForm.html')
    


def onpremise(request):

        form =OnpremiseForm(request.POST)
        #Test Connection.
        HostName = request.POST.get('HostName')
        Port = request.POST.get('Port')
        UserName = request.POST.get('UserName')
        Password = request.POST.get('Password')
        # print(HostName,Port,UserName,Password)
        data = f"""(DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = {HostName})(PORT = {Port}))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = ORA12C.dbaora.com)
    )
  )"""
        query = """
SELECT 

    project_name AS project, 

    SUM(profile_count) AS profile_count, 

    SUM(scorecard_count) AS scorecard_count, 

    SUM(mapping_count) AS mapping_count, 

    SUM(rules_count) AS rules_count, 

    SUM(ldo_count) AS ldo_count, 

    SUM(pdo_count) AS pdo_count 

FROM ( 

    SELECT 

        profile_project AS project_name, 

        COUNT(*) AS profile_count, 

        0 AS scorecard_count, 

        0 AS mapping_count, 

        0 AS rules_count, 

        0 AS ldo_count, 

        0 AS pdo_count 

    FROM EDC_BETAMTRMRS.MRX_COL_PROFILE_INFO 

    GROUP BY profile_project 

 

    UNION ALL 

 

    SELECT 

        SC_PROJECT_NAME AS project_name, 

        0 AS profile_count, 

        COUNT(*) AS scorecard_count, 

        0 AS mapping_count, 

        0 AS rules_count, 

        0 AS ldo_count, 

        0 AS pdo_count 

    FROM EDC_BETAMTRMRS.MRX_SCORECARD_INFO 

    GROUP BY SC_PROJECT_NAME 

 

    UNION ALL 

 

    SELECT 

        project_name, 

        0 AS profile_count, 

        0 AS scorecard_count, 

        COUNT(*) AS mapping_count, 

        0 AS rules_count, 

        0 AS ldo_count, 

        0 AS pdo_count 

    FROM EDC_BETAMTRMRS.MRX_MAPPINGS 

    GROUP BY project_name 

 

    UNION ALL 

 

    SELECT 

        profile_project AS project_name, 

        0 AS profile_count, 

        0 AS scorecard_count, 

        0 AS mapping_count, 

        COUNT(*) AS rules_count, 

        0 AS ldo_count, 

        0 AS pdo_count 

    FROM EDC_BETAMTRMRS.MRX_PROFILE_RULES 

    GROUP BY profile_project 

 

    UNION ALL 

 

    SELECT 

        project_name AS project_name, 

        0 AS profile_count, 

        0 AS scorecard_count, 

        0 AS mapping_count, 

        0 AS rules_count, 

        COUNT(*) AS ldo_count, 

        0 AS pdo_count 

    FROM EDC_BETAMTRMRS.MRX_LDO_SRCCNT 

    GROUP BY project_name 

 

    UNION ALL 

 

    SELECT 

        project_name AS project_name, 

        0 AS profile_count, 

        0 AS scorecard_count, 

        0 AS mapping_count, 

        0 AS rules_count, 

        0 AS ldo_count, 

        COUNT(*) AS pdo_count 

    FROM EDC_BETAMTRMRS.MRX_PDO 

    GROUP BY project_name 

) subquery 

GROUP BY project_name """


        try : 
          connection = oracledb.connect(user=UserName, password=Password, dsn=data)
          print(connection)
          cursor = connection.cursor()
          cursor.execute(query)
          onpremise_data = cursor.fetchall()
          # Serialize the list to a JSON string
          serialized_list = json.dumps(onpremise_data)
          request.session['premise_data'] = serialized_list
          
          flag  = "Test Connection Successful"
          print(flag)
          connection.close()
          return render(request,'ReportForm.html',{'message1': flag,'data':onpremise_data})

        except Exception as e :
          print(e)      
          flag = "Test Connection Failed, Try Again!!"
          print(flag)
          return render(request,'ReportForm.html',{'message2': flag})
        


        
def FetchData1(request):
        serialized_list = request.session.get('premise_data', '[]')
        onpremise_data = json.loads(serialized_list)
        print(type(onpremise_data))
        return render(request,'OnPremise.html',{'data':onpremise_data})
        
        
        
def cloud(request):
        form =CloudForm(request.POST)
        UserName = request.POST.get('IUserName')
        Password = request.POST.get('IPassword')
        IURL = request.POST.get('IURL')
        POD_region = 'us'
        login_api_url = "https://dm-" + POD_region + IURL
        credentials = {
                "username": UserName,
                "password": Password
        }
        login_headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
        }

        login_response = requests.request("POST", login_api_url, json=credentials, headers=login_headers)
        if login_response.status_code == 200:
                serialized_list = request.session.get('premise_data', '[]')
                onpremise_data = json.loads(serialized_list)
                return render(request,'ReportForm.html',{'message3': 'Test Connection Successfull','second':True,'data':onpremise_data})
        else:
                
                return render(request,'ReportForm.html',{'message4': 'Test Connection Failed'})

