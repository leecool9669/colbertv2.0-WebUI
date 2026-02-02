# -*- coding: utf-8 -*-
"""ColBERT v2.0 检索与可视化 WebUI 演示（不加载真实模型权重）。"""
from __future__ import annotations

import gradio as gr


def fake_load_model():
    """模拟加载 ColBERT v2.0 模型，仅用于界面演示。"""
    return "模型状态：ColBERT v2.0 已就绪（演示模式，未加载真实权重）"


def fake_retrieve(query: str, top_k: int) -> str:
    """模拟检索结果与可视化描述。"""
    if not (query or "").strip():
        return "请输入查询文本以进行检索。"
    k = max(1, min(100, int(top_k) if isinstance(top_k, (int, float)) else 10))
    lines = [
        "[演示] 已对查询进行 ColBERT 晚期交互检索（未加载真实模型）。",
        f"查询：{query[:120]}{'...' if len(query) > 120 else ''}",
        f"Top-{k} 检索结果（占位）：",
        "",
        "1. [pid=1] 得分 0.92 — 示例段落 A（MaxSim 匹配）",
        "2. [pid=2] 得分 0.88 — 示例段落 B（上下文晚期交互）",
        "3. [pid=3] 得分 0.85 — 示例段落 C",
        "",
        "说明：加载真实 ColBERT v2.0 模型并构建索引后，将在此显示真实检索段落与得分。",
    ]
    return "\n".join(lines[: 5 + min(k, 5)])


def fake_index_status():
    """模拟索引状态。"""
    return (
        "[演示] 索引状态：未构建。\n"
        "真实使用时需先对语料进行 ColBERT 编码并建索引（nbits=2 等），"
        "再进行检索与可视化。"
    )


def build_ui():
    with gr.Blocks(title="ColBERT v2.0 WebUI") as demo:
        gr.Markdown("## ColBERT v2.0 · 晚期交互检索与可视化 WebUI 演示")
        gr.Markdown(
            "本界面以交互方式展示 ColBERT v2.0 的典型使用流程："
            "模型加载、语料索引状态、查询检索及结果可视化（演示模式，未加载真实模型）。"
        )

        with gr.Row():
            load_btn = gr.Button("加载模型（演示）", variant="primary")
            status_box = gr.Textbox(label="模型状态", value="尚未加载", interactive=False)
        load_btn.click(fn=fake_load_model, outputs=status_box)

        with gr.Tabs():
            with gr.Tab("检索"):
                gr.Markdown("输入查询与 Top-K，模型将进行晚期交互检索并展示结果。")
                query_in = gr.Textbox(
                    label="查询文本",
                    placeholder="例如：What is ColBERT late interaction?",
                    lines=2,
                )
                top_k = gr.Slider(1, 50, value=10, step=1, label="Top-K")
                retrieve_btn = gr.Button("检索（演示）")
                retrieve_out = gr.Textbox(
                    label="检索结果说明", lines=12, interactive=False
                )
                retrieve_btn.click(
                    fn=fake_retrieve,
                    inputs=[query_in, top_k],
                    outputs=retrieve_out,
                )

            with gr.Tab("索引状态"):
                gr.Markdown("查看当前 ColBERT 索引状态（演示）。")
                idx_btn = gr.Button("查看索引状态")
                idx_out = gr.Textbox(label="索引状态", lines=4, interactive=False)
                idx_btn.click(fn=fake_index_status, outputs=idx_out)

        gr.Markdown(
            "---\n*说明：当前为轻量级演示界面，未实际下载与加载 ColBERT v2.0 模型参数。*"
        )
    return demo


def main():
    app = build_ui()
    app.launch(server_name="127.0.0.1", server_port=8765, share=False)


if __name__ == "__main__":
    main()
