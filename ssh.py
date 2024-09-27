
####import the Paramiko library:
###
###
###from paramiko.client import SSHClient, AutoAddPolicy
###SSH_USER = "red"
###SSH_PASSWORD = "W1ldcat$"
###SSH_HOST = "10.38.254.252"
###SSH_PORT = 22 # Change this if your SSH port is different
###client = SSHClient()
###client.set_missing_host_key_policy(AutoAddPolicy())
###client.load_system_host_keys()
###try:
###    client.connect(SSH_HOST, port=SSH_PORT,
###                             username=SSH_USER,
###                             password=SSH_PASSWORD,
###                             look_for_keys=False)
###    print("Connected successfully!")
###except Exception:
###    print("Failed to establish connection.")
###
###finally:
###    client.close()
#To run this script, go to your terminal and execute it with the following:
#python3 initiating.py
#How it works...
#In this example, we first imported the Paramiko library's SSHClient class. Next, we set up our connection details. While you could also provide these details directly when calling the connect method on the client object, it is good practice to put them into variables. This means that if you are creating multiple client objects at different points of your script, you don't have to change the username/password and host in each of these calls but just once in the variables. Be careful when submitting these scripts to your colleagues or uploading them to code hosting services though, as they do contain your login details. You can have a look at the There's more section of this recipe to see how you can either prompt for this information interactively or get it from your environment.

#Before connecting to the device, using the connect method, we load the host keys. SSH uses host keys and the fingerprints of an SSH server to make sure that the IP you are connecting to is the server you connected to before. When connecting to a brand-new device, you'll have to accept this new host key. While we can keep a separate set of host keys for our Paramiko client, it is usually best to just use the host keys that the user executing the script has. By doing this, you can connect to every device you have previously connected to from your command line, also from your Paramiko scripts.

#To do this loading, we are using the load_system_host_keys() function. This function searches the default known hosts file used by OpenSSH and copies them over into Paramiko. See the following section for an example of how to make Paramiko accept new keys by default.

#With our host keys configured, we can now actually connect to the device that we have specified. To do so, we are using a try-catch block. This is a Python construct that allows us to catch exceptions, errors that can be raised by any part of the code we are using, and handle them. Python will attempt to execute the instructions in the try block. If any part of that code, in our example the connect() method, errors out and raises an exception, Python will jump into the except block and execute the instructions within that block. In our example, we are only printing out a message that our connection was unsuccessful. The third block, our finally block, will be executed both when the connection has been successful (our except block was not executed) as well as after a failed connection (our except block was executed). This allows us to clean up after both a successful and unsuccessful connection and avoids dangling SSH connections.

#There's more...
#In this example, we relied on the user having already logged into the device from their command line in order for the host to be known. If we use the preceding code to connect to a device that was not previously known, the code will fail with an exception.

#The way Paramiko handles unknown host keys can be specified using a policy. One of these policies, AutoAddPolicy, allows us to just add unknown host keys to our scripts set of host keys:


from pexpect import pxssh
import getpass
try:
    s = pxssh.pxssh()
    hostname = raw_input('hostname: ')
    username = raw_input('username: ')
    password = getpass.getpass('password: ')
    s.login(hostname, username, password)
    s.sendline('uptime')   # run a command
    s.prompt()             # match the prompt
    print(s.before)        # print everything before the prompt.
    s.sendline('ls -l')
    s.prompt()
    print(s.before)
    s.sendline('df')
    s.prompt()
    print(s.before)
    s.logout()
except pxssh.ExceptionPxssh as e:
    print("pxssh failed on login.")
    print(e)




