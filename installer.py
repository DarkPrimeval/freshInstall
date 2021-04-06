import os
import requests
from bs4 import BeautifulSoup


#Install these packages
tool_packages = ['rlwrap', 'xclip', 'ffuf', 'radare2', 'obs-studio']
functional_packages = ['ocl-icd-libopencl1', 'nvidia-cuda-toolkit', 'nvidia-driver', 'apt-transport-https', 'software-properties-common', 'ca-certificates', 'docker-ce']
packages = tool_packages + functional_packages
services = ['docker']
modules = ['pwn']

def apt_key_add():
    os.system('add-apt-repository ppa:obsproject/obs-studio')
    os.system('curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -')
    os.system('echo "deb [arch=amd64] https://download.docker.com/linux/debian stretch stable" | tee /etc/apt/sources.list.d/docker-engi')

def apt_update():
    os.system('apt-get update')
    os.system('apt-get full-upgrade -y')

def apt_install():
    apt_update()
    for package in packages:
        os.system('apt-get install ' + package + ' -y')

def enable_services():
    for service in services:
        os.system('systemctl start' + service)
        os.system('systemctl enable' + service)

def docker_priv():
    os.system('gpasswd -a "${USER}" docker')

def website_downloader(pattern, url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, features="lxml")
    for link in soup.find_all('a'):
        if pattern in link.get('href'):
            return link.get('href')
        else:
            continue

def ghidra_download():
    url = "https://ghidra-sre.org/"
    pattern = "PUBLIC"
    link = website_downloader(pattern, url)
    ghidraPath = '/opt/' + link[:-13]
    if os.path.isdir(ghidraPath):
        print("Deleting Old Ghidra Version")
        os.system('rm -rf ' + ghidraPath)
        os.system('wget '+ url + link)
        os.system('unzip ' + link + ' -d /opt/')
        os.system('rm -rf ' + link)
    else:
        os.system('wget https://ghidra-sre.org/' + link)
        os.system('unzip ' + link + ' -d /opt/')
        os.system('rm -rf ' + link)
    
def obsidian_download():
    url = "https://obsidian.md/download"
    pattern = "amd64.deb"
    link = website_downloader(pattern, url)
    os.system('wget ' + link + ' && dpkg -i obsidian* && rm -rf obsidian*')

def vmware_download():
    os.system('wget --user-agent="Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0" https://www.vmware.com/go/getplayer-linux')
    os.system('chmod +x getplayer-linux && ./getplayer-linux && rm -rf getplayer-linux')

def git_downloads():
    #SecLists
    if os.path.isdir("/opt/seclists"):
        os.system('cd /opt/seclists && git pull origin master')
    else:
        os.system('git clone https://github.com/danielmiessler/SecLists.git /opt/seclists')
    
    #Peass
    if os.path.isdir("/opt/peass"):
        os.system('cd /opt/peass && git pull origin master')
    else:
        os.system('git clone https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite /opt/peass')

def GEF_GDB():
    os.system('wget -q -O- https://github.com/hugsy/gef/raw/master/scripts/gef.sh | sh')

def python_modules():
    for module in modules:
        os.system('echo pip3 install ' + module)

def nvidia_driver():
    with open("/etc/modprobe.d/blacklist-nouveau.conf", "w") as f:
        f.write("blacklist nouveau\nblacklist lbm-nouveau\noptions nouveau modeset=0\nalias nouveau off\nalias lbm-nouveau off")

def reboot_system():
    os.system('shutdown -r now')

apt_key_add()
apt_update()
nvidia_driver()
apt_install()
git_downloads()
obsidian_download()
ghidra_download()
vmware_download()
GEF_GDB()
python_modules()
docker_priv()
enable_services()
