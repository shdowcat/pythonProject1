from netmiko import ConnectHandler
import netmiko
import getpass
import socket
import sys

password = getpass.getpass('Password:')
cmd_save = 'save'
switch_login_failed_lists = []
switch_connection_failed_lists = []
switch_config_done_lists = []

with open('ip.txt') as ip_list :

    for line in ip_list.readlines() :
        try:
            ip = line.strip()
            SW = {
            'device_type':'huawei',
            'ip':ip,
            'username':'admin',
            'password':password,
             }
            connect = ConnectHandler(**SW)
            print ("successful connected to " +  SW['ip'] + " !!!")
            output_1 = connect.send_config_from_file('commands.txt')
       # config_commands = ['int loop 0','ip add 2.2.2.2 32']
       # output = connect.send_config_set(config_commands)
       # print (output_1)
            output_2 = connect.send_command(cmd_save,expect_string=r'\[Y/N\]')
            output_2 += connect.send_command('Y',expect_string=r'>')
            print(ip + " Saved !!!")
            #print (output_2)
            #result = connect.send_command('dis acl 2000 ')
            #print (result)
            print (ip + " all config done !!!")
            switch_config_done_lists.append(ip)
        except netmiko.exceptions.NetmikoAuthenticationException:
            print ("Login  failed for " + ip + " !!!")
            switch_login_failed_lists.append(ip)
        except netmiko.exceptions.NetmikoTimeoutException:
            print ("Connetction failed for " + ip + " !!!")
            switch_connection_failed_lists.append(ip)

print ('\nUser authentication failed for below swtiches : ')
for i in switch_login_failed_lists :
    print (i)
print ('\nBelow switches are not reachable : ')
for i in switch_connection_failed_lists :
    print (i)
print ('\nBelow switches are successful configured : ')
for i in switch_config_done_lists :
    print (i)
