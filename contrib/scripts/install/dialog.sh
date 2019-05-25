#!/bin/bash
#
# Copyright (c) 2017 Igor Pecovnik, igor.pecovnik@gma**.com
#
# This file is licensed under the terms of the GNU General Public
# License version 2. This program is licensed "as is" without any
# warranty of any kind, whether express or implied.

# Functions:
# check_status
# choose_webserver
# server_conf
# install_packet
# alive_port
# alive_process
# install_basic
# create_ispconfig_configuration
# install_cups
# install_samba
# install_omv
# install_tvheadend
# install_urbackup
# install_transmission
# install_transmission_seed_armbian_torrents
# install_syncthing
# install_vpn_server
# install_vpn_client
# install_DashNTP
# install_MySQL
# install_MySQLDovecot
# install_Virus
# install_hhvm
# install_phpmyadmin
# install_apache
# install_nginx
# install_PureFTPD
# install_Bind
# install_Stats
# install_Jailkit
# install_Fail2BanDovecot
# install_Fail2BanRulesDovecot
# install_ISPConfig
# check_if_installed

#
# load functions, local first
#
if  [[ -f debian-config-jobs ]]; then source debian-config-jobs;
    elif  [[ -f /usr/lib/armbian-config/jobs.sh ]]; then source /usr/lib/armbian-config/jobs.sh;
    else exit 1;
fi

if  [[ -f debian-config-submenu ]]; then source debian-config-submenu;
    elif  [[ -f /usr/lib/armbian-config/submenu.sh ]]; then source /usr/lib/armbian-config/submenu.sh;
    else exit 1;
fi

if  [[ -f debian-config-functions ]]; then source debian-config-functions;
    elif  [[ -f /usr/lib/armbian-config/functions.sh ]]; then source /usr/lib/armbian-config/functions.sh;
    else exit 1;
fi

if  [[ -f debian-config-functions-network ]]; then source debian-config-functions-network;
    elif  [[ -f /usr/lib/armbian-config/functions-network.sh ]]; then source /usr/lib/armbian-config/functions-network.sh;
    else exit 1;
fi




#
# not sure if needed
#
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin




function check_status
{
#
# Check if service is already installed and show it's status
#

dialog --backtitle "$BACKTITLE" --title "Please wait" --infobox "\nLoading install info ... " 5 28
LIST=()
LIST_CONST=3

# Samba
SAMBA_STATUS="$(check_if_installed samba && echo "on" || echo "off" )"
alive_port "Windows compatible file sharing" "445" "boolean"
LIST+=( "Samba" "$DESCRIPTION" "$SAMBA_STATUS" )

# CUPS
CUPS_STATUS="$(check_if_installed cups && echo "on" || echo "off" )"
alive_port "Common UNIX Printing System (CUPS)" "631" "boolean"
LIST+=( "CUPS" "$DESCRIPTION" "$CUPS_STATUS" )

# TV headend
TVHEADEND_STATUS="$(check_if_installed tvheadend && echo "on" || echo "off" )"
alive_port "TV streaming server" "9981"
LIST+=( "TV headend" "$DESCRIPTION" "$TVHEADEND_STATUS" )

# Synthing
SYNCTHING_STATUS="$([[ -d /usr/bin/syncthing ]] && echo "on" || echo "off" )"
alive_port "Personal cloud @syncthing.net" "8384" "boolean"
LIST+=( "Syncthing" "$DESCRIPTION" "$SYNCTHING_STATUS" )

# Mayan EDMS
MAYAN_STATUS="$( [[ -d /opt/mayan ]] && echo "on" || echo "off" )"
alive_port "Electronic Document Management System" "8000" "boolean"
LIST+=( "Mayan EDMS" "$DESCRIPTION" "$MAYAN_STATUS" )

# Exagear
if [[ "$(check_if_installed xserver-xorg && echo "on")" == "on" && "$family" == "Ubuntu" ]]; then
    EXAGEAR_STATUS="$(check_if_installed exagear-armbian && echo "on" || echo "off" )"
    LIST+=( "ExaGear" "32bit x86 Linux/Windows emulator trial" "$EXAGEAR_STATUS" )
fi

if [[ "$(dpkg --print-architecture)" == "armhf" || "$(dpkg --print-architecture)" == "amd64" ]]; then
    LIST_CONST=2
    # vpn server
    VPN_SERVER_STATUS="$([[ -d /usr/local/vpnserver ]] && echo "on" || echo "off" )"
    LIST+=( "VPN server" "Softether VPN server" "$VPN_SERVER_STATUS" )
    # vpn client
    VPN_CLIENT_STATUS="$([[ -d /usr/local/vpnclient ]] && echo "on" || echo "off" )"
    LIST+=( "VPN client" "Softether VPN client" "$VPN_CLIENT_STATUS" )
fi
# NCP
NCP_STATUS="$( [[ -d /var/www/nextcloud ]] && echo "on" || echo "off" )"
[[ "$family" != "Ubuntu" ]] && LIST+=( "NCP" "Nextcloud personal cloud" "$NCP_STATUS" )
# OMV
OMV_STATUS="$(check_if_installed openmediavault && echo "on" || echo "off" )"
[[ "$family" != "Ubuntu" ]] && LIST+=( "OMV" "OpenMediaVault NAS solution" "$OMV_STATUS" ) && LIST_CONST=3

# Plex media server
PLEX_STATUS="$((check_if_installed plexmediaserver || check_if_installed plexmediaserver-installer) && echo "on" || echo "off" )"
alive_port "Plex media server" "32400"
LIST+=( "Plex" "$DESCRIPTION" "$PLEX_STATUS" )

# Radarr
RADARR_STATUS="$([[ -d /opt/Radarr ]] && echo "on" || echo "off" )"
alive_port "Movies downloading server" "7878"
LIST+=( "Radarr" "$DESCRIPTION" "$RADARR_STATUS" )

# Sonarr
SONARR_STATUS="$([[ -d /opt/NzbDrone ]] && echo "on" || echo "off" )"
alive_port "TV shows downloading server" "8989"
LIST+=( "Sonarr" "$DESCRIPTION" "$SONARR_STATUS" )

# MINIdlna
MINIDLNA_STATUS="$(check_if_installed minidlna && echo "on" || echo "off" )"
alive_port "Lightweight DLNA/UPnP-AV server" "8200" "boolean"
LIST+=( "Minidlna" "$DESCRIPTION" "$MINIDLNA_STATUS" )

# Pi hole
PI_HOLE_STATUS="$([[ -d /etc/pihole ]] && echo "on" || echo "off" )"
alive_process "Ad blocker" "pihole-FTL"
LIST+=( "Pi hole" "$DESCRIPTION" "$PI_HOLE_STATUS" )

# Transmission
TRANSMISSION_STATUS="$(check_if_installed transmission-daemon && echo "on" || echo "off" )"
alive_port "Torrent download server" "9091" "boolean"
LIST+=( "Transmission" "$DESCRIPTION" "$TRANSMISSION_STATUS" )


# UrBackup
URBACKUP_STATUS="$((check_if_installed urbackup-server || check_if_installed urbackup-server-dbg) && echo "on" || echo "off" )"
alive_port "Client/server backup system" "51413" "boolean"
LIST+=( "UrBackup" "$DESCRIPTION" "$URBACKUP_STATUS" )


# ISPconfig
ISPCONFIG_STATUS="$([[ -d /usr/local/ispconfig ]] && echo "on" || echo "off" )"
LIST+=( "ISPConfig" "SMTP mail, IMAP, POP3 & LAMP/LEMP web server" "$ISPCONFIG_STATUS" )
}




function choose_webserver
{
#
# Target web server selection
#
check_if_installed openmediavault
case $? in
    0)
        # OMV installed, prevent switching from nginx to apache which would trash OMV installation
        server="nginx"
        ;;
    *)
        dialog --title "Choose a webserver" --backtitle "$BACKTITLE" --yes-label "Apache" --no-label "Nginx" \
        --yesno "\nChoose a web server which you are familiar with. They both work almost the same." 8 70
        response=$?
        case $response in
            0) server="apache";;
            1) server="nginx";;
            255) exit;;
        esac
        ;;
esac
}




function server_conf
{
#
# Add some reqired date for installation
#
exec 3>&1
dialog --title "Server configuration" --separate-widget $'\n' --ok-label "Install" --backtitle "$BACKTITLE" \
--form "\nPlease fill out this form:\n " \
12 70 0 \
"Your FQDN for $serverip:"  1 1 "$hostnamefqdn"         1 31 32 0 \
"Mysql root password:"      2 1 "$mysql_pass"                   2 31 32 0 \
2>&1 1>&3 | {

read -r hostnamefqdn
read -r mysql_pass
echo $mysql_pass > ${TEMP_DIR}/mysql_pass
echo $hostnamefqdn > ${TEMP_DIR}/hostnamefqdn
# end
}
exec 3>&-
# read variables back
read MYSQL_PASS < ${TEMP_DIR}/mysql_pass
read HOSTNAMEFQDN < ${TEMP_DIR}/hostnamefqdn
}




