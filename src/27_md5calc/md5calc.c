/**
 * @file md5calc.c
 * @brief md5 计算
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
#include <openssl/md5.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#if defined(__linux) || defined(__linux__)
	#include <getopt.h>
	#include <sys/types.h>
	#include <sys/stat.h>
	#include <fcntl.h>
	#include <unistd.h>
#elif
    #error "请在 Linux 下构建该程序！"
#endif

#if !defined(__x86_64__)
	#error "请在64位环境下构建！"
#endif

/**
 * @brief 摘要数据转文本
 * @param digest 摘要数据
 * @return 文本结果
 */
char *digestToString(const unsigned char *digest)
{
	char tmp[3] = {'\0'};
	char *string = (char *)malloc(33);
	for (int i = 0; i < 16; ++i)
	{
		sprintf(tmp, "%02x", digest[i]);
		strcat(string, tmp);
	}
	return string;
}

/**
 * @brief 32位MD5计算
 * @param data 数据
 * @param len 数据长度
 * @return 32位MD5
 */
char *md5_32(const void *data, size_t len)
{
    MD5_CTX ctx;
    MD5_Init(&ctx);
    MD5_Update(&ctx, data, len);
    unsigned char digest[MD5_DIGEST_LENGTH] = {0};
    MD5_Final(digest, &ctx);
    return digestToString(digest);
}

/**
 * @brief 16位MD5计算
 * @param digest32 32位MD5
 * @param 16位MD5
 */
char *md5_16(const char *digest32)
{
	char *digest16 = (char *)malloc(17);
	memset(digest16, '\0', 17);
	for (int i = 8, j = 0; j < 16; ++i, ++j)
	{
		digest16[j] = digest32[i];
	}
	return digest16;    
}

/**
 * @brief HMAC-MD5计算
 * @param data 数据
 * @param dataLen 数据长度
 * @param key 密钥
 * @param leyLen 密钥长度
 * @return HMAC-MD5
 */
char* hmac_md5(const void *data, size_t dataLen, const void *key, size_t keyLen)
{
	unsigned char digest[17];
	digest[16] = 0x00;
	MD5_CTX context;
	unsigned char k_ipad[65];
	unsigned char k_opad[65];
	unsigned char tk[MD5_DIGEST_LENGTH];
	
	if (keyLen > 64){
		MD5_CTX tctx;
		MD5_Init(&tctx);
		MD5_Update(&tctx, key, keyLen);
		MD5_Final(tk,&tctx);
		
		key = tk;
		keyLen= 16;
	}
	
	memset( k_ipad, 0, sizeof(k_ipad));
	memset( k_opad, 0, sizeof(k_opad));
	memcpy( k_ipad, key, keyLen);
	memcpy( k_opad, key, keyLen);
	for(int i = 0; i < 64; i++)
	{
			k_ipad[i] ^= 0x36;
			k_opad[i] ^= 0x5c;
	}
	
	MD5_Init(&context);
	MD5_Update(&context, k_ipad, 64);
	MD5_Update(&context, data, dataLen);
	MD5_Final(digest, &context);
	
	MD5_Init(&context);
	MD5_Update(&context, k_opad, 64);
	MD5_Update(&context, digest, 16);
	MD5_Final(digest,&context);

	return digestToString(digest);
}

/**
 * @brief 释放内存
 * @param ptr 地址指针
 */
void release(void *ptr)
{
	free(ptr);
	ptr = NULL;
}

int main(int argc, char **argv)
{
	int opt;
    while ((opt = getopt(argc, argv, "s:f:")) != -1)
	{
		switch (opt)
		{
			// 字符串摘要计算
			case 's':
			{
				char *m32 = md5_32(optarg, strlen(optarg));
				char *m16 = md5_16(m32);
				char *hmac = hmac_md5(optarg, strlen(optarg), argv[optind], strlen(argv[optind]));

				printf("32 位 MD5: %s\n", m32);
				printf("16 位 MD5: %s\n", m16);
				printf("HMAC-MD5: %s\n", hmac);

				release(m32);
				release(m16);
				release(hmac);

				return 0;
			}
			// 文件摘要计算
			case 'f':
			{
				int fd = open(optarg, O_RDONLY);
				if (fd == -1)
				{
					perror("打开文件失败");
					return 1;
				}

				MD5_CTX ctx;
				MD5_Init(&ctx);

				char buff[64] = {0};
				while (1)
				{
					memset(buff, 0, 64);

					ssize_t ret = read(fd, buff, 64);
					if (ret > 0)
					{
						MD5_Update(&ctx, buff, (size_t)ret);
					}
					else if (ret == 0)
					{
						break;
					}
					else
					{
						perror("读取文件过程中出错");
						return 1;
					}
				}

				unsigned char digest[MD5_DIGEST_LENGTH] = {0};
				MD5_Final(digest, &ctx);
				char *m = digestToString(digest);
				printf("文件的MD5值为: %s\n", m);

				release(m);
				close(fd);

				return 0;
			}
			case '?':
			{
				printf("未知参数： %c\n", (char)optopt);
				return 1;
			}
			default:
			{
				;
			}
		}
	}
	printf("参数非法！\n");
}