# extract-dialogue-MajoTabi

本仓库fork了[KMnO4-zx/extract-dialogue: 从小说中提取对话数据集 (github.com)](https://github.com/KMnO4-zx/extract-dialogue/tree/master)仓库用来提取轻小说《魔女之旅》中的伊雷娜对话信息，之后处理成Alpaca格式供以微调。

已从轻小说中提取2万＋的对话集，之后手动处理了二百条数据。

对话集详见：`output/elaina.json`

微调数据集详见：`elaina_Alpaca.json`

> 项目待改进：
>
> 1. 使用多线程进行处理
> 2. 保存中断信息，以防从头开始
> 3. 需要手动处理的信息放置`config.ini`中

**⚠️ 本项目不包含任何小说原文，仅提供数据处理代码。使用者需自行确保数据来源合法性。**

克隆项目：

```shell
git clone git@github.com:golitter/extract-dialogue-MajoTabi.git
```

进入项目主目录：

```shell
cd extract-dialogue-MajoTabi-master/
```

环境配置：

```shell
# conda
conda create --name my_env --file spec-file.txt
# pip 
pip install -r requirements.txt
```

- 将文本放到`data`目录内，文本文件名为**英文**，文内编码格式为`utf-8`。

- 将`config_pub.ini`更改为`config.ini`，并配置好参数。运行`start.py`脚本进行处理文本，得到的数据在`output`目录内。

  ```python
  [settings]
  # API key for authentication
  api_key = {api_key}
  # Base URL of the API service
  base_url = {base_url}
  # Output file path for storing results
  file_name = ./output/elaina.json
  # Input file path containing the data to process
  file_path = ./data/mnzl.txt
  
  [progress]
  # The starting index for processing, useful for resuming progress
  start_idx = 0
  # Maximum token length allowed for each API request
  max_token_len = 600
  # Number of tokens to overlap between consecutive text chunks
  cover_content = 50
  ```

  

  挂后台运行：

  ```shell
  nohup python start.py > output.log 2>&1 &
  ```

- 在项目主目录内运行所有脚本即可。`test`目录内的文件运行采用`python -m test.example`形式运行。（不带`.py`）

- 将`output`目录内提取的数据集进行检查并手动处理成Alpaca格式。



# Extract Dialogue

>***本仓库只为`huanhuan-chat`泛化版的一部分内容（文本对话抽取），欢迎大家给`huanhuan-chat`仓库star！本仓库的最大贡献就是为泛化的Character AI提供了从小说中建立数据集的功能。***
>
>`huanhuan-chat: https://github.com/KMnO4-zx/huanhuan-chat.git`

## Show

`repo`：https://github.com/KMnO4-zx/extract-dialogue.git

本项目利用`chatgpt`从小说中提取对话集，提取的样本中包括`role`，`dialogue`，比如以下的形式：

```json
{
    "role": "艾伦",
    "dialogue": "不，不要提，这真是太倒霉了！我从楼梯上摔了下去，出现了较为严重的骨裂，只能打石膏做固定。"
}
{
    "role": "克莱恩",
    "dialogue": "真是不够走运啊。"
}
```

## QuickStart

- 克隆仓库并切换目录：`git clone https://github.com/KMnO4-zx/extract-dialogue.git `，`cd extract-dialogue`

- 安装依赖：`pip install -r requirements.txt`
- 在当前目录创建`.env`文件，并填入`DEEPSEEK_API`。
- 把你要提取的小说或文本，放到当前目录，在`example.py`中修改`path`。
- ***强烈建议您结合要提取的小说修改`schema.py`中的`schema`示例。在下面的部分中有详细介绍`schema`。***

- 运行`example.py`，`python example.py`

结果如下所示：

```json
{"role": "克莱恩", "dialogue": "在帮警察们调查那起连环杀人案，虽然不一定能有收获，但赏金足够诱人，而且，和警察部门建立良好的关系对我们私家侦探来说非常重要。"}
{"role": "塔利姆", "dialogue": "这果然是大侦探忙碌的事情。"}
{"role": "塔利姆", "dialogue": "莫里亚蒂先生，我能请教一个问题吗？"}
{"role": "克莱恩", "dialogue": "这单免费，还有，叫我夏洛克就行了。"}
{"role": "塔利姆", "dialogue": "我有个朋友，爱上了不该爱的人，这种情况该怎么处理？"}
{"role": "塔利姆", "dialogue": "莫里亚蒂先生，我能请教一个问题吗？"}
{"role": "克莱恩", "dialogue": "这单免费，还有，叫我夏洛克就行了。"}
{"role": "塔利姆", "dialogue": "我有个朋友，爱上了不该爱的人，这种情况该怎么处理？"}
{"role": "克莱恩", "dialogue": "我唯一的建议是，不要犯法。"}
{"role": "克莱恩", "dialogue": "首先，我们要弄清楚‘不该’是源于什么？双方的家庭之间有仇恨关系？"}
{"role": "塔利姆", "dialogue": "不，这不是《罗密欧与朱丽叶》的故事！"}
```


## Introduction

```python
from extract import system_prompt
from schema import novel_schema
from LLM import DeepseekChat
from utils import ReadFiles
from tqdm import tqdm
import json

file_path = './data/test.txt'
docs = ReadFiles(file_path).get_content(max_token_len=500, cover_content=0)

sys_prompt = system_prompt(novel_schema)

model = DeepseekChat()

file_name = file_path.split('/')[-1].split('.')[0]

for i in tqdm(range(len(docs))):
    response = model.chat(sys_prompt, docs[i])
    try:
        response = json.loads(response)
        for item in response:
            with open(f'{file_name}.jsonl', 'a', encoding='utf-8') as f:
                json.dump(item, f, ensure_ascii=False)
                f.write('\n')
    except Exception as e:
        print(e)
```

## 参考

【1】https://eyurtsev.github.io/kor/index.html#

【2】https://zhuanlan.zhihu.com/p/646948797