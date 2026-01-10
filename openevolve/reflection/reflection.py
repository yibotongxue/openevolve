import re
import threading

from openai import OpenAI


def extract_last_code_block(text: str, language: str = "") -> str | None:
    """
    从文本中提取最后一个代码块

    参数
    ----
    text : str
        包含代码块的文本
    language : str, 默认为空字符串
        代码块的语言标识符（如"python"）

    返回
    ----
    str | None
        提取的代码块内容，如果未找到则返回None
    """

    pattern = rf"```{language}\n(.*?)\n```" if language else r"```(?:\w+)?\n(.*?)\n```"
    matches = re.findall(pattern, text, re.DOTALL)
    if matches and len(matches) > 0 and isinstance(matches[-1], str):
        return matches[-1].strip()
    return None

client = OpenAI(
    base_url="https://api.deepseek.com/v1"
)

class ReflectionGenerator:
    def __init__(self, dimension: int, sota_number: int):
        self.reflection = ""
        # self.lock = threading.Lock()
        self.dimension = dimension
        self.sota_number = sota_number

    def generate_reflection(self, previous_code: str, previous_number: int, generated_code: str, generated_number: int, changes: str) -> str:
        if generated_number <= previous_number:
            task_description = f"why the kissing number achieved by your generated code ({generated_number}) is not greater than the previous {previous_number}"
        else:
            task_description = f"what make your generated code better than the previous code and how to further improve the kissing number beyond your generated code's result of {generated_number}"
        prompt = f"""You are a coding assistant expertise in developing and review codes for finding kissing number.
Now you will be given thwo versions of code attempting to solve the problem of finding kissing number for {self.dimension} dimensions:
## Base Code:
This is the original code as the starting point for this step of evolution.
```python
{previous_code}
```
This code yielded a kissing number {previous_number}.
## The code you generated when trying to improve the base code:
```python
{generated_code}
```
This code yielded a kissing number {generated_number}.
## Changes
The changes from the base code to your generated code are as follows:
{changes}
## Task
Your final task is relect to help youself find better kissing number. Current sota result is {self.sota_number}. Currently, your task is to reflect on these three versions of code and their results. You should conduct detailed reasoning on {task_description}.Then provide several suggestions that help you develop better code in the next time based on your analysis.
## Final Instruction
You should provide your reflection after thorough analysis. Your reflection should be general enough and not indicate too much details. Your reflection should be brief and just be several sentences. Your reflection should just be some guidelines for you to follow in the next code generation step. Don't give new code or pseudo code. Just provide your reflection in several sentences.
The final reflection should be just some general guidelines and don't include the analysis why you fail or success, don't include the specific next attempt.
Please provide your reflection with the json format as below:
```json
{{
  "reflection": "<your reflection here>"
}}
```
""".strip()
        response = client.chat.completions.create(
            model='deepseek-chat',
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=8192,
        )
        content = response.choices[0].message.content
        if not content:
            print("没有收到反思内容")
            return ""
        code_block = extract_last_code_block(content, "json")
        if not code_block:
            print("没有提取到反思内容")
            return ""
        print(f"反思内容: {code_block}")
        return code_block
    
    def update_reflection(self, generated_reflection: str):
        prompt = f"""You are a coding assistant expertise in developing and review codes for finding kissing number.
Now we will provide you with your previous reflection and the new reflection you just generated.
Your task is to update your previous reflection based on the new reflection to make it more comprehensive and useful for guiding future code generation.
## Previous Reflection
```
{self.reflection}
```
## New Reflection
```
{generated_reflection}
```
## Task
Your final task is to update your previous reflection by incorporating insights from the new reflection.
## Final Instruction
Don't expand too much, just combine them and adjust some words to make it more fluent. Don't include anything that is not in neither reflection.
If there are conflicts, prioritize the new reflection.
Please provide your updated reflection with the json format as below:
```json
{{
  "reflection": "<your updated reflection here>"
}}
```
""".strip()
        response = client.chat.completions.create(
            model='deepseek-chat',
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=8192,
        )
        content = response.choices[0].message.content
        if not content:
            print("没有收到更新后的反思内容")
            return
        code_block = extract_last_code_block(content, "json")
        if not code_block:
            print("没有提取到更新后的反思内容")
            return
        print(f"更新后的反思内容: {code_block}")
        # with self.lock:
        self.reflection = code_block

    def get_reflection(self) -> str:
        # with self.lock:
        return self.reflection
