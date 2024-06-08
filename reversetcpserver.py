import socket
import threading
#tcp服务器端
#client->server的报文类型有两种
#type_no=1,Initialization
#type_no=3,reverseRequest

def handle_client(client_socket,addr):
    while True:
        request=client_socket.recv(4096).decode('utf-8')#接收客户端的消息
        if not request:
            break
        request=request.split('--&--')
        #判断报文类型
        type_no=int(request[0])
        if type_no==1:#回复agree报文
            client_socket.send(f'{2}--&--'.encode())
        
        elif type_no==3:#回复reverseAnswer报文
            text=request[2]
            text=text[::-1]
            client_socket.send(f'{4}--&--{len(text)}--&--{text}'.encode('utf-8'))
    client_socket.close()


def main():
    #设置tcp服务器端
    tcp_server_ip="localhost"
    tcp_server_port=9999
    tcp_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_server.bind((tcp_server_ip,tcp_server_port))
    tcp_server.listen(5)
    print("tcp服务器已开启...")

    #接收客户端
    while True:
        try:
            client_socket,addr=tcp_server.accept()
            print(f"客户端{addr[0]}:{addr[1]}已连接")
            client_thread=threading.Thread(target=handle_client,args=(client_socket,addr))
            client_thread.start()
        except KeyboardInterrupt:
            print("已关闭服务器")
            break
    tcp_server.close()

if __name__=="__main__":
    main()