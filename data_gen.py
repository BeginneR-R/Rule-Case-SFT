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

from gpt_api import nl2logic, logic2coverage, coverage2nl, nl2instruction

data_path_01 = "data/DF/rules1_type.json"
written_path_01 = "data/DF/DF_step01.json"

data_path_02 = written_path_01
written_path_02 = "data/DF/DF_step02.json"

data_path_03 = written_path_02
written_path_03 = "data/DF/DF_step03.json"

data_path_04 = written_path_03
written_path_04 = "data/DF/DF_step04.json"

# 执行step01：规则转化为逻辑表达式
# nl2logic(data_path_01, written_path_01)

# 执行step02：逻辑表达式根据覆盖率取值
# logic2coverage(data_path_02, written_path_02)

# 执行step03：逻辑表达式转化为自然语言
# coverage2nl(data_path_03, written_path_03)

# 执行step04：自然语言转化为指令
nl2instruction(data_path_04, written_path_04)
