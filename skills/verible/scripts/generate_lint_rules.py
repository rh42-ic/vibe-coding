# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "questionary",
#   "rich",
# ]
# ///

import os
import sys
import json
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()

RULES = [
    {
        "name": "always-comb",
        "desc": {"en": "Checks that there are no occurrences of 'always @*'. Use 'always_comb' instead.", "zh": "检查是否存在 'always @*'，建议改用 'always_comb'。"},
        "default": True,
        "params": [],
        "example": "// Violation: Use always_comb instead\nalways @* a = b;"
    },
    {
        "name": "always-comb-blocking",
        "desc": {"en": "Checks that there are no occurrences of non-blocking assignment in combinational logic.", "zh": "检查组合逻辑中是否存在非阻塞赋值。"},
        "default": True,
        "params": [],
        "example": "// Violation: Non-blocking assignment in combinational logic\nalways_comb a <= b;"
    },
    {
        "name": "always-ff-non-blocking",
        "desc": {"en": "Checks that blocking assignments are, at most, targeting locals in sequential logic.", "zh": "检查时序逻辑中除了局部变量外是否使用了阻塞赋值。"},
        "default": True,
        "params": [
            {
                "name": "catch_modifying_assignments",
                "default": "False"
            },
            {
                "name": "waive_for_locals",
                "default": "False"
            }
        ],
        "example": "// Violation: Blocking assignment in sequential logic\nalways_ff @(posedge clk) a = b;"
    },
    {
        "name": "banned-declared-name-patterns",
        "desc": {"en": "Checks for banned declared name against set of unwanted patterns.", "zh": "检查声明的名称是否匹配禁止的模式。"},
        "default": False,
        "params": [],
        "example": "// Violation (if matches a banned pattern)\nwire bad_name_123;"
    },
    {
        "name": "case-missing-default",
        "desc": {"en": "Checks that a default case-item is always defined unless the case statement has the 'unique' qualifier.", "zh": "检查 case 语句是否包含 default 分支（除非使用了 unique 限定符）。"},
        "default": True,
        "params": [],
        "example": "// Violation: Missing default case\ncase (sel)\n  1'b1: out = 1;\nendcase"
    },
    {
        "name": "constraint-name-style",
        "desc": {"en": "Check that constraint names follow the required name style specified by a regular expression.", "zh": "检查约束名称是否符合指定的正则风格。"},
        "default": True,
        "params": [
            {
                "name": "pattern",
                "default": "([a-z0-9]+_)+c"
            }
        ],
        "example": "// Compliant: Name ends in _c\nconstraint valid_c { }"
    },
    {
        "name": "create-object-name-match",
        "desc": {"en": "Checks that the 'name' argument of 'type_id::create()' matches the name of the variable to which it is assigned.", "zh": "检查 'type_id::create()' 的名称参数是否与赋值变量名匹配。"},
        "default": True,
        "params": [],
        "example": "// Violation: 'name' must match variable name 'a'\na = my_type::type_id::create(\"b\");"
    },
    {
        "name": "dff-name-style",
        "desc": {"en": "Checks that D Flip-Flops use appropiate naming conventions in both input and output ports. The left hand side (output) and right hand side (input) are checked against a set of valid suffixes. Additionally, register names might end in a number to denote the pipeline stage index (var_q/var_q1, var_q2, ...). Pipelined signals must get their value from the previous stage: var_q3 <= var_q2. Exceptions to this rule can be configured using a regular expression or waiving whole 'if' blocks", "zh": "检查 D 触发器的输入输出端口是否使用了合适的命名后缀（如 _d, _q）。"},
        "default": False,
        "params": [
            {
                "name": "input",
                "default": "next,n,d"
            },
            {
                "name": "output",
                "default": "reg,r,ff,q"
            }
        ],
        "example": "// Compliant: Flip-flop output ends in _q\noutput logic valid_q;"
    },
    {
        "name": "disable-statement",
        "desc": {"en": "Checks that there are no occurrences of 'disable some_label' if label is referring to a fork or other none sequential block label. Use 'disable fork' instead.", "zh": "检查是否存在对非顺序块标签的 disable 语句，建议改用 disable fork。"},
        "default": False,
        "params": [],
        "example": "// Violation: Use disable fork instead\ndisable my_label;"
    },
    {
        "name": "endif-comment",
        "desc": {"en": "Checks that a Verilog '' 'endif'' directive is followed by a comment that matches the name of the opening '' 'ifdef'' or '' 'ifndef''.", "zh": "检查 endif 指令后是否跟着匹配 ifdef/ifndef 的注释。"},
        "default": False,
        "params": [],
        "example": "// Compliant: Matches opening macro\n`ifdef FOO\n`endif // FOO"
    },
    {
        "name": "enum-name-style",
        "desc": {"en": "Checks that enum type names follow a naming convention defined by a RE2 regular expression. The default regex pattern expects 'lower_snake_case' with either a '_t' or '_e' suffix. Refer to https://github.com/chipsalliance/verible/tree/master/verilog/tools/lint#readme for more detail on verible regex patterns.", "zh": "检查枚举类型名称是否符合风格要求（默认下划线结尾带 _t 或 _e）。"},
        "default": True,
        "params": [],
        "example": "// Compliant: Ends in _t or _e\ntypedef enum {A} my_enum_t;"
    },
    {
        "name": "explicit-begin",
        "desc": {"en": "Checks that a Verilog ''begin'' directive follows all if, else, always, always_comb, always_latch, always_ff, for, forever, foreach, while and initial statements.", "zh": "检查 if/else/always 等语句后是否显式使用了 begin。"},
        "default": False,
        "params": [
            {
                "name": "if_enable",
                "default": "True"
            },
            {
                "name": "else_enable",
                "default": "True"
            },
            {
                "name": "always_enable",
                "default": "True"
            },
            {
                "name": "always_comb_enable",
                "default": "True"
            },
            {
                "name": "always_latch_enable",
                "default": "True"
            },
            {
                "name": "always_ff_enable",
                "default": "True"
            },
            {
                "name": "for_enable",
                "default": "True"
            },
            {
                "name": "forever_enable",
                "default": "True"
            },
            {
                "name": "foreach_enable",
                "default": "True"
            },
            {
                "name": "while_enable",
                "default": "True"
            },
            {
                "name": "initial_enable",
                "default": "True"
            }
        ],
        "example": "// Violation: Missing begin/end block\nif (en) a = 1;"
    },
    {
        "name": "explicit-function-lifetime",
        "desc": {"en": "Checks that every function declared outside of a class is declared with an explicit lifetime (static or automatic).", "zh": "检查类外的函数是否显式声明了生命周期（static 或 automatic）。"},
        "default": True,
        "params": [],
        "example": "// Violation: Needs explicit lifetime (static/automatic)\nfunction void foo();"
    },
    {
        "name": "explicit-function-task-parameter-type",
        "desc": {"en": "Checks that every function and task parameter is declared with an explicit storage type.", "zh": "检查函数和任务的参数是否显式声明了存储类型。"},
        "default": True,
        "params": [],
        "example": "// Violation: Parameter 'a' needs an explicit type\nfunction void f(a);"
    },
    {
        "name": "explicit-parameter-storage-type",
        "desc": {"en": "Checks that every 'parameter' and 'localparam' is declared with an explicit storage type.", "zh": "检查 parameter 和 localparam 是否显式声明了类型。"},
        "default": True,
        "params": [
            {
                "name": "exempt_type",
                "default": ""
            }
        ],
        "example": "// Violation: Needs explicit type (e.g., parameter int P = 1)\nparameter P = 1;"
    },
    {
        "name": "explicit-task-lifetime",
        "desc": {"en": "Checks that every task declared outside of a class is declared with an explicit lifetime (static or automatic).", "zh": "检查类外的任务是否显式声明了生命周期（static 或 automatic）。"},
        "default": True,
        "params": [],
        "example": "// Violation: Needs explicit lifetime (static/automatic)\ntask t();"
    },
    {
        "name": "forbid-consecutive-null-statements",
        "desc": {"en": "Checks that there are no occurrences of consecutive null statements like ';;'", "zh": "检查是否存在连续的空语句（如 ;;）。"},
        "default": True,
        "params": [],
        "example": "// Violation: Consecutive null statements\na = b;;"
    },
    {
        "name": "forbid-defparam",
        "desc": {"en": "Do not use defparam.", "zh": "禁止使用 defparam。"},
        "default": True,
        "params": [],
        "example": "// Violation: defparam is forbidden\ndefparam top.A = 1;"
    },
    {
        "name": "forbid-line-continuations",
        "desc": {"en": "Checks that there are no occurrences of '\\' when breaking the string literal line. Use concatenation operator with braces instead.", "zh": "检查字符串字面量中是否使用了反斜杠换行，建议使用拼接。"},
        "default": True,
        "params": [],
        "example": "// Violation: Line continuation forbidden\nstring s = \"hello \\\nworld\";"
    },
    {
        "name": "forbid-negative-array-dim",
        "desc": {"en": "Check for negative constant literals inside array dimensions.", "zh": "检查数组维度中是否存在负数常量。"},
        "default": False,
        "params": [],
        "example": "// Violation: Negative constant in dimension\nlogic [-1:0] a;"
    },
    {
        "name": "forbidden-macro",
        "desc": {"en": "Checks that no forbidden macro calls are used.", "zh": "检查是否使用了禁用的宏。"},
        "default": True,
        "params": [],
        "example": "// Violation (if macro is blacklisted)\n`forbidden_macro(a)"
    },
    {
        "name": "generate-label",
        "desc": {"en": "Checks that every generate block statement is labeled.", "zh": "检查 generate 块是否带有标签。"},
        "default": True,
        "params": [],
        "example": "// Violation: Generate block lacks a label\ngenerate if (1) begin a = 1; end endgenerate"
    },
    {
        "name": "generate-label-prefix",
        "desc": {"en": "Checks that every generate block label starts with g_ or gen_.", "zh": "检查 generate 块标签是否以 g_ 或 gen_ 开头。"},
        "default": True,
        "params": [],
        "example": "// Violation: Label must start with gen_ or g_\ngenerate if (1) begin : my_blk"
    },
    {
        "name": "instance-shadowing",
        "desc": {"en": "Warns if there are multiple declarations in the same scope that shadow each other with the same name.", "zh": "警告在同一作用域内是否存在同名声明导致的遮蔽。"},
        "default": False,
        "params": [],
        "example": "// Violation: Inner 'a' shadows outer 'a'\nint a;\nif (1) begin int a; end"
    },
    {
        "name": "interface-name-style",
        "desc": {"en": "Checks that 'interface' names follow a naming convention defined by a RE2 regular expression. The default regex pattern expects 'lower_snake_case' with a '_if' or '_e' suffix. Refer to https://github.com/chipsalliance/verible/tree/master/verilog/tools/lint#readme for more detail on regex patterns.", "zh": "检查接口名称是否符合风格要求（默认以 _if 结尾）。"},
        "default": True,
        "params": [
            {
                "name": "style_regex",
                "default": "[a-z_0-9]+(_if)"
            }
        ],
        "example": "// Compliant: Name ends in _if\ninterface apb_if;"
    },
    {
        "name": "invalid-system-task-function",
        "desc": {"en": "Checks that no forbidden system tasks or functions are used. These consist of the following functions: '$psprintf', '$random', and '$dist_*'. As well as non-LRM function '$srandom'.", "zh": "检查是否使用了禁用的系统任务或函数（如 $psprintf, $random）。"},
        "default": True,
        "params": [],
        "example": "// Violation: $psprintf is forbidden\nstring s = $psprintf(\"%d\", 1);"
    },
    {
        "name": "legacy-generate-region",
        "desc": {"en": "Checks that there are no generate regions.", "zh": "检查是否存在 generate region 块。"},
        "default": False,
        "params": [],
        "example": "// Violation: Legacy generate block\ngenerate\n  if (1) begin : gen_blk end\nendgenerate"
    },
    {
        "name": "legacy-genvar-declaration",
        "desc": {"en": "Checks that there are no separate 'genvar' declarations.", "zh": "检查是否存在单独的 genvar 声明。"},
        "default": False,
        "params": [],
        "example": "// Violation: Declare genvar inside loop init\ngenvar i;\nfor(i=0; i<4; i++)"
    },
    {
        "name": "line-length",
        "desc": {"en": "Checks that all lines do not exceed the maximum allowed length.", "zh": "检查行宽是否超过限制。"},
        "default": True,
        "params": [
            {
                "name": "length",
                "default": "100"
            }
        ],
        "example": "// Violation: Exceeds configured line length limit\n// A line that is over 100 characters long..."
    },
    {
        "name": "macro-name-style",
        "desc": {"en": "Checks that macro names conform to a naming convention defined by a RE2 regular expression. The default regex pattern expects 'UPPER_SNAKE_CASE'. Exceptions are made for UVM like macros, where macros named 'uvm_*' and 'UVM_*' follow 'lower_snake_case' and 'UPPER_SNAKE_CASE' naming conventions respectively. Refer to https://github.com/chipsalliance/verible/tree/master/verilog/tools/lint#readme for more detail on verible regex patterns.", "zh": "检查宏名称是否符合风格要求（默认大写蛇形）。"},
        "default": True,
        "params": [
            {
                "name": "style_regex",
                "default": "[A-Z_0-9]+"
            }
        ],
        "example": "// Violation: Use UPPER_SNAKE_CASE\n`define my_macro 1"
    },
    {
        "name": "macro-string-concatenation",
        "desc": {"en": "Concatenation will not be evaluated here. Use ''...'' instead.", "zh": "检查宏字符串拼接，建议使用 \"...\"。"},
        "default": False,
        "params": [],
        "example": "// Violation: Use `\"x`\" instead\n`define M(x) \"x\""
    },
    {
        "name": "mismatched-labels",
        "desc": {"en": "Check for matching begin/end labels.", "zh": "检查 begin/end 标签是否匹配。"},
        "default": False,
        "params": [],
        "example": "// Violation: Begin and end labels must match\nbegin : foo\nend : bar"
    },
    {
        "name": "module-begin-block",
        "desc": {"en": "Checks that there are no begin-end blocks declared at the module level.", "zh": "检查模块层级是否直接声明了 begin-end 块。"},
        "default": True,
        "params": [],
        "example": "// Violation: begin-end at module level\nmodule m;\n  begin\n  end\nendmodule"
    },
    {
        "name": "module-filename",
        "desc": {"en": "If a module is declared, checks that at least one module matches the first dot-delimited component of the file name. Depending on configuration, it is also allowed to replace underscore with dashes in filenames.", "zh": "检查模块名是否与文件名匹配。"},
        "default": True,
        "params": [
            {
                "name": "allow-dash-for-underscore",
                "default": "False"
            }
        ],
        "example": "// Compliant if saved in my_mod.sv\nmodule my_mod;"
    },
    {
        "name": "module-parameter",
        "desc": {"en": "Checks that module instantiations with more than one parameter are passed in as named parameters, rather than positional parameters.", "zh": "检查多参数模块实例化是否使用了命名传参。"},
        "default": True,
        "params": [],
        "example": "// Violation: Use named parameters #(.P(1))\nmod #(1, 2) inst();"
    },
    {
        "name": "module-port",
        "desc": {"en": "Checks that module instantiations with more than one port are passed in as named ports, rather than positional ports.", "zh": "检查多端口模块实例化是否使用了命名端口。"},
        "default": True,
        "params": [],
        "example": "// Violation: Use named ports .P(a)\nmod inst(a, b);"
    },
    {
        "name": "no-tabs",
        "desc": {"en": "Checks that no tabs are used. Spaces should be used instead of tabs.", "zh": "检查是否使用了 Tab，建议使用空格。"},
        "default": True,
        "params": [],
        "example": "// Violation: Uses tab for indentation\na = b;"
    },
    {
        "name": "no-trailing-spaces",
        "desc": {"en": "Checks that there are no trailing spaces on any lines.", "zh": "检查是否存在行尾空格。"},
        "default": True,
        "params": [],
        "example": "// Violation: Line has trailing spaces\nassign a = b;"
    },
    {
        "name": "numeric-format-string-style",
        "desc": {"en": "Checks that string literals with numeric format specifiers have proper prefixes for hex and bin values and no prefixes for decimal values.", "zh": "检查数值格式化字符串是否带有合适的前缀。"},
        "default": False,
        "params": [],
        "example": "// Compliant: Hex string matches hex literal prefix\n$display(\"%h\", 8'hA);"
    },
    {
        "name": "one-module-per-file",
        "desc": {"en": "Checks that at most one module is declared per file.", "zh": "检查是否每个文件只包含一个模块。"},
        "default": False,
        "params": [],
        "example": "// Violation: Multiple modules in one file\nmodule m1; endmodule\nmodule m2; endmodule"
    },
    {
        "name": "package-filename",
        "desc": {"en": "Checks that the package name matches the filename. Depending on configuration, it is also allowed to replace underscore with dashes in filenames.", "zh": "检查包名是否与文件名匹配。"},
        "default": True,
        "params": [
            {
                "name": "allow-dash-for-underscore",
                "default": "False"
            }
        ],
        "example": "// Compliant if saved in my_pkg.sv\npackage my_pkg;"
    },
    {
        "name": "packed-dimensions-range-ordering",
        "desc": {"en": "Checks that packed dimension ranges are declare in little-endian (decreasing) order, e.g. '[N-1:0]'.", "zh": "检查 packed 维度范围是否为小端序（如 [N-1:0]）。"},
        "default": True,
        "params": [],
        "example": "// Violation: Use little-endian ordering [7:0]\nlogic [0:7] a;"
    },
    {
        "name": "parameter-name-style",
        "desc": {"en": "Checks that parameter and localparm names conform to a naming convention based on a choice of 'CamelCase', 'ALL_CAPS' and a user defined regex ORed together. Empty configurtaion: no style enforcement. Refer to https://github.com/chipsalliance/verible/tree/master/verilog/tools/lint#readme for more detail on verible regex patterns.", "zh": "检查参数名是否符合风格要求（默认 CamelCase 或 ALL_CAPS）。"},
        "default": True,
        "params": [
            {
                "name": "localparam_style",
                "default": "CamelCase"
            }
        ],
        "example": "// Violation: Default requires CamelCase or ALL_CAPS\nparameter int my_param = 1;"
    },
    {
        "name": "parameter-type-name-style",
        "desc": {"en": "Checks that parameter type names follow the lower_snake_case naming convention and end with _t.", "zh": "检查参数类型名是否符合风格要求（下划线结尾带 _t）。"},
        "default": False,
        "params": [],
        "example": "// Violation: Use lower_snake_case with _t suffix\nparameter type MyType;"
    },
    {
        "name": "plusarg-assignment",
        "desc": {"en": "Checks that plusargs are always assigned a value, by ensuring that plusargs are never accessed using the '$test$plusargs' system task.", "zh": "检查 plusarg 是否总被赋值，建议不直接使用 $test$plusargs。"},
        "default": True,
        "params": [],
        "example": "// Violation: Use $value$plusargs to ensure assignment\nif ($test$plusargs(\"f\"))"
    },
    {
        "name": "port-name-suffix",
        "desc": {"en": "Check that port names end with _i for inputs, _o for outputs and _io for inouts. Alternatively, for active-low signals use _n[io], for differential pairs use _n[io] and _p[io].", "zh": "检查端口名是否带后缀（如 _i, _o, _io）。"},
        "default": False,
        "params": [],
        "example": "// Compliant: Input port ends in _i\ninput logic clk_i;"
    },
    {
        "name": "positive-meaning-parameter-name",
        "desc": {"en": "Checks that no parameter name starts with 'disable', using positive naming (starting with 'enable') is recommended.", "zh": "检查参数名是否具有积极含义（建议以 enable 而非 disable 开头）。"},
        "default": True,
        "params": [],
        "example": "// Violation: Parameter name should use positive meaning (e.g., EnableFeature)\nparameter int DisableFeature = 1;"
    },
    {
        "name": "posix-eof",
        "desc": {"en": "Checks that the file ends with a newline.", "zh": "检查文件是否以换行符结尾。"},
        "default": True,
        "params": [],
        "example": "// Violation\nendmodule\n// EOF without newline"
    },
    {
        "name": "proper-parameter-declaration",
        "desc": {"en": "Checks that every 'parameter' declaration is inside a formal parameter list of modules/classes and every 'localparam' declaration is inside a module, class or package.", "zh": "检查参数声明位置是否正确（parameter 应在参数列表内）。"},
        "default": False,
        "params": [
            {
                "name": "package_allow_parameter",
                "default": "False"
            },
            {
                "name": "package_allow_localparam",
                "default": "True"
            }
        ],
        "example": "// Violation: Declare in module parameter list #()\nmodule m;\n  parameter int P = 1;\nendmodule"
    },
    {
        "name": "signal-name-style",
        "desc": {"en": "Checks that signal names conform to a naming convention defined by a RE2 regular expression. Signals are defined as 'a net, variable, or port within a SystemVerilog design'. The default regex pattern expects 'lower_snake_case'. Refer to https://github.com/chipsalliance/verible/tree/master/verilog/tools/lint#readme for more detail on verible regex patterns.", "zh": "检查信号名是否符合风格要求（默认小写蛇形）。"},
        "default": False,
        "params": [
            {
                "name": "style_regex",
                "default": "[a-z_0-9]+"
            }
        ],
        "example": "// Violation: Default requires lower_snake_case\nwire MySignal;"
    },
    {
        "name": "struct-union-name-style",
        "desc": {"en": "Checks that 'struct' and 'union' names use lower_snake_case naming convention and end with '_t'.", "zh": "检查结构体/联合体名是否符合风格要求（默认以 _t 结尾）。"},
        "default": True,
        "params": [
            {
                "name": "exceptions",
                "default": ""
            }
        ],
        "example": "// Compliant: Ends in _t\ntypedef struct {int a;} my_struct_t;"
    },
    {
        "name": "suggest-parentheses",
        "desc": {"en": "Recommend extra parentheses around subexpressions where it helps readability.", "zh": "建议在子表达式周围添加额外括号以提高可读性。"},
        "default": True,
        "params": [],
        "example": "// Violation: Add parentheses for clarity: a & (b == c)\nif (a & b == c)"
    },
    {
        "name": "suspicious-semicolon",
        "desc": {"en": "Checks that there are no suspicious semicolons that might affect code behaviour but escape quick visual inspection", "zh": "检查是否存在可能影响行为的 suspicious 分号。"},
        "default": False,
        "params": [],
        "example": "// Violation: Semicolon after if-condition\nif (a);\n  b = 1;"
    },
    {
        "name": "truncated-numeric-literal",
        "desc": {"en": "Checks that numeric literals are not longer than their stated bit-width to avoid undesired accidental truncation.", "zh": "检查数值字面量是否超过其声明的位宽导致截断。"},
        "default": True,
        "params": [],
        "example": "// Violation: Numeric literal is longer than its stated bit-width\nlogic [3:0] a = 5'h1f;"
    },
    {
        "name": "typedef-enums",
        "desc": {"en": "Checks that a Verilog 'enum' declaration is named using 'typedef'.", "zh": "检查枚举声明是否使用了 typedef。"},
        "default": True,
        "params": [],
        "example": "// Violation: Must use typedef enum\nenum {A, B} a_val;"
    },
    {
        "name": "typedef-structs-unions",
        "desc": {"en": "Checks that a Verilog 'struct' or 'union' declaration is named using 'typedef'.", "zh": "检查结构体/联合体声明是否使用了 typedef。"},
        "default": True,
        "params": [
            {
                "name": "allow_anonymous_nested",
                "default": "False"
            }
        ],
        "example": "// Violation: Must use typedef struct\nstruct {int a;} s_val;"
    },
    {
        "name": "undersized-binary-literal",
        "desc": {"en": "Checks that the digits of binary literals for the configured bases match their declared width, i.e. has enough padding prefix zeros.", "zh": "检查二进制字面量是否与其声明的宽度匹配（是否有足够的补零）。"},
        "default": True,
        "params": [
            {
                "name": "bin",
                "default": "True"
            },
            {
                "name": "oct",
                "default": "False"
            },
            {
                "name": "hex",
                "default": "False"
            },
            {
                "name": "lint_zero",
                "default": "False"
            },
            {
                "name": "autofix",
                "default": "True"
            }
        ],
        "example": "// Violation: Binary literal needs padding prefix zeros\nlogic [31:0] a = 32'b1;"
    },
    {
        "name": "unpacked-dimensions-range-ordering",
        "desc": {"en": "Checks that unpacked dimension ranges are declared in big-endian order '[0:N-1]', and when an unpacked dimension range is zero-based '[0:N-1]', the size is declared as '[N]' instead.", "zh": "检查 unpacked 维度范围是否为大端序（[0:N-1]）或使用单个大小声明 [N]。"},
        "default": True,
        "params": [],
        "example": "// Violation: Use [8] or big-endian [0:7] for unpacked dimensions\nlogic a [7:0];"
    },
    {
        "name": "uvm-macro-semicolon",
        "desc": {"en": "Checks that no 'uvm_* macro calls end with ';'.", "zh": "检查 uvm_* 宏调用是否以分号结尾。"},
        "default": False,
        "params": [],
        "example": "// Violation: UVM macros should not end with a semicolon\n`uvm_info(...);"
    },
    {
        "name": "v2001-generate-begin",
        "desc": {"en": "Checks that there are no generate-begin blocks inside a generate region.", "zh": "检查 generate region 内是否存在 generate-begin 块。"},
        "default": True,
        "params": [],
        "example": "// Violation: generate-begin block inside generate region\ngenerate\n  begin : gen_blk end\nendgenerate"
    },
    {
        "name": "void-cast",
        "desc": {"en": "Checks that void casts do not contain certain function/method calls.", "zh": "检查 void 转换是否包含特定的函数/方法调用。"},
        "default": True,
        "params": [],
        "example": "// Compliant: Explicitly casts function return to void\nvoid'(some_func());"
    }
]

KEY_RULES = [
    "line-length",
    "no-tabs",
    "always-comb",
    "always-comb-blocking",
    "always-ff-non-blocking",
    "enum-name-style",
    "module-filename",
    "signal-name-style"
]

UI_TEXT = {
    "title": {
        "en": "Verible Lint Rules Wizard",
        "zh": "Verible Lint 规则配置向导"
    },
    "subtitle": {
        "en": "Configure your SystemVerilog linting rules easily.",
        "zh": "轻松配置您的 SystemVerilog Lint 规则。"
    },
    "profile_select": {
        "en": "Choose a base profile:",
        "zh": "选择一个基础配置方案 (Choose a base profile):"
    },
    "profile_choices": {
        "en": [
            "Default (Verible defaults)",
            "Strict (Enable all rules)",
            "Relaxed (Disable formatting/style rules)"
        ],
        "zh": [
            "Default (Verible 默认方案)",
            "Strict (启用所有规则)",
            "Relaxed (禁用格式/风格规则)"
        ]
    },
    "key_rules_header": {
        "en": "=== Key Rules Configuration ===",
        "zh": "=== 关键规则配置 ==="
    },
    "advanced_header": {
        "en": "=== Advanced Configuration ===",
        "zh": "=== 高级配置 ==="
    },
    "manual_confirm": {
        "en": "Do you want to manually configure the remaining rules?",
        "zh": "您想手动配置剩余规则吗？"
    },
    "success": {
        "en": "Success! Lint rules written to ",
        "zh": "成功! Lint 规则已写入 "
    },
    "rule_enable_prompt": {
        "en": "Enable '{}'?",
        "zh": "启用规则 '{}'？"
    },
    "param_prompt": {
        "en": "Value for parameter '{}':",
        "zh": "参数 '{}' 的值："
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
        sys.exit(0)

    console.print(Panel.fit(f"[bold blue]{UI_TEXT['title'][lang]}[/bold blue]\n{UI_TEXT['subtitle'][lang]}"))
    
    profile_choice = questionary.select(
        UI_TEXT["profile_select"][lang],
        choices=UI_TEXT["profile_choices"][lang]
    ).ask()

    if not profile_choice:
        sys.exit(0)

    # Initialize states
    state = {}
    for rule in RULES:
        if "Strict" in profile_choice:
            state[rule["name"]] = {"enabled": True, "params": {p["name"]: p["default"] for p in rule.get("params", [])}}
        elif "Relaxed" in profile_choice:
            enabled = rule["default"]
            if rule["name"] in ["line-length", "no-tabs", "no-trailing-spaces", "explicit-begin", "signal-name-style"]:
                enabled = False
            state[rule["name"]] = {"enabled": enabled, "params": {p["name"]: p["default"] for p in rule.get("params", [])}}
        else:
            state[rule["name"]] = {"enabled": rule["default"], "params": {p["name"]: p["default"] for p in rule.get("params", [])}}

    # Configure Key Rules
    console.print(f"\n[bold green]{UI_TEXT['key_rules_header'][lang]}[/bold green]")
    for rule_name in KEY_RULES:
        rule = next((r for r in RULES if r["name"] == rule_name), None)
        if rule:
            configure_rule(rule, state[rule_name], lang)

    # Ask for remaining
    console.print(f"\n[bold green]{UI_TEXT['advanced_header'][lang]}[/bold green]")
    configure_all = questionary.confirm(UI_TEXT["manual_confirm"][lang]).ask()
    if configure_all is None: sys.exit(0)
    
    if configure_all:
        for rule in RULES:
            if rule["name"] not in KEY_RULES:
                configure_rule(rule, state[rule["name"]], lang)

    # Generate output
    output_lines = [
        f"# Verible Lint Rules File (Language: {lang})",
        f"# Generated with base profile: {profile_choice}",
        ""
    ]
    for rule in RULES:
        r_state = state[rule["name"]]
        if r_state["enabled"]:
            line = f"+{rule['name']}"
            if r_state["params"]:
                params_str = ";".join(f"{k}:{v}" for k, v in r_state["params"].items() if v)
                if params_str:
                    line += f"={params_str}"
            output_lines.append(line)
        else:
            output_lines.append(f"-{rule['name']}")

    out_file = ".rules.verible_lint"
    with open(out_file, "w") as f:
        f.write("\n".join(output_lines) + "\n")
    
    console.print(f"\n[bold green]{UI_TEXT['success'][lang]}[bold]{out_file}[/bold][/bold green]")


def configure_rule(rule, current_state, lang):
    console.print(f"\n[bold cyan]Rule: {rule['name']}[/bold cyan]")
    console.print(f"[italic]{rule['desc'][lang]}[/italic]")
    if rule["example"]:
        console.print(Panel(Syntax(rule["example"], "systemverilog", theme="monokai", background_color="default", word_wrap=True), title="Example", border_style="dim", expand=False))
    
    enabled = questionary.confirm(UI_TEXT["rule_enable_prompt"][lang].format(rule['name']), default=current_state["enabled"]).ask()
    if enabled is None: sys.exit(0)
    current_state["enabled"] = enabled

    if enabled and rule.get("params"):
        for p in rule["params"]:
            val = questionary.text(
                UI_TEXT["param_prompt"][lang].format(p['name']), 
                default=current_state["params"].get(p["name"], p["default"])
            ).ask()
            if val is None: sys.exit(0)
            current_state["params"][p["name"]] = val

if __name__ == "__main__":
    main()
