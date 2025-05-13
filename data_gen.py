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

from gpt_api import nl2logic

data_path = "data/DF/rules1_type.json"
written_path = "data/DF/DF_step01.json"

# 执行step01：规则转化为逻辑表达式
nl2logic(data_path, written_path)

