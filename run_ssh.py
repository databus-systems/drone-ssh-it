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
    p_key = vargs.get('private_key', '')
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

    if not p_key and not password:
        print("You must provide a password")
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
    print('****PAYLOAD****')
    print(payload)
    print('***************')
    check_vargs(vargs)
    print('check')
    host = vargs.get('host', '')
    port = vargs.get('port', '')
    p_key = vargs.get('private_key', '')
    passphrase = vargs.get('key_passphrase', None)
    username = vargs.get('username', '')
    password = vargs.get('password', '')
    commands = vargs.get('exec_commands', '')

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko.util.log_to_file("support_scripts.log")

    if p_key:
        with open('temp_key', 'w') as f_key:
            f_key.write(p_key)

        ssh.connect(host, port=int(port), username=username, key_filename='temp_key', password=passphrase)
    else:
        ssh.connect(host, port=int(port), username=username, password=password)

    if commands:
        stdin, stdout, stderr = ssh.exec_command(commands.replace(',', '&&'))
        print('\n'.join(['>' + x for x in commands.split(',')]))
        print('---STDOUT---')
        print(stdout.read().decode())
        print('---STDERROR---')
        err = stderr.read()
        print(err.decode())
        if err:
            sys.exit(1)

    ssh.close()

if __name__ == "__main__":
    # os.environ = {'DRONE_BUILD_STARTED': '0', 'PLUGIN_USERNAME': 'costi', 'DRONE_PREV_COMMIT_SHA': '17af977afbb308c791c48bee4b03fb03e2a55f12', 'DRONE_BUILD_CREATED': '1492717443', 'PLUGIN_HOST': '127.0.0.1', 'DRONE_COMMIT_AUTHOR_EMAIL': 'costin.bleotu@databus.systems', 'DRONE_REPO_AVATAR': 'https://git.databus.systems/avatars/3', 'DRONE_JOB_STATUS': 'running', 'DRONE_REPO_OWNER': 'costi', 'DRONE_COMMIT_MESSAGE': 'drone testing5\n', 'DRONE_NETRC_PASSWORD': 'x-oauth-basic', 'DRONE_PREV_BUILD_NUMBER': '14', 'DRONE_BUILD_NUMBER': '15', 'DRONE_YAML_SIGNED': 'true', 'DRONE_PREV_BUILD_STATUS': 'failure', 'DRONE_REMOTE_URL': 'https://git.databus.systems/costi/plugin-test.git', 'DRONE_JOB_FINISHED': '0', 'LANG': 'C.UTF-8', 'DRONE_COMMIT_REF': 'refs/heads/master', 'DRONE_JOB_EXIT_CODE': '0', 'DRONE_BUILD_EVENT': 'push', 'PLUGIN_PORT': '22', 'GPG_KEY': '97FC712E4C024BBEA48A61ED3A5CA953F73C700D', 'DRONE_NETRC_USERNAME': 'a0e14f3aa0d6a80afe58f6fa5bab2483c713978e', 'PYTHON_VERSION': '3.5.3', 'PLUGIN_KEY_PASSPHRASE': 'testtest', 'DRONE_REPO_PRIVATE': 'true', 'DRONE_COMMIT_AUTHOR_AVATAR': 'https://git.databus.systems/avatars/3', 'DRONE_BUILD_FINISHED': '0', 'PYTHON_PIP_VERSION': '9.0.1', 'DRONE_COMMIT_AUTHOR': 'costi', 'PLUGIN_EXEC_COMMANDS': 'ls -al,mkdir /tmp/mega,cd /tmp/mega,touch is_it_in_this_dir', 'DRONE_REPO_TRUSTED': 'false', 'DRONE_BUILD_STATUS': 'success', 'PLUGIN_PRIVATE_KEY': '-----BEGIN EC PRIVATE KEY-----\nProc-Type: 4,ENCRYPTED\nDEK-Info: AES-128-CBC,E5B24E4F20B380F245A8C7B6DDE0A3C7\n\nca9eLtxQ2o68b4f+qmcOWatcZ/d+HFgnF5HWE6apftg8at/5xFE+n7s4t0sEIz5M\nVyco2ZSxXSf7vrfUwMnBnwr8ojpxZ/I34TZJ/RsUA+esaJxUwUrvUIiqDXzzEAgM\nNlvbT2B7Ww3bH4eLyxWtWOAKHW+IGnO97bQRl8WiS78=\n-----END EC PRIVATE KEY-----\n', 'DRONE_REPO_NAME': 'plugin-test', 'DRONE_YAML_VERIFIED': 'true', 'CI': 'drone', 'HOME': '/root', 'DRONE_REPO': 'costi/plugin-test', 'PATH': '/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'DRONE_COMMIT_LINK': 'https://git.databus.systems/costi/plugin-test/compare/17af977afbb308c791c48bee4b03fb03e2a55f12...b52579212a94c71088794fbc8bfb93c29e00c445', 'DRONE_REPO_BRANCH': 'master', 'DRONE_REPO_LINK': 'https://git.databus.systems/costi/plugin-test', 'DRONE_JOB_STARTED': '1492717443', 'DRONE_NETRC_MACHINE': 'git.databus.systems', 'DRONE_COMMIT_SHA': 'b52579212a94c71088794fbc8bfb93c29e00c445', 'DRONE': 'true', 'DRONE_BRANCH': 'master', 'DRONE_BUILD_LINK': 'https://drone.databus.systems/costi/plugin-test/15', 'DRONE_ARCH': 'linux/amd64', 'DRONE_VERSION': '0.5.0+922', 'DRONE_COMMIT_BRANCH': 'master', 'DRONE_REPO_SCM': 'git', 'DRONE_JOB_NUMBER': '1', 'HOSTNAME': '3b0587cd5907', 'DRONE_COMMIT': 'b52579212a94c71088794fbc8bfb93c29e00c445', 'PLUGIN_SSH_COMMANDS': 'ls -al,mkdir /tmp/mega,cd /tmp/mega,touch is_it_in_this_dir'}
    main()
