import socket
import random
import argparse
#tcp客户端
#server->client的报文类型有两种
#type_no=2，agree
#type_no=4，reverseAnswer

#获取文件内容函数
def open_file(filename):
    file=open(filename,'r',encoding='utf-8')
    lines = [line.strip() for line in file.readlines()]
    con=''.join(lines)
    file.close()
    return con

def main(tcp_server_ip,tcp_server_port,min_len,max_len):
    tcp_client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_client.connect((tcp_server_ip,tcp_server_port))

    #获取文件内容
    content=open_file("ascii.txt")

    #获取文件长度
    total_len_content=len(content)

    
    blocks=[]#块数

    #获取所有块数
    while True:
        block=random.randint(min_len,max_len)
        if block>=total_len_content:
            blocks.append(block)
            break
        else:
            total_len_content-=block
            blocks.append(block)
    
    answer=input("已经计算完毕所需要的块数，请回答是否开始反转(yes or no):")
    if answer=='yes':
        tcp_client.send(f'{1}--&--N={len(blocks)}'.encode())
        response=tcp_client.recv(4096).decode()
        response=response.split('--&--')
        type_no=int(response[0])
        reverse_content=[]#反转的内容
        if type_no==2:
            print("开始打印文件的reserve版本!")

            #根据块数进行切割文件内容发送
            for i in range(len(blocks)):
                if i==0:
                    s=content[0:blocks[i]]
                elif i==len(blocks)-1:
                    pre_sum=sum(blocks[:i])
                    s=content[pre_sum:]
                else:
                    pre_sum=sum(blocks[:i])
                    s=content[pre_sum:pre_sum+blocks[i]]
                #发送reverseRequest报文
                tcp_client.send(f'{3}--&--{len(s)}--&--{s}'.encode())
                #接收reverseAnswer报文
                response=tcp_client.recv(4096).decode()
                response=response.split('--&--')
                type_no=int(response[0])
                reverse_content.append(response[2])
                if type_no==4:
                    print(f'第{i+1}块: ',response[2])
        else:
            print("没有收到服务器端的回复")
        with open("reverse_ascii.txt",'w',encoding='utf-8') as file:
            file.writelines(reverse_content)
    else:
        print("你已拒绝反转文件")
    tcp_client.close()


    
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--tcp_server_ip",help="TCP Server IP address")
    parser.add_argument("--tcp_server_port",type=int,help="TCP Server Port")
    parser.add_argument("--min_len",default=50,type=int,help="minimum length of block")
    parser.add_argument("--max_len",default=100,type=int,help="maximum length of block")
    args=parser.parse_args()
    main(args.tcp_server_ip,args.tcp_server_port,args.min_len,args.max_len)