# After resolving errors on Individual pcaps, we will run this script

Before running script for signature matching on master pcaps:

We need to run the script: pcap_2_master.py (it will create master pcaps for all the apps in a particular folder(you need to specify the path))

Now put the main script i.e. process_Master_pcaps_file.py in the folder having all the master pcaps.

Run the process_Master_pcaps_file.py, it tasks assembla_data(output of assembla validation script) and master pcaps as an input.
