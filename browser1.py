import requests, json, random, os, time, zipfile, socket, subprocess, pychrome
from pro_gen import updateme
from fnmatch import fnmatch


class Launch:
    def __init__(self):

        self.blocked_patterns = [
            "https://pdx-col.eum-appdynamics.com/eumcollector/beacons/browser/v2/AD-AAB-AAY-BSX/adrum",
            "https://www.uplift-platform.com/*",
            "https://dpm.demdex.net/*",
            "https://cdn.appdynamics.com/adrum/web-vitals/*",
            "https://s.go-mpulse.net/boomerang/*",
            "https://southwestairlines.mpeasylink.com/*",
            "https://ponos.zeronaught.com/*",
            "https://cdn.branch.io/branch-latest.min.js",
            "https://geolocation.onetrust.com/*",
            "https://cdn.cookielaw.org/scripttemplates/*",
            "https://cdn.quantummetrics.com/qscripts/quantum-southwest.js",
            "https://www.uplift-platform.com/*",
            "https://www.southwest.com/di/swadc/beacon/*"
        ]
        self.userid = "0668"
        brow_ver = 128
        self.platform_type = random.choice(["linux", "windows", "macos"])
        self.executablePath = os.path.join(
            os.getcwd(), ".ownbrowser", "browser", "orbita-browser-118", "chrome"
        )
        # self.executablePath = os.path.join(os.getcwd(), "brave", "browser")

        self.result_set = updateme(
            platform_type=self.platform_type,
            browser_ver=brow_ver,
            latest_fingerprint="False",
        )
        self.profile_name = self.result_set["gologin"]["name"]
        print(self.profile_name)
        self.main_path_main = os.path.join(os.getcwd(), "profile_data")
        if self.profile_name:
            self.main_path = os.path.join(
                self.main_path_main, f"profile_{self.profile_name}"
            )
            os.makedirs(self.main_path, exist_ok=True)
            zip_path = os.path.join(os.getcwd(), "main.zip")
            if os.path.isfile(zip_path):
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(self.main_path)
        preferences_dir = os.path.join(self.main_path, "Default")
        os.makedirs(preferences_dir, exist_ok=True)
        self.preferences_path = os.path.join(preferences_dir, "Preferences")
        with open(self.preferences_path, "w") as wrt:
            wrt.write(json.dumps(self.result_set))
        self.logger_post_count = 0
        self.launch_browser()

    def callbackfun(self, **kwargs):
        try:
            request_id = kwargs.get("requestId")
            response_url = kwargs.get("response").get("url")
            if "https://www.southwest.com/favicon.ico" in response_url:
                response_status = kwargs.get("response").get("status")
                if str(response_status) == "403":
                    self.block = True
            if "air-booking/page/air/booking/shopping" in response_url:
                time.sleep(1)
                response_status = kwargs.get("response").get("status")
                if str(response_status) == "403":
                    self.ckclk += 1
                    self.logger_post_count += 1
                if str(response_status) == "200":
                    response_body = self.tab.Network.getResponseBody(
                        requestId=request_id
                    )
                    data = response_body.get("body", "")
                    self.postdata(data)
                    time.sleep(1)
                self.check_url = response_url
        except Exception as e:
            print(f"error {e}")
            pass

    def postdata(self, data):
        for i in range(5):
            headers = {
                "Accept": "application/json",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/json",
                "Origin": "https://www.southwest.com/",
                "Pragma": "no-cache",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "none",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            }
            json_data = {
                "id": int(self.refid),
                "url": self.load_url1,
                "data": data,
                "userid": self.userid,
                "X-Request-ID": "SW-key-AI-getaccess-P8g7b@62#uHm-23061995-process_tajar",
            }
            try:
                response = requests.post(
                    "https://aida-dataapi.cloudtsf.com/postdata/",
                    headers=headers,
                    json=json_data,
                    timeout=10,
                )
                print("POST DATA", response.text)
                if response.status_code == 200:
                    try:
                        self.success = True
                        requests.get(
                            "http://localhost:8000/count/py",
                            params={"ref": self.refid, "dd": str(len(json_data))},
                        )
                    except Exception as e:
                        return
                    return
            except requests.RequestException as e:
                print(f"Error posting data: {e}")

    def getdata(self):
        for i in range(500):
            headers = {
                "Accept": "application/json",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/json",
                "Origin": "https://www.southwest.com/",
                "Pragma": "no-cache",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "none",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                "X-Request-ID": "SW-key-AI-getaccess-P8g7b@62#uHm-23061995-process_tajar",
            }

            json_data = {
                "requesturl": "string",
            }

            try:
                response = requests.post(
                    "https://aida-dataapi.cloudtsf.com/geturl/",
                    headers=headers,
                    json=json_data,
                    timeout=10,
                )
                print("URL Response", response.text)
                if "no result" in response.text:
                    print("Null in get URL")
                    time.sleep(3)
                    continue
                if not response or response.status_code != 200:
                    break
                response_data = json.loads(response.text)
                return response_data
            except requests.RequestException as e:
                print(f"Error getting data: {e}")
                continue
        return None

    def getRandomPort(self):
        while True:
            port = random.randint(1000, 35000)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(("127.0.0.1", port))
            sock.close()
            if result == 0:
                continue
            else:
                return port

    def click_search_button(self):
        print("clicking")
        submit_button = self.tab.Runtime.evaluate(
            expression="""document.getElementById('flightBookingSubmit');"""
        )
        if submit_button and "result" in submit_button:
            result = submit_button["result"]
            # Check if the element is not None and is a button element
            if (
                result.get("type") == "object"
                and result.get("className") == "HTMLButtonElement"
            ):
                self.tab.Runtime.evaluate(
                    expression="""document.getElementById('flightBookingSubmit').click();"""
                )
                print("clicked")
                return True
        return False

    def match_url_pattern(self, url, pattern):
        return fnmatch(url, pattern)

    def intercept_request(self, **kwargs):
        interception_id = kwargs.get("interceptionId")
        request = kwargs.get("request", {})
        url = request.get("url", "")

        for pattern in self.blocked_patterns:
            if self.match_url_pattern(url, pattern):
                print(f"Blocked URL: {url}")
                self.tab.Network.continueInterceptedRequest(
                    interceptionId=interception_id, errorReason="Aborted"
                )
                return

        self.tab.Network.continueInterceptedRequest(interceptionId=interception_id)

    def launch_browser(self):
        self.random_port = self.getRandomPort()
        self.main_path = os.path.join(
            os.getcwd(), "profile_data", f"profile_{self.profile_name}"
        )
        # cmd = [f"{self.executablePath}", f"--remote-debugging-port={self.random_port}", #"--no-sandbox",
        #          f"--remote-allow-origins=*", f"--password-store=basic", f"--user-data-dir={self.main_path}",# f"--user-data-dir={self.main_path}",
        #          f"--tz={self.result_set['gologin']['timezone']['id']}", f"--gologin-profile={self.profile_name}",
        #          f"--lang=en-US"
        #          ]
