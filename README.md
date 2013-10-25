Rsyslog Openshift cartridge README
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Roger Nunn <rnunn@redhat.com>


The Rsyslog cartridge uses the in gear: configuration/etc/rsyslog.conf config dir
by default. 

The Rsyslog cartridge can also use the system wide /etc/rsyslog.conf
enabling a central point of log administration for all gears if needed

Logs are located in tmp/logs along with a socket for application logs to use: 
/tmp/log for convenience these are symlinked into <gear_instance>/rsyslog/{logs,log_socket}

Please note that this is experimental, the socket is world readable and located 
in the gear dirs .tmp dir. With this in mind. There is selinux protection but 
TODO: improve log socket security as much as possible

Test this in your app gear with the logger command (note the node and gear in the message origin)
logger -d -u /tmp/log "hello world" 

FOR REMOTE LOGGING TO AN EXTERNAL HOST: 
There are two options for remote logging 
either open an rsyslogd remote logging port on the local node (universal for all gears whether
visiting or not), 
and configure the remote host line in the rsyslog.conf file located
in this directory to 127.0.0.1:514 (this assumes that your openshift node 
runs a log parser/agent) 

or export the logs straight from the gear itself by adding an alternative 
forwarder network address in your <app_git_repo>.openshift/rsyslogd/rsyslogd.d/rsyslog.conf 
rsyslog include dir for the gear. (remember to restart rsyslog, you are not limited by name 
*.conf is included)  

For your application you may want to create a sym-link to the required directory
in app-root for the logging socket: /tmp/log 

When you remove the rsyslogd configuration the cartridge is disabled from the gear
but the logs are left in place. 

Otherwise you are on your own :) 

