# ReflectEvolve

这是我们2025秋机器学习课程Term Project的代码仓库。我们基于[OpenEvolve](https://github.com/algorithmicsuperintelligence/openevolve)开发，并实现了两个改进：

1. 增加Reflection模块，代码主要在[reflection.py](./openevolve/reflection/reflection.py)和[controller.py](./openevolve/controller.py)中。
2. 改进Evaluator，代码主要在[improved.py](./examples/alphaevolve_math_problems/kissing_number/improved.py)。

## 环境

创建conda环境：

```bash
conda create -n openevolve python=3.12
```

安装依赖

```bash
pip install openevolve
```

激活环境

```bash
conda activate openevolve
```

配置Deepseek密钥

```bash
export OPENAI_API_KEY="<your api key>"
```

## 运行

使用原来的Evaluator和Reflection

```bash
python ./openevolve-run.py ./examples/alphaevolve_math_problems/kissing_number/initial_program.py ./examples/alphaevolve_math_problems/kissing_number/evaluator.py --config ./examples/alphaevolve_math_problems/kissing_number/config.yaml --iterations 50 --output ./output
```

如果要使用改进的Evaluator和Reflection，则运行

```bash
python ./openevolve-run.py ./examples/alphaevolve_math_problems/kissing_number/initial_program.py ./examples/alphaevolve_math_problems/kissing_number/improved.py --config ./examples/alphaevolve_math_problems/kissing_number/deepseek.yaml --iterations 50 --output ./output
```

如果要修改维度和SOTA，需要同时修改[config.yaml](./examples/alphaevolve_math_problems/kissing_number/config.yaml)和[evaluator.py](./examples/alphaevolve_math_problems/kissing_number/evaluator.py)。
