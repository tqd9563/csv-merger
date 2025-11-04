# CSV/TXT文件合并去重工具

一个基于Streamlit的简单网页工具，用于合并多个CSV或TXT文件并自动去重。

## 功能特点

- ✅ 支持上传多个CSV或TXT文件
- ✅ 自动检测文件格式
- ✅ 智能去重（CSV基于所有列，TXT基于行内容）
- ✅ 支持多种编码格式（UTF-8, GBK, GB2312等）
- ✅ 实时显示处理进度和统计信息
- ✅ 一键下载合并结果

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行本地服务

```bash
streamlit run app.py
```

应用会在本地启动，默认地址：`http://localhost:8501`

## 部署到公网

### 方法一：Streamlit Cloud（推荐，最简单）

1. 将代码推送到GitHub仓库
2. 访问 [Streamlit Cloud](https://streamlit.io/cloud)
3. 使用GitHub账号登录
4. 点击"New app"，选择你的仓库
5. 设置主文件路径为 `app.py`
6. 点击"Deploy"，几分钟后就能获得公网链接

**优点**：完全免费，自动部署，无需服务器

### 方法二：使用ngrok（快速测试）

1. 安装ngrok：访问 [ngrok.com](https://ngrok.com/) 下载或使用brew安装
   ```bash
   brew install ngrok  # macOS
   ```

2. 启动Streamlit应用
   ```bash
   streamlit run app.py
   ```

3. 在另一个终端运行ngrok
   ```bash
   ngrok http 8501
   ```

4. ngrok会提供一个公网链接（如：`https://xxxx.ngrok.io`），分享给朋友即可

**优点**：快速，适合临时使用  
**缺点**：免费版链接会变化，需要保持本地服务运行

### 方法三：部署到云服务器

如果你有云服务器（如阿里云、腾讯云等）：

1. 在服务器上安装Python和依赖
2. 使用screen或tmux保持服务运行
   ```bash
   screen -S streamlit
   streamlit run app.py --server.port 8501 --server.address 0.0.0.0
   ```

3. 配置防火墙开放8501端口
4. 通过 `http://你的服务器IP:8501` 访问

**注意**：生产环境建议配置Nginx反向代理和HTTPS

## 使用说明

1. 打开网页应用
2. 点击上传区域，选择多个CSV或TXT文件（格式需相同）
3. 点击"开始处理"按钮
4. 查看处理结果和统计信息
5. 点击"下载"按钮获取合并后的文件

## 注意事项

- 同一批次上传的文件格式必须相同（都是CSV或都是TXT）
- CSV文件需要有表头（第一行）
- TXT文件每行一条数据
- 大文件处理可能需要一些时间，请耐心等待

## 技术栈

- **Streamlit**: Web应用框架
- **Pandas**: 数据处理

## 许可证

MIT License

