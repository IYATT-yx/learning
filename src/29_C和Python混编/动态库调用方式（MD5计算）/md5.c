/**
 * @file md5.c
 * @brief MD5库
 * MD5 和 HAMC-MD5
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
#include "md5.h"

#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define HMAC_IPAD 0x36
#define HMAC_OPAD 0x5c
#define BLOCK_SIZE 16

typedef struct
{
	long unsigned lo, hi;
	long unsigned a, b, c, d;
	unsigned char buffer[64];
	long unsigned block[16];
} md5ctx;

/**
 * @brief md5 计算算法
 * @param ctx md5ctx 句柄
 * @param data 数据
 * @param size 数据长度
 */
static const void *_body(md5ctx *ctx, const void *data, size_t size);

/**
 * @brief 初始化
 * @param ctx md5ctx 句柄
 */
static void _md5Init(md5ctx *ctx);

/**
 * @brief 添加数据
 * @param ctx md5ctx 句柄
 * @param data 数据
 * @param size 数据的长度
 */
static void _md5Update(md5ctx *ctx, const void *data, size_t size);

/**
 * @brief 完成数据处理，返回 md5
 * @param result md5 结果
 * @param ctx md5ctx 句柄
 */
static void _md5Final(unsigned char *result, md5ctx * ctx);

/**
 * @brief md5 转文本
 * @param md5 md5 数据
 * @return md5 文本
 */
static char *_digestToString(const unsigned char *md5);



#define F(x, y, z)			((z) ^ ((x) & ((y) ^ (z))))
#define G(x, y, z)			((y) ^ ((z) & ((x) ^ (y))))
#define H(x, y, z)			((x) ^ (y) ^ (z))
#define I(x, y, z)			((y) ^ ((x) | ~(z)))

#define STEP(f, a, b, c, d, x, t, s) \
	(a) += f((b), (c), (d)) + (x) + (t); \
	(a) = (((a) << (s)) | (((a) & 0xffffffff) >> (32 - (s)))); \
	(a) += (b);

#if defined(__i386__) || defined(__x86_64__) || defined(__vax__)
	# define SET(n) \
		(*(const long unsigned *)&ptr[(n) * 4])
	# define GET(n) \
		SET(n)
#else
	# define SET(n) \
		(ctx->block[(n)] = \
		(long unsigned)ptr[(n) * 4] | \
		((long unsigned)ptr[(n) * 4 + 1] << 8) | \
		((long unsigned)ptr[(n) * 4 + 2] << 16) | \
		((long unsigned)ptr[(n) * 4 + 3] << 24))
	# define GET(n) \
		(ctx->block[(n)])
#endif


const void *_body(md5ctx *ctx, const void *data, size_t size)
{
	const unsigned char *ptr;
	long unsigned a, b, c, d;
	long unsigned saved_a, saved_b, saved_c, saved_d;

	ptr = (const unsigned char*)data;

	a = ctx->a;
	b = ctx->b;
	c = ctx->c;
	d = ctx->d;

	do {
		saved_a = a;
		saved_b = b;
		saved_c = c;
		saved_d = d;

// 第一轮
		STEP(F, a, b, c, d, SET(0), 0xd76aa478, 7)
		STEP(F, d, a, b, c, SET(1), 0xe8c7b756, 12)
		STEP(F, c, d, a, b, SET(2), 0x242070db, 17)
		STEP(F, b, c, d, a, SET(3), 0xc1bdceee, 22)
		STEP(F, a, b, c, d, SET(4), 0xf57c0faf, 7)
		STEP(F, d, a, b, c, SET(5), 0x4787c62a, 12)
		STEP(F, c, d, a, b, SET(6), 0xa8304613, 17)
		STEP(F, b, c, d, a, SET(7), 0xfd469501, 22)
		STEP(F, a, b, c, d, SET(8), 0x698098d8, 7)
		STEP(F, d, a, b, c, SET(9), 0x8b44f7af, 12)
		STEP(F, c, d, a, b, SET(10), 0xffff5bb1, 17)
		STEP(F, b, c, d, a, SET(11), 0x895cd7be, 22)
		STEP(F, a, b, c, d, SET(12), 0x6b901122, 7)
		STEP(F, d, a, b, c, SET(13), 0xfd987193, 12)
		STEP(F, c, d, a, b, SET(14), 0xa679438e, 17)
		STEP(F, b, c, d, a, SET(15), 0x49b40821, 22)

// 第二轮
		STEP(G, a, b, c, d, GET(1), 0xf61e2562, 5)
		STEP(G, d, a, b, c, GET(6), 0xc040b340, 9)
		STEP(G, c, d, a, b, GET(11), 0x265e5a51, 14)
		STEP(G, b, c, d, a, GET(0), 0xe9b6c7aa, 20)
		STEP(G, a, b, c, d, GET(5), 0xd62f105d, 5)
		STEP(G, d, a, b, c, GET(10), 0x02441453, 9)
		STEP(G, c, d, a, b, GET(15), 0xd8a1e681, 14)
		STEP(G, b, c, d, a, GET(4), 0xe7d3fbc8, 20)
		STEP(G, a, b, c, d, GET(9), 0x21e1cde6, 5)
		STEP(G, d, a, b, c, GET(14), 0xc33707d6, 9)
		STEP(G, c, d, a, b, GET(3), 0xf4d50d87, 14)
		STEP(G, b, c, d, a, GET(8), 0x455a14ed, 20)
		STEP(G, a, b, c, d, GET(13), 0xa9e3e905, 5)
		STEP(G, d, a, b, c, GET(2), 0xfcefa3f8, 9)
		STEP(G, c, d, a, b, GET(7), 0x676f02d9, 14)
		STEP(G, b, c, d, a, GET(12), 0x8d2a4c8a, 20)

// 第三轮
		STEP(H, a, b, c, d, GET(5), 0xfffa3942, 4)
		STEP(H, d, a, b, c, GET(8), 0x8771f681, 11)
		STEP(H, c, d, a, b, GET(11), 0x6d9d6122, 16)
		STEP(H, b, c, d, a, GET(14), 0xfde5380c, 23)
		STEP(H, a, b, c, d, GET(1), 0xa4beea44, 4)
		STEP(H, d, a, b, c, GET(4), 0x4bdecfa9, 11)
		STEP(H, c, d, a, b, GET(7), 0xf6bb4b60, 16)
		STEP(H, b, c, d, a, GET(10), 0xbebfbc70, 23)
		STEP(H, a, b, c, d, GET(13), 0x289b7ec6, 4)
		STEP(H, d, a, b, c, GET(0), 0xeaa127fa, 11)
		STEP(H, c, d, a, b, GET(3), 0xd4ef3085, 16)
		STEP(H, b, c, d, a, GET(6), 0x04881d05, 23)
		STEP(H, a, b, c, d, GET(9), 0xd9d4d039, 4)
		STEP(H, d, a, b, c, GET(12), 0xe6db99e5, 11)
		STEP(H, c, d, a, b, GET(15), 0x1fa27cf8, 16)
		STEP(H, b, c, d, a, GET(2), 0xc4ac5665, 23)

// 第四轮
		STEP(I, a, b, c, d, GET(0), 0xf4292244, 6)
		STEP(I, d, a, b, c, GET(7), 0x432aff97, 10)
		STEP(I, c, d, a, b, GET(14), 0xab9423a7, 15)
		STEP(I, b, c, d, a, GET(5), 0xfc93a039, 21)
		STEP(I, a, b, c, d, GET(12), 0x655b59c3, 6)
		STEP(I, d, a, b, c, GET(3), 0x8f0ccc92, 10)
		STEP(I, c, d, a, b, GET(10), 0xffeff47d, 15)
		STEP(I, b, c, d, a, GET(1), 0x85845dd1, 21)
		STEP(I, a, b, c, d, GET(8), 0x6fa87e4f, 6)
		STEP(I, d, a, b, c, GET(15), 0xfe2ce6e0, 10)
		STEP(I, c, d, a, b, GET(6), 0xa3014314, 15)
		STEP(I, b, c, d, a, GET(13), 0x4e0811a1, 21)
		STEP(I, a, b, c, d, GET(4), 0xf7537e82, 6)
		STEP(I, d, a, b, c, GET(11), 0xbd3af235, 10)
		STEP(I, c, d, a, b, GET(2), 0x2ad7d2bb, 15)
		STEP(I, b, c, d, a, GET(9), 0xeb86d391, 21)

		a += saved_a;
		b += saved_b;
		c += saved_c;
		d += saved_d;

		ptr += 64;
	} while (size -= 64);

	ctx->a = a;
	ctx->b = b;
	ctx->c = c;
	ctx->d = d;

	return ptr;
}


void _md5Init(md5ctx *ctx)
{
	ctx->a = 0x67452301;
	ctx->b = 0xefcdab89;
	ctx->c = 0x98badcfe;
	ctx->d = 0x10325476;

	ctx->lo = 0;
	ctx->hi = 0;
}


void _md5Update(md5ctx *ctx, const void *data, size_t size)
{
	long unsigned saved_lo;
	long unsigned used, free;

	saved_lo = ctx->lo;
	if ((ctx->lo = (saved_lo + size) & 0x1fffffff) < saved_lo)
	{
		ctx->hi++;
	}
	ctx->hi += size >> 29;

	used = saved_lo & 0x3f;

	if (used)
	{
		free = 64 - used;

		if (size < free)
		{
			memcpy(&ctx->buffer[used], data, size);
			return;
		}

		memcpy(&ctx->buffer[used], data, free);
		data = (const unsigned char *)data + free;
		size -= free;
		_body(ctx, ctx->buffer, 64);
	}

	if (size >= 64)
	{
		data = _body(ctx, data, size & ~(size_t)0x3f);
		size &= 0x3f;
	}

	memcpy(ctx->buffer, data, size);
}


