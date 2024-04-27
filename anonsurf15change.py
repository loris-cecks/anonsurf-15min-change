import subprocess
import time
import shlex

def run_command(command):
    try:
        # Adding sudo directly to the command for elevated privileges
        full_command = f"sudo {command}"
        result = subprocess.run(full_command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}': {e.stderr.decode().strip()}")
        return None

def get_anonsurf_ip():
    # Runs the command 'anonsurf myip' to get the current IP address
    return run_command("anonsurf myip")

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}:{:02d}'.format(mins // 60, mins % 60, secs)
        print(f"Time until next IP change: {timer}", end="\r")
        time.sleep(1)
        t -= 1

def main():
    # Start anonsurf
    if run_command("anonsurf start"):
        print("Anonsurf successfully started.")
    else:
        print("Error starting Anonsurf.")
        return
    
    # Wait for 1 minute after starting Anonsurf before fetching IP
    print("Waiting for 1 minute after starting Anonsurf...")
    time.sleep(60)  # Wait for 60 seconds

    # Infinite loop to change IP with anonsurf every 15 minutes
    while True:
        ip = get_anonsurf_ip()
        if ip:
            print(f"Current IP in use: {ip}")
        else:
            print("Error retrieving IP.")
        print("Anonsurf will change IP in 15 minutes...")
        countdown(900)  # Wait for 15 minutes with countdown
        if run_command("anonsurf change"):
            print("IP successfully changed with Anonsurf.")
        else:
            print("Error changing IP with Anonsurf.")

if __name__ == "__main__":
    main()
