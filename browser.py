import requests, json, random, os, time, zipfile, socket, subprocess, pychrome
from pro_gen import updateme
from fnmatch import fnmatch


class Launch:
    def __init__(self):

        self.userid = "0668"
        self.platform_type = random.choice(["linux", "windows", "macos"])
        self.executablePath = os.path.join(
            os.getcwd(), ".ownbrowser", "browser", "orbita-browser-118", "chrome"
        )
        # self.executablePath = os.path.join(
        #     os.getcwd(), "brave", "browser"
        # )
        self.result_set = updateme(
            platform_type=self.platform_type,
            browser_ver=128,
            latest_fingerprint=random.choice(["False","True"]),
        )
        self.profile_name = self.result_set["gologin"]["name"]
        self.main_path = os.path.join(
            os.getcwd(), "profile_data", f"profile_{self.profile_name}"
        )
        os.makedirs(self.main_path, exist_ok=True)

        # Extract profile ZIP
        zip_path = os.path.join(os.getcwd(), "main.zip")
        if os.path.isfile(zip_path):
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(self.main_path)

        # Write Preferences
        preferences_dir = os.path.join(self.main_path, "Default")
        os.makedirs(preferences_dir, exist_ok=True)
        with open(os.path.join(preferences_dir, "Preferences"), "w") as wrt:
            json.dump(self.result_set, wrt)

        self.launch_browser()

    def callbackfun(self, **kwargs):
        try:
            request_id = kwargs.get("requestId")
            url = kwargs.get("response", {}).get("url", "")
            status = kwargs.get("response", {}).get("status", "")

            if "favicon.ico" in url and str(status) == "403":
                self.block = True

            if "air-booking/page/air/booking/shopping" in url:
                if str(status) == "403":
                    if self.ckclk==0:
                        self.logger_post_count += 1
                    self.ckclk += 1
                    
                elif str(status) == "200":
                    body = self.tab.Network.getResponseBody(requestId=request_id).get(
                        "body", ""
                    )
                    self.postdata(body)
        except Exception as e:
            print(f"callbackfun error: {e}")

    def postdata(self, data):
        for _ in range(5):
            try:
                response = requests.post(
                    "https://aida-dataapi.cloudtsf.com/postdata/",
                    headers={
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
                    },
                    json={
                        "id": int(self.refid),
                        "url": self.load_url1,
                        "data": data,
                        "userid": self.userid,
                        "X-Request-ID": "SW-key-AI-getaccess-P8g7b@62#uHm-23061995-process_thsum",
                    },
                    timeout=10,
                )
                if response.status_code == 200:
                    print("POSTED DATA")
                    self.success = True
                    try:
                        requests.get(
                            "http://localhost:8000/count/py",
                            params={"ref": self.refid, "dd": str(len(data))},
                        )

                    except:
                        pass
                    return
            except Exception as e:
                print(f"postdata error: {e}")

    def getdata(self):
        for _ in range(500):
            try:
                resp = requests.post(
                    "https://aida-dataapi.cloudtsf.com/geturl/",
                    headers={
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
                        "X-Request-ID": "SW-key-AI-getaccess-P8g7b@62#uHm-23061995-process_thsum",
                    },
                    json={"requesturl": "string"},
                    timeout=10,
                )
                print(resp.text)
                if "no result" in resp.text:
                    time.sleep(3)
                    continue
                if resp.status_code == 200:
                    return resp.json()
            except Exception as e:
                print(f"getdata error: {e}")
        return None

    def getRandomPort(self):
        while True:
            port = random.randint(1000, 35000)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                if sock.connect_ex(("127.0.0.1", port)) != 0:
                    return port

    def click_search_button(self):
        try:
            button = self.tab.Runtime.evaluate(
                expression="document.getElementById('flightBookingSubmit')"
            )
            if button.get("result", {}).get("className") == "HTMLButtonElement":
                self.tab.Runtime.evaluate(
                    expression="document.getElementById('flightBookingSubmit').click();"
                )
                print("Clicked search button.")
                return True
        except Exception as e:
            print(f"Click error: {e}")
        return False

    def launch_browser(self):
        self.random_port = self.getRandomPort()
        cmd = [
            f"{self.executablePath}",
            f"--remote-debugging-port={self.random_port}",
            f"--user-data-dir={self.main_path}",
            f"--tz={self.result_set['gologin']['timezone']['id']}",
            f"--gologin-profile={self.profile_name}",
            f"--lang=en-US",
            f"--password-store=basic",
            # "--p"
            f"--load-extension={os.path.join(os.getcwd(),'network_interceptor')}",
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
            # "--no-sandbox"
        ]
        # print (cmd)
        try:
            self.process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            time.sleep(random.uniform(3, 6))
        except Exception as e:
            print(f"Failed to launch browser: {e}")
            return

        self.browser = pychrome.Browser(url=f"http://localhost:{self.random_port}")
        tabs = self.browser.list_tab()
        if not tabs:
            print("No tabs found, exiting.")
            return self.stop()

        self.logger_post_count = 0
        self.block = False

        for hit in range(300):
            try:
                self.tab = self.browser.new_tab()
                self.tab.start()
                self.tab.Network.enable()
                # self.tab.Network.setBlockedURLs(urls=self.blocked_patterns)
                self.tab.Network.responseReceived = self.callbackfun

                getresp = self.getdata()
                if not getresp:
                    break

                self.refid = getresp.get("id")
                self.load_url1 = getresp.get("url")
                if not self.refid or not self.load_url1:
                    break

                self.tab.Page.navigate(url=self.load_url1)
                time.sleep(random.uniform(2.1, 3.6))
                self.success, self.ckclk, total_time = False, 0, 0
                submit_check = True

                while total_time <= 40:
                    print(self.ckclk)
                    if self.block or self.success or self.ckclk >= 2:
                        time.sleep(5)
                        break
                    if submit_check:
                        if self.click_search_button():
                            submit_check = False
                    sleep_time = random.uniform(2.1, 3.6)
                    time.sleep(sleep_time)
                    total_time += sleep_time

                self.tab.stop()
                self.browser.close_tab(self.tab)

                if self.block or self.logger_post_count >= 3:
                    break
            except Exception as e:
                print(f"Error during tab loop: {e}")
                continue

        for tab in self.browser.list_tab():
            try:
                tab.stop()
                self.browser.close_tab(tab)
            except Exception:
                pass

        self.stop()

    def stop(self):
        try:
            if hasattr(self, "process") and self.process.poll() is None:
                self.process.terminate()
                self.process.wait(timeout=5)
                print("Browser process terminated.")
        except Exception as e:
            print(f"Error stopping browser: {e}")


if __name__ == "__main__":
    Launch()
