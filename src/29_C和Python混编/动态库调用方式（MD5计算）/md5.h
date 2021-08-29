/**
 * @file md5.h
 * @brief MD5库 - Python 扩展模块
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

#ifndef MD5_H
#define MD5_H

#include <stddef.h>

/**
 * @brief 32 位 MD5
 * @param data 数据
 * @param len 数据的长度
 * @return 计算结果
 */
extern const char *md5_32(const void *data, size_t len);

/**
 * @brief 16 位 MD5
 * @param digest32 32 位 md5
 * @return 计算结果
 */
extern char *md5_16(char *digest32);

/**
 * @brief HMAC
 * @param data 数据
 * @param dataLen 数据长度
 * @param key 密钥
 * @param keyLen 密钥长度
 * @return 计算结果
 */
extern char* hmac_md5(const void *data, size_t dataLen, const void *key, size_t keyLen);

#endif