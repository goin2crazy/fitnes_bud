import time 
import subprocess

def get_interface_names():
    result = subprocess.run(
        ['netsh', 'interface', 'show', 'interface'],
        capture_output=True, text=True, encoding='cp866'  # <- magic fix 💖
    )
    lines = result.stdout.splitlines()

    interfaces = []

    for line in lines[3:]:  # Skip header rows
        parts = line.strip().split()
        if len(parts) >= 4:
            # The interface name is everything after the first 3 columns
            interface_name = ' '.join(parts[3:])
            interfaces.append(interface_name)

    return interfaces

# 💔 Disable internet
def disable_internet():
    print("Disabling internet now, no distractions for my precious baby~ 💻❌")
    network_names = get_interface_names() 
    for network_name in network_names: 
        try:
            subprocess.run(
                ['netsh', 'interface', 'set', 'interface', network_name, 'disable'],
                check=True
            )
        except subprocess.CalledProcessError:
            print("Assistant couldn’t disable it 😢 Maybe wrong name or no admin rights?")

# 💖 Enable internet
def enable_internet():
    networks_names = get_interface_names() 
    for network_name in networks_names: 
        print("Welcome back, my queen 👑 Re-enabling your internet~ 🌐💕")
        try:
            subprocess.run(
                ['netsh', 'interface', 'set', 'interface', network_name, 'enable'],
                check=True
            )
        except subprocess.CalledProcessError:
            print("Hmm... still couldn’t enable it 🥺 Check if the name is right?")


if __name__ == "__main__": 
    get_interface_names() 

    print("Disabling internet after 5 seconds...")
    time.sleep(5)
    disable_internet() 

    print("Returning internet back after 5 seconds...")
    time.sleep(5)
    enable_internet() 