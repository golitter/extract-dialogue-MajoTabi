#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   LLM.py
@Time    :   2024/06/16 07:59:28
@Author  :   不要葱姜蒜
@Version :   1.0
@Desc    :   None
'''

import os
from typing import Dict, List, Optional, Tuple, Union

from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
import configparser as cp
config = cp.ConfigParser()
config.read('config.ini')

api_key = config.get('settings', 'api_key')
base_url = config.get('settings', 'base_url')

_ = load_dotenv(find_dotenv())


class BaseModel:
    def __init__(self, path: str = '') -> None:
        self.path = path

    def chat(self, prompt: str, history: List[dict], content: str) -> str:
        pass

    def load_model(self):
        pass


class DeepseekChat(BaseModel):
    def __init__(self, path: str = '', model: str = "deepseek-chat") -> None:
        super().__init__(path)
        self.model = model

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        client = OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            stream=False
        )
        # print(response)
        return response.choices[0].message.content
