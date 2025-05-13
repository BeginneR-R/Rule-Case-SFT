from typing import List
from typing import Optional
from typing import Dict

import os
import json
import jsonlines
from pathlib import Path

import httpx
from openai import OpenAI

import requests

import time
import re
from tqdm import tqdm
import random


# 设置随机种子（可选，用于确保结果可复现）
random.seed(42)

api_key = "sk-gNToXJPO4Ih8NDZnDloSXR780dQDEZ2Epu49wcVA1sWb4Ecw" # 你的API密钥
data_language = "zh"


# 读取文本文件内容
def load_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# 创建缓存
def create_cache(file_content):
    data = {
        "model": "moonshot-v1",
        "messages": [
            {
                "role": "system",
                "content": file_content
            }
        ],
        "name": "example_cache",
        "ttl": 3600  # 缓存有效期，单位为秒
    }
    response = requests.post(
        url="https://api.moonshot.cn/v1/caching",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=data
    )
    cache_response = json.loads(response.text)
    return cache_response['id']


# 检查缓存是否存在且未过期
def check_cache(cache_id):
    response = requests.get(
        url=f"https://api.moonshot.cn/v1/caching/{cache_id}",
        headers={
            "Authorization": f"Bearer {api_key}"
        }
    )
    if response.status_code == 200:
        return True
    return False


# 重新加载数据并更新缓存
def reload_and_update_cache(file_path, cache_id):
    new_file_content = load_file_content(file_path)
    data = {
        "model": "moonshot-v1",
        "messages": [
            {
                "role": "system",
                "content": new_file_content
            }
        ],
        "name": "example_cache",
        "ttl": 3600  # 缓存有效期，单位为秒
    }
    response = requests.put(
        url=f"https://api.moonshot.cn/v1/caching/{cache_id}",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=data
    )
    return response.status_code == 200


# 使用缓存内容并添加问题
def use_cache_with_question(cache_id, question):
    data = {
        "model": "moonshot-v1-32k",
        "messages": [
            {
                "role": "cache",
                "content": f"cache_id={cache_id};reset_ttl=3600",
            },
            {
                "role": "user",
                "content": question
            }
        ],
        "max_tokens": 8192,
    }
    response = requests.post(
        url="https://api.moonshot.cn/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=data
    )
    return response.json()['choices'][0]['message']['content']


# 规则自然语言转化为logic表达式
def nl2logic(data_path, written_path):
    file_path = 'prompts/DataFountain/translation.txt'
    file_content = load_file_content(file_path)
    print(f"File{file_path} success read")
    cache_id = create_cache(file_content)
    print(f"cache id:{cache_id}")
    print("cache cuccess")

    # 检查缓存是否存在且未过期
    if not check_cache(cache_id):
        print("检查不到缓存")
        # 重新加载数据并更新缓存
        if reload_and_update_cache(file_path, cache_id):
            print("缓存更新成功")
        else:
            print("缓存更新失败")

    with open(data_path, 'r', encoding='utf-8') as file:
        answer = json.load(file)

    # 随机打乱列表
    random.shuffle(answer)

    for idx, value in tqdm(enumerate(answer[303:]), total=len(answer), desc="Processing"):
        # 使用缓存内容并添加问题
        context = value["rule"]
        question = f"请回答关于文件内容的问题，其中[[CONTEXT]]代表的数据为{context}"
        response = use_cache_with_question(cache_id, question)
        judgement = {
            "ori_id": value["id"],
            "id": idx + 303,
            "rule": context,
            "answer": response
        }
        # 打开文件以进行写入，如果文件不存在，会创建文件
        with jsonlines.open(written_path, mode='a') as writer:
            writer.write(judgement)

    return None


