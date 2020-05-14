#!/usr/bin/python
from ansible.module_utils.basic import *
from os import path
import xml.etree.ElementTree as ET


# Desired Setting for Kernel Parameters
kernel_settings  = dict(dirty_ratio = 15,
			dirty_background_ratio = 3,
			dirty_writeback_centisecs = 100,
			dirty_expire_centisecs = 500,
			swappiness = 30
 			)



def run_os_command(v_command):
    process = subprocess.Popen(v_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    v_output, v_error = process.communicate()
    v_output = v_output.decode('ascii').strip()
    v_error = v_error.decode('ascii').strip()
    if v_error:
        fail_module(v_error)
    else:
        return str(v_output)

def fail_module(p_message, p_code=245):
    module.fail_json(rc=p_code, msg="module fail: " + str (p_message))


def main():
    global module
    module = AnsibleModule(argument_spec={})
    d={}
    error_flag=False
    # Iterate through each key in the desired setting dictionary
    # and get its current value. Compare the values between the 
    # desired setting and current setting. If they dont match
    # add the parameter and its value to a dict object that will be 
    # returned to the calling task and displayed with an error message

    for key in kernel_settings.keys():
         os_str="sysctl -a 2>/dev/null| grep -v sysctl | grep "+key+" " 
         op_str=run_os_command(os_str)
         # Split around = to get key and value
         split=op_str.split("=")
         # split the key further around . to remove the prefix
         pkey=split[0].split(".")

         param_key=pkey[1].strip()
         param_val=split[1].strip()
         if int(param_val) != kernel_settings[param_key]:
            d[param_key]  = param_val
            error_flag=True
    if not error_flag:
        module.exit_json(changed_flag=False,msg="****Kernel Parameter Setting are CORRECTLY set****" ,**d)
    else:
        module.fail_json(changed_flag=False,msg="****Kernel Parameter Settings are INCORRECTLY set****", **d)
if __name__ == '__main__':
     main()

