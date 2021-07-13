import os
import requests
from bs4 import BeautifulSoup


#Install these packages
tool_packages = ['rlwrap', 'xclip', 'ffuf', 'radare2', 'obs-studio', 'exploitdb']
functional_packages = ['ocl-icd-libopencl1', 'nvidia-cuda-toolkit', 'nvidia-driver' ]
packages = tool_packages + functional_packages
modules = ['pwn']
docker_packages = ['curl', 'apt-transport-https', 'software-properties-common', 'ca-certificates', 'docker.io']

#Install docker
def docker_install():   
    apt_update()
    for package in docker_packages:
        os.system('sudo apt-get install %s -y' % package)
    os.system('sudo systemctl enable docker.service')
    os.system('sudo systemctl start docker.service')
    os.system('sudo gpasswd -a "${USER}" docker')

#Update the OS
def apt_update():
    os.system('sudo apt-get update')
    os.system('sudo apt-get full-upgrade -y')

#Install packages listed above.
def apt_install():
    apt_update()
    for package in packages:
        os.system('sudo apt-get install %s -y' % package)

#Download function
def website_downloader(pattern, url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, features="lxml")
    for link in soup.find_all('a'):
        if pattern in link.get('href'):
            return link.get('href')
        else:
            continue


#Download and install latest ghidra version.
def ghidra_download():
    url = "https://ghidra-sre.org/"
    pattern = "PUBLIC"
    link = website_downloader(pattern, url)
    ghidraPath = '/opt/' + link[:-13]
    if os.path.isdir(ghidraPath):
        print("Deleting Old Ghidra Version")
        os.system('sudo rm -rf %s' % ghidraPath)
        os.system('sudo wget %s %s' % (url, link))
        os.system('sudo unzip %s -d /opt/' % link)
        os.system('sudo rm -rf %s' % link)
    else:
        os.system('sudo wget https://ghidra-sre.org/' + link)
        os.system('sudo unzip %s -d /opt/' % link)
        os.system('sudo rm -rf %s' % link)

#Download and instlal latest obsidian version.    
def obsidian_download():
    url = "https://obsidian.md/download"
    pattern = "amd64.deb"
    link = website_downloader(pattern, url)
    os.system('wget %s && sudo dpkg -i obsidian* && rm -rf obsidian*' % link)


#Download and install latest VMWare
def vmware_download():
    os.system('wget --user-agent="Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0" https://www.vmware.com/go/getworkstation-linux')
    os.system('chmod +x getworkstation-linux && ./getworkstation-linux && rm -rf getworkstation-linux')



#GitHub.com Downloads
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
    os.system('wget -q -O- https://github.com/hugsy/gef/raw/master/scripts/gef.sh | bash')

def python_modules():
    for module in modules:
        os.system('pip3 install %s' % module)

def nvidia_driver():
    with open("/etc/modprobe.d/blacklist-nouveau.conf", "w") as f:
        f.write("blacklist nouveau\nblacklist lbm-nouveau\noptions nouveau modeset=0\nalias nouveau off\nalias lbm-nouveau off")

def reboot_system():
    os.system('shutdown -r now')

choice = True
while choice:
    try:
        
        print("""
        1. apt_update
        2. apt_install
        3. docker_install
        4. nvidia_driver
        5. git_downloads
        6. obsidian_download
        7. ghidra_download
        8. vmware_download
        9. GEF_GDB
        10. python_modules
        """)
        commands = list()
        choice = str(input("Please enter the numbers delimited by a , (IE 1,3,5) or type \"all\" for everything or use -# (IE -7) to skip an install: "))

        if choice.lower == "all":  
            apt_update()
            apt_install()
            docker_install()
            nvidia_driver()
            git_downloads()
            obsidian_download()
            ghidra_download()
            vmware_download()
            GEF_GDB()
            python_modules()
        elif "-" in choice:
            for i in range(1, 10):
                if str(i) in choice:
                    pass
                else:
                    commands.append(i)
            pass
        elif "," in choice or len(choice) == 1:
            for i in choice.split(","):
                commands.append(i)
        elif choice == "exit":
            break
        else:
            print("Invalid Options")
        for i in commands:
            print(type(i))
            i = str(i)
            if i == "1":
                apt_update()
            if i == "2":
                apt_install()
            if i == "3":
                docker_install()
            if i == "4":
                nvidia_driver()
            if i == "5":
                git_downloads()
            if i == "6":
                obsidian_download()
            if i == "7":
                ghidra_download()
            if i == "8":
                vmware_download()
            if i == "9":
                GEF_GDB()
            if i == "10":
                python_modules()
    except:
        print("Error")