install_packet ()
{
#
# Install missing packets
#
i=0
j=1
IFS=" "
declare -a PACKETS=($1)
#skupaj=$(apt-get -s -y -qq install $1 | wc -l)
skupaj=${#PACKETS[@]}
while [[ $i -lt $skupaj ]]; do
procent=$(echo "scale=2;($j/$skupaj)*100"|bc)
        x=${PACKETS[$i]}
        if [ $(dpkg-query -W -f='${Status}' $x 2>/dev/null | grep -c "ok installed") -eq 0 ]; then
            printf '%.0f\n' $procent | dialog \
            --backtitle "$BACKTITLE" \
            --title "Installing" \
            --gauge "\n$2\n\n$x" 10 70
        if [ "$(DEBIAN_FRONTEND=noninteractive apt-get -qq -y install $x >${TEMP_DIR}/install.log 2>&1 || echo 'Installation failed' \
        | grep 'Installation failed')" != "" ]; then
            echo -e "[\e[0;31m error \x1B[0m] Installation failed"
            tail ${TEMP_DIR}/install.log
            exit
        fi
        fi
        i=$[$i+1]
        j=$[$j+1]
done
echo ""
}


alive_port ()
{
#
# Displays URL to the service $1 on port $2 or just that is active if $3 = boolean
#
DEFAULT_ADAPTER=$(ip -4 route ls | grep default | grep -Po '(?<=dev )(\S+)')
LOCALIPADD=$(ip -4 addr show dev $DEFAULT_ADAPTER | awk '/inet/ {print $2}' | cut -d'/' -f1)
if [[ -n $(netstat -lnt | awk '$6 == "LISTEN" && $4 ~ ".'$2'"') ]]; then
    if [[ $3 == boolean ]]; then
        DESCRIPTION="$1 is \Z1active\Z0";
        else
        DESCRIPTION="Active on http://${LOCALIPADD}:\Z1$2\Z0";
    fi
else
DESCRIPTION="$1";
fi
}



alive_process ()
{
#
# check if process name $2 is running. Display it's name $1 or $1 is active if active
#
if pgrep -x "$2" > /dev/null 2>&1; then DESCRIPTION="$1 is \Z1active\Z0"; else DESCRIPTION="$1"; fi
}







install_basic (){
#
# Set hostname, FQDN, add to sources list
#
IFS=" "
set ${HOSTNAMEFQDN//./ }
HOSTNAMESHORT="$1"
cp /etc/hosts /etc/hosts.backup
cp /etc/hostname /etc/hostname.backup
# create new
echo "127.0.0.1   localhost.localdomain   localhost" > /etc/hosts
echo "${serverIP} ${HOSTNAMEFQDN} ${HOSTNAMESHORT} #ispconfig " >> /etc/hosts
echo "$HOSTNAMESHORT" > /etc/hostname
/etc/init.d/hostname.sh start >/dev/null 2>&1
hostnamectl set-hostname $HOSTNAMESHORT
if [[ $family == "Ubuntu" ]]; then
    # set hostname in Ubuntu
    hostnamectl set-hostname $HOSTNAMESHORT
    # disable AppArmor
    if [[ -n $(service apparmor status | grep -w active | grep -w running) ]]; then
        service apparmor stop
        update-rc.d -f apparmor remove
        apt-get -y -qq remove apparmor apparmor-utils
    fi
else
    grep -q "contrib" /etc/apt/sources.list || sed -i 's|main|main contrib|' /etc/apt/sources.list
    grep -q "non-free" /etc/apt/sources.list || sed -i 's|contrib|contrib non-free|' /etc/apt/sources.list
    grep -q "deb http://ftp.debian.org/debian jessie-backports main" /etc/apt/sources.list || echo "deb http://ftp.debian.org/debian jessie-backports main" >> /etc/apt/sources.list
    debconf-apt-progress -- apt-get update
fi
}




create_ispconfig_configuration (){
#
# ISPConfig autoconfiguration
#
cat > ${TEMP_DIR}/isp.conf.php <<EOF
<?php
\$autoinstall['language'] = 'en'; // de, en (default)
\$autoinstall['install_mode'] = 'standard'; // standard (default), expert

\$autoinstall['hostname'] = '$HOSTNAMEFQDN'; // default
\$autoinstall['mysql_hostname'] = 'localhost'; // default: localhost
\$autoinstall['mysql_root_user'] = 'root'; // default: root
\$autoinstall['mysql_root_password'] = '$MYSQL_PASS';
\$autoinstall['mysql_database'] = 'dbispconfig'; // default: dbispcongig
\$autoinstall['mysql_charset'] = 'utf8'; // default: utf8
\$autoinstall['mysql_port'] = '3306'; // default: 3306
\$autoinstall['configure_jailkit'] = 'y'; // y (default), n
\$autoinstall['configure_firewall'] = 'y'; // y (default), n
\$autoinstall['configure_$server'] = 'y'; // y (default), n
\$autoinstall['configure_dns'] = 'y'; // y (default), n
\$autoinstall['http_server'] = '$server'; // y (default), n
\$autoinstall['ispconfig_port'] = '8080'; // default: 8080
\$autoinstall['ispconfig_admin_password'] = '1234'; // default: 1234
\$autoinstall['ispconfig_use_ssl'] = 'y'; // y (default), n

/* SSL Settings */
\$autoinstall['ssl_cert_country'] = 'AU';
\$autoinstall['ssl_cert_state'] = 'Some-State';
\$autoinstall['ssl_cert_locality'] = 'Chicago';
\$autoinstall['ssl_cert_organisation'] = 'Internet Widgits Pty Ltd';
\$autoinstall['ssl_cert_organisation_unit'] = 'IT department';
\$autoinstall['ssl_cert_common_name'] = \$autoinstall['hostname'];
\$autoinstall['ssl_cert_email'] = 'joe@lamer.com';
?>
EOF
}



install_cups ()
{
#
# Install printer system
#
debconf-apt-progress -- apt-get -y install cups lpr cups-filters
# cups-filters if jessie
sed -e 's/Listen localhost:631/Listen 631/g' -i /etc/cups/cupsd.conf
sed -e 's/<Location \/>/<Location \/>\nallow $SUBNET/g' -i /etc/cups/cupsd.conf
sed -e 's/<Location \/admin>/<Location \/admin>\nallow $SUBNET/g' -i /etc/cups/cupsd.conf
sed -e 's/<Location \/admin\/conf>/<Location \/admin\/conf>\nallow $SUBNET/g' -i /etc/cups/cupsd.conf
service cups restart
service samba restart | service smbd restart >/dev/null 2>&1
}




install_samba ()
{
#
# install Samba file sharing
#
local SECTION="Samba"
SMBUSER=$(whiptail --inputbox "What is your samba username?" 8 78 $SMBUSER --title "$SECTION" 3>&1 1>&2 2>&3)
exitstatus=$?; if [ $exitstatus = 1 ]; then exit 1; fi
SMBPASS=$(whiptail --inputbox "What is your samba password?" 8 78 $SMBPASS --title "$SECTION" 3>&1 1>&2 2>&3)
exitstatus=$?; if [ $exitstatus = 1 ]; then exit 1; fi
SMBGROUP=$(whiptail --inputbox "What is your samba group?" 8 78 $SMBGROUP --title "$SECTION" 3>&1 1>&2 2>&3)
exitstatus=$?; if [ $exitstatus = 1 ]; then exit 1; fi
#
debconf-apt-progress -- apt-get -y install samba samba-common-bin samba-vfs-modules
useradd $SMBUSER
echo -ne "$SMBPASS\n$SMBPASS\n" | passwd $SMBUSER >/dev/null 2>&1
echo -ne "$SMBPASS\n$SMBPASS\n" | smbpasswd -a -s $SMBUSER >/dev/null 2>&1
service samba stop | service smbd stop >/dev/null 2>&1
cp /etc/samba/smb.conf /etc/samba/smb.conf.stock
cat > /etc/samba/smb.conf.tmp << EOF
[global]
    workgroup = SMBGROUP
    server string = %h server
    hosts allow = SUBNET
    log file = /var/log/samba/log.%m
    max log size = 1000
    syslog = 0
    panic action = /usr/share/samba/panic-action %d
    load printers = yes
    printing = cups
    printcap name = cups
    min receivefile size = 16384
    write cache size = 524288
    getwd cache = yes
    socket options = TCP_NODELAY IPTOS_LOWDELAY

[printers]
    comment = All Printers
    path = /var/spool/samba
    browseable = no
    public = yes
    guest ok = yes
    writable = no
    printable = yes
    printer admin = SMBUSER

[print$]
    comment = Printer Drivers
    path = /etc/samba/drivers
    browseable = yes
    guest ok = no
    read only = yes
    write list = SMBUSER

[ext]
    comment = Storage
    path = /ext
    writable = yes
    public = no
    valid users = SMBUSER
    force create mode = 0644
EOF
sed -i "s/SMBGROUP/$SMBGROUP/" /etc/samba/smb.conf.tmp
sed -i "s/SMBUSER/$SMBUSER/" /etc/samba/smb.conf.tmp
sed -i "s/SUBNET/$SUBNET/" /etc/samba/smb.conf.tmp
dialog --backtitle "$BACKTITLE" --title "Review samba configuration" --no-collapse --editbox /etc/samba/smb.conf.tmp 30 0 2> /etc/samba/smb.conf.tmp.out
if [[ $? = 0 ]]; then
    mv /etc/samba/smb.conf.tmp.out /etc/samba/smb.conf
    install -m 755 -g $SMBUSER -o $SMBUSER -d /ext
    service service smbd stop >/dev/null 2>&1
    sleep 3
    service service smbd start >/dev/null 2>&1
fi
}

install_ncp (){
    curl -sSL https://raw.githubusercontent.com/nextcloud/nextcloudpi/master/install.sh | bash
}

install_omv (){
#
# On Debian install OpenMediaVault 3 (Jessie) or 4 (Stretch)
#
# TODO: Some OMV packages lack authentication

if [[ "$family" == "Ubuntu" ]]; then
    dialog --backtitle "$BACKTITLE" --title "Dependencies not met" --msgbox "\nOpenMediaVault can only be installed on Debian." 7 52
    sleep 5
    exit 1
fi

case $distribution in
    jessie)
        OMV_Name="erasmus"
        OMV_EXTRAS_URL="https://github.com/OpenMediaVault-Plugin-Developers/packages/raw/master/openmediavault-omvextrasorg_latest_all3.deb"
        ;;
    stretch)
        OMV_Name="arrakis"
        OMV_EXTRAS_URL="https://github.com/OpenMediaVault-Plugin-Developers/packages/raw/master/openmediavault-omvextrasorg_latest_all4.deb"
        ;;
esac

systemctl status log2ram >/dev/null 2>&1 && (systemctl stop log2ram ; systemctl disable log2ram >/dev/null 2>&1; rm /etc/cron.daily/log2ram)
export APT_LISTCHANGES_FRONTEND=none
if [ -f /etc/armbian-release ]; then
    . /etc/armbian-release
else
    sed -i "s/^# en_US.UTF-8/en_US.UTF-8/" /etc/locale.gen
    locale-gen
fi

# preserve cpufrequtils settings:
if [ -f /etc/default/cpufrequtils ]; then
    . /etc/default/cpufrequtils
fi

cat > /etc/apt/sources.list.d/openmediavault.list << EOF
deb https://openmediavault.github.io/packages/ ${OMV_Name} main

## Uncomment the following line to add software from the proposed repository.
deb https://openmediavault.github.io/packages/ ${OMV_Name}-proposed main

## This software is not part of OpenMediaVault, but is offered by third-party
## developers as a service to OpenMediaVault users.
# deb https://openmediavault.github.io/packages/ ${OMV_Name} partner
EOF

debconf-apt-progress -- apt-get update

read HOSTNAME </etc/hostname
read TZ </etc/timezone
debconf-set-selections <<< "postfix postfix/mailname string ${HOSTNAME}"
debconf-set-selections <<< "postfix postfix/main_mailer_type string 'No configuration'"
SPACE_NEEDED=$(apt-get --assume-no --allow-unauthenticated --fix-missing --no-install-recommends install openmediavault postfix dirmngr 2>/dev/null | awk -F" " '/additional disk space will be used/ {print $4}')
SPACE_AVAIL=$(df -k / | awk -F" " '/\/$/ {printf ("%0.0f",$4/1200); }')
if [ ${SPACE_AVAIL} -lt ${SPACE_NEEDED} ]; then
    dialog --backtitle "$BACKTITLE" --title "No space left on device" --msgbox "\nOpenMediaVault needs ${SPACE_NEEDED} MB for installation while only ${SPACE_AVAIL} MB are available." 7 52
    exit 1
fi
apt-get --allow-unauthenticated install openmediavault-keyring
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 7AA630A1EDEE7D73
debconf-apt-progress -- apt-get -y --allow-unauthenticated --fix-missing --no-install-recommends \
    -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install openmediavault postfix dirmngr
FILE="${TEMP_DIR}/omv_extras.deb"; wget "$OMV_EXTRAS_URL" -qO $FILE && dpkg -i $FILE ; rm $FILE
# /usr/sbin/omv-update
debconf-apt-progress -- apt-get update
debconf-apt-progress -- apt-get --yes --force-yes --fix-missing --auto-remove --allow-unauthenticated \
  --show-upgraded --option DPkg::Options::="--force-confold" dist-upgrade

# Install flashmemory plugin and netatalk by default, use nice logo for the latter,
# disable OMV monitoring by default
. /usr/share/openmediavault/scripts/helper-functions
debconf-apt-progress -- apt-get -y --fix-missing --no-install-recommends --auto-remove install openmediavault-flashmemory openmediavault-netatalk
AFP_Options="mimic model = Macmini"
SMB_Options="min receivefile size = 16384\nwrite cache size = 524288\ngetwd cache = yes\nsocket options = TCP_NODELAY IPTOS_LOWDELAY"
xmlstarlet ed -L -u "/config/services/afp/extraoptions" -v "$(echo -e "${AFP_Options}")" ${OMV_CONFIG_FILE}
xmlstarlet ed -L -u "/config/services/smb/extraoptions" -v "$(echo -e "${SMB_Options}")" ${OMV_CONFIG_FILE}
xmlstarlet ed -L -u "/config/services/flashmemory/enable" -v "1" ${OMV_CONFIG_FILE}
xmlstarlet ed -L -u "/config/services/ssh/enable" -v "1" ${OMV_CONFIG_FILE}
xmlstarlet ed -L -u "/config/services/ssh/permitrootlogin" -v "1" ${OMV_CONFIG_FILE}
xmlstarlet ed -L -u "/config/system/time/ntp/enable" -v "1" ${OMV_CONFIG_FILE}
xmlstarlet ed -L -u "/config/system/time/timezone" -v "${TZ}" ${OMV_CONFIG_FILE}
xmlstarlet ed -L -u "/config/system/network/dns/hostname" -v "${HOSTNAME}" ${OMV_CONFIG_FILE}
/usr/sbin/omv-rpc -u admin "perfstats" "set" '{"enable":false}'
/usr/sbin/omv-rpc -u admin "config" "applyChanges" '{ "modules": ["monit","rrdcached","collectd"],"force": true }'
sed -i 's|-j /var/lib/rrdcached/journal/ ||' /etc/init.d/rrdcached
/sbin/folder2ram -enablesystemd 2>/dev/null

# Prevent accidentally destroying board performance by clicking around in OMV UI since
# OMV sets 'powersave' governor when touching 'Power Management' settings.
if [ ! -f /etc/default/cpufrequtils ]; then
    DEFAULT_GOV="$(zgrep "^CONFIG_CPU_FREQ_DEFAULT_GOV_" /proc/config.gz 2>/dev/null | sed 's/CONFIG_CPU_FREQ_DEFAULT_GOV_//')"
    if [ -n "${DEFAULT_GOV}" ]; then
        GOVERNOR=$(cut -f1 -d= <<<"${DEFAULT_GOV}" | tr '[:upper:]' '[:lower:]')
    else
        GOVERNOR=ondemand
    fi
    MIN_SPEED="0"
    MAX_SPEED="0"
fi
echo -e "OMV_CPUFREQUTILS_GOVERNOR=${GOVERNOR}" >>/etc/default/openmediavault
echo -e "OMV_CPUFREQUTILS_MINSPEED=${MIN_SPEED}" >>/etc/default/openmediavault
echo -e "OMV_CPUFREQUTILS_MAXSPEED=${MAX_SPEED}" >>/etc/default/openmediavault
for i in netatalk samba flashmemory ssh ntp timezone monit rrdcached collectd cpufrequtils ; do
    /usr/sbin/omv-mkconf $i
done

# Hardkernel Cloudshell 1 and 2 fixes, read the whole thread for details:
# https://forum.openmediavault.org/index.php/Thread/17855
lsusb | grep -q -i "05e3:0735" && sed -i "/exit 0/i echo 20 > /sys/class/block/sda/queue/max_sectors_kb" /etc/rc.local
if [ "X${BOARD}" = "Xodroidxu4" ]; then
    HMP_Fix='; taskset -c -p 4-7 $i '
    apt install -y i2c-tools
    /usr/sbin/i2cdetect -y 1 | grep -q "60: 60"
    if [ $? -eq 0 ]; then
        add-apt-repository -y ppa:kyle1117/ppa
        sed -i 's/jessie/xenial/' /etc/apt/sources.list.d/kyle1117-ppa-jessie.list
        apt install -y -q cloudshell-lcd odroid-cloudshell cloudshell2-fan &
        lsusb -v | awk -F"__" '/RANDOM_/ {print $2}' | head -n1 | while read ; do
            echo "ATTRS{idVendor}==\"152d\", ATTRS{idProduct}==\"0561\", KERNEL==\"sd*\", ENV{DEVTYPE}==\"disk\", SYMLINK=\"disk/by-id/\$env{ID_BUS}-CloudShell2-${REPLY}-\$env{ID_MODEL}\"" >> /etc/udev/rules.d/99-cloudshell2.rules
            echo "ATTRS{idVendor}==\"152d\", ATTRS{idProduct}==\"0561\", KERNEL==\"sd*\", ENV{DEVTYPE}==\"partition\", SYMLINK=\"disk/by-id/\$env{ID_BUS}-CloudShell2-${REPLY}-\$env{ID_MODEL}-part%n\"" >> /etc/udev/rules.d/99-cloudshell2.rules
        done
    fi
fi

# Add a cron job to make NAS processes more snappy
systemctl status rsyslog >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo ':msg, contains, "do ionice -c1" ~' >/etc/rsyslog.d/omv-armbian.conf
    systemctl restart rsyslog
fi
echo "* * * * * root for i in \`pgrep \"ftpd|nfsiod|smbd|afpd|cnid\"\` ; do ionice -c1 -p \$i ${HMP_Fix}; done >/dev/null 2>&1" >/etc/cron.d/make_nas_processes_faster
chmod 600 /etc/cron.d/make_nas_processes_faster

/usr/sbin/omv-initsystem
}




