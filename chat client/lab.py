import socket
import threading

def listening():
    data = ""
    dataVal = 1024

    while True:
        new_msg = sock.recv(dataVal).decode("utf-8")
        data += new_msg

        if(len(new_msg) < dataVal):
            arr = []
            arr = data.splitlines(True)

            for i in range(len(arr)):
                dataHandle(arr[i])
            data = ""

def dataHandle(data):
    status = data.split()[0]
    if(status == "SEND-OK"):
        pass
    elif(status == "UNKNOWN"):
        print("Requested user is not logged in!")
    elif(status == "BAD-RQST-HDR"):
        print("An error occured: Bad request header!")
    elif(status == "BAD-RQST-BODY"):
        print("An error occured: Bad request body!")
    else: 
        msg = "~" + data[len(status) + 1: len(data) -1]
        print(msg)
    
a = "Login with a username:\n"
while True:
	try:
	    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    host_port = ("18.195.107.195", 5378)
	    sock.connect(host_port)
	    username = input(a)
	    message = ("HELLO-FROM " + username + "\n").encode("utf-8")
	    sock.sendall(message)
	    data = sock.recv(4096).decode("utf-8")
	    if(username):
	        if(data == "IN-USE\n"):
	            a = "The username is already in use! Try to login with another username:\n"
	            sock.close()
	            continue
	        elif(data == "BUSY\n"):
	            print("The server has reached its user limit!")
	            sock.close()
	            sys.exit()
	        else:
	            break
	except OSError as msg: 
		print(msg)

t = threading.Thread(target=listening, daemon=True)
t.start()

while True:
	try:
	    user_input = input()
	    if(user_input):
	        if(user_input == "!quit"):
	            sock.close()
	            break
	        elif(user_input == "!who"):
	            command = "WHO\n".encode("utf-8")
	        elif(user_input[0] == "@"):
	            user = user_input.split()[0]
	            msg = user_input[len(user):]
	            username = user[1:]
	            command = ("SEND " + username + " " + msg + "\n").encode("utf-8")
	        else:
	            print("Unvalid command!")
	            continue
	        sock.sendall(command)    
	except OSError as msg: 
		print(msg)