# /home/ai/GITHUB/Faz/nnew/new/network_interceptor
        cmd = [
            f"{self.executablePath}",
            f"--remote-debugging-port={self.random_port}",
            f"--user-data-dir={self.main_path}",
            f"--tz={self.result_set['gologin']['timezone']['id']}",
            f"--gologin-profile={self.profile_name}",
            f"--lang=en-US",
            f"--password-store=basic",
            f"--load-extension=/home/ai/GITHUB/Faz/nnew/new/network_interceptor",
            "--disable-domain-reliability",
            "--enable-dom-distiller",
            "--enable-distillability-service",
            "--origin-trial-public-key=bYUKPJoPnCxeNvu72j4EmPuK7tr1PAC7SHh8ld9Mw3E=,fMS4mpO6buLQ/QMd+zJmxzty/VQ6B1EUZqoCU04zoRU=",
            "--lso-url=https://no-thanks.invalid",
            "--sync-url=https://sync-v2.brave.com/v2",
            "--variations-server-url=https://variations.brave.com/seed",
            "--variations-insecure-server-url=https://variations.brave.com/seed",
            "--flag-switches-begin",
            "--flag-switches-end",
            "--component-updater=url-source=https://go-updater.brave.com/extensions",
        ]
        try:
            self.process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except Exception as e:
            print(f"Failed to launch browser process: {e}")
            return
        self.pid = self.process.pid
        time.sleep(random.uniform(3, 6))
        self.browser = pychrome.Browser(url=f"http://localhost:{self.random_port}")
        tabs = self.browser.list_tab()
        if not tabs:
            print("No tabs found in browser")
            self.stop()
            return

        # self.tab = self.browser.new_tab()
        # self.tab.start()
        # self.tab.Network.enable()
        # patterns = [{"urlPattern": pattern, "resourceType": "Document", "interceptionStage": "HeadersReceived"}
        #             for pattern in self.blocked_patterns]
        # self.tab.Network.setRequestInterception(patterns=patterns)
        # self.tab.Network.requestIntercepted = self.intercept_request

        # self.tab.Network.setBlockedURLs(urls=self.blocked_patterns)

        # self.tab.Network.responseReceived = self.callbackfun
        self.logger_post_count = 0
        self.block = False
        for hit in range(300):
            self.tab = self.browser.new_tab()
            self.tab.start()
            self.tab.Network.enable()
            # self.tab.Network.setBlockedURLs(urls=self.blocked_patterns)

            self.tab.Network.responseReceived = self.callbackfun
            if self.block:
                break
            getresp = self.getdata()
            if not getresp:
                print("No data received from getdata()")
                break
            self.refid = getresp.get("id")
            self.load_url1 = getresp.get("url")
            if not self.refid or not self.load_url1:
                print("Invalid data received from getdata()")
                break
            print(hit, "-------->", self.refid)

            self.check_url = ""
            self.tab.Page.navigate(url=self.load_url1)
            wait_time = random.uniform(2.1, 3.6)
            time.sleep(wait_time)
            print("url navigated")
            total_time = 0
            submit_check = True
            self.success = False
            self.ckclk = 0
            while True:
                print("clclk",self.ckclk)
                if self.block or self.success or self.ckclk >= 2:
                    break
                print("totaltime", total_time)
                wait_time = random.uniform(2.1, 3.6)
                time.sleep(wait_time)
                total_time += wait_time
                if self.check_url:
                    if submit_check:
                        if self.click_search_button():
                            submit_check = False
                    if total_time > 40:
                        break
            if total_time > 40:
                break
            if self.logger_post_count >= 3 :
                break
            self.tab.stop()
            self.browser.close_tab(self.tab)
        
        tabs = self.browser.list_tab()
        if tabs:
            for i in tabs:
                i.stop()
                self.browser.close_tab(i)
        
        self.stop()

    def stop(self):
        # Terminate the browser process if running
        try:
            if hasattr(self, "process") and self.process.poll() is None:
                self.process.terminate()
                self.process.wait(timeout=5)
                print("Browser process terminated.")
        except Exception as e:
            print(f"Error terminating browser process: {e}")


if __name__ == "__main__":
    obj = Launch()
