#!/bin/bash

USR=$SUDO_USER

if [ "$USR" == "" ]; then
  echo "Please run command with 'sudo'"
  exit 0
fi

cd /tmp
mkdir kinst
cd kinst
rm *deb > /dev/null 2>&1

apt-get update -y
apt-get install -y --no-install-recommends openbox pulseaudio freerdp2-x11 gdm3
wget http://images.udsenterprise.com/files/UDSClient/UDS-2.2.1/udsclient_2.2.1_all.deb
dpkg -i udsclient_2.2.1_all.deb > /dev/null 2>&1
apt -y -f install

cd ..
rm -rf kinst

usermod -a -G audio $USR

mv /etc/xdg/openbox/autostart /etc/xdg/openbox/autostart.old
cat > /etc/xdg/openbox/autostart <<EOF
#
# These things are run when an Openbox X Session is started.
# You may place a similar script in $HOME/.config/openbox/autostart
# to run user-specific things.
#

# If you want to use GNOME config tools...
#
#if test -x /usr/lib/x86_64-linux-gnu/gnome-settings-daemon >/dev/null; then
#  /usr/lib/x86_64-linux-gnu/gnome-settings-daemon &
#elif which gnome-settings-daemon >/dev/null 2>&1; then
#  gnome-settings-daemon &
#fi

# If you want to use XFCE config tools...
#
#xfce-mcs-manager &
/usr/bin/chromium-browser http://localhost &
EOF

mv /etc/gdm3/custom.conf /etc/gdm3/custom-old.conf
cat > /etc/gdm3/custom.conf <<EOF
[daemon]
#WaylandEnable=false

# Enabling automatic login
AutomaticLoginEnable = true
AutomaticLogin = $USR

# Enabling timed login
#  TimedLoginEnable = true
#  TimedLogin = user1
#  TimedLoginDelay = 10

[security]

[xdmcp]

[chooser]
EOF

cat > /var/lib/AccountsService/users/$USR <<EOF
[InputSource0]
xkb=es

[User]
XSession=openbox
SystemAccount=false
EOF

#mv /etc/xdg/openbox/menu.xml /etc/xdg/openbox/menu.xml.old
cat > /etc/xdg/openbox/menu.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>

<openbox_menu xmlns="http://openbox.org/"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://openbox.org/
                file:///usr/share/openbox/menu.xsd">

<menu id="root-menu" label="Openbox 3">
  <item label="Web browser">
  e <action name="Execute"><execute>x-www-browser</execute></action>
  </item>
  <separator />
  <item label="Exit">
    <action name="Exit" />
  </item>
</menu>

</openbox_menu>
EOF
