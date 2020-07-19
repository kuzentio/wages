from fabric2 import task, Connection
from invoke import Responder

SSH_TEST_USER_USERNAME = 'igor'
SSH_TEST_USER_PASSWORD = '1'

connection = Connection(
    '192.168.0.113', user='igor', port=22, connect_kwargs={'password': SSH_TEST_USER_PASSWORD}
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
def sudo_pip3_install(ctx, packages):
    _packages = ' '.join(packages)
    connection.run(f'sudo pip3 install {_packages}', pty=True, watchers=[sudopass, ])


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
def nistallRedis(ctx):
    apt_get_install(ctx, ['redis', ])
    connection.run('pip3 install redis')


@task
def installOpenCV(ctx):
    connection.run('git clone https://github.com/JetsonHacksNano/buildOpenCV')
    connection.run('cd buildOpenCV')
    connection.run('./buildOpenCV.sh |& tee openCV_build.log')
    connection.run('sudo ldconfig -v', pty=True, watchers=[sudopass, ])
    connection.run('cd ~/')


@task
def installPyTorch(ctx):
    cmd = """
    sudo apt-get update &&
    sudo apt-get install -y git cmake libpython3-dev python3-numpy python-matplotlib &&
    git clone --recursive https://github.com/dusty-nv/jetson-inference &&
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
    cmd = """
    sudo apt-get install -y curl libffi-dev python-openssl libssl-dev gcc g++ make python3-pip libhdf5-serial-dev hdf5-tools &&
    pip3 install Cython &&
    pip3 install Pillow &&
    pip3 install -e git+https://github.com/kuzentio/detecto.git#egg=detecto
    """
    connection.run(cmd, pty=True, watchers=[sudopass, ])


@task
def provision(ctx):
    apt_upgrade(ctx)
    install_pip3(ctx)
    installOpenCV(ctx)
    installPostgres(ctx)
    nistallRedis(ctx)
    installPyTorch(ctx)
    installDetecto(ctx)
