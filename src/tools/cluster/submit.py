#!/bin/env python

import os
import stat
import glob
import subprocess
import time

start_time = time.time()
maxjobs = 5000
# maxjobs = 3000
first_job = 0
jobcount = 0
skipped_jobs = 0
max_concurrent_jobs = 250
bstat_freq = 25
bstat_countdown = 0
os.chdir('jobscripts_2017-06-28')
all_jobs = glob.glob("subtree*.sh")
for job in all_jobs:
    if first_job > skipped_jobs:
        skipped_jobs += 1
        continue
    jobcount += 1
    if jobcount > maxjobs:
        break
    # Make sure script is executable
    permissions = os.stat(job).st_mode
    desired_permissions = permissions | stat.S_IEXEC
    if permissions != desired_permissions:
        os.chmod(job, desired_permissions)
    # Don't submit so many jobs at once
    if bstat_countdown <= 0:
        print("%d jobs submitted so far, out of %d total" % (jobcount, len(all_jobs)))
        job_list = subprocess.check_output(['bjobs',])
        running_count = len(job_list.splitlines()) - 1
        while running_count > (max_concurrent_jobs - bstat_freq):
            sleep_interval = 10
            print("%d jobs are currently running. Waiting %d seconds before checking again..." % (running_count, sleep_interval) )
            time.sleep(10)
            job_list = subprocess.check_output(['bjobs', ])
            running_count = len(job_list.splitlines()) - 1
        bstat_countdown = bstat_freq
    bstat_countdown -= 1
    # print (job)
    cmd = "bsub -P mouselight -o %s.log -W 60 -We 12 ./%s" % (job, job)
    print (cmd)
    os.system(cmd)
elapsed_time = time.time() - start_time
print("Submitted %d jobs in %d seconds" % (elapsed_time, len(all_jobs)))