install_tvheadend ()
{
#
# TVheadend https://tvheadend.org/ unofficial port https://tvheadend.org/boards/5/topics/21528
#
if [ ! -f /etc/apt/sources.list.d/tvheadend.list ]; then
    echo "deb https://dl.bintray.com/tvheadend/deb xenial release-4.2" >> /etc/apt/sources.list.d/tvheadend.list
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 379CE192D401AB61 >/dev/null 2>&1
fi

if [[ $distribution == "stretch" ]]; then
    URL="http://security.debian.org/debian-security/pool/updates/main/o/openssl/libssl1.0.0_1.0.1t-1+deb8u8_"$(dpkg --print-architecture)".deb"
    fancy_wget "$URL" "-O ${TEMP_DIR}/package.deb"
    dpkg -i ${TEMP_DIR}/package.deb >/dev/null 2>&1
    local pkglist="libssl-doc zlib1g-dev tvheadend xmltv-util"
else
    local pkglist="libssl-doc libssl1.0.0 zlib1g-dev tvheadend xmltv-util"
fi

debconf-apt-progress -- apt-get update
debconf-apt-progress -- apt-get -y install $pkglist
}




install_urbackup ()
{
#
# Client/server backup system https://www.urbackup.org/
#
if [ "$(dpkg --print-architecture | grep arm64)" == "arm64" ]; then local arch=armhf; else local arch=$(dpkg --print-architecture); fi
PREFIX="http://hndl.urbackup.org/Server/latest/"
URL="http://hndl.urbackup.org/Server/latest/"$(wget -q $PREFIX -O - | html2text -width 120 | grep deb | awk ' { print $3 }' | grep $arch)
fancy_wget "$URL" "-O ${TEMP_DIR}/package.deb"
dpkg -i ${TEMP_DIR}/package.deb >/dev/null 2>&1
apt-get -yy -f install
}




