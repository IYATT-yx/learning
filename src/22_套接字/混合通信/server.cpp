/**
 * @file server.cpp
 * @brief TCP 服务器
 * 
 * 支持多客户端接入 - 基于多进程，每个接入的连接有独立的进程进行处理
 * 服务器会将收到的数据原路发送回客户端
 * 
 * Copyright (C) 2021 IYATT-yx (Zhao Hongfei, 赵洪飞)，2514374431@qq.com
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
#include <iostream>
#include <cstring>
#include <cerrno>
#include <string>

extern "C"
{
    #include <sys/types.h>
    #include <sys/socket.h>
    #include <arpa/inet.h>
    #include <unistd.h>
    #include <signal.h>
    #include <sys/wait.h>
    #include <getopt.h>
}


/**
 * @brief 回收子进程
 * @param num 被回收子进程的 pid
 */
void recycle(int num)
{
    (void)num;
    while (waitpid(-1, NULL, WNOHANG) > 0)
    {
        return;
    }
}

int main(int argc, char **argv)
{
    /**
     * 服务器信息初始化
     */
    struct sockaddr_in server;
    memset(&server, 0, sizeof(server));
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = htonl(INADDR_ANY);

    /**
     * 解析命令行参数获取要监听的端口号
     */
    int opt;
    bool is_false = true;  // 正确获取到端口号时置为 false
    while ((opt = getopt(argc, argv, "p:")) != -1)
    {
        switch (opt)
        {
            case 'p':
            {
                unsigned short port = static_cast<unsigned short>(atoi(optarg));
                /**
                 * 当参数出现非数字，转换结果为 0
                 * 当端口取值在 0～1023 时，需要 root 权限才可使用
                 * 端口号取值范围 0～65535，unsigned short 可储存的数据范围为 0～65536，不用再比较大于 65535
                 */
                if (port < 1024)
                {
                    std::cerr << "请确认输入的端口号在 1024～65535 之间！\n";
                    exit(EXIT_FAILURE);
                }
                std::cout << "监听端口： " << port << "\n";
                server.sin_port = htons(port);
                is_false = false;
                break;
            }
            default:
            {
                break;
            }
        }
    }
    if (is_false)
    {
        std::cerr << "请按格式 [-p] [port] 指定要监听的端口号！\n";
        exit(EXIT_FAILURE);
    }

    int lfd = socket(AF_INET, SOCK_STREAM, 0);
    if (lfd == -1)
    {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    int flag = 1;
    if (setsockopt(lfd, SOL_SOCKET, SO_REUSEADDR, &flag, sizeof(flag)) == -1)
    {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }

    if (bind(lfd, (struct sockaddr *)&server, sizeof(server)) == -1)
    {
        perror("bind");
        exit(EXIT_FAILURE);
    }

    if (listen(lfd, 5) == -1)
    {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    /**
     * 回收终止连接的子进程
     */
    struct sigaction act;
    act.sa_handler = recycle;
    act.sa_flags = 0;
    sigemptyset(&act.sa_mask);
    sigaction(SIGCHLD, &act, NULL);

    struct sockaddr_in client;  // 储存建立连接的客户端信息
    socklen_t len = sizeof(client);
    memset(&client, 0, len);
    while (true)
    {
        int cfd = accept(lfd, (struct sockaddr *)&client, &len);  // 接受连接请求
        if (cfd == -1 && errno == EINTR)
        {
            cfd = accept(lfd, (struct sockaddr *)&client, &len);
        }
        else if (cfd == -1)
        {
            perror("accept");
            exit(EXIT_FAILURE);
        }

        char ipbuf[64] = {0};
        uint16_t port = ntohs(client.sin_port);
        std::cout << "\n"
                    << inet_ntop(AF_INET, &client.sin_addr.s_addr, ipbuf, sizeof(ipbuf))
                    << port
                    << " 接入连接\n";

        pid_t pid = fork();
        if (pid == 0)
        {
            close(lfd);
            while (true)
            {
                char buf[1024];
                memset(buf, 0, sizeof(buf));
                ssize_t length = read(cfd, buf, sizeof(buf));
                if (length == -1)
                {
                    perror("read error");
                    exit(EXIT_FAILURE);
                }
                else if (length == 0)
                {
                    std::cout << ipbuf << ":" << port << "断开了连接！\n";
                    close(cfd);
                    exit(EXIT_SUCCESS);
                }
                else
                {
                    std::cout << ipbuf << ":" << port << ": " << buf << "\n";
                    write(cfd, buf, strlen(buf));
                    memset(buf, 0, sizeof(buf));
                    continue;
                }
                return EXIT_SUCCESS;
            }
        }
        else if (pid > 0)
        {
            close(cfd);
        }
    }
    close(lfd);
}
