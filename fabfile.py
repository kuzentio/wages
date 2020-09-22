from fabric2 import task, Connection
from invoke import Responder

SSH_TEST_USER_USERNAME = 'igor'
SSH_TEST_USER_PASSWORD = '1'
SSH_NANO_HOST = '192.168.0.111'
POSTGRES_PASSWORD = "root"

connection = Connection(
    SSH_NANO_HOST, user=SSH_TEST_USER_USERNAME, port=22, connect_kwargs={'password': SSH_TEST_USER_PASSWORD}
)
sudopass = [
    Responder(
        pattern=r'\[sudo\] password for {}:'.format(SSH_TEST_USER_USERNAME),
        response=f'{SSH_TEST_USER_PASSWORD}\n',
    ),
    Responder(
        pattern=r'Password:',
        response=f'{SSH_TEST_USER_PASSWORD}\n',
    ),
    Responder(
        pattern=r"{}@{}'s password:".format(SSH_TEST_USER_USERNAME, SSH_NANO_HOST),
        response=f'{SSH_TEST_USER_PASSWORD}\n',
    )
]
local_sudopass = Responder(
    pattern=r"{0}@{1}\'s password:".format(SSH_TEST_USER_USERNAME, SSH_NANO_HOST),
    response=f'{SSH_TEST_USER_PASSWORD}\n',
)
github_approve_watcher = Responder(
    pattern=r"Are you sure you want to continue connecting",
    response=f'yes\n',
)


@task
def apt_get_install(ctx, packages, is_sudo=True):
    _packages = ' '.join(packages)
    cmd = f'apt-get install -y {_packages}'
    if is_sudo:
        cmd = f'sudo apt-get install -y {_packages}'
    connection.run(cmd, pty=True, watchers=sudopass)


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
    connection.run(cmd, pty=True, watchers=sudopass)


@task
def install_pip3(ctx):
    apt_get_install(ctx, ['python3-pip', 'python3-setuptools', ])


@task
def apt_upgrade(ctx):
    connection.run('sudo apt-get update', pty=True, watchers=sudopass)
    connection.run('sudo apt-get -y upgrade', pty=True, watchers=sudopass)


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
    connection.run('sudo ldconfig -v', pty=True, watchers=sudopass)


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
    connection.run(cmd, pty=True, watchers=sudopass)


@task
def installDetecto(ctx):
    apt_get_install(ctx, [
        'curl', 'libffi-dev', 'python-openssl', 'libssl-dev', 'gcc', 'g++', 'make', 'python3-pip',
        'libhdf5-serial-dev', 'hdf5-tools'
    ])
    pip3_install(ctx, ['Cython==0.29.21', 'Pillow==7.2.0'], params=[])
    connection.run(
        'pip3 install -e git+https://github.com/kuzentio/detecto.git#egg=detecto', pty=True, watchers=sudopass
    )


@task
def installTorchvision(ctx):
    git_clone(ctx, 'https://github.com/pytorch/vision')
    cmd = """
    cd vision
    export TORCHVISION_PYTORCH_DEPENDENCY_NAME=torch
    sudo python3 setup.py install; cd
    """
    connection.run(cmd, pty=True, watchers=sudopass)


@task
def installNode(ctx):
    cmd = """
    wget https://nodejs.org/dist/v12.13.0/node-v12.13.0-linux-arm64.tar.xz &&
    tar -xJf node-v12.13.0-linux-arm64.tar.xz &&
    cd node-v12.13.0-linux-arm64 &&
    sudo cp -R * /usr/local/
    """
    connection.run(cmd, pty=True, watchers=sudopass)


@task
def copy_local_ssh_to_nano(ctx):
    connection.local(
        f'ssh-copy-id -i ~/.ssh/id_rsa.pub {SSH_TEST_USER_USERNAME}@{SSH_NANO_HOST}',
        pty=True, watchers=[local_sudopass, ]
    )


@task
def copy_nano_wages_key(ctx):
    connection.local(
        f'scp -r ~/workspace/wages/ssh/nano/ {SSH_TEST_USER_USERNAME}@{SSH_NANO_HOST}:/home/igor/.ssh/', pty=True,
        watchers=sudopass + [github_approve_watcher, ]
    )
    connection.run('chmod 700 ~/.ssh', watchers=sudopass)
    connection.run('chmod 600 ~/.ssh/id_rsa', watchers=sudopass)
    connection.run('chmod 644 ~/.ssh/id_rsa.pub', watchers=sudopass)


@task
def install_wages(ctx):
    copy_nano_wages_key(ctx)
    git_clone(ctx, "git@github.com:kuzentio/wages.git")
    with connection.cd("wages"):
        pip3_install(ctx, params=['r', ], packages=['requirements/nano.txt', ], is_sudo=False)
        git_clone(ctx, "git@github.com:kuzentio/frontend.git")
        with connection.cd("frontend"):
            connection.run("npm install")


@task
def stream_camera_register_task(ctx):
    """
    Warn! Runs only ones on initialization.
    """
    cmd = "gst-launch-1.0 -v nvarguscamerasrc ! 'video/x-raw(memory:NVMM), format=NV12, width=1920, " \
          "height=1080, framerate=30/1' ! nvvidconv ! 'video/x-raw, width=640, height=480, format=I420, " \
          "framerate=30/1' ! videoconvert ! identity drop-allocation=1 ! 'video/x-raw, width=640, height=480, " \
          "format=RGB, framerate=30/1' ! v4l2sink device=/dev/video2"
    connection.run(f'echo "@reboot {cmd}" | crontab -')


def su(command):
    return connection.run(f"sudo su root -c '{command}'", pty=True, watchers=sudopass)


@task
def setup_mipi_camera_virtual_device(ctx):
    with connection.cd('/usr/src/linux-headers-4.9.140-tegra-ubuntu18.04_aarch64/kernel-4.9'):
        su('mkdir v4l2loopback')
        su('git clone https://github.com/umlaeute/v4l2loopback.git v4l2loopback')
        with connection.cd('v4l2loopback'):
            su('git checkout -b v0.10.0')
            su('make')
            su('make install')
            su('apt-get install -y v4l2loopback-dkms v4l2loopback-utils')
            su('modprobe v4l2loopback devices=1 video_nr=2 exclusive_caps=1')
            su('echo options v4l2loopback devices=1 video_nr=2 exclusive_caps=1 > /etc/modprobe.d/v4l2loopback.conf')
            su('echo v4l2loopback > /etc/modules')
            su('update-initramfs -u')


@task
def remove_pink_tint_from_camera_module(ctx):
    connection.run('wget https://www.waveshare.com/w/upload/e/eb/Camera_overrides.tar.gz')
    connection.run('tar zxvf Camera_overrides.tar.gz')
    connection.run(
        'sudo cp camera_overrides.isp /var/nvidia/nvcam/settings/', pty=True, watchers=sudopass
    )
    connection.run(
        'sudo chmod 664 /var/nvidia/nvcam/settings/camera_overrides.isp', pty=True, watchers=sudopass
    )
    connection.run(
        'sudo chown root:root /var/nvidia/nvcam/settings/camera_overrides.isp', pty=True, watchers=sudopass
    )


@task
def init_db(ctx):
    connection.run('sudo -u postgres psql -t -A -c "CREATE DATABASE wages;"', pty=True, watchers=sudopass)


@task
def set_postgres_password(ctx):
    connection.run(
        f'sudo -u postgres psql -t -A -c "ALTER USER postgres WITH PASSWORD \'{POSTGRES_PASSWORD}\';"',
        pty=True, watchers=sudopass
    )


@task
def provision(ctx):
    apt_upgrade(ctx)
    setup_mipi_camera_virtual_device(ctx)
    remove_pink_tint_from_camera_module(ctx)

    install_pip3(ctx)
    installOpenCV(ctx)
    installPostgres(ctx)
    inistallRedis(ctx)
    installPyTorch(ctx)
    installTorchvision(ctx)
    installDetecto(ctx)
    installDockerCompose(ctx)
    installNode(ctx)
    stream_camera_register_task(ctx)
    install_wages(ctx)
    init_db(ctx)
    set_postgres_password(ctx)
    connection.run("sudo reboot", pty=True, watchers=sudopass)