install_transmission ()
{
#
# transmission
#
install_packet "debconf-utils unzip build-essential html2text apt-transport-https" "Downloading dependencies"
install_packet "transmission-cli transmission-common transmission-daemon" "Install torrent server"
# systemd workaround
# https://forum.armbian.com/index.php?/topic/4017-programs-does-not-start-automatically-at-boot/
sed -e 's/exit 0//g' -i /etc/rc.local
    cat >> /etc/rc.local <<"EOF"
service transmission-daemon restart
exit 0
EOF
}



install_transmission_seed_armbian_torrents ()
{
#
# seed our torrents
#
# adjust network buffers if necessary
rmem_recommended=4194304
wmem_recommended=1048576
rmem_actual=$(sysctl net.core.rmem_max | awk -F" " '{print $3}')
if [ ${rmem_actual} -lt ${rmem_recommended} ]; then
    grep -q net.core.rmem_max /etc/sysctl.conf && \
        sed -i "s/net.core.rmem_max =.*/net.core.rmem_max = ${rmem_recommended}/" /etc/sysctl.conf || \
        echo "net.core.rmem_max = ${rmem_recommended}" >> /etc/sysctl.conf
fi
wmem_actual=$(sysctl net.core.wmem_max | awk -F" " '{print $3}')
if [ ${wmem_actual} -lt ${wmem_recommended} ]; then
    grep -q net.core.wmem_max /etc/sysctl.conf && \
        sed -i "s/net.core.wmem_max =.*/net.core.wmem_max = ${wmem_recommended}/" /etc/sysctl.conf || \
        echo "net.core.wmem_max = ${wmem_recommended}" >> /etc/sysctl.conf
fi
/sbin/sysctl -p
# create cron job for daily sync with official Armbian torrents
cat > /etc/cron.daily/seed-armbian-torrent <<"EOF"
#!/bin/bash
#
# armbian torrents auto update
#
# download latest torrent pack
wget -qO- -O ${TEMP_DIR}/armbian-torrents.zip https://dl.armbian.com/torrent/all-torrents.zip
# test zip for corruption
unzip -t ${TEMP_DIR}/armbian-torrents.zip >/dev/null 2>&1
[[ $? -ne 0 ]] && echo "Error in zip" && exit
# extract zip
unzip -o ${TEMP_DIR}/armbian-torrents.zip -d ${TEMP_DIR}/torrent-tmp >/dev/null 2>&1
# create list of current active torrents
transmission-remote -n 'transmission:transmission' -l | sed '1d; $d' > ${TEMP_DIR}/torrent-tmp/active.torrents
# loop and add/update torrent files
for f in ${TEMP_DIR}/torrent-tmp/*.torrent; do
        transmission-remote -n 'transmission:transmission' -a $f > /dev/null 2>&1
        # remove added from the list
        pattern="${f//.torrent}"; pattern="${pattern##*/}";
        sed -i "/$pattern/d" ${TEMP_DIR}/torrent-tmp/active.torrents
done
# remove old armbian torrents
while read i; do
        [[ $i == *Armbian_* ]] && transmission-remote -n 'transmission:transmission' -t $(echo "$i" | awk '{print $1}';) --remove-and-delete
done < ${TEMP_DIR}/torrent-tmp/active.torrents
# remove temporally files and direcotories
EOF
chmod +x /etc/cron.daily/seed-armbian-torrent
/etc/cron.daily/seed-armbian-torrent &
}




install_syncthing ()
{
#
# Install Personal cloud https://syncthing.net/
#

if [ "$(dpkg --print-architecture | grep armhf)" == "armhf" ]; then
    local filename="linux-arm"
elif [ "$(dpkg --print-architecture | grep arm64)" == "arm64" ]; then
    local filename="linux-arm64"
else
    local filename="linux-amd64"
fi
mkdir -p /usr/bin/syncthing
wgeturl=$(curl -s "https://api.github.com/repos/syncthing/syncthing/releases" | grep $filename | grep 'browser_download_url' | head -1 | cut -d \" -f 4)
fancy_wget "$wgeturl" "-O ${TEMP_DIR}/syncthing.tgz"
wgeturl=$(curl -s "https://api.github.com/repos/syncthing/syncthing-inotify/releases" | grep $filename | grep 'browser_download_url' | head -1 | cut -d \" -f 4)
fancy_wget "$wgeturl" "-O ${TEMP_DIR}/syncthing-inotify.tgz"
tar xf ${TEMP_DIR}/syncthing.tgz -C ${TEMP_DIR}
tar xf ${TEMP_DIR}/syncthing-inotify.tgz -C /usr/bin
cp -R ${TEMP_DIR}/syncthing-*/syncthing /usr/bin
cp ${TEMP_DIR}/syncthing-*/etc/linux-systemd/system/syncthing* /etc/systemd/system/
cp /etc/systemd/system/syncthing@.service /etc/systemd/system/syncthing-inotify@.service

# adjust service for inotify
sed  -i "s/^Description=.*/Description=Syncthing Inotify File Watcher/" /etc/systemd/system/syncthing-inotify@.service
sed  -i "s/^After=.*/After=network.target syncthing.service/" /etc/systemd/system/syncthing-inotify@.service
sed  -i "s/^ExecStart=.*/ExecStart=\/usr\/bin\/syncthing-inotify -logfile=\/var\/log\/syncthing-inotify.log -logflags=3/" /etc/systemd/system/syncthing-inotify@.service
sed  -i "/^\[Install\]/a Requires=syncthing.service" /etc/systemd/system/syncthing-inotify@.service

# increase open file limit
if !(grep -qs "fs.inotify.max_user_watches=204800" "/etc/sysctl.conf");then
    echo -e "fs.inotify.max_user_watches=204800" | tee -a /etc/sysctl.conf
fi
add_choose_user
systemctl enable syncthing@${CHOSEN_USER}.service >/dev/null 2>&1
systemctl start syncthing@${CHOSEN_USER}.service >/dev/null 2>&1
systemctl enable syncthing-inotify@${CHOSEN_USER}.service >/dev/null 2>&1
systemctl start syncthing-inotify@${CHOSEN_USER}.service >/dev/null 2>&1
}




install_plex_media_server ()
{
#
# Media server
#
if [ "$(dpkg --print-architecture | grep armhf)" == "armhf" ]; then
    echo -e "deb [arch=armhf] http://dev2day.de/pms/ stretch main" > /etc/apt/sources.list.d/plex.list
    wget -q -O - http://dev2day.de/pms/dev2day-pms.gpg.key | apt-key add - >/dev/null 2>&1
    debconf-apt-progress -- apt-get update
    debconf-apt-progress -- apt-get -y install plexmediaserver-installer
elif [ "$(dpkg --print-architecture | grep arm64)" == "arm64" ]; then
    echo -e "deb [arch=armhf] http://dev2day.de/pms/ stretch main" > /etc/apt/sources.list.d/plex.list
    wget -q -O - http://dev2day.de/pms/dev2day-pms.gpg.key | apt-key add - >/dev/null 2>&1
    debconf-apt-progress -- apt-get update
    debconf-apt-progress -- apt-get -y install binutils:armhf plexmediaserver-installer:armhf
else
    fancy_wget "https://downloads.plex.tv/plex-media-server/1.12.3.4973-215c28d86/plexmediaserver_1.12.3.4973-215c28d86_amd64.deb" "-O ${TEMP_DIR}/package.deb"
    dpkg -i ${TEMP_DIR}/package.deb >/dev/null 2>&1
fi
}




install_radarr ()
{
#
# Automatically downloading movies
#
debconf-apt-progress -- apt-get update
debconf-apt-progress -- apt-get -y install mono-devel mediainfo libmono-cil-dev
wgeturl=$(curl -s "https://api.github.com/repos/Radarr/Radarr/releases" | grep 'linux.tar.gz' | grep 'browser_download_url' | head -1 | cut -d \" -f 4)
fancy_wget "$wgeturl" "-O ${TEMP_DIR}/radarr.tgz"
tar xf ${TEMP_DIR}/radarr.tgz -C /opt
cat << _EOF_ > /etc/systemd/system/radarr.service
[Unit]
Description=Radarr Daemon
After=network.target
[Service]
User=root
Type=simple
ExecStart=/usr/bin/mono --debug /opt/Radarr/Radarr.exe -nobrowser
[Install]
WantedBy=multi-user.target
_EOF_
systemctl enable radarr >/dev/null 2>&1
systemctl start radarr
}




install_sonarr ()
{
#
# Automatically downloading TV shows
#
if [ "$(dpkg --print-architecture | grep arm64)" == "arm64" ]; then
    debconf-apt-progress -- apt-get update
    debconf-apt-progress -- apt-get -y install mono-complete mediainfo
    fancy_wget "http://update.sonarr.tv/v2/develop/mono/NzbDrone.develop.tar.gz" "-O ${TEMP_DIR}/sonarr.tgz"
    tar xf ${TEMP_DIR}/sonarr.tgz -C /opt
else
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys FDA5DFFC >/dev/null 2>&1
    echo -e "deb https://apt.sonarr.tv/ develop main" > /etc/apt/sources.list.d/sonarr.list
    debconf-apt-progress -- apt-get update
    debconf-apt-progress -- apt-get -y install nzbdrone
fi
cat << _EOF_ > /etc/systemd/system/sonarr.service
[Unit]
Description=Sonarr (NzbDrone) Daemon
After=network.target
[Service]
User=root
Type=simple
ExecStart=/usr/bin/mono --debug /opt/NzbDrone/NzbDrone.exe -nobrowser
[Install]
WantedBy=multi-user.target
_EOF_
systemctl enable sonarr >/dev/null 2>&1
systemctl start sonarr
}




install_vpn_server ()
{
#
# Script downloads latest stable
#
cd ${TEMP_DIR}
PREFIX="http://www.softether-download.com/files/softether/"
install_packet "debconf-utils unzip build-essential html2text apt-transport-https" "Downloading basic packages"
URL=$(wget -q $PREFIX -O - | html2text | grep rtm | awk ' { print $(NF) }' | tail -1)
SUFIX="${URL/-tree/}"
if [ "$(dpkg --print-architecture | grep armhf)" != "" ]; then
DLURL=$PREFIX$URL"/Linux/SoftEther_VPN_Server/32bit_-_ARM_EABI/softether-vpnserver-$SUFIX-linux-arm_eabi-32bit.tar.gz"
else
install_packet "gcc-multilib" "Install libraries"
DLURL=$PREFIX$URL"/Linux/SoftEther_VPN_Server/32bit_-_Intel_x86/softether-vpnserver-$SUFIX-linux-x86-32bit.tar.gz"
fi
wget -q $DLURL -O - | tar -xz
cd vpnserver
make i_read_and_agree_the_license_agreement | dialog --backtitle "$BACKTITLE" --title "Compiling SoftEther VPN" --progressbox $TTY_Y $TTY_X
cd ..
cp -R vpnserver /usr/local
cd /usr/local/vpnserver/
chmod 600 *
chmod 700 vpncmd
chmod 700 vpnserver
if [[ -d /run/systemd/system/ ]]; then
cat <<EOT >/lib/systemd/system/ethervpn.service
[Unit]
Description=VPN service

[Service]
Type=oneshot
ExecStart=/usr/local/vpnserver/vpnserver start
ExecStop=/usr/local/vpnserver/vpnserver stop
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOT
systemctl enable ethervpn.service
service ethervpn start

else

cat <<EOT > /etc/init.d/vpnserver
#!/bin/sh
### BEGIN INIT INFO
# Provides:          vpnserver
# Required-Start:    \$remote_fs \$syslog
# Required-Stop:     \$remote_fs \$syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable Softether by daemon.
### END INIT INFO
DAEMON=/usr/local/vpnserver/vpnserver
LOCK=/var/lock/vpnserver
test -x $DAEMON || exit 0
case "\$1" in
start)
\$DAEMON start
touch \$LOCK
;;
stop)
\$DAEMON stop
rm \$LOCK
;;
restart)
\$DAEMON stop
sleep 3
\$DAEMON start
;;
*)
echo "Usage: \$0 {start|stop|restart}"
exit 1
esac
exit 0
EOT
chmod 755 /etc/init.d/vpnserver
mkdir /var/lock/subsys
update-rc.d vpnserver defaults >> $logfile
/etc/init.d/vpnserver start
fi
}




