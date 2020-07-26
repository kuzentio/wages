from fabric2 import task, Connection
from invoke import Responder

SSH_TEST_USER_USERNAME = 'igor'
SSH_TEST_USER_PASSWORD = '1'

connection = Connection(
    '192.168.0.113', user=SSH_TEST_USER_USERNAME, port=22, connect_kwargs={'password': SSH_TEST_USER_PASSWORD}
)
sudopass = Responder(
    pattern=r'\[sudo\] password for {}:'.format(SSH_TEST_USER_USERNAME),
    response=f'{SSH_TEST_USER_PASSWORD}\n',
)


@task
def apt_get_install(ctx, packages):
    _packages = ' '.join(packages)
    connection.run(f'sudo apt-get install -y {_packages}', pty=True, watchers=[sudopass, ])


@task
def git_clone(ctx, uri, args=list):
    _args = ''
    if args:
        _args = '--' + ' --'.join(list(args))
    connection.run(f'git clone {_args} {uri}', pty=True, watchers=[sudopass, ])


@task
def pip3_install(ctx, packages, args=list, is_sudo=False):
    _packages = ' '.join(packages)
    _args = ''
    if args:
        _args = '-' + ' -'.join(list(args))
    cmd = f'pip3 {_args} install {_packages}'
    if is_sudo:
        cmd = f'sudo pip3 {_args} install {_packages}'
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
    connection.run('pip3 install psycopg2')


@task
def inistallRedis(ctx):
    apt_get_install(ctx, ['redis', ])
    connection.run('pip3 install redis')


@task
def installOpenCV(ctx):
    git_clone('https://github.com/JetsonHacksNano/buildOpenCV')
    connection.run('cd buildOpenCV')
    connection.run('./buildOpenCV.sh |& tee openCV_build.log')
    connection.run('sudo ldconfig -v', pty=True, watchers=[sudopass, ])
    connection.run('cd ~/')


@task
def installPyTorch(ctx):
    apt_get_install(ctx, ['git', 'cmake', 'libpython3-dev', 'python3-numpy', 'python-matplotlib'])
    git_clone('https://github.com/dusty-nv/jetson-inference', args=['recursive', ])
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
    apt_get_install([
        'curl', 'libffi-dev', 'python-openssl', 'libssl-dev', 'gcc', 'g++', 'make', 'python3-pip',
        'libhdf5-serial-dev', 'hdf5-tools'
    ])
    pip3_install(['Cython==0.29.21', 'Pillow==7.2.0'])
    pip3_install(['git+https://github.com/kuzentio/detecto.git#egg=detecto'], args=['-e'])


@task
def installTorchvision(ctx):
    git_clone('https://github.com/pytorch/vision')
    cmd = """
    cd vision
    export TORCHVISION_PYTORCH_DEPENDENCY_NAME=torch
    sudo python3 setup.py install; cd
    """
    connection.run(cmd, pty=True, watchers=[sudopass, ])


# @task
# def startCaddyDockerDeamon(ctx):
#     cmd = """
#     sudo docker run -d \
#     --name wages-caddy \
#     -p 80:8000 \
#     -v /var/www/html:/frontend/build \
#     elswork/arm-caddy:latest
#     """
#     connection.run(cmd, pty=True, watchers=[sudopass, ])


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
def provision(ctx):
    apt_upgrade(ctx)
    install_pip3(ctx)
    installOpenCV(ctx)
    installPostgres(ctx)
    inistallRedis(ctx)
    installDetecto(ctx)
    installPyTorch(ctx)
    installTorchvision(ctx)
    installNode(ctx)
