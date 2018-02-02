#Import modules for connection to ssh and parsing file
import paramiko 
import fnmatch
import glob
import re

def main():
    host, search_parh, file_type, search_str = get_user_data()
    user, secret = auth_data(host)
    sftp_client = connect_to_ssh(host, user, secret)
    parse_file(search_path, sftp_client, file_type, search_str)
    
def auth_data(ip_adress):
    # to use dictiany 
    ssh_data_dict = {
        "grex.org": {
            "user": "v_vzakaryan",
            "password": "Today12345!"
        },
        "xxx.xxx.x.x": {
            "user": "username",
            "password": "password"
        }
    }
    user_data = ssh_data_dict.get(ip_adress, "grex.org")
    return user_data["user"], user_data["password"]

def get_user_data():
    host = raw_input("Enter the ip : ")
    search_path = raw_input("Enter log directory path to search : ")
    file_type = raw_input("Enter log file extension (last few symbols) : ")
    search_str = raw_input("Enter the id (or another text) : ")
    return host, search_path, file_type, search_str   

def connect_to_ssh(host, user, secret):
    print("Connecting to ssh")
    print(user, secret)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=22)
    sftp_client = client.open_sftp()
    return sftp_client
    
def parse_file(search_path, sftp_client, file_type, search_str):
    # Append a directory separator if not already present
    print("Starting parsing")
    if not (search_path.endswith("/") or search_path.endswith("\\") ): 
        search_path = search_path + "/"
                                                          
    # If path does not exist, set search path to current directory
    if search_path == "":
        search_path ="."

    # Repeat for each file in the directory  
    for fname in sftp_client.listdir(path=search_path):
        # Apply file type filter   
        if fname.endswith(file_type):

            with open(search_path + fname, "r") as f:
                for num, line in enumerate(f, 1):
                    if search_str in line:
                        print("String number is: " + str(num))
                        f.seek(1)            
                        break
    
                # Check number of line with search result and define line from
                if (num < 100):
                    lineFrom = 1
                else:
                    lineFrom = num - 100

                # Check size of log and define line To
                num_lines = sum(1 for line in open(search_path + fname))
                if (num_lines < (num + 100)):
                    lineTo = num_lines
                else:
                    lineTo = num + 100

                # Print lines from lineFrom to lineTo
                for num, line in enumerate(f, 1):
                    if (num >= 0 and num <= lineTo):         
                        num = str(num)
                        print ("{} {}".format(line.split(','), num))

        else:
            print("There are no search string in file " + fname)

#-------------------------------
if __name__ == "__main__":
    main()