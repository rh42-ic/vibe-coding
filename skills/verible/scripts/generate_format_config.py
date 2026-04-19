# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "questionary",
#     "rich",
# ]
# ///

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
import os

console = Console()

# 全量格式化选项元数据
FORMAT_OPTIONS = {
    # --- 基础通用配置 (General) ---
    "column_limit": {
        "group": {"en": "General Settings", "zh": "基础配置"},
        "desc": {"en": "Target line length limit", "zh": "单行字符限制"},
        "default": "100",
        "type": "int",
    },
    "indentation_spaces": {
        "group": {"en": "General Settings", "zh": "基础配置"},
        "desc": {"en": "Indentation spaces per level", "zh": "缩进空格数"},
        "default": "2",
        "type": "int",
    },
    "wrap_spaces": {
        "group": {"en": "General Settings", "zh": "基础配置"},
        "desc": {"en": "Wrap indentation spaces", "zh": "换行后的额外缩进空格"},
        "default": "4",
        "type": "int",
    },
    "line_terminator": {
        "group": {"en": "General Settings", "zh": "基础配置"},
        "desc": {"en": "Line terminator style", "zh": "行尾符样式"},
        "choices": ["auto", "LF", "CRLF"],
        "default": "auto",
    },
    # --- 对齐配置 (Alignment) ---
    "assignment_statement_alignment": {
        "group": {"en": "Alignment Settings", "zh": "对齐配置"},
        "desc": {"en": "General assignment alignment", "zh": "常规赋值语句对齐"},
        "choices": ["align", "flush-left", "preserve", "infer"],
        "default": "infer",
    },
    "enum_assignment_statement_alignment": {
        "group": {"en": "Alignment Settings", "zh": "对齐配置"},
        "desc": {"en": "Enum assignment alignment", "zh": "枚举赋值对齐"},
        "choices": ["align", "flush-left", "preserve", "infer"],
        "default": "infer",
    },
    "case_items_alignment": {
        "group": {"en": "Alignment Settings", "zh": "对齐配置"},
        "desc": {"en": "Case items alignment", "zh": "Case 语句项对齐"},
        "choices": ["align", "flush-left", "preserve", "infer"],
        "default": "infer",
    },
    "class_member_variable_alignment": {
        "group": {"en": "Alignment Settings", "zh": "对齐配置"},
        "desc": {"en": "Class member variable alignment", "zh": "类成员变量声明对齐"},
        "choices": ["align", "flush-left", "preserve", "infer"],
        "default": "infer",
    },
    "distribution_items_alignment": {
        "group": {"en": "Alignment Settings", "zh": "对齐配置"},
        "desc": {"en": "Distribution items alignment", "zh": "约束分布项对齐"},
        "choices": ["align", "flush-left", "preserve", "infer"],
        "default": "infer",
    },
    "formal_parameters_alignment": {
        "group": {"en": "Alignment Settings", "zh": "对齐配置"},
        "desc": {"en": "Formal parameters alignment", "zh": "形参声明对齐"},
        "choices": ["align", "flush-left", "preserve", "infer"],
        "default": "infer",
    },
    "module_net_variable_alignment": {
        "group": {"en": "Alignment Settings", "zh": "对齐配置"},
        "desc": {"en": "Net/variable declarations alignment", "zh": "模块内网表/变量声明对齐"},
        "choices": ["align", "flush-left", "preserve", "infer"],
        "default": "infer",
    },
    "named_parameter_alignment": {
        "group": {"en": "Alignment Settings", "zh": "对齐配置"},
        "desc": {"en": "Named parameter alignment", "zh": "例化参数赋值对齐"},
        "choices": ["align", "flush-left", "preserve", "infer"],
        "default": "infer",
    },
    "named_port_alignment": {
        "group": {"en": "Alignment Settings", "zh": "对齐配置"},
        "desc": {"en": "Named port connections alignment", "zh": "模块端口连接对齐"},
        "choices": ["align", "flush-left", "preserve", "infer"],
        "default": "infer",
    },
    "port_declarations_alignment": {
        "group": {"en": "Alignment Settings", "zh": "对齐配置"},
        "desc": {"en": "Port declarations alignment", "zh": "端口声明对齐"},
        "choices": ["align", "flush-left", "preserve", "infer"],
        "default": "infer",
    },
    "struct_union_members_alignment": {
        "group": {"en": "Alignment Settings", "zh": "对齐配置"},
        "desc": {"en": "Struct/union members alignment", "zh": "结构体/联合体成员对齐"},
        "choices": ["align", "flush-left", "preserve", "infer"],
        "default": "infer",
    },
    # --- 缩进与换行策略 (Indentation & Wrapping) ---
    "formal_parameters_indentation": {
        "group": {"en": "Indentation & Wrapping", "zh": "换行缩进"},
        "desc": {"en": "Formal parameters indentation", "zh": "形参缩进样式"},
        "choices": ["indent", "wrap"],
        "default": "wrap",
    },
    "named_parameter_indentation": {
        "group": {"en": "Indentation & Wrapping", "zh": "换行缩进"},
        "desc": {"en": "Named parameter indentation", "zh": "例化参数缩进样式"},
        "choices": ["indent", "wrap"],
        "default": "wrap",
    },
    "named_port_indentation": {
        "group": {"en": "Indentation & Wrapping", "zh": "换行缩进"},
        "desc": {"en": "Named port indentation", "zh": "端口连接缩进样式"},
        "choices": ["indent", "wrap"],
        "default": "wrap",
    },
    "port_declarations_indentation": {
        "group": {"en": "Indentation & Wrapping", "zh": "换行缩进"},
        "desc": {"en": "Port declarations indentation", "zh": "端口声明缩进样式"},
        "choices": ["indent", "wrap"],
        "default": "wrap",
    },
    "wrap_end_else_clauses": {
        "group": {"en": "Indentation & Wrapping", "zh": "换行缩进"},
        "desc": {"en": "Split 'end' and 'else' lines", "zh": "将 end 和 else 分行"},
        "choices": ["true", "false"],
        "default": "false",
    },
    "expand_coverpoints": {
        "group": {"en": "Indentation & Wrapping", "zh": "换行缩进"},
        "desc": {"en": "Always expand coverpoints", "zh": "始终展开 coverpoints"},
        "choices": ["true", "false"],
        "default": "false",
    },
    "compact_indexing_and_selections": {
        "group": {"en": "Indentation & Wrapping", "zh": "换行缩进"},
        "desc": {"en": "Compact indexing/selections", "zh": "索引/位选表达式使用紧凑格式"},
        "choices": ["true", "false"],
        "default": "true",
    },
    "try_wrap_long_lines": {
        "group": {"en": "Indentation & Wrapping", "zh": "换行缩进"},
        "desc": {"en": "Optimize long line wrapping", "zh": "尝试优化长行换行"},
        "choices": ["true", "false"],
        "default": "false",
    },
    # --- 细粒度对齐控制 (Detail Control) ---
    "port_declarations_right_align_packed_dimensions": {
        "group": {"en": "Detail Control", "zh": "细节控制"},
        "desc": {"en": "Right-align packed dimensions", "zh": "右对齐端口声明的 Packed 维度"},
        "choices": ["true", "false"],
        "default": "false",
    },
    "port_declarations_right_align_unpacked_dimensions": {
        "group": {"en": "Detail Control", "zh": "细节控制"},
        "desc": {"en": "Right-align unpacked dimensions", "zh": "右对齐端口声明的 Unpacked 维度"},
        "choices": ["true", "false"],
        "default": "false",
    },
    # --- 惩罚权重 (Penalties) ---
    "line_break_penalty": {
        "group": {"en": "Penalties", "zh": "惩罚权重"},
        "desc": {"en": "Penalty for line breaks", "zh": "引入换行的惩罚权重"},
        "default": "2",
        "type": "int",
    },
    "over_column_limit_penalty": {
        "group": {"en": "Penalties", "zh": "惩罚权重"},
        "desc": {"en": "Baseline penalty for exceeding limit", "zh": "超出列限制的基础惩罚"},
        "default": "100",
        "type": "int",
    },
}