void _md5Final(unsigned char *result, md5ctx *ctx)
{
	long unsigned used, free;

	used = ctx->lo & 0x3f;

	ctx->buffer[used++] = 0x80;

	free = 64 - used;

	if (free < 8)
	{
		memset(&ctx->buffer[used], 0, free);
		_body(ctx, ctx->buffer, 64);
		used = 0;
		free = 64;
	}

	memset(&ctx->buffer[used], 0, free - 8);

	ctx->lo <<= 3;
	ctx->buffer[56] = (unsigned char)(ctx->lo);
	ctx->buffer[57] = (unsigned char)(ctx->lo >> 8);
	ctx->buffer[58] = (unsigned char)(ctx->lo >> 16);
	ctx->buffer[59] = (unsigned char)(ctx->lo >> 24);
	ctx->buffer[60] = (unsigned char)(ctx->hi);
	ctx->buffer[61] = (unsigned char)(ctx->hi >> 8);
	ctx->buffer[62] = (unsigned char)(ctx->hi >> 16);
	ctx->buffer[63] = (unsigned char)(ctx->hi >> 24);

	_body(ctx, ctx->buffer, 64);

	result[0] = (unsigned char)(ctx->a);
	result[1] = (unsigned char)(ctx->a >> 8);
	result[2] = (unsigned char)(ctx->a >> 16);
	result[3] = (unsigned char)(ctx->a >> 24);
	result[4] = (unsigned char)(ctx->b);
	result[5] = (unsigned char)(ctx->b >> 8);
	result[6] = (unsigned char)(ctx->b >> 16);
	result[7] = (unsigned char)(ctx->b >> 24);
	result[8] = (unsigned char)(ctx->c);
	result[9] = (unsigned char)(ctx->c >> 8);
	result[10] = (unsigned char)(ctx->c >> 16);
	result[11] = (unsigned char)(ctx->c >> 24);
	result[12] = (unsigned char)(ctx->d);
	result[13] = (unsigned char)(ctx->d >> 8);
	result[14] = (unsigned char)(ctx->d >> 16);
	result[15] = (unsigned char)(ctx->d >> 24);

	memset(ctx, 0, sizeof(*ctx));
}

char* hmac_md5(const void *data, size_t dataLen, const void *key, size_t keyLen)
{
	unsigned char digest[17];
	digest[16] = 0x00;
	md5ctx context;
	unsigned char k_ipad[65];
	unsigned char k_opad[65];
	unsigned char tk[BLOCK_SIZE];
	
	if (keyLen > 64){
		md5ctx tctx;
		_md5Init(&tctx);
		_md5Update(&tctx, key, keyLen);
		_md5Final(tk,&tctx);
		
		key = tk;
		keyLen= 16;
	}
	
	memset( k_ipad, 0, sizeof(k_ipad));
	memset( k_opad, 0, sizeof(k_opad));
	memcpy( k_ipad, key, keyLen);
	memcpy( k_opad, key, keyLen);
	
	for(int i = 0; i < 64; i++)
	{
			k_ipad[i] ^= HMAC_IPAD;
			k_opad[i] ^= HMAC_OPAD;
	}
	
	_md5Init(&context);
	_md5Update(&context, k_ipad, 64);
	_md5Update(&context, data, dataLen);
	_md5Final(digest, &context);
	
	_md5Init(&context);
	_md5Update(&context, k_opad, 64);
	_md5Update(&context, digest, 16);
	_md5Final(digest,&context);

	return _digestToString(digest);
}

char string[33] = {'\0'};
char *_digestToString(const unsigned char *digest)
{
	memset(string, 0, 33);
	char tmp[3] = {'\0'};
	for (int i = 0; i < 16; ++i)
	{
		sprintf(tmp, "%02x", digest[i]);
		strcat(string, tmp);
	}
	return string;
}

const char *md5_32(const void *data, size_t len)
{
	md5ctx ctx;
	_md5Init(&ctx);
	_md5Update(&ctx, data, len);
	unsigned char md5[BLOCK_SIZE] = {0};
	_md5Final(md5, &ctx);
	return _digestToString(md5);
}

char *md5_16(char *digest32)
{
	char *digest16 = (char *)malloc(17);
	memset(digest16, '\0', 17);
	for (int i = 8, j = 0; j < 16; ++i, ++j)
	{
		digest16[j] = digest32[i];
	}
	return digest16;
}
