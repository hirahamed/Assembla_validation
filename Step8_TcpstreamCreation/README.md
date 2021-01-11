# Create TCP streams after clearing all the errors.

To create the TCP streams, consider the following things:

1) Put the Tcpstream_creation.py script in the Wireshark folder
Change the input paths to respective paths.
- The input will be individual pcaps (folder approach)
- assembla_data (output of assembla validation)
- matched results (from Signature verification script on individual pcaps)

Run Script: Tcpstream_creation.py (output tcps into separate folder, need to specify the path)
