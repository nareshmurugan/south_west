def updateme(platform_type,proxy=None,browser_ver=None,latest_fingerprint=True):
    import json
    import zipfile
    import os, random, json
    import pandas as pd
    import uuid
    import requests
    from faker import Faker
    import zipfile
    from re import findall,sub

    platform_mapping = {
    "windows": "Win32",
    "android": "Linux arm81",
    "linux": "Linux x86_64",
    "macos": "MacIntel"
    }

    file_plat=platform_type
    platform_type = platform_mapping.get(platform_type)
    
    if not proxy:
        proxy=None
    if proxy:
        if '[' in proxy and '@' in proxy:
            user_pass = proxy.split("@")[0]
            proxy_imp = {
                "mode": "http",
                "host": "["+proxy.split('[')[1].split(']')[0]+"]",
                "port": proxy.split("]:")[1],
                "username": user_pass.split(":")[0],
                "password": user_pass.split(":")[1],}
        elif '[' in proxy:
            proxy_imp = {
                "mode": "http",
                "host": proxy.split("]:")[0]+']',
                "port": proxy.split("]:")[1],
                "username": "",
                "password": "",
            }
        elif "@" in proxy:
                    user_pass = proxy.split("@")[0]
                    proxy_host_port = proxy.split("@")[1]
                    proxy_imp = {
                        "mode": "http",
                        "host": proxy_host_port.split(":")[0],
                        "port": proxy_host_port.split(":")[1],
                        "username": user_pass.split(":")[0],
                        "password": user_pass.split(":")[1],
                    }
        else:
            proxy_imp = {
                "mode": "http",
                "host": proxy.split(":")[0],
                "port": proxy.split(":")[1],
                "username": "",
                "password": "",
            }
    else:
        proxy_imp = {
            "mode": "none",
            "host": "",
            "port": 0,
            "username": "",
            "password": "",
        }

    def get_time_zone():
        proxy_val={"https":f"http://{proxy}"} if proxy else None      
        data = requests.get('https://time.gologin.com',proxies=proxy_val,timeout=5)
        return json.loads(data.content.decode('utf-8'))
    
    if latest_fingerprint:
        useragent_path=os.path.join(os.getcwd(), f'parquet_files/{file_plat}/useragent.parquet')
    else:
        useragent_path=os.path.join(os.getcwd(), f'parquet_files/{file_plat}/useragentoverall.parquet')


    
    hardware_path=os.path.join(os.getcwd(), f'parquet_files/{file_plat}/hardwareConcurrency.parquet'),
    maxtouchpoints_path=os.path.join(os.getcwd(), f'parquet_files/{file_plat}/maxtouchpoints.parquet'),
    devicememory_path=os.path.join(os.getcwd(), f'parquet_files/{file_plat}/devicememory.parquet'),
    language_path=os.path.join(os.getcwd(), f'parquet_files/{file_plat}/language.parquet'),
    webgl_path=os.path.join(os.getcwd(), f'parquet_files/{file_plat}/webgl.parquet'),
    resolution_path=os.path.join(os.getcwd(), f'parquet_files/{file_plat}/resolution.parquet'),
    devicepixel_path=os.path.join(os.getcwd(), f'parquet_files/{file_plat}/devicepixelratio.parquet')
    webgpu=os.path.join(os.getcwd(), f'parquet_files/{file_plat}/webgpu.parquet')
    fake = Faker()
    tz = get_time_zone()
    timezone = tz.get('timezone')


    useragent_df = pd.read_parquet(useragent_path)
    hardware_df = pd.read_parquet(hardware_path[0])
    maxtouchpoints_df = pd.read_parquet(maxtouchpoints_path[0])
    devicememory_df = pd.read_parquet(devicememory_path[0])
    language_df = pd.read_parquet(language_path[0])
    webgl_df = pd.read_parquet(webgl_path[0])
    res_df = pd.read_parquet(resolution_path[0])
    devicepixel_df = pd.read_parquet(devicepixel_path)  
    webgpu_data=pd.read_parquet(webgpu).sample(n=1).values[0]

    cversions=useragent_df[useragent_df['cversion'] == browser_ver]['useragent'].tolist()

    if cversions==[]:
        userval = random.choice(useragent_df['useragent'].to_list())
    else:
        userval = random.choice(cversions)

    wpmval = random.choice(webgl_df['webGlParamsValues'].to_list())
    mtpval = random.choice(maxtouchpoints_df['maxtouchpoints'].to_list())
    hwval = random.choice(hardware_df['hardwareConcurrency'].to_list())
    dmval = random.choice(devicememory_df['devicememory'].to_list())
    lanval = random.choice(language_df['language'].to_list())
    resval = random.choice(res_df['resolution'].to_list())
    dpval = random.choice(devicepixel_df['devicepixelratio'].to_list())

    vendor=webgpu_data[0]
    renderer=webgpu_data[1]
    json_like_string = sub(r'\'', r'"', str(webgpu_data[3]))
    json_like_string = json_like_string.replace("None", "null")
    json_like_string = json_like_string.replace("True", "true")
    json_like_string = json_like_string.replace("False", "false")
    webgpu_val=json.loads(json_like_string)

    Meta= {
        'mode': 'mask',
        'rerender': ''
    }
    Meta["vendor"]=vendor
    Meta["renderer"]=renderer
    webglparam = json.loads(wpmval)
    webgl={}
    webgl['vendor']=vendor
    webgl['renderer']=renderer
    result = {}
    result['navigator'] = {
        'platform': platform_type
    }
    result['navigator']['maxTouchPoints'] = int(mtpval)
    
    if dmval== '4':
        result['deviceMemory'] = 4096
    elif dmval== '2':
        result['deviceMemory'] = 2048
    elif dmval== '8':
        result['deviceMemory'] = 8192
    elif dmval== '16':
        result['deviceMemory'] = 16384
    else:
        result['deviceMemory'] = 4096
    
    result.update({
        'name': fake.name(),
        'profile_id': str(uuid.uuid4()).replace('-', ''),
        
        'timezone': {
            'id': timezone,
        },
        'screenWidth': int(resval.split('x')[0]),
        'screenHeight': int(resval.split('x')[1]),
        's3Date': '',
        's3Path': 'zero_profile.zip',
        'devicePixelRatio': float(dpval),
        'owner': str(uuid.uuid4()).replace('-', '')[:58],
        'autoProxyPassword': proxy_imp['password'],
        'autoProxyServer': proxy_imp['host'],
        'autoProxyUsername': proxy_imp['username'],
        'dns': '',
        'languages':tz.get('languages'),   
        'autoLang': True,
        'proxyEnabled': False,
        'startUrl': '',
        'googleServicesEnabled': True,      
        
    })  
    
    if proxy is not None:
        result['proxy'] = {
                'username': proxy_imp['username'],
                'password': proxy_imp['password'],   
                'host': proxy_imp['host'],
                'port': proxy_imp['port'],
        }
    else:
        result['proxy'] = {
                'username': '',
                'password': '',
                'host': '',
                'port': '',
        }
    if result['navigator']['platform'] == "Linux arm81":

        webglnoise = round(random.uniform(20, 40),2)
        webglnoice = round(random.uniform(1, 20),6)

        result['audioContext'] = {
            'enable': random.choice([True,False]),
            'noiseValue': float(f'{random.uniform(1e-10, 1e-7):.12e}')
        }
        result['canvasMode'] = random.choice(["noise","off","mode"])
        result['canvasNoise'] = round(random.uniform(0,4),8)
        result['client_rects_noise_enable'] = random.choice([True,False])
        result['deviceMemory'] = result['deviceMemory']
        result['dns'] = ""
        result['doNotTrack'] = random.choice([True,False])

        result['geoLocation']={            
            'accuracy': tz.get('accuracy', 0),
            'latitude': float(tz.get('ll', [0, 0])[0]),
            'longitude': float(tz.get('ll', [0, 0])[1]),
            'mode': 'prompt',
            
        }
        result['getClientRectsNoice'] =  webglnoice
        result['get_client_rects_noise'] =  webglnoice
        result['hardwareConcurrency'] = int(hwval)
        result['is_m1'] = random.choice([True,False])
        result['langHeader'] =  lanval
        result['languages'] =  tz.get('languages')

        result['mediaDevices'] = {
            'audioInputs' : random.randint(0,5),
            'audioOutputs' : random.randint(0,4),
            'enable': True,
            'uid': (str(uuid.uuid4()) + str(uuid.uuid4())).replace('-', '')[:58],
            'videoInputs' : random.randint(0,4)
        }
        # result["mobile"]={
        #     "device_scale_factor": random.uniform(2.10, 4.99),
        #     "enable":True,
        #     "height":int(result['screenHeight']),
        #     "width":int(result['screenWidth'])
        # }
        result['navigator'] = {
            'max_touch_points' : int(result['navigator']['maxTouchPoints']),
            'platform': result['navigator']['platform'],
        }

        result['plugins'] = {
            'all_enable': random.choice([True,False]),
            'flash_enable': random.choice([True,False])
        }
        result['profile_id'] = str(uuid.uuid4()).replace('-', '')

        result['screenWidth'] = int(resval.split('x')[0])
        result['screenHeight'] = int(resval.split('x')[1])
        result['startupUrl'] = ""
        result['startup_urls']=[""]
        result['storage'] = {
            'enable': random.choice([True,False])
        }
        result['timezone']= {
            'id': timezone,
        }
        result['unpinable_extension_names']=["passwords-ext"]
        result['userAgent'] = userval
        result['webGl']={
            'mode': 'true',
            "renderer" : webgl['renderer'],
            "vendor" : webgl['vendor']
        }
        result['webgl']={
            'metadata' : {
            'mode': 'true',
            "renderer" : webgl['renderer'],
            "vendor" : webgl['vendor']
            }
        }
        result['webglNoiceEnable'] = random.choice([True,False])
        result['webglNoiseValue'] =  webglnoise
        result['webglParams'] = webglparam
        result['webgl_noice_enable'] = random.choice([True,False])
        result['webgl_noise_enable'] = random.choice([True,False])
        result['webgl_noise_value'] =  webglnoise
        result['webrtc'] = {
            'enable':random.choice([True,False]),
            'mode': 'alerted',
            'should_fill_empty_ice_list':random.choice([True,False])
        }
   
    elif result['navigator']['platform'] == "iPhone":

        webglnoise = round(random.uniform(20, 40), 2)
        webglnoice = round(random.uniform(1, 20), 6)

        result['audioContext'] = {
            'enable': random.choice([True,False]),
            'noiseValue': float(f'{random.uniform(1e-10, 1e-7):.12e}')
        }
        result['canvasMode'] = random.choice(["noise","off","mode"])
        result['canvasNoise'] = round(random.uniform(0,4),8)
        result['client_rects_noise_enable'] = random.choice([True,False])
        result['deviceMemory'] = result['deviceMemory']
        result['dns'] = ""
        result['doNotTrack'] = random.choice([True,False])

        result['geoLocation']={            
            'accuracy': tz.get('accuracy', 0),
            'latitude': float(tz.get('ll', [0, 0])[0]),
            'longitude': float(tz.get('ll', [0, 0])[1]),
            'mode': 'prompt',
            
        }
        result['getClientRectsNoice'] =  webglnoice
        result['get_client_rects_noise'] =  webglnoice
        result['hardwareConcurrency'] = int(hwval)
        result['is_m1'] = random.choice([True,False])
        result['langHeader'] =  lanval
        result['languages'] =  tz.get('languages')

        result['mediaDevices'] = {

            'audioInputs' : random.randint(0,5),
            'audioOutputs' : random.randint(0,4),
            'enable': True,
            'uid': (str(uuid.uuid4()) + str(uuid.uuid4())).replace('-', '')[:58],
            'videoInputs' : random.randint(0,4)
        }
        
        result["mobile"]={
            "device_scale_factor": random.uniform(2.10, 4.99),
            "enable":True,
            "height":int(result['screenHeight']),
            "width":int(result['screenWidth'])
        }

        result['navigator'] = {
            'max_touch_points' : int(result['navigator']['maxTouchPoints']),
            'platform': result['navigator']['platform'],
        }

        result['plugins'] = {
            'all_enable': random.choice([True,False]),
            'flash_enable': random.choice([True,False])
        }
        result['profile_id'] = str(uuid.uuid4()).replace('-', '')


        result['screenWidth'] = int(resval.split('x')[0])
        result['screenHeight'] = int(resval.split('x')[1])
        result['startupUrl'] = ""
        result['startup_urls']=[""]
        result['storage'] = {
            'enable': random.choice([True,False])
        }
        result['timezone']= {
            'id': timezone,
        }
        result['unpinable_extension_names']=["passwords-ext"]
        result['userAgent'] = userval
        result['webGl']={
            'mode': 'true',
            "renderer" : webgl['renderer'],
            "vendor" : webgl['vendor']
        }
        result['webgl']={
            'metadata' : {
            'mode': 'true',
            "renderer" : webgl['renderer'],
            "vendor" : webgl['vendor']
            }
        }
        result['webglNoiceEnable'] = random.choice([True,False])
        result['webglNoiseValue'] =  webglnoise
        result['webglParams'] = webglparam
        result['webgl_noice_enable'] = random.choice([True,False])
        result['webgl_noise_enable'] = random.choice([True,False])
        result['webgl_noise_value'] =  webglnoise
        result['webrtc'] = {
            'enable':random.choice([True,False]),
            'mode': 'alerted',
            'should_fill_empty_ice_list':random.choice([True,False])
        }

    elif result['navigator']['platform'] == "Linux x86_64":
        webglnoise = round(random.uniform(20, 40), 2)
        webglnoice = round(random.uniform(1, 20), 6)
        result['audioContext'] = {
            'enable': random.choice([True,False]),
            'noiseValue': float(f'{random.uniform(1e-10, 1e-7):.12e}')
        }
        result['canvasMode'] = random.choice(["noise","off","mode"])
        result['canvasNoise'] = round(random.uniform(0,4),8)
        result['client_rects_noise_enable'] = random.choice([True,False])
        result['deviceMemory'] = result['deviceMemory']
        result['dns'] = ""
        result['doNotTrack'] = random.choice([True,False])

        result['geoLocation']={            
            'accuracy': tz.get('accuracy', 0),
            'latitude': float(tz.get('ll', [0, 0])[0]),
            'longitude': float(tz.get('ll', [0, 0])[1]),
            'mode': 'prompt',
            
        }
        result['getClientRectsNoice'] =  webglnoice
        result['get_client_rects_noise'] =  webglnoice
        result['hardwareConcurrency'] = int(hwval)
        result['is_m1'] = random.choice([True,False])
        result['langHeader'] =  lanval
        result['languages'] =  tz.get('languages')

        result['mediaDevices'] = {
            'audioInputs' : random.randint(0,5),
            'audioOutputs' : random.randint(0,4),
            'enable': True,
            'uid': (str(uuid.uuid4()) + str(uuid.uuid4())).replace('-', '')[:58],
            'videoInputs' : random.randint(0,4)
        }
        
        result['navigator'] = {
            'max_touch_points' : int(result['navigator']['maxTouchPoints']),
            'platform': result['navigator']['platform'],
        }

        result['plugins'] = {
            'all_enable': random.choice([True,False]),
            'flash_enable': random.choice([True,False])
        }
        result['profile_id'] = str(uuid.uuid4()).replace('-', '')


        result['screenWidth'] = int(resval.split('x')[0])
        result['screenHeight'] = int(resval.split('x')[1])
        result['startupUrl'] = ""
        result['startup_urls']=[""]
        result['storage'] = {
            'enable': random.choice([True,False])
        }
        result['timezone']= {
            'id': timezone,
        }
        result['unpinable_extension_names']=["passwords-ext"]
        result['userAgent'] = userval
        result['webGl']={
            'mode': 'noise',
            "renderer" : webgl['renderer'],
            "vendor" : webgl['vendor']
        }
        result['webgl']={
            'metadata' : {
            'mode': 'noise',
            "renderer" : webgl['renderer'],
            "vendor" : webgl['vendor']
            }
        }
        result['webglNoiceEnable'] = random.choice([True,False])
        result['webglNoiseValue'] =  webglnoise
        result['webglParams'] = webglparam
        result['webgl_noice_enable'] = random.choice([True,False])
        result['webgl_noise_enable'] = random.choice([True,False])
        result['webgl_noise_value'] =  webglnoise
        result['webrtc'] = {
            'enable':random.choice([True,False]),
            'mode': 'alerted',
            'should_fill_empty_ice_list':random.choice([True,False])
        }

    elif result['navigator']['platform'] == "Win32":
        webglnoise = round(random.uniform(20, 40), 2)
        webglnoice = round(random.uniform(1, 20), 6)
        result['audioContext'] = {
            'enable': random.choice([True,False]),
            'noiseValue': float(f'{random.uniform(1e-10, 1e-7):.12e}')
        }
        result['canvasMode'] = random.choice(["noise","off","mode"])
        result['canvasNoise'] = round(random.uniform(0,4),8)
        result['client_rects_noise_enable'] = random.choice([True,False])
        result['deviceMemory'] = result['deviceMemory']
        result['dns'] = ""
        result['doNotTrack'] = random.choice([True,False])
        result['geoLocation']={            
            'accuracy': tz.get('accuracy', 0),
            'latitude': float(tz.get('ll', [0, 0])[0]),
            'longitude': float(tz.get('ll', [0, 0])[1]),
            'mode': 'prompt',
            
        }
        result['getClientRectsNoice'] =  webglnoice
        result['get_client_rects_noise'] =  webglnoice
        result['hardwareConcurrency'] = int(hwval)
        result['is_m1'] = random.choice([True,False])
        result['langHeader'] =  lanval
        result['languages'] =  tz.get('languages')

        result['mediaDevices'] = {
            'audioInputs' : random.randint(0,5),
            'audioOutputs' : random.randint(0,4),
            'enable': True,
            'uid': (str(uuid.uuid4()) + str(uuid.uuid4())).replace('-', '')[:58],
            'videoInputs' : random.randint(0,4)
        }
        
        result['navigator'] = {
            'max_touch_points' : int(result['navigator']['maxTouchPoints']),
            'platform': result['navigator']['platform'],
        }

        result['plugins'] = {
            'all_enable': random.choice([True,False]),
            'flash_enable': random.choice([True,False])
        }
        result['profile_id'] = str(uuid.uuid4()).replace('-', '')

        result['screenWidth'] = int(resval.split('x')[0])
        result['screenHeight'] = int(resval.split('x')[1])
        result['startupUrl'] = ""
        result['startup_urls']=[""]
        result['storage'] = {
            'enable': random.choice([True,False])
        }
        result['timezone']= {
            'id': timezone,
        }
        result['unpinable_extension_names']=["passwords-ext"]
        result['userAgent'] = userval
        result['webGl']={
            'mode': 'true',
            "renderer" : webgl['renderer'],
            "vendor" : webgl['vendor']
        }
        result['webgl']={
            'metadata' : {
            'mode': 'true',
            "renderer" : webgl['renderer'],
            "vendor" : webgl['vendor']
            }
        }
        result['webglNoiceEnable'] = random.choice([True,False])
        result['webglNoiseValue'] =  webglnoise
        result['webglParams'] = webglparam
        result['webgl_noice_enable'] = random.choice([True,False])
        result['webgl_noise_enable'] = random.choice([True,False])
        result['webgl_noise_value'] =  webglnoise
        result['webrtc'] = {
            'enable':random.choice([True,False]),
            'mode': 'alerted',
            'should_fill_empty_ice_list':random.choice([True,False])
        }

    elif result['navigator']['platform'] == "MacIntel":
        webglnoise = round(random.uniform(20, 40), 2)
        webglnoice = round(random.uniform(1, 20), 6)
        result['audioContext'] = {
            'enable': random.choice([True,False]),
            'noiseValue': float(f'{random.uniform(1e-10, 1e-7):.12e}')
        }
        result['canvasMode'] = random.choice(["noise","off","mode"])
        result['canvasNoise'] = round(random.uniform(0,4),8)
        result['client_rects_noise_enable'] = random.choice([True,False])
        result['deviceMemory'] = result['deviceMemory']
        result['dns'] = ""
        result['doNotTrack'] = random.choice([True,False])

        result['geoLocation']={            
            'accuracy': tz.get('accuracy', 0),
            'latitude': float(tz.get('ll', [0, 0])[0]),
            'longitude': float(tz.get('ll', [0, 0])[1]),
            'mode': 'prompt',
            
        }
        result["mobile"]={
            "device_scale_factor": random.uniform(2.10, 4.99),
            "enable":True,
            "height":int(result['screenHeight']),
            "width":int(result['screenWidth'])
        }
        result['getClientRectsNoice'] =  webglnoice
        result['get_client_rects_noise'] =  webglnoice
        result['hardwareConcurrency'] = int(hwval)
        result['is_m1'] = random.choice([True,False])
        result['langHeader'] =  lanval
        result['languages'] =  tz.get('languages')

        result['mediaDevices'] = {
            'audioInputs' : random.randint(0,5),
            'audioOutputs' : random.randint(0,4),
            'enable': True,
            'uid': (str(uuid.uuid4()) + str(uuid.uuid4())).replace('-', '')[:58],
            'videoInputs' : random.randint(0,4)
        }
        
        result['navigator'] = {
            'max_touch_points' : int(result['navigator']['maxTouchPoints']),
            'platform': result['navigator']['platform'],
        }

        result['plugins'] = {
            'all_enable': random.choice([True,False]),
            'flash_enable': random.choice([True,False])
        }
        result['profile_id'] = str(uuid.uuid4()).replace('-', '')

        result['screenWidth'] = int(resval.split('x')[0])
        result['screenHeight'] = int(resval.split('x')[1])
        result['startupUrl'] = ""
        result['startup_urls']=[""]
        result['storage'] = {
            'enable': random.choice([True,False])
        }
        result['timezone']= {
            'id': timezone,
        }
        result['unpinable_extension_names']=["passwords-ext"]
        result['userAgent'] = userval
        result['webGl']={
            'mode': 'true',#change
            "renderer" : webgl['renderer'],
            "vendor" : webgl['vendor']
        }
        result['webgl']={
            'metadata' : {
            'mode': 'true',  #change
            "renderer" : webgl['renderer'],
            "vendor" : webgl['vendor']
            }
        }
        result['webglNoiceEnable'] = random.choice([True,False])
        result['webglNoiseValue'] =  webglnoise
        result['webglParams'] = webglparam
        result['webgl_noice_enable'] = random.choice([True,False])
        result['webgl_noise_enable'] = random.choice([True,False])
        result['webgl_noise_value'] =  webglnoise
        result['webrtc'] = {
            'enable':random.choice([True,False]),
            'mode': 'alerted',
            'should_fill_empty_ice_list':random.choice([True,False])
        }
    
    pth1=os.path.join(os.getcwd(),"platform",f'{platform_type}_main.zip')
    with zipfile.ZipFile(pth1,'r') as zip_obj:
        pth=os.path.join('Default','Preferences')
        with zip_obj.open(pth) as pref_obj:
            data=json.loads(pref_obj.read().decode('utf-8'))
            data['gologin']={}
            data['gologin']=result                        #change start
            data["gologin"]["webGpu"]=webgpu_val
            li=["Chrome","YaBrowser","Yowser","Safari","Firefox","TizenBrowser"]
            for i in li:
                if i in userval:
                    reten_pol_val=findall(fr"{i}/(.*?)\.",userval)
                    last_chrome_val=findall(fr"{i}/(.*?)$",userval)
                    break
            try:
                data["autocomplete"]["retention_policy_last_version"] = int(reten_pol_val[0])
            except Exception as e:
                print(f"Error: {e}")

            data["autofill"]["last_version_deduped"]=int(reten_pol_val[0])
            data["extensions"]["last_chrome_version"]=last_chrome_val[0]
            data["web_apps"]["last_preinstall_synchronize_version"]=reten_pol_val[0]
            return data
