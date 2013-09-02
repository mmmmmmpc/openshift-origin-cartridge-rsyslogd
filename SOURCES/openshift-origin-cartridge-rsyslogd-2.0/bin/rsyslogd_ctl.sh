#!/bin/bash -e

cartridge_type="rsyslogd-1.0"
source "/etc/openshift/node.conf"
source ${CARTRIDGE_BASE_PATH}/abstract/info/lib/util

# Control application's embedded remote logging service (rsyslog)
CART_INFO_DIR="${CARTRIDGE_BASE_PATH}/embedded/${cartridge_type}/info/"

function _is_rsyslogd_enabled() {
   [ -f $CART_INSTANCE_DIR/run/syslogd.pid ]  &&  return 0
   return 1

}  #  End of function  _is_syslogd_enabled.


function _rsyslogd_status() {
   if [ -f "$CART_INSTANCE_DIR/run/syslogd.pid" ]; then
      njobs=1
      if (pidof rsyslogd); then 
        echo "rsyslogd is running"
      else 
        echo "rsyslogd lockfile present but process dead" 1>&2
      fi
   fi
   if _is_rsyslogd_enabled; then
      echo "rsyslogd logging service is enabled" 1>&2
   else
      echo "rsyslogd logging service is disabled" 1>&2
   fi

}  #  End of function  _rsyslogd_status.


function _rsyslogd_enable() {
    # if we are not configured then configure us
    # we should probably call hooks/configure instead here
    if [ -d /$CART_INSTANCE_DIR ] ; then
       echo "${CART_INSTANCE_DIR} is present"
    else
       mkdir -p /${CART_INSTANCE_DIR}/configuration 
       mkdir -p /${CART_INSTANCE_DIR}/run
       mkdir -p /${CART_INSTANCE_DIR}/etc
       chmod go+rwx /${CART_INSTANCE_DIR}/run 
       cp /${RSYSLOG_INSTANCE_DIR}/embedded/info/configuration/etc/{rsyslog,rsyslog.conf} /${CART_INSTANCE_DIR}/etc/
    fi
    if [ -f /$RSYSLOG_INSTANCE_DIR/embedded/info/configuration/etc/rsyslog ] ; then
       echo "using rsyslog variables dir: /${RSYSLOG_INSTANCE_DIR}/embedded/info/configuration/etc/rsyslog"
       source /$RSYSLOG_INSTANCE_DIR/embedded/info/configuration/etc/rsyslog
    else
       SYSLOGD_OPTIONS="-c5"
       echo "using default rsyslogd options ${SYSLOGD_OPTIONS}"
    fi


    if _is_rsyslogd_enabled; then
        src_user_hook pre_start_rsyslogd-1.0
        echo "rsyslogd service is already enabled" 1>&2
        run_user_hook post_start_rsyslogd-1.0
    else
        echo "starting rsyslogd" 1>&2
        echo $"Starting system logger: "
        echo "starting: /sbin/rsyslogd -f ${CART_INFO_DIR}/configuration/etc/rsyslog.conf -c5 -i $CART_INSTANCE_DIR/run/syslogd.pid" 
        /sbin/rsyslogd -c5 -f ${CART_INFO_DIR}/configuration/etc/rsyslog.conf -i "$CART_INSTANCE_DIR/run/syslogd.pid" 
        RETVAL=$?
        echo
        [ $RETVAL -eq 0 ] && touch $CART_INSTANCE_DIR/run/syslogd.pid
        return $RETVAL
    fi

}  #  End of function  _rsyslogd_enable.


function _rsyslogd_disable() {
    if _is_rsyslogd_enabled; then
        src_user_hook pre_stop_rsyslogd-1.0
        run_as_user "/usr/bin/killall rsyslogd"
        rm -f $CART_INSTANCE_DIR/run/syslogd.pid
        run_user_hook post_stop_rsyslogd-1.0
    else
        echo "rsyslogd service is already disabled" 1>&2
    fi

}  #  End of function  _rsyslogd_disable.


function _rsyslogd_reenable() {
   _rsyslogd_disable
   _rsyslogd_enable

}  #  End of function  _rsyslogd_reenable.


#
# main():
#
# Ensure arguments.
if ! [ $# -eq 1 ]; then
    echo "Usage: $0 [enable|reenable|disable|status|start|restart|stop]"
    exit 1
fi

# Import Environment Variables
for f in ~/.env/*; do
  . $f
done

translate_env_vars
validate_run_as_user

# Cartridge instance dir and control script name.
CART_INSTANCE_DIR="$OPENSHIFT_HOMEDIR/$cartridge_type"
CTL_SCRIPT="$CARTRIDGE_BASE_PATH/$cartridge_type/info/bin/app_ctl.sh"

case "$1" in
   enable|start)      _rsyslogd_enable   ;;
   disable|stop)      _rsyslogd_disable  ;;
   reenable|restart)  _rsyslogd_reenable ;;
   status)            _rsyslogd_status   ;;
esac

