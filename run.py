import os, random, psutil, threading, time, subprocess
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1280, 720))
display.start()

max_retries = 5  
retry_delay = 3  
thread_count = 2


def kill_chrome(port):
    for process in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        try:
            if 'chrome' in process.info['name'].lower():
                for arg in process.info['cmdline']:
                    if f'--remote-debugging-port={port}' in arg:
                        process.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def run_code_after_vpn_connected(vpn):
    run = Run('browser.py').process_run(thread_count)

def connect_vpn(ovpn_path, auth_file=None, timeout_seconds=6):
    command = ["sudo", "openvpn", "--config", ovpn_path]
    if auth_file:
        command += ["--auth-user-pass", auth_file]

    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    start_time = time.time()

    try:
        while True:

            if time.time() - start_time > timeout_seconds:
                print(f"⏱️ VPN connection timeout after {timeout_seconds} seconds. Retrying...")
                process.terminate()
                process.wait()
                return False

            line = process.stdout.readline()
            if line == '' and process.poll() is not None:
                break

            if "Initialization Sequence Completed" in line:
                print("✅ VPN Connected Successfully!")

                # Run your post-VPN code
                run_code_after_vpn_connected(vpn=ovpn_path)

                # Disconnect VPN after code runs
                print("🔌 Disconnecting VPN...")
                process.terminate()
                process.wait()
                print("🔚 VPN Disconnected after code execution.")
                return True

    except Exception as e:
        print(f"⚠️ Error during VPN connection: {e}")

    finally:
        if process.poll() is None:
            process.terminate()
            process.wait()

    return False


def handle_vpn():
    attempt = 0
    while True:
        vpns = ['proton','nord','express','pia','vypr',] #'mulvad','sursar']
        vpn = random.choice(vpns)
        vpn_dir =os.path.join(os.getcwd(),"vpn",vpn)
        regions = [os.path.join(vpn_dir,i) for i in os.listdir(vpn_dir)]
        region = random.choice(regions)
        vpnfiles = [os.path.join(region,i) for i in os.listdir(region)]
        if vpn != 'mulvad':
            os.system("sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1")
            os.system("sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1")
        else:
            os.system("sudo sysctl -w net.ipv6.conf.all.disable_ipv6=0")
            os.system("sudo sysctl -w net.ipv6.conf.default.disable_ipv6=0")
        # os.system(f'mkdir -p {region.replace('sw/vpn','sw/vpn1')}')
        ovpn_file = random.choice(vpnfiles)
        # os.system('mv '+ovpn_file+' '+region.replace('sw/vpn','sw/vpn1'))
        ## ovpn_file = '/home/ai/GITLAB/sw/ae57.nordvpn.com.udp.ovpn'
        # ovpn_file = ovpn_file.replace('sw/vpn','sw/vpn1')
        print(ovpn_file)
        attempt += 1
        print(f"🔁 Attempt {attempt} to connect to VPN...")

        if connect_vpn(ovpn_file):
            break

        if max_retries and attempt >= max_retries:
            print("❌ Maximum retries reached. Exiting.")
            break

        print(f"⏳ Waiting {retry_delay}s before retrying...")
        time.sleep(retry_delay)


class Run:

    def __init__(self,file):
        self.ports = []
        self.file = file

    def crawl(self, file, proxy=0):
        python = 'python' if os.name == 'nt' else 'python3'
        port = random.randint(1024, 65535)
        self.ports.append(port)
        cmd = f"{python} -W ignore {file} {port} {proxy}"
        print(cmd)
        os.system(cmd)

    def create_thread(self,num_of_thread):
        for i in range(num_of_thread):
            thread = threading.Thread(target=self.crawl, args=(self.file,))
            thread.start()

    def process_run(self, num_of_thread):

        self.create_thread(num_of_thread)

        time_stoped = 0

        while True:

            time.sleep(1)

            current_thread_count = threading.active_count()

            ttl = num_of_thread + 1 - current_thread_count

            if ttl == num_of_thread:
                break
            if ttl == 0:
                time_stoped = 0
            else:
                if time_stoped == 0:
                    time_stoped = time.time()
                    print("stoped time",time_stoped)
                else:
                    if time.time() - time_stoped > 40:
                        print("new thread is creating.........")
                        self.create_thread(ttl)
        kill_chrome(self.ports)



def main():
    handle_vpn()

if __name__ == '__main__':
    main()
    display.stop()