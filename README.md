# TCP-socket-Program
作业介绍：
	使用python TCP socket程序自定义应用层报文以及模拟报文交互。
作业功能：
	1.client每次发送全英文可打印字符的ASCII文件的不定长的一段给server,server端把文本reverse，并返回给client。
	2.一共有四种报文类型，通过Type字段来区分。client端向server端发送Initialization报文，告知server要做reverse的块数N,server回复agree报文。client逐次向server发送reverseRequest报文，包含了要做reverse的数据；server端返回reverseAnswer报文，其中包含了reverse之后的数据。reverseRequest、reverseAnswer报文中Length字段分别指的是Data和reverseData的长度，单位是Byte。
	3.client每次发送的reverseRequest中的长度都不一样（即不是例如每次固定发送500字节)，长度限定在一个[Lmin,Lmax]之间，最后一块除外。
	
作业配置：
	操作系统：Windows10，ubuntu.20.04.1
	开发语言：python 3.8.10，python 3.12.1
	编辑器：VS Code
	Unicode字符编码：utf-8