PRESETS = {
    "Default (Verible Standard) / Verible 标准风格": {
        # 使用选项自带的默认值
    },
    "Strict Alignment / 强制深度对齐风格": {
        "column_limit": "120",
        "assignment_statement_alignment": "align",
        "enum_assignment_statement_alignment": "align",
        "case_items_alignment": "align",
        "class_member_variable_alignment": "align",
        "formal_parameters_alignment": "align",
        "module_net_variable_alignment": "align",
        "named_parameter_alignment": "align",
        "named_port_alignment": "align",
        "port_declarations_alignment": "align",
        "struct_union_members_alignment": "align",
        "wrap_end_else_clauses": "true",
        "try_wrap_long_lines": "true",
    },
    "Compact / 节省空间/紧凑风格": {
        "column_limit": "80",
        "assignment_statement_alignment": "flush-left",
        "named_port_alignment": "flush-left",
        "wrap_end_else_clauses": "false",
        "compact_indexing_and_selections": "true",
    },
}

UI_TEXT = {
    "title": {
        "en": "Verible Verilog Format Configuration Wizard",
        "zh": "Verible Verilog Format 全量配置向导"
    },
    "subtitle": {
        "en": "This script will guide you through all 27 formatting flags",
        "zh": "此脚本将引导您逐一确认所有 27 个格式化 Flag"
    },
    "preset_select": {
        "en": "Select a base preset for initial defaults:",
        "zh": "选择一个基准模板以加载初始默认值 (Select a preset for initial defaults):"
    },
    "success": {
        "en": "Success! Configuration file generated: ",
        "zh": "成功! 配置文件已生成: "
    },
    "preview": {
        "en": "Content Preview",
        "zh": "内容预览"
    }
}


