#! /usr/bin/env python
import lcddriver
import os
import sys
import subprocess
import time
import OPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Variaveis de conexão
path = "Z00209.JCL"
ipHost = "192.86.32.153"
portHost = "10443"
user = "z00209"
passwd = "fruit102"

# Function to submit the job
def jobSub(job):
    # Submit and get jobid
    jobid = subprocess.check_output('zowe zos-jobs submit data-set "' + path + '(' + job + ')" -H ' + ipHost + ' -P ' + portHost + ' -u ' + user + ' --pw ' + passwd + ' --ru false --rff jobid --rft string', shell=True).decode(sys.stdout.encoding).strip()
    
    text = "JOB ID: " + jobid
    lcd.lcd_display_string(text, 3)
    
    
    # Check job status every three seconds
    status="NULL"
    while ( status != "OUTPUT" ):
      lcd.lcd_display_string("Awaiting completion.", 4)
      status = subprocess.check_output('zowe zos-jobs view job-status-by-jobid ' + jobid + ' -H ' + ipHost + ' -P ' + portHost + ' -u ' + user + ' --pw ' + passwd + ' --ru false --rff status --rft string', shell=True).decode(sys.stdout.encoding).strip()
      time.sleep(3)
    
    # Check return code
    rc = subprocess.check_output('zowe zos-jobs view job-status-by-jobid ' + jobid + ' -H ' + ipHost + ' -P ' + portHost + ' -u ' + user + ' --pw ' + passwd + ' --ru false --rff retcode --rft string', shell=True).decode(sys.stdout.encoding).strip()
    
    if (rc == "CC 0000"):
      lcd.lcd_display_string("                    ", 4)
      lcd.lcd_display_string("Congratulation, the ", 3)
      lcd.lcd_display_string("JCL " + job + " run OK!", 4)
      GPIO.output(23, True)
    elif (rc == "JCL ERROR"):
      lcd.lcd_display_string("                    ", 3)
      lcd.lcd_display_string("Sorry, JCL " + job, 3)
      lcd.lcd_display_string("not run: JCL ERROR  ", 4)
      GPIO.output(19, True)
    elif (rc.split(" ")[0] == "CC" and int(rc.split(" ")[1]) <= 4):
      lcd.lcd_display_string("                    ", 3)
      lcd.lcd_display_string("                    ", 4)
      lcd.lcd_display_string("Warning JCL " + job, 3)
      lcd.lcd_display_string("run with RC " + rc.split(" ")[1], 4)
      GPIO.output(21, True)
    elif (rc.split(" ")[0] == "CC" and int(rc.split(" ")[1]) > 4):
      lcd.lcd_display_string("                    ", 3)
      lcd.lcd_display_string("                    ", 4)
      lcd.lcd_display_string("Fail! JCL " + job, 3)
      lcd.lcd_display_string("run with RC " + rc.split(" ")[1], 4)
      GPIO.output(19, True)
    else:
      lcd.lcd_display_string("Ops, something went ", 3)
      lcd.lcd_display_string("  wrong! ¯\_(ツ)_/¯  ", 4) 
    updt = 1
# End jobSub

# Initialize display
lcd = lcddriver.lcd()
# Display title
lcd.lcd_display_string('MTM20 JOB SUBMITTER!', 1)
lcd.lcd_display_string('SEARCHING FILE LIST.', 3)

# List partitioned dataset
ds = subprocess.check_output('zowe zos-files list all-members "' + path + '" -H ' + ipHost + ' -P ' + portHost + ' -u ' + user + ' --pw ' + passwd + ' --ru false', shell=True).decode(sys.stdout.encoding).strip()
count = 0
updt = 1
dsList = ds.split("\n")

try:
    print("Press CTRL+C to Exit")
    lcd.lcd_display_string("                    ", 3)
    while True:
        if updt == 1:
            lcd.lcd_display_string("                    ", 2)
            lcd.lcd_display_string(dsList[count] + " < SELECT   ", 2)
            GPIO.output(19, True)
            GPIO.output(21, True)
            GPIO.output(23, True)
            updt = 0
        if GPIO.input(15) == GPIO.LOW:
            count += 1
            updt = 1
        if GPIO.input(13) == GPIO.LOW:
            count -= 1
            updt = 1
        if count == len(dsList):
            count = 0
        if count == - 1:
            count = len(dsList) - 1
        if GPIO.input(11) == GPIO.LOW:
            lcd.lcd_display_string(dsList[count] + " > SUB      ", 2)
            lcd.lcd_display_string("                    ", 3)
            lcd.lcd_display_string("                    ", 4)
            jobSub(dsList[count])
        time.sleep(0.1)

except KeyboardInterrupt:
    print(" ")
    print("Bye")

finally:
    GPIO.cleanup()
