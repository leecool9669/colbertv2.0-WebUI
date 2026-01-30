# -*- coding: utf-8 -*-
"""ColBERT v2.0 检索模型 WebUI 演示界面（不加载真实模型权重）。"""
from __future__ import annotations

import gradio as gr


def fake_load_model():
    """模拟加载 ColBERT v2.0 模型，仅用于界面演示。"""
    return "模型状态：ColBERT v2.0 已就绪（演示模式，未加载真实权重）"


def fake_search(query: str, top_k: int) -> str:
    """模拟检索：输入查询与 top-k，返回示例检索结果说明。"""
    if not (query or "").strip():
        return "请输入检索查询文本。"
    k = max(1, min(20, int(top_k) if isinstance(top_k, (int, float)) else 10))
    lines = [
        f"【演示】针对查询「{query[:50]}{'…' if len(query) > 50 else ''}」的 Top-{k} 检索结果（未加载模型与索引）：",
        "",
    ]
    for i in range(1, k + 1):
        lines.append(f"  {i}. 段落 pid={1000+i} | MaxSim 得分：0.{95 - i * 2}（示例）")
    lines.append("")
    lines.append("加载 ColBERT v2.0 模型并构建索引后，此处将显示真实检索段落与相似度分数。")
    return "\n".join(lines)


def fake_encode_passage(passage: str) -> str:
    """模拟段落编码为 token 级嵌入矩阵。"""
    if not (passage or "").strip():
        return "请输入待编码的段落文本。"
    return (
        "【演示】已将段落编码为 token 级嵌入矩阵（未加载模型）。\n"
        "实际使用中，ColBERT 会对每个 token 输出一维向量，组成矩阵用于后续 MaxSim 检索。"
    )


def build_ui():
    with gr.Blocks(title="ColBERT v2.0 WebUI") as demo:
        gr.Markdown("# ColBERT v2.0 检索模型 · WebUI 演示")
        gr.Markdown(
            "本界面以交互方式展示 ColBERT v2.0 的典型使用流程："
            "模型加载、检索查询与段落编码可视化。基于上下文迟交互（Late Interaction）与 MaxSim 的细粒度检索。"
        )

        with gr.Row():
            load_btn = gr.Button("加载模型（演示）", variant="primary")
            status_box = gr.Textbox(label="模型状态", value="尚未加载", interactive=False)
        load_btn.click(fn=fake_load_model, outputs=status_box)

        with gr.Tabs():
            with gr.Tab("检索测试"):
                gr.Markdown("输入查询与 Top-K，模拟检索并展示结果（演示模式不访问真实索引）。")
                query_in = gr.Textbox(
                    label="检索查询",
                    placeholder="例如：What is ColBERT late interaction?",
                    lines=2,
                )
                top_k_num = gr.Slider(1, 20, value=5, step=1, label="Top-K")
                search_btn = gr.Button("执行检索（演示）")
                search_out = gr.Textbox(label="检索结果", lines=12, interactive=False)
                search_btn.click(fn=fake_search, inputs=[query_in, top_k_num], outputs=search_out)

            with gr.Tab("段落编码"):
                gr.Markdown("模拟将单段文本编码为 token 级嵌入矩阵，用于索引构建。")
                passage_in = gr.Textbox(
                    label="段落文本",
                    placeholder="输入一段待编码的文档段落。",
                    lines=4,
                )
                enc_btn = gr.Button("编码（演示）")
                enc_out = gr.Textbox(label="编码说明", lines=6, interactive=False)
                enc_btn.click(fn=fake_encode_passage, inputs=passage_in, outputs=enc_out)

        gr.Markdown("---\n*说明：当前为轻量级演示界面，未实际下载与加载 ColBERT v2.0 模型参数与索引。*")

    return demo


def main():
    app = build_ui()
    app.launch(server_name="127.0.0.1", server_port=7870, share=False)


if __name__ == "__main__":
    main()
