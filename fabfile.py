from fabric2 import task, Connection
from invoke import Responder

SSH_TEST_USER_USERNAME = 'igor'
SSH_TEST_USER_PASSWORD = '1'
SSH_NANO_HOST = '192.168.0.113'

connection = Connection(
    SSH_NANO_HOST, user=SSH_TEST_USER_USERNAME, port=22, connect_kwargs={'password': SSH_TEST_USER_PASSWORD}
)
sudopass = Responder(
    pattern=r'\[sudo\] password for {}:'.format(SSH_TEST_USER_USERNAME),
    response=f'{SSH_TEST_USER_PASSWORD}\n',
)
local_sudopass = Responder(
    pattern=r"{0}@{1}\'s password:".format(SSH_TEST_USER_USERNAME, SSH_NANO_HOST),
    response=f'{SSH_TEST_USER_PASSWORD}\n',
)
github_approve_watcher = Responder(
    pattern=r"Are you sure you want to continue connecting (yes/no)?",
    response=f'yes\n',
)


@task
def apt_get_install(ctx, packages):
    _packages = ' '.join(packages)
    connection.run(f'sudo apt-get install -y {_packages}', pty=True, watchers=[sudopass, ])


@task
def git_clone(ctx, uri, params=None):
    _params = ''
    if params:
        _params = '--' + ' --'.join(params)
    connection.run(f'git clone {_params} {uri}', pty=True, watchers=[github_approve_watcher, ])


@task
def pip3_install(ctx, packages, params=None, is_sudo=False):
    _packages = ' '.join(packages)
    if not isinstance(params, list):
        raise Exception("params should be list")
    _params = ''
    if params:
        _params = '-' + ' -'.join(params)
    cmd = f'pip3 install {_params} {_packages}'
    if is_sudo:
        cmd = f'sudo pip3 install {_params} {_packages}'
    connection.run(cmd, pty=True, watchers=[sudopass, ])


@task
def install_pip3(ctx):
    apt_get_install(ctx, ['python3-pip', 'python3-setuptools', ])


@task
def apt_upgrade(ctx):
    connection.run('sudo apt-get -y update', pty=True, watchers=[sudopass, ])
    connection.run('sudo apt-get -y upgrade', pty=True, watchers=[sudopass, ])


@task
def installPostgres(ctx):
    apt_get_install(ctx, ['postgresql', 'libpq-dev'])
    pip3_install(ctx, ['psycopg2==2.8.5', ], params=[])


@task
def inistallRedis(ctx):
    apt_get_install(ctx, ['redis', ])
    pip3_install(ctx, ['redis==3.5.3', ], params=[])


def installDockerCompose(ctx):
    pip3_install(ctx, ['docker-compose==1.26.2', ], params=[], is_sudo=True)


@task
def installOpenCV(ctx):
    git_clone(ctx, 'https://github.com/JetsonHacksNano/buildOpenCV')
    connection.run('cd buildOpenCV')
    connection.run('./buildOpenCV.sh |& tee openCV_build.log')
    connection.run('sudo ldconfig -v', pty=True, watchers=[sudopass, ])
    connection.run('cd ~/')


@task
def installPyTorch(ctx):
    apt_get_install(ctx, ['git', 'cmake', 'libpython3-dev', 'python3-numpy', 'python-matplotlib'])
    git_clone(ctx, uri='https://github.com/dusty-nv/jetson-inference', params=['recursive', ])
    cmd = """
    cd jetson-inference &&
    mkdir build &&
    cd build &&
    cmake ../ &&
    make -j$(nproc) &&
    sudo make install &&
    sudo ldconfig
    """
    connection.run(cmd, pty=True, watchers=[sudopass, ])


@task
def installDetecto(ctx):
    apt_get_install(ctx, [
        'curl', 'libffi-dev', 'python-openssl', 'libssl-dev', 'gcc', 'g++', 'make', 'python3-pip',
        'libhdf5-serial-dev', 'hdf5-tools'
    ])
    pip3_install(ctx, ['Cython==0.29.21', 'Pillow==7.2.0'], params=[])
    pip3_install(ctx, ['git+https://github.com/kuzentio/detecto.git#egg=detecto'], params=['-e'])


@task
def installTorchvision(ctx):
    git_clone(ctx, 'https://github.com/pytorch/vision')
    cmd = """
    cd vision
    export TORCHVISION_PYTORCH_DEPENDENCY_NAME=torch
    sudo python3 setup.py install; cd
    """
    connection.run(cmd, pty=True, watchers=[sudopass, ])


@task
def startCaddyDockerDeamon(ctx):
    cmd = """
    sudo docker run -d \
    --name wages-caddy \
    
    """
    connection.run(cmd, pty=True, watchers=[sudopass, ])


@task
def installNode(ctx):
    cmd = """
    wget https://nodejs.org/dist/v12.13.0/node-v12.13.0-linux-arm64.tar.xz
    tar -xJf node-v12.13.0-linux-arm64.tar.xz
    cd node-v12.13.0-linux-arm64
    sudo cp -R * /usr/local/; cd
    """
    connection.run(cmd, pty=True, watchers=[sudopass, ])


@task
def ssh_scp_local_to_nano(ctx):
    connection.local(
        f'scp ~/.ssh/id_rsa {SSH_TEST_USER_USERNAME}@{SSH_NANO_HOST}:/home/igor/.ssh/',
        pty=True, watchers=[local_sudopass, ]
    )


@task
def copy_local_ssh_to_nano(ctx):
    connection.local(
        f'ssh-copy-id -i ~/.ssh/id_rsa.pub {SSH_TEST_USER_USERNAME}@{SSH_NANO_HOST}',
        pty=True, watchers=[local_sudopass, ]
    )


@task
def install(ctx):
    copy_local_ssh_to_nano(ctx)
    ssh_scp_local_to_nano(ctx)
    git_clone(ctx, "git@github.com:kuzentio/wages.git")
    pip3_install(ctx, params=['r', ], packages=['wages/requirements/nano.txt', ], is_sudo=False)
    with connection.cd("wages"):
        git_clone(ctx, "git@github.com:kuzentio/frontend.git")
        with connection.cd("frontend"):
            connection.run("npm install")


@task
def provision(ctx):
    apt_upgrade(ctx)
    install_pip3(ctx)
    installOpenCV(ctx)
    installPostgres(ctx)
    inistallRedis(ctx)
    installDetecto(ctx)
    installPyTorch(ctx)
    installTorchvision(ctx)
    installDockerCompose(ctx)
    installNode(ctx)