install_vpn_client ()
{
#
# Script downloads latest stable
#
cd ${TEMP_DIR}
PREFIX="http://www.softether-download.com/files/softether/"
install_packet "debconf-utils unzip build-essential html2text apt-transport-https" "Downloading basic packages"
URL=$(wget -q $PREFIX -O - | html2text | grep rtm | awk ' { print $(NF) }' | tail -1)
SUFIX="${URL/-tree/}"
if [ "$(dpkg --print-architecture | grep armhf)" != "" ]; then
DLURL=$PREFIX$URL"/Linux/SoftEther_VPN_Client/32bit_-_ARM_EABI/softether-vpnclient-$SUFIX-linux-arm_eabi-32bit.tar.gz"
else
install_packet "gcc-multilib" "Install libraries"
DLURL=$PREFIX$URL"/Linux/SoftEther_VPN_Client/32bit_-_Intel_x86/softether-vpnclient-$SUFIX-linux-x86-32bit.tar.gz"
fi
wget -q $DLURL -O - | tar -xz
cd vpnclient
make i_read_and_agree_the_license_agreement | dialog --backtitle "$BACKTITLE" --title "Compiling SoftEther VPN vpnclient" --progressbox $TTY_Y $TTY_X
cd ..
cp -R vpnclient /usr/local
cd /usr/local/vpnclient/
chmod 600 *
chmod 700 vpncmd
chmod 700 vpnclient
}




install_DashNTP ()
{
#
# Install DASH and ntp service
#
echo "dash dash/sh boolean false" | debconf-set-selections
dpkg-reconfigure -f noninteractive dash > /dev/null 2>&1
install_packet "ntp ntpdate" "Install DASH and ntp service"
}




