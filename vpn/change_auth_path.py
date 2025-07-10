import os
import subprocess

def update_auth_path_in_ovpn(root_dir, new_auth_path):

    count = 0
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".ovpn"):
                full_path = os.path.join(dirpath, file)
                # print(full_path)
                with open(full_path, 'r') as f:
                    lines = f.readlines()

                updated_lines = []
                for line in lines:
                    if line.strip().startswith("auth-user-pass"):
                        updated_lines.append(f"auth-user-pass {new_auth_path}\n")
                        # updated_lines.append(f"{line.strip().replace("/GITLAB",'')}\n")
                    elif line.strip().startswith("script-security 2"):
                        continue
                    elif line.strip().startswith("up /etc/openvpn/update-resolv-conf"):
                        continue
                    elif line.strip().startswith("down /etc/openvpn/update-resolv-conf"):
                        continue
                    elif line.strip().startswith("verb"):
                        continue
                    else:
                        updated_lines.append(line)

                with open(full_path, 'w') as f:
                    f.writelines(updated_lines)

                print(f"✅ Updated: {full_path}")
                count += 1

    print(f"\n🎉 Done! Updated {count} .ovpn files.")

if __name__ =="__main__":
    vpns = ['express','mulvad','nord','pia','proton','pure','sursar','vypr']
    for vpn in vpns:
        vpn_path =os.path.join(os.getcwd(),"vpn",vpn)
        vpn_auth_path =os.path.join(os.getcwd(),"vpn","secrets",vpn)+".txt"
        # vpn_auth_path =vpn_auth_path+".txt"
        subprocess.run(['sudo','chmod','777',vpn_auth_path])
        update_auth_path_in_ovpn(vpn_path,vpn_auth_path)


# script-security 2
# up /etc/openvpn/update-resolv-conf
# down /etc/openvpn/update-resolv-conf