def main():
    lang = questionary.select(
        "Select Language / 选择语言:",
        choices=[
            questionary.Choice("English", "en"),
            questionary.Choice("中文", "zh"),
        ],
    ).ask()

    if not lang:
        return

    console.print(
        Panel(
            f"[bold cyan]{UI_TEXT['title'][lang]}[/bold cyan]\n{UI_TEXT['subtitle'][lang]}",
            expand=False,
        )
    )

    preset_choice = questionary.select(
        UI_TEXT["preset_select"][lang],
        choices=list(PRESETS.keys()),
    ).ask()

    # 初始化 config，优先使用选定的模板值，否则使用全局默认值
    preset_values = PRESETS[preset_choice]

    config = {}
    
    # 获取唯一的组列表，保持原始顺序
    groups_en = []
    for opt in FORMAT_OPTIONS.values():
        g_en = opt["group"]["en"]
        if g_en not in groups_en:
            groups_en.append(g_en)

    # 逐一确认所有选项
    for group_en in groups_en:
        # 获取当前组的本地化名称
        group_zh = next(opt["group"]["zh"] for opt in FORMAT_OPTIONS.values() if opt["group"]["en"] == group_en)
        group_display = group_zh if lang == "zh" else group_en
        
        console.print(f"\n[bold yellow]>>> {group_display}[/bold yellow]")
        group_opts = {k: v for k, v in FORMAT_OPTIONS.items() if v["group"]["en"] == group_en}

        for key, info in group_opts.items():
            # 确定当前提示的默认值：Preset -> Global Default
            current_default = preset_values.get(key, info["default"])

            prompt_text = f"{info['desc'][lang]} (Flag: --{key}):"

            if "choices" in info:
                val = questionary.select(
                    prompt_text,
                    choices=info["choices"],
                    default=str(current_default),
                ).ask()
            else:
                val = questionary.text(
                    prompt_text, default=str(current_default)
                ).ask()

            config[key] = val

    # 生成最终文件
    output_file = ".verible_format"
    output_content = [
        f"# Verible Verilog Format Configuration File (Language: {lang})",
        f"# Generated with base preset: {preset_choice}",
        "",
    ]

    for group_en in groups_en:
        group_zh = next(opt["group"]["zh"] for opt in FORMAT_OPTIONS.values() if opt["group"]["en"] == group_en)
        group_display = group_zh if lang == "zh" else group_en
        
        output_content.append(f"# --- {group_display} ---")
        group_keys = [k for k, v in FORMAT_OPTIONS.items() if v["group"]["en"] == group_en]
        for k in group_keys:
            output_content.append(f"--{k}={config[k]}")
        output_content.append("")

    with open(output_file, "w") as f:
        f.write("\n".join(output_content))

    console.print(f"\n[bold green]✅ {UI_TEXT['success'][lang]}{output_file}[/bold green]")
    console.print(Panel("\n".join(output_content), title=f"{output_file} {UI_TEXT['preview'][lang]}"))



if __name__ == "__main__":
    main()
