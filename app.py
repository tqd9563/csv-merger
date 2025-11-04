import streamlit as st
import pandas as pd
import io
from typing import List, Union
import tempfile
import os

st.set_page_config(
    page_title="CSV/TXT文件合并去重工具",
    page_icon="📊",
    layout="wide"
)

st.title("📊 CSV/TXT文件合并去重工具")
st.markdown("---")

# 侧边栏说明
with st.sidebar:
    st.header("📖 使用说明")
    st.markdown("""
    1. **上传文件**：点击下方上传区域，选择多个CSV或TXT文件
    2. **文件要求**：
       - 格式必须相同（都是CSV或都是TXT）
       - CSV文件需要有表头（第一行）
       - TXT文件每行一条数据
    3. **去重规则**：
       - CSV文件：基于所有列的组合去重
       - TXT文件：基于每行内容去重
    4. **下载结果**：处理完成后点击下载按钮
    """)
    
    st.markdown("---")
    st.markdown("**💡 提示**：如果文件格式不同，请分别上传处理")

def detect_file_type(file_content: bytes, filename: str) -> str:
    """检测文件类型"""
    if filename.lower().endswith('.csv'):
        return 'csv'
    elif filename.lower().endswith('.txt'):
        return 'txt'
    else:
        # 尝试通过内容判断
        try:
            content = file_content.decode('utf-8')
            first_line = content.split('\n')[0]
            # 如果包含逗号，可能是CSV
            if ',' in first_line:
                return 'csv'
            return 'txt'
        except:
            return 'txt'

def process_csv_files(files: List) -> pd.DataFrame:
    """处理CSV文件"""
    all_data = []
    
    for uploaded_file in files:
        try:
            # 尝试不同的编码
            encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
            df = None
            
            for encoding in encodings:
                try:
                    uploaded_file.seek(0)  # 重置文件指针
                    df = pd.read_csv(uploaded_file, encoding=encoding)
                    break
                except:
                    continue
            
            if df is None:
                st.error(f"无法读取文件 {uploaded_file.name}，请检查文件格式")
                continue
                
            all_data.append(df)
            st.success(f"✅ 成功读取 {uploaded_file.name} ({len(df)} 行)")
            
        except Exception as e:
            st.error(f"处理文件 {uploaded_file.name} 时出错: {str(e)}")
    
    if not all_data:
        return None, 0, 0
    
    # 合并所有数据
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # 去重
    original_count = len(combined_df)
    deduplicated_df = combined_df.drop_duplicates()
    deduplicated_count = len(deduplicated_df)
    
    return deduplicated_df, original_count, deduplicated_count

def process_txt_files(files: List) -> List[str]:
    """处理TXT文件"""
    all_lines = set()
    total_lines = 0
    
    for uploaded_file in files:
        try:
            # 尝试不同的编码
            encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
            content = None
            
            for encoding in encodings:
                try:
                    uploaded_file.seek(0)  # 重置文件指针
                    content = uploaded_file.read().decode(encoding)
                    break
                except:
                    continue
            
            if content is None:
                st.error(f"无法读取文件 {uploaded_file.name}，请检查文件编码")
                continue
            
            lines = content.splitlines()
            file_lines_count = len(lines)
            total_lines += file_lines_count
            
            # 去除空行并添加到集合（自动去重）
            for line in lines:
                line = line.strip()
                if line:  # 忽略空行
                    all_lines.add(line)
            
            st.success(f"✅ 成功读取 {uploaded_file.name} ({file_lines_count} 行)")
            
        except Exception as e:
            st.error(f"处理文件 {uploaded_file.name} 时出错: {str(e)}")
    
    # 转换为排序后的列表
    result_lines = sorted(list(all_lines))
    
    return result_lines, total_lines, len(result_lines)

# 主界面
uploaded_files = st.file_uploader(
    "选择要上传的文件（可多选）",
    type=['csv', 'txt'],
    accept_multiple_files=True,
    help="支持同时上传多个CSV或TXT文件，但同一批次的文件格式必须相同"
)

if uploaded_files:
    st.markdown("---")
    
    # 检测文件类型
    if len(uploaded_files) > 0:
        # 读取第一个文件来检测类型
        first_file = uploaded_files[0]
        first_file.seek(0)
        first_content = first_file.read()
        file_type = detect_file_type(first_content, first_file.name)
        
        st.info(f"📄 检测到文件类型: {file_type.upper()}")
        
        # 显示上传的文件列表
        st.subheader("📋 已上传的文件")
        file_info = []
        for file in uploaded_files:
            file_size = len(file.getvalue()) / 1024  # KB
            file_info.append({
                "文件名": file.name,
                "大小": f"{file_size:.2f} KB"
            })
        st.dataframe(pd.DataFrame(file_info), use_container_width=True)
        
        # 处理按钮
        if st.button("🚀 开始处理", type="primary", use_container_width=True):
            with st.spinner("正在处理文件，请稍候..."):
                if file_type == 'csv':
                    result_df, original_count, deduplicated_count = process_csv_files(uploaded_files)
                    
                    if result_df is not None:
                        st.success("✅ 处理完成！")
                        
                        # 显示统计信息
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("合并前总行数", original_count)
                        with col2:
                            st.metric("去重后行数", deduplicated_count)
                        
                        if original_count > deduplicated_count:
                            st.info(f"去除了 {original_count - deduplicated_count} 条重复数据")
                        
                        # 显示预览
                        st.subheader("📊 数据预览（前10行）")
                        st.dataframe(result_df.head(10), use_container_width=True)
                        
                        # 下载按钮
                        csv_buffer = io.StringIO()
                        result_df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
                        st.download_button(
                            label="📥 下载合并后的CSV文件",
                            data=csv_buffer.getvalue(),
                            file_name="merged_result.csv",
                            mime="text/csv",
                            type="primary",
                            use_container_width=True
                        )
                
                elif file_type == 'txt':
                    result_lines, original_count, deduplicated_count = process_txt_files(uploaded_files)
                    
                    if result_lines:
                        st.success("✅ 处理完成！")
                        
                        # 显示统计信息
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("合并前总行数", original_count)
                        with col2:
                            st.metric("去重后行数", deduplicated_count)
                        
                        if original_count > deduplicated_count:
                            st.info(f"去除了 {original_count - deduplicated_count} 条重复数据")
                        
                        # 显示预览
                        st.subheader("📊 数据预览（前20行）")
                        preview_text = "\n".join(result_lines[:20])
                        st.text_area("预览", preview_text, height=200, disabled=True)
                        
                        # 下载按钮
                        result_content = "\n".join(result_lines)
                        st.download_button(
                            label="📥 下载合并后的TXT文件",
                            data=result_content,
                            file_name="merged_result.txt",
                            mime="text/plain",
                            type="primary",
                            use_container_width=True
                        )

# 页脚
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "💡 如有问题或建议，请联系开发者"
    "</div>",
    unsafe_allow_html=True
)

