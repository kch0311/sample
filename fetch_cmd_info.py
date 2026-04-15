import paramiko
from datetime import datetime

# Path to your private key
SSH_KEY_PATH = "/home/youruser/.ssh/id_rsa"

SERVERS = [
    {"host": "******", "user": "ubuntu"},
    {"host": "*****", "user": "ubuntu"},
]

KEYWORDS = ["error", "fail", "warn", "critical"]

def check_server(server):
    issues = []

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Load private key
        key = paramiko.RSAKey.from_private_key_file(SSH_KEY_PATH)

        ssh.connect(
            hostname=server["host"],
            username=server["user"],
            pkey=key,
            timeout=10
        )

        # Run dmesg for last 1 hour
        stdin, stdout, stderr = ssh.exec_command('dmesg --since "1 hour ago"')

        output = stdout.read().decode().lower()

        for line in output.splitlines():
            if any(keyword in line for keyword in KEYWORDS):
                issues.append(line)

        ssh.close()

    except Exception as e:
        issues.append(f"Connection error: {e}")

    return issues


def main():
    for server in SERVERS:
        issues = check_server(server)

        if issues:
            with open("remote_dmesg.log", "a") as f:
                f.write(f"\n[{datetime.now()}] {server['host']}:\n")
                for issue in issues:
                    f.write(issue + "\n")

            print(f"{server['host']} → Issues found")
        else:
            print(f"{server['host']} → No issues")


if __name__ == "__main__":
    main()
