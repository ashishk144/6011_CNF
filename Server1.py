from socket import *
from threading import *
import mimetypes
# import signal
import os
import sys
# import time
import subprocess

ROOT= "/home/ubuntu/Downloads/Test"

def create_socket():
    host = "127.0.0.1"
    port = 8888
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((host,port))
    return s

def start_server(soc):
    soc.listen(500)
    print("Server has started")
    try:
        while True:
            conn, addr = soc.accept()
            print("Connection established with: " + str(addr))
            thread = Thread(target = start_thread, args = (conn,)).start()
    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\r\n'
        data = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode()

def start_thread(con):
    recv = con.recv(1024).decode()
    req_file, arg = get_file(recv)
    content = get_content(req_file, arg)
    con.send(content)
    con.close()

def get_file(data):
    pieces = data.split(" ")
    myfile = ""
    args = 0
    if (len(pieces) > 0 ) :
        requesting_file = pieces[1]
        fileargs = requesting_file.split('?')
        myfile = fileargs[0]
        if len(fileargs) > 1:
            args = fileargs[1].split("=")[1]
        myfile = myfile.lstrip('/')
    return myfile, args

def execute(file, arg):
    # p = subprocess.Popen("python3 " + ROOT + "/" + file, stdout=subprocess.PIPE, shell=True)
    # (output, err) = p.communicate()
    # return output
    stdin  = sys.stdin.fileno() # usually 0
    stdout = sys.stdout.fileno() # usually 1
    parentin, childout  = os.pipe()
    childin,  parentout = os.pipe() 
    sys.stdout.flush()
    pid = os.fork()
    # print(arg)
    if pid > 0:
        os.close(childout)
        # parentout = os.fdopen(parentout,'w')
        # os.dup2(parentin,  stdin)
        # os.dup2(parentout, stdout)
        parentout = os.fdopen(parentout,'w')
        if arg:
            parentout.write(str(arg))
        parentout.close()
        os.close(childin)
        os.dup2(parentin,  stdin)
        # print(arg)
        parentin = os.fdopen(parentin,'r')
        s = input()
        # parentin.close()
        return s
    else:
        os.close(parentin)
        os.close(parentout)
        os.dup2(childin,  stdin)
        childin = os.fdopen(childin,'r')
        os.dup2(childout, stdout)
        childout = os.fdopen(childout,'w')
        exec(open(ROOT +"/" + file).read())
        sys.exit(0)

def get_content(filename, arg):
    header = "HTTP/1.1 200 OK\r\n"
    resp = "".encode()
    if "%20" in filename:
        filename = filename.replace("%20", " ")

    if filename == "":
        header += "Content-Type: text/html; charset=utf-8\r\n\r\n"
        res = get_files(filename)
        resp += res.encode()
    elif filename.endswith(".py"):
        header += "Content-Type: text/html; charset=utf-8\r\n\r\n"
        resp = "<strong><center>Code Executed!</center></strong><br>"
        resp += execute(filename, arg)
        # print("resp: ", resp)
        resp=resp.encode()
        # if resp != None:
        #     resp.encode()
    else:
        mimetype = mimetypes.guess_type(filename)[0]
        if mimetype != None:
            header += "Content-Type: " + str(mimetype) + "\r\n\r\n"
            # print(filename)
            try:
                file = open(filename,'rb')
                res = file.read()
                # print(res)
                file.close()
                resp += res
            except Exception as e:
                # print("Except")
                header = 'HTTP/1.1 404 Not Found\r\n'
                resp = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode()
        else:
            header += "Content-Type: text/html; charset=utf-8\r\n\r\n"
            res = get_files("/"+filename)
            # print(res)
            resp += res.encode()
    header = header.encode()
    final_resp = header + resp
    return final_resp

def get_files(path):
    files = []
    for file in os.listdir(ROOT + path):
        files.append("<a href = \""+os.path.join(path, file) + "\"  > " + file +"</a> <br>")
    return ''.join(files)

def main():
    start_server(create_socket())

if __name__ == '__main__':
    main()