install_MySQL ()
{
#
# Maria SQL
#
install_packet "mariadb-client mariadb-server" "SQL client and server"
#Allow MySQL to listen on all interfaces
cp /etc/mysql/my.cnf /etc/mysql/my.cnf.backup
[[ -f /etc/mysql/my.cnf ]] && sed -i 's|bind-address.*|#bind-address           = 127.0.0.1|' /etc/mysql/my.cnf
[[ -f /etc/mysql/mariadb.conf.d/50-server.cnf ]] && sed -i 's|bind-address.*|#bind-address           = 127.0.0.1|' /etc/mysql/mariadb.conf.d/50-server.cnf
SECURE_MYSQL=$(expect -c "
set timeout 3
spawn mysql_secure_installation
expect \"Enter current password for root (enter for none):\"
send \"\r\"
expect \"root password?\"
send \"y\r\"
expect \"New password:\"
send \"$MYSQL_PASS\r\"
expect \"Re-enter new password:\"
send \"$MYSQL_PASS\r\"
expect \"Remove anonymous users?\"
send \"y\r\"
expect \"Disallow root login remotely?\"
send \"y\r\"
expect \"Remove test database and access to it?\"
send \"y\r\"
expect \"Reload privilege tables now?\"
send \"y\r\"
expect eof
")
#
# Execution mysql_secure_installation
#
echo "${SECURE_MYSQL}" >> /dev/null
# ISP config exception
mkdir -p /etc/mysql/mariadb.conf.d/
cat > /etc/mysql/mariadb.conf.d/99-ispconfig.cnf<<"EOF"
[mysqld]
sql-mode="NO_ENGINE_SUBSTITUTION"
EOF
service mysql restart >> /dev/null
}




install_MySQLDovecot ()
{
#
# Install Postfix, Dovecot, Saslauthd, rkhunter, binutils
#
echo "postfix postfix/main_mailer_type select Internet Site" | debconf-set-selections
echo "postfix postfix/mailname string $HOSTNAMEFQDN" | debconf-set-selections
install_packet "postfix postfix-mysql postfix-doc openssl getmail4 rkhunter binutils dovecot-imapd dovecot-pop3d dovecot-mysql \
dovecot-sieve sudo libsasl2-modules" "postfix, dovecot, saslauthd, rkhunter, binutils"
#Uncommenting some Postfix configuration files
cp /etc/postfix/master.cf /etc/postfix/master.cf.backup
sed -i 's|#submission inet n       -       -       -       -       smtpd|submission inet n       -       -       -       -       smtpd|' /etc/postfix/master.cf
sed -i 's|#  -o syslog_name=postfix/submission|  -o syslog_name=postfix/submission|' /etc/postfix/master.cf
sed -i 's|#  -o smtpd_tls_security_level=encrypt|  -o smtpd_tls_security_level=encrypt|' /etc/postfix/master.cf
sed -i 's|#  -o smtpd_sasl_auth_enable=yes|  -o smtpd_sasl_auth_enable=yes|' /etc/postfix/master.cf
sed -i 's|#  -o smtpd_client_restrictions=permit_sasl_authenticated,reject|  -o smtpd_client_restrictions=permit_sasl_authenticated,reject|' /etc/postfix/master.cf
sed -i 's|#  -o smtpd_sasl_auth_enable=yes|  -o smtpd_sasl_auth_enable=yes|' /etc/postfix/master.cf
sed -i 's|#  -o smtpd_sasl_auth_enable=yes|  -o smtpd_sasl_auth_enable=yes|' /etc/postfix/master.cf
sed -i 's|#  -o smtpd_sasl_auth_enable=yes|  -o smtpd_sasl_auth_enable=yes|' /etc/postfix/master.cf
sed -i 's|#smtps     inet  n       -       -       -       -       smtpd|smtps     inet  n       -       -       -       -       smtpd|' /etc/postfix/master.cf
sed -i 's|#  -o syslog_name=postfix/smtps|  -o syslog_name=postfix/smtps|' /etc/postfix/master.cf
sed -i 's|#  -o smtpd_tls_wrappermode=yes|  -o smtpd_tls_wrappermode=yes|' /etc/postfix/master.cf
service postfix restart >> /dev/null
}




install_Virus ()
{
#
# Install Amavisd-new, SpamAssassin, And Clamav
#
install_packet "amavisd-new spamassassin clamav clamav-daemon zoo unzip bzip2 arj p7zip unrar-free ripole rpm nomarch lzop \
cabextract apt-listchanges libnet-ldap-perl libauthen-sasl-perl clamav-docs daemon libio-string-perl libio-socket-ssl-perl \
libnet-ident-perl zip libnet-dns-perl postgrey" "amavisd, spamassassin, clamav"
sed -i "s/^AllowSupplementaryGroups.*/AllowSupplementaryGroups true/" /etc/clamav/clamd.conf
service spamassassin stop >/dev/null 2>&1
systemctl disable spamassassin >/dev/null 2>&1
}




install_hhvm ()
{
#
# Install HipHop Virtual Machine
#
apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xB4112585D386EB94 >/dev/null 2>&1
add-apt-repository https://dl.hhvm.com/"${family,,}" >/dev/null 2>&1
debconf-apt-progress -- apt-get update
install_packet "hhvm" "HipHop Virtual Machine"
}




install_phpmyadmin ()
{
#
# Phpmyadmin unattended installation
#
if [[ "$family" != "Ubuntu" ]]; then
DEBIAN_FRONTEND=noninteractive debconf-apt-progress -- apt-get -y install phpmyadmin
else
debconf-set-selections <<< "phpmyadmin phpmyadmin/internal/skip-preseed boolean true"
debconf-set-selections <<< "phpmyadmin phpmyadmin/reconfigure-webserver multiselect true"
debconf-set-selections <<< "phpmyadmin phpmyadmin/dbconfig-install boolean false"
echo "phpmyadmin phpmyadmin/internal/skip-preseed boolean true" | debconf-set-selections
echo "phpmyadmin phpmyadmin/reconfigure-webserver multiselect" | debconf-set-selections
echo "phpmyadmin phpmyadmin/dbconfig-install boolean false" | debconf-set-selections
debconf-apt-progress -- apt-get install -y phpmyadmin
fi
}




install_apache ()
{
#
# Install Apache2, PHP5, FCGI, suExec, Pear and mcrypt
#

local pkg="apache2 apache2-doc apache2-utils libapache2-mod-fcgid php-pear mcrypt imagemagick libruby libapache2-mod-python memcached"

local pkg_xenial="libapache2-mod-php php7.0 php7.0-common php7.0-gd php7.0-mysql php7.0-imap php7.0-cli php7.0-cgi \
apache2-suexec-pristine php-auth php7.0-mcrypt php7.0-curl php7.0-intl php7.0-pspell php7.0-recode php7.0-sqlite3 php7.0-tidy \
php7.0-xmlrpc php7.0-xsl php-memcache php-imagick php-gettext php7.0-zip php7.0-mbstring php7.0-opcache php-apcu \
libapache2-mod-fastcgi php7.0-fpm letsencrypt"

local pkg_stretch="libapache2-mod-php php7.0 php7.0-common php7.0-gd php7.0-mysql php7.0-imap php7.0-cli php7.0-cgi libapache2-mod-fcgid \
apache2-suexec-pristine php7.0-mcrypt libapache2-mod-python php7.0-curl php7.0-intl php7.0-pspell php7.0-recode php7.0-sqlite3 \
php7.0-tidy php7.0-xmlrpc php7.0-xsl php-memcache php-imagick php-gettext php7.0-zip php7.0-mbstring libapache2-mod-passenger \
php7.0-soap php7.0-fpm php7.0-opcache php-apcu certbot"

local pkg_jessie="apache2.2-common apache2-mpm-prefork libexpat1 ssl-cert libapache2-mod-php5 php5 php5-common php5-gd php5-mysql \
php5-imap php5-cli php5-cgi libapache2-mod-fcgid apache2-suexec php-pear php-auth php5-mcrypt mcrypt php5-imagick libapache2-mod-python \
php5-curl php5-intl php5-memcache php5-memcached php5-pspell php5-recode php5-sqlite php5-tidy php5-xmlrpc php5-xsl \
libapache2-mod-passenger php5-xcache libapache2-mod-fastcgi php5-fpm"

local temp="pkg_${distribution}"
install_packet "${pkg} ${!temp}" "Apache for $family $distribution"
# fix HTTPOXY vulnerability
cat <<EOT > /etc/apache2/conf-available/httpoxy.conf
<IfModule mod_headers.c>
    RequestHeader unset Proxy early
</IfModule>

EOT

a2enmod actions proxy_fcgi setenvif fastcgi alias httpoxy suexec rewrite ssl actions include dav_fs dav auth_digest cgi headers >/dev/null 2>&1
a2enconf php7.0-fpm >/dev/null 2>&1
service apache2 restart >> /dev/null
}




install_nginx ()
{
#
# Install NginX, PHP5, FCGI, suExec, Pear, And mcrypt
#
local pkg="nginx php-pear memcached fcgiwrap"

local pkg_xenial="php7.0-fpm php7.0-opcache php7.0-fpm php7.0 php7.0-common php7.0-gd php7.0-mysql php7.0-imap php7.0-cli php7.0-cgi \
php7.0-mcrypt mcrypt imagemagick libruby php7.0-curl php7.0-intl php7.0-pspell php7.0-recode php7.0-sqlite3 php7.0-tidy \
php7.0-xmlrpc php7.0-xsl php-memcache php-imagick php-gettext php7.0-zip php7.0-mbstring php-apcu"

local pkg_stretch="php7.0-fpm php7.0-opcache php7.0-fpm php7.0 php7.0-common php7.0-gd php7.0-mysql php7.0-imap php7.0-cli php7.0-cgi \
php7.0-mcrypt mcrypt imagemagick libruby php7.0-curl php7.0-intl php7.0-pspell php7.0-recode php7.0-sqlite3 php7.0-tidy \
php7.0-xmlrpc php7.0-xsl php-memcache php-imagick php-gettext php7.0-zip php7.0-mbstring php-apcu"

local pkg_jessie="php5-fpm php5-mysql php5-curl php5-gd php5-intl php5-imagick php5-imap php5-mcrypt php5-memcache \
php5-memcached php5-pspell php5-recode php5-snmp php5-sqlite php5-tidy php5-xmlrpc php5-xsl php-apc"

local temp="pkg_${distribution}"
install_packet "${pkg} ${!temp}" "Nginx for $family $distribution"

phpenmod mcrypt mbstring

if [[ -f /etc/php/7.0/fpm/php.ini ]]; then
    tz=$(cat /etc/timezone | sed 's/\//\\\//g')
    sed -i "s/^cgi.fix_pathinfo=.*/cgi.fix_pathinfo=0/" /etc/php/7.0/fpm/php.ini
    sed -i "s/^date.timezone=.*/date.timezone=""$tz""/" /etc/php/7.0/fpm/php.ini
    service php7.0-fpm reload >> /dev/null
else
    debconf-apt-progress -- apt-get install -y python-certbot -t jessie-backports
    service php5-fpm reload >> /dev/null
fi
}




install_PureFTPD ()
{
#
# Install PureFTPd and Quota
#
install_packet "pure-ftpd-common pure-ftpd-mysql quota quotatool" "pureFTPd and Quota"

sed -i 's/VIRTUALCHROOT=false/VIRTUALCHROOT=true/' /etc/default/pure-ftpd-common
echo 1 > /etc/pure-ftpd/conf/TLS
mkdir -p /etc/ssl/private/
openssl req -x509 -nodes -days 7300 -newkey rsa:2048 -subj "/C=GB/ST=GB/L=GB/O=GB/OU=GB/CN=$(hostname -f)/emailAddress=joe@joe.com" -keyout /etc/ssl/private/pure-ftpd.pem -out /etc/ssl/private/pure-ftpd.pem >/dev/null 2>&1
chmod 600 /etc/ssl/private/pure-ftpd.pem
/etc/init.d/pure-ftpd-mysql restart >/dev/null 2>&1
local temp=$(cat /etc/fstab | grep "/ " | tail -1 | awk '{print $4}')
sed -i "s/$temp/$temp,usrjquota=quota.user,grpjquota=quota.group,jqfmt=vfsv0/" /etc/fstab
mount -o remount / >/dev/null 2>&1
quotacheck -avugm >/dev/null 2>&1
quotaon -avug >/dev/null 2>&1
}




install_Bind ()
{
#
# Install BIND DNS Server
#
install_packet "bind9 dnsutils" "Install BIND DNS Server"
}




install_Stats ()
{
#
# Install Vlogger, Webalizer, And AWstats
#
install_packet "vlogger webalizer awstats geoip-database libclass-dbi-mysql-perl" "vlogger, webalizer, awstats"
sed -i "s/*/10 * * * * www-data/#*/10 * * * * www-data/" /etc/cron.d/awstats
sed -i "s/10 03 * * * www-data/#10 03 * * * www-data/" /etc/cron.d/awstats
}




install_Jailkit()
{
#
debconf-apt-progress -- apt-get install -y build-essential autoconf automake libtool flex bison debhelper binutils
cd ${TEMP_DIR}
wget -q http://olivier.sessink.nl/jailkit/jailkit-2.19.tar.gz -O - | tar -xz && cd jailkit-2.19
echo 5 > debian/compat
./debian/rules binary > /dev/null 2>&1
dpkg -i ../jailkit_2.19-1_*.deb > /dev/null 2>&1
}




install_Fail2BanDovecot()
{
#
# Install fail2ban
#
install_packet "fail2ban ufw" "Install fail2ban and UFW Firewall"
if [[ $distribution == "stretch" ]]; then
cat > /etc/fail2ban/jail.local <<"EOF"
[pure-ftpd]
enabled = true
port = ftp
filter = pure-ftpd
logpath = /var/log/syslog
maxretry = 3

[dovecot]
enabled = true
filter = dovecot
logpath = /var/log/mail.log
maxretry = 5

[postfix-sasl]
enabled = true
port = smtp
filter = postfix-sasl
logpath = /var/log/mail.log
maxretry = 3
EOF
else
cat > /etc/fail2ban/jail.local <<"EOF"
[pureftpd]
enabled  = true
port     = ftp
filter   = pureftpd
logpath  = /var/log/syslog
maxretry = 3

[dovecot-pop3imap]
enabled = true
filter = dovecot-pop3imap
action = iptables-multiport[name=dovecot-pop3imap, port="pop3,pop3s,imap,imaps", protocol=tcp]
logpath = /var/log/mail.log
maxretry = 5

[sasl]
enabled  = true
port     = smtp
filter   = postfix-sasl
logpath  = /var/log/mail.log
maxretry = 3
EOF
fi
}




install_Fail2BanRulesDovecot()
{
#
# Dovecot rules
#
cat > /etc/fail2ban/filter.d/pureftpd.conf <<"EOF"
[Definition]
failregex = .*pure-ftpd: \(.*@<HOST>\) \[WARNING\] Authentication failed for user.*
ignoreregex =
EOF

cat > /etc/fail2ban/filter.d/dovecot-pop3imap.conf <<"EOF"
[Definition]
failregex = (?: pop3-login|imap-login): .*(?:Authentication failure|Aborted login \(auth failed|Aborted login \(tried to use disabled|Disconnected \(auth failed|Aborted login \(\d+ authentication attempts).*rip=(?P<host>\S*),.*
ignoreregex =
EOF
# Add the missing ignoreregex line
echo "ignoreregex =" >> /etc/fail2ban/filter.d/postfix-sasl.conf
service fail2ban restart >> /dev/null
}




install_ISPConfig (){
#------------------------------------------------------------------------------------------------------------------------------------------
# Install ISPConfig 3
#------------------------------------------------------------------------------------------------------------------------------------------
cd ${TEMP_DIR}
wget -q http://www.ispconfig.org/downloads/ISPConfig-3-stable.tar.gz -O - | tar -xz
cd ${TEMP_DIR}/ispconfig3_install/install/
#apt-get -y install php5-cli php5-mysql
php -q install.php --autoinstall=${TEMP_DIR}/isp.conf.php
echo "Admin panel: https://$serverIP:8080"
echo "PHPmyadmin: http://$serverIP:8081/phpmyadmin"
}


install_mayan_edms (){
#
# Install Mayan EDMS
#

# Default values
MAYAN_DATABASE_PASSWORD="mayandbpass"
MAYAN_INSTALLATION_FOLDER="/opt/mayan-edms"
MAYAN_MEDIA_ROOT="/opt/mayan-edms-data"

# User interaction
exec 3>&1
dialog --title "Server configuration" --separate-widget $'\n' \
--ok-label "Install" --backtitle "$BACKTITLE" \
--form "\nPlease fill out this form:\n " 13 70 0 \
"Ddatabase password:"  1 1 "$MAYAN_DATABASE_PASSWORD"          1 31 32 0 \
"Installation folder:"  2 1 "$MAYAN_INSTALLATION_FOLDER"  2 31 32 0 \
"Data folder:"  3 1 "$MAYAN_MEDIA_ROOT"                   3 31 32 0 \
2>&1 1>&3 | {
read -r MAYAN_DATABASE_PASSWORD
read -r MAYAN_MEDIA_ROOT
read -r MAYAN_INSTALLATION_FOLDER
echo $MAYAN_DATABASE_PASSWORD > ${TEMP_DIR}/MAYAN_DATABASE_PASSWORD
echo $MAYAN_MEDIA_ROOT > ${TEMP_DIR}/MAYAN_MEDIA_ROOT
echo $MAYAN_INSTALLATION_FOLDER > ${TEMP_DIR}/MAYAN_INSTALLATION_FOLDER
}
exec 3>&-
read MAYAN_DATABASE_PASSWORD < ${TEMP_DIR}/MAYAN_DATABASE_PASSWORD
read MAYAN_MEDIA_ROOT < ${TEMP_DIR}/MAYAN_MEDIA_ROOT
read MAYAN_INSTALLATION_FOLDER < ${TEMP_DIR}/MAYAN_INSTALLATION_FOLDER

# OS dependencies
install_packet "g++ gcc ghostscript gnupg1 graphviz libffi-dev libjpeg-dev libmagic1 libpq-dev libpng-dev libreoffice libssl-dev libtiff-dev poppler-utils postgresql python-dev python-pip python-virtualenv redis-server sane-utils supervisor tesseract-ocr zlib1g-dev" "Installing dependencies"

# Mayan OS user account
dialog --infobox "Adding Mayan EDMS user account" 3 70
adduser mayan --disabled-password --disabled-login --no-create-home --gecos "" >/dev/null 2>&1
sleep 1

# Create installtion and data folders
mkdir -p "${MAYAN_INSTALLATION_FOLDER}"
mkdir -p "${MAYAN_MEDIA_ROOT}"

# Create the Python virtualenv to isolate Python dependencies of Mayan
dialog --infobox "Creating Python virtual environment" 3 70
python /usr/lib/python2.7/dist-packages/virtualenv.py $MAYAN_INSTALLATION_FOLDER > /dev/null

# Give ownership to the Mayan OS user
chown mayan:mayan "${MAYAN_INSTALLATION_FOLDER}" -R
chown mayan:mayan "${MAYAN_MEDIA_ROOT}" -R

# Pillow can't find zlib or libjpeg on aarch64 (ODROID C2)
if [ "$(uname -m)" = "aarch64" ]; then \
    ln -s /usr/lib/aarch64-linux-gnu/libz.so /usr/lib/ && \
    ln -s /usr/lib/aarch64-linux-gnu/libjpeg.so /usr/lib/ \
; fi

# Pillow can't find zlib or libjpeg on armv7l (ODROID HC1)
if [ "$(uname -m)" = "armv7l" ]; then \
    ln -s /usr/lib/arm-linux-gnueabihf/libz.so /usr/lib/ && \
    ln -s /usr/lib/arm-linux-gnueabihf/libjpeg.so /usr/lib/ \
; fi

# Install Mayan from the web and all its Python dependencies
MAYAN_PIP=$MAYAN_INSTALLATION_FOLDER/bin/pip
dialog --infobox "Installing Mayan EDMS Python package (Takes several minutes)" 3 70
sudo -u mayan $MAYAN_PIP install --no-cache-dir mayan-edms > /dev/null 2>&1

# Python Postgres driver
dialog --infobox "Installing PostgreSQL database driver" 3 70
sudo -u mayan $MAYAN_PIP install --no-cache-dir psycopg2==2.7.3.2 > /dev/null

# Python Redis driver
dialog --infobox "Installing Redis driver" 3 70
sudo -u mayan $MAYAN_PIP install --no-cache-dir redis==2.10.6 > /dev/null

# Create postgres Mayan user and database
MAYAN_BIN=$MAYAN_INSTALLATION_FOLDER/bin/mayan-edms.py
dialog --infobox "Creating and initializing database (Takes several minutes)" 3 70
sudo -u postgres psql -c "CREATE USER mayan WITH password '$MAYAN_DATABASE_PASSWORD';"
sudo -u postgres createdb -O mayan mayan

# Execute initialsetup command. Migrate DB, create base files, downloads Javascript libraries
sudo -u mayan \
    MAYAN_DATABASE_ENGINE=django.db.backends.postgresql \
    MAYAN_DATABASE_NAME=mayan \
    MAYAN_DATABASE_USER=mayan \
    MAYAN_DATABASE_HOST=127.0.0.1 \
    MAYAN_MEDIA_ROOT=$MAYAN_MEDIA_ROOT \
    MAYAN_DATABASE_PASSWORD=$MAYAN_DATABASE_PASSWORD \
    $MAYAN_BIN initialsetup --force  > /dev/null

# Compress and merge Javascript, CSS for web serving
dialog --infobox "Preparing static files" 3 70
sudo -u mayan \
    MAYAN_MEDIA_ROOT=$MAYAN_MEDIA_ROOT \
    $MAYAN_BIN preparestatic --noinput > /dev/null

# Create supervisor file for gunicorn (frontend), 3 background workers, and the scheduler for periodic tasks
cat > /etc/supervisor/conf.d/mayan.conf <<EOF
[supervisord]
environment=
        MAYAN_ALLOWED_HOSTS="*", # Allow access to other network hosts other than localhost
        MAYAN_CELERY_RESULT_BACKEND="redis://127.0.0.1:6379/0",
        MAYAN_BROKER_URL="redis://127.0.0.1:6379/0",
        PYTHONPATH=${MAYAN_INSTALLATION_FOLDER}/lib/python2.7/site-packages:$MAYAN_MEDIA_ROOT,
        MAYAN_DATABASE_ENGINE=django.db.backends.postgresql,
        MAYAN_DATABASE_HOST=127.0.0.1,
        MAYAN_DATABASE_NAME=mayan,
        MAYAN_DATABASE_USER=mayan,
        MAYAN_DATABASE_CONN_MAX_AGE=60,
        DJANGO_SETTINGS_MODULE=mayan.settings.production,
        MAYAN_DATABASE_PASSWORD=${MAYAN_DATABASE_PASSWORD},
        MAYAN_MEDIA_ROOT=${MAYAN_MEDIA_ROOT}

[program:mayan-gunicorn]
autorestart = true
autostart = true
command = ${MAYAN_INSTALLATION_FOLDER}/bin/gunicorn -w 2 mayan.wsgi --max-requests 500 --max-requests-jitter 50 --worker-class gevent --bind 0.0.0.0:8000
user = mayan

[program:mayan-worker-fast]
autorestart = true
autostart = true
command = nice -n 1 ${MAYAN_BIN} celery worker -Ofair -l ERROR -Q converter -n mayan-worker-fast.%%h --concurrency=1
killasgroup = true
numprocs = 1
priority = 998
startsecs = 10
stopwaitsecs = 1
user = mayan

[program:mayan-worker-medium]
autorestart = true
autostart = true
command = nice -n 18 ${MAYAN_BIN} celery worker -Ofair -l ERROR -Q checkouts_periodic,documents_periodic,indexing,metadata,sources,sources_periodic,uploads,documents -n mayan-worker-medium.%%h --concurrency=1
killasgroup = true
numprocs = 1
priority = 998
startsecs = 10
stopwaitsecs = 1
user = mayan

[program:mayan-worker-slow]
autorestart = true
autostart = true
command = nice -n 19 ${MAYAN_BIN} celery worker -Ofair -l ERROR -Q mailing,tools,statistics,parsing,ocr -n mayan-worker-slow.%%h --concurrency=1
killasgroup = true
numprocs = 1
priority = 998
startsecs = 10
stopwaitsecs = 1
user = mayan

[program:mayan-celery-beat]
autorestart = true
autostart = true
command = nice -n 1 ${MAYAN_BIN} celery beat --pidfile= -l ERROR
killasgroup = true
numprocs = 1
priority = 998
startsecs = 10
stopwaitsecs = 1
user = mayan
EOF

# Discard data when Redis runs out of memory
echo "maxmemory-policy allkeys-lru" >> /etc/redis/redis.conf

# This starts all of Mayan's processes
dialog --infobox "Starting service" 3 70
systemctl restart supervisor.service

# Installation report
dialog --msgbox "Installation complete.\nInstallation folder: $MAYAN_INSTALLATION_FOLDER\nData folder: $MAYAN_MEDIA_ROOT\nPort: 8000" 10 70
}


#------------------------------------------------------------------------------------------------------------------------------------------
# Main choices
#------------------------------------------------------------------------------------------------------------------------------------------

# check for root
#
if [[ $EUID != 0 ]]; then
    dialog --title "Warning" --infobox "\nThis script requires root privileges.\n\nExiting ..." 7 41
    sleep 3
    exit
fi

# nameserver backup
if [ -d /etc/resolvconf/resolv.conf.d ]; then
    echo 'nameserver 8.8.8.8' > /etc/resolvconf/resolv.conf.d/head
    resolvconf -u
fi

# Create a safe temporary directory
TEMP_DIR=$(mktemp -d || exit 1)
chmod 700 ${TEMP_DIR}
trap "rm -rf \"${TEMP_DIR}\" ; exit 0" 0 1 2 3 15

# Install basic stuff, we have to wait for other apt tasks to finish
# (eg unattended-upgrades)
i=0
tput sc
while fuser /var/lib/dpkg/lock >/dev/null 2>&1 ; do
    case $(($i % 4)) in
        0 ) j="-" ;;
        1 ) j="\\" ;;
        2 ) j="|" ;;
        3 ) j="/" ;;
    esac
    tput rc
    echo -en "\r[$j] Waiting for other software managers to finish..."
    sleep 0.5
    ((i=i+1))
done

apt-get -qq -y --no-install-recommends install debconf-utils html2text apt-transport-https dialog whiptail lsb-release bc expect > /dev/null

# gather some info
#
TTY_X=$(($(stty size | awk '{print $2}')-6)) # determine terminal width
TTY_Y=$(($(stty size | awk '{print $1}')-6)) # determine terminal height
distribution=$(lsb_release -cs)
family=$(lsb_release -is)
serverIP=$(ip route get 8.8.8.8 | awk '{ print $NF; exit }')
set ${serverIP//./ }
SUBNET="$1.$2.$3."
hostnamefqdn=$(hostname -f)
mysql_pass=""
BACKTITLE="Softy - Armbian post deployment scripts, http://www.armbian.com"
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#check_status

# main dialog routine
#
DIALOG_CANCEL=1
DIALOG_ESC=255

while true; do

    # prepare menu items
    check_status
    LISTLENGHT="$((${#LIST[@]}/2))"
    exec 3>&1
    selection=$(dialog --backtitle "$BACKTITLE" --title "Installing to $family $distribution" --colors --clear --cancel-label \
    "Exit" --checklist "\nChoose what you want to install:\n " $(($LISTLENGHT+$LIST_CONST)) 70 15 "${LIST[@]}" 2>&1 1>&3)
    exit_status=$?
    exec 3>&-
    case $exit_status in
    $DIALOG_ESC | $DIALOG_CANCEL)
        clear
        exit 1
        ;;
    esac

    # cycle trought all install options
    i=0

    while [ "$i" -lt "$LISTLENGHT" ]; do

        if [[ "$selection" == *Samba* && "$SAMBA_STATUS" != "on" ]]; then
            install_samba
            selection=${selection//Samba/}
        fi

        if [[ "$selection" == *CUPS* && "$CUPS_STATUS" != "on" ]]; then
            install_cups
            selection=${selection//CUPS/}
        fi

        if [[ "$selection" == *headend* && "$TVHEADEND_STATUS" != "on" ]]; then
            install_tvheadend
            selection=${selection//\"TV headend\"/}
        fi

        if [[ "$selection" == *Minidlna* && "$MINIDLNA_STATUS" != "on" ]]; then
            install_packet "minidlna" "Install lightweight DLNA/UPnP-AV server"
            selection=${selection//Minidlna/}
        fi

        if [[ "$selection" == *ISPConfig* && "$ISPCONFIG_STATUS" != "on" ]]; then
            server_conf
            if [[ "$MYSQL_PASS" == "" ]]; then
                dialog --msgbox "Mysql password can't be blank. Exiting..." 7 70
                exit
            fi
            if [[ "$(echo $HOSTNAMEFQDN | grep -P '(?=^.{1,254}$)(^(?>(?!\d+\.)[a-zA-Z0-9_\-]{1,63}\.?)+(?:[a-zA-Z]{2,})$)')" == "" ]]; then
                dialog --msgbox "Invalid FQDN. Exiting..." 7 70
                exit
            fi
            choose_webserver; install_basic; install_DashNTP; install_MySQL; install_MySQLDovecot; install_Virus; install_$server;
            install_phpmyadmin
            [[ -z "$(dpkg --print-architecture | grep arm)" ]] && install_hhvm
            create_ispconfig_configuration;install_PureFTPD;
            install_Jailkit; install_Fail2BanDovecot; install_Fail2BanRulesDovecot;
            install_ISPConfig
            read -n 1 -s -p "Press any key to continue"
            selection=${selection//ISPConfig/}
        fi

        if [[ "$selection" == *Syncthing* && "$SYNCTHING_STATUS" != "on" ]]; then
            install_syncthing
            selection=${selection//Syncthing/}
        fi

        if [[ "$selection" == *ExaGear* && "$EXAGEAR_STATUS" != "on" ]]; then
            debconf-apt-progress -- apt-get update
            debconf-apt-progress -- apt-get -y install exagear-armbian exagear-desktop exagear-dsound-server exagear-guest-ubuntu-1604
            selection=${selection//ExaGear/}
        fi

        if [[ "$selection" == *server* && "$VPN_SERVER_STATUS" != "on" ]]; then
            install_vpn_server
            selection=${selection//\"VPN server\"/}
        fi

        if [[ "$selection" == *client* && "$VPN_CLIENT_STATUS" != "on" ]]; then
            install_vpn_client
            selection=${selection//\"VPN client\"/}
        fi
                if [[ "$selection" == *NCP* && "$NCP_STATUS" != "on" ]]; then
            install_ncp
                        selection=${selection//NCP/}
        fi

        if [[ "$selection" == *OMV* && "$OMV_STATUS" != "on" ]]; then
            install_omv
            selection=${selection//OMV/}
        fi

        if [[ "$selection" == *Plex* && "$PLEX_STATUS" != "on" ]]; then
            install_plex_media_server
            selection=${selection//Plex/}
        fi

        if [[ "$selection" == *Radarr* && "$RADARR_STATUS" != "on" ]]; then
            install_radarr
            selection=${selection//Radarr/}
        fi

        if [[ "$selection" == *Sonarr* && "$SONARR_STATUS" != "on" ]]; then
            install_sonarr
            selection=${selection//Sonarr/}
        fi

        if [[ "$selection" == *hole* && "$PI_HOLE_STATUS" != "on" ]]; then
            curl -L "https://install.pi-hole.net" | bash
            selection=${selection//\"Pi hole\"/}
        fi

        if [[ "$selection" == *Transmission* && "$TRANSMISSION_STATUS" != "on" ]]; then
            install_transmission
            selection=${selection//Transmission/}
            dialog --title "Seed Armbian torrents" --backtitle "$BACKTITLE" --yes-label "Yes" --no-label "Cancel" --yesno "\
            \nDo you want to help community and seed armbian torrent files? It will ensure faster download for everyone.\
            \n\nWe need around 80Gb of your space." 11 44
                if [[ $? = 0 ]]; then
                    install_transmission_seed_armbian_torrents
                fi
        fi

        if [[ "$selection" == *UrBackup* && "$URBACKUP_STATUS" != "on" ]]; then
            install_urbackup
            selection=${selection//UrBackup/}
        fi

        if [[ "$selection" == *Mayan* && "$MAYAN_STATUS" != "on" ]]; then
            install_mayan_edms
            selection=${selection//\"Mayan EDMS\"/}
        fi

        i=$[$i+1]
    done
    # reread statuses
    check_status
done



