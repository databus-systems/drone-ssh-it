import paramiko
import os
import sys


def check_vargs(vargs):
    """
    Check over the args passed in to make sure that we have everything we
    need for ssh. Exit with code 1 if the input is bad.

    :param dict vargs: Contents of the 'vargs' JSON array in the
        the plugin input.
    """

    host = vargs.get('host', '')
    key_passphrase = vargs.get('key_passphrase', '')
    host = vargs.get('host', '')
    username = vargs.get('username', '')
    password = vargs.get('password', '')

    if not host:
        print("You must specify a host.")
        sys.exit(1)

    if not username:
        print("You must specify the user.")
        sys.exit(1)

    if not key_passphrase and not password:
        print("You must provide a key or password")
        sys.exit(1)


def extract_vargs(payload):
    vargs = {}
    for k in payload:
        if 'PLUGIN_' in k:
            vargs[k.replace('PLUGIN_', '').lower()] = payload[k]
    return vargs


def main():
    payload = os.environ
    vargs = extract_vargs(payload)
    check_vargs(vargs)
    print('********')
    print(payload)
    print('********')

    host = vargs.get('host', '')
    port = vargs.get('port', '')
    p_key = vargs.get('private_key', '')
    passphrase = vargs.get('key_passphrase', '')
    username = vargs.get('username', '')
    password = vargs.get('password', '')
    commands = vargs.get('commands', [])

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko.util.log_to_file("support_scripts.log")

    if p_key:
        with open('temp_key', 'w') as f_key:
            f_key.write(p_key)

        if passphrase:
            key = paramiko.RSAKey.from_private_key(
                open('temp_key', 'r'), password=passphrase)
        else:
            key = paramiko.RSAKey.from_private_key(open('temp_key', 'r'))

        ssh.connect(host, port=int(port), username=username, pkey=key)
    else:
        ssh.connect(host, port=int(port), username=username, password=password)

    if commands:
        stdin, stdout, stderr = ssh.exec_command('\n'.join(commands))
        print('\n'.join(['>' + x for x in commands]))
        print('---STDOUT---')
        print(stdout.read().decode())
        print('---STDERROR---')
        print(stderr.read().decode())


if __name__ == "__main__":
    main()
