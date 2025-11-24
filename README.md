# YouTube数据集可视化分析项目

本项目旨在通过对YouTube数据集的深入分析和可视化，揭示YouTube平台上内容创作者的表现、用户行为模式以及各类别视频的受欢迎程度。

## 项目结构

```
.
├── app.py                 # 主应用文件
├── sections/              # 页面各部分模块
│   ├── intro.py           # 项目介绍和背景
│   ├── overview.py        # 数据概览和基本信息
│   ├── deep_dives.py      # 深入分析和可视化
│   └── conclusions.py     # 结论和洞察
├── utils/                 # 工具函数模块
│   ├── io.py              # 数据加载和输入输出功能
│   ├── prep.py            # 数据预处理和特征工程
│   └── viz.py             # 可视化工具函数
├── YouTubeDataset_withChannelElapsed.csv  # 数据集文件
└── youtube_visualization.py              # 原始单文件版本
```

## 功能特点

1. **模块化设计**：将应用拆分为多个模块，便于维护和扩展
2. **数据预处理**：自动处理缺失值、异常值和数据类型转换
3. **特征工程**：计算衍生指标如互动率、综合评分等
4. **多样化可视化**：提供多种图表类型展示数据
5. **交互式过滤**：支持数据采样和过滤选项
6. **多语言支持**：中英文双语界面和说明

## 运行应用

```bash
streamlit run app.py
```

## 依赖库

- streamlit
- pandas
- numpy
- plotly
- matplotlib
- seaborn

安装依赖：
```bash
pip install streamlit pandas numpy plotly matplotlib seaborn
```