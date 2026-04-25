---
name: synthesizable-systemverilog-best-practices
description: "Best practices for writing synthesizable, modern, and structured SystemVerilog RTL code. Trigger this skill whenever the user asks you to: write new SystemVerilog RTL modules, refactor or review existing RTL."
---

# Synthesizable SystemVerilog Best Practices

This skill enforces a modern, highly-abstracted, and structured SystemVerilog RTL coding style. It explicitly rejects outdated Verilog-2001 habits, in favor of using advanced SystemVerilog features to write elegant, highly cohesive, and self-documenting code.

When writing or reviewing RTL, prioritize the following principles.

## 1. Modern SystemVerilog

## 1.1 Structured Development & Architecture First

Before writing the core logic, follow a top-down approach:

1. **Design `package` and `interface` first.**
2. **Prototype the main module** and establish its architectural boundaries.
3. **Fill in the logic** (control, datapath, FSMs).
4. **Write concurrent `assert` statements**.
5. **Automated formatting**: Focus on semantic correctness. Let automated Lint and formatting tools (e.g., Verible) handle whitespace and alignment.

## 1.2 Writing Elegant Synthesizable SystemVerilog

**Clarifying a Common Misconception**:
* **Myth**: Verilog is the synthesizable Hardware Description Language (HDL), while SystemVerilog is strictly a verification language.
* **Fact**: Both Verilog and SystemVerilog are hybrid languages designed for both HDL design and RTL verification. SystemVerilog is the legitimate evolution and successor to Verilog. In fact, the initial versions of the SystemVerilog specification were almost entirely focused on improving synthesizable RTL design constructs; advanced verification features were only introduced in later revisions.

While ensuring 100% synthesizability, we should maximize the code's level of abstraction. You might have heard of legacy coding guidelines requiring `_i` and `_o` suffixes for ports, or `_q` suffixes for register outputs. Forget these ugly "patches"; they are merely relics left over from the era when early Verilog lacked expressive power.

1. Signal declarations do not need to indicate their physical implementation; the implementation should be determined by procedural blocks.
2. A multi-bit type or a parameterized type should be defined before being declared.
3. The purpose of signal declarations and type definitions is to reflect their semantics as much as possible. Naming, prefixes, and suffixes should serve this goal.
4. Use packed data structures and interfaces to bundle signals, reducing scattered loose wires.
5. Control submodule length: unless there is a justifiable reason, forbid creating modules exceeding 1,000 lines.
6. Control the number of submodule interfaces, use interfaces and structs to reduce the number of ports.

## 1.3 Commenting Standard

High-quality comments should supplement the code, not translate it line-by-line. The core principles include the following four points:

1. **Module Header**: Every `module` must contain a header comment that clearly explains the overall functionality, design intent, and usage constraints of the module.
2. **Ports & Parameters**: All `parameter` and `port` declarations must be accompanied by concise comments explaining their purpose, valid range, or protocol association.
3. **Logical Partitioning**: Internal logic should be reasonably partitioned, with prominent delimiters and titles added for each partition to improve code readability and structure.
4. **Self-Documenting Code**: Avoid adding meaningless, obvious, and repetitive comments to every signal or procedural block. Prioritize making the code "self-documenting" through precise naming and logical data structures. Comments should be reserved for explaining complex algorithms, special design trade-offs, or high-level architectural intent.

## 2. Syntax

### 2.1 Declarations and Procedural Blocks

- **Logic Types**: Use `logic` for all standard signals. Only use `wire` sparingly for tri-state or multiply-driven signals. Forbid the use of `reg`.
- **Procedural Blocks**: Use `always_comb`, `always_ff`, and `always_latch`.

### 2.2 Packed Data Structures

Modern SystemVerilog encourages using structured types for data manipulation.

- **Encourage Packed Structs**: For logically related signals (e.g., headers, command packets), use `typedef struct packed`. Remember the order: the first declared signal in the struct is at the MSB position.
- **Encourage Packed Arrays**: Prefer multidimensional packed arrays (e.g., `[ROW-1:0][WIDTH-1:0] array_a`) over old-style flat bit-vectors (e.g., `[WIDTH*ROW-1:0] vector_b`).
- **Bit-Equivalence**: Packed types are physically equivalent to flat bit-vectors. Direct assignment (`array_a = vector_b`) or interface connection is sufficient.
- **Natural Indexing**: Avoid manual bit-offset calculations (e.g., `data[i*WIDTH +: WIDTH]`). Access elements directly using packed array or struct indices.

### 2.3 Package Management & Parameterization

Packages are the "Single Source of Truth" for shared types, constants, and logic; they are very friendly to the synthesizer's elaboration phase.

- **Centralized Parameter Calculation**: Centrally calculate cross-module bit-widths and depths within packages. Using direct calculations or static `function`s are both excellent methods.
  - *Port Width Management*: When a submodule does not require parameter overriding globally, consider defining port-related widths in the package.
  - *Package Import (Header Import)*: `package` `import` can be done directly in the module header rather than inside the module body. For example: `module my_module import my_pkg::*; ( input my_struct_t data_in );`
- **Layered Design**: Avoid mixing raw configuration with derived logic. Place project-level static constants in a **Config Package** and derived widths, types, and functions in a **Derived Package** (the latter `import`s or `export`s the former).
- **Data Abstraction**: A clever way to encapsulate logic is pairing `typedef struct packed` with synthesizable "methods" (`function`s) within the same package, achieving lightweight logic encapsulation.
- **Override Strategy**: Since package content is static and cannot be overridden:
  - *Large SoC*: Consider using external scripts and configuration files to generate SystemVerilog code.
  - *Native Syntax*: Use "Struct Type Parameterization" for structured module configuration (`parameter my_pkg::cfg_t CFG = my_pkg::DEFAULT_CFG`).

### 2.4 Interface Encapsulation

- **External Buses**: Prioritize using existing standard `interface` definitions from the SoC RTL library (especially for AMBA/SoC buses like AXI, APB).
- **Modports**: Define `modport`s (e.g., `manager`, `subordinate`) within the `interface`. When a module connects to an interface, specify the `modport` in its port list (e.g., `my_bus_if.subordinate bus`).
- **Data Bundles**: For data-heavy interfaces, import `packed struct` definitions within the interface to keep modports clean and logically grouped (leveraging types from Section 1.1).
- **Internal Communication**: For signal bundles used globally across submodules, create a dedicated internal `interface` and distribute it via `modport`s. Avoid top-level scattered loose wires.
- **Logic-Free Interfaces**: Interfaces should focus on wire bundles and protocol definitions. Avoid placing complex combinational control logic inside an `interface` (concurrent assertions are allowed).
- **Forbid Extracting Parameters from Interface Instances**: Defining and using `parameter`s *inside* an `interface` is perfectly valid. However, **extracting parameters from an interface instance in external logic** (e.g., using `my_if.PARAM` or using `$bits()` to get the width from a parameterized interface) is strictly forbidden. This behavior has extremely poor compatibility in some synthesis tools and frequently causes severe bugs by conflicting with the compiler's elaboration order.

### 2.5 Syntax Sugar

- Simplify `function`: In modern SystemVerilog standards, nested `begin` and `end` blocks are no longer required inside functions.
- Simplify `generate`: In modern SystemVerilog standards, `generate` and `endgenerate` keywords are no longer needed, though retaining them for compatibility with older tools is acceptable.
- Use `for (genvar i = 0; ...)` instead of declaring `genvar` independently.
- In FSM development, using constructs like `state inside {ST_IDLE, ST_RUN}` is an elegant way to express outputs.
- `signal ==? 3'b1??` gracefully implements don't-care bits.

## 3. Naming Style

Code should be self-documenting through accurate signal naming while rejecting dogmatic prefix/suffix rules. The ultimate goal is to improve readability and the level of abstraction.

### 3.1 Module Definition

- **Prefix Grouping**: Submodules of a large module should inherit the logical prefix of their parent.
- **One Module per File**: Except for cell libs, other files should only contain one module.
- **Package**: Packages use the `_pkg` suffix.
- **Interface**: Interfaces use the `_if` suffix.
- **Top-level**: Top-level modules use the `_top` suffix.

### 3.2 Type Definition

- `type` should use the `_t` suffix.
- `modport` uses the `_mp` suffix.
- `enum` should be `typedef`ed and use the `_e` suffix.
- `struct` should be `typedef`ed and use the `_t` or `_s` suffix.

### 3.3 Constants and Macros

- **Constants**: Use `localparam` and `parameter` exclusively. They should be named using `ALL_CAPS_WITH_UNDERSCORES`.
  - **Explicit Typing**: Strongly recommended to explicitly specify the data type for constants (e.g., `parameter int WIDTH = 8` or `parameter logic [7:0] VAL = 8'hFF`) to enhance strong type checking and prevent unexpected implicit truncation during synthesis.
  - **Do Not Use `string` Type**: For parameters storing strings, **do not use the SystemVerilog `string` type**, as legacy Verilog modules will fail to override it during instantiation. Instead, use a sufficiently large logic vector (e.g., `parameter logic [8*16-1:0] MODE = "DEFAULT"`).
- **Macros (`define`)**: Also `ALL_CAPS_WITH_UNDERSCORES`. Discouraged for general constants.
  - *Allowed Exception 1*: Global control macros (e.g., `` `ifdef FPGA ``, assertion toggles).
  - *Allowed Exception 2*: Massive, irregular repetitive code generation. Cleanup with `` `undef `` at the end of the module.
- **Enum values**: Also `ALL_CAPS_WITH_UNDERSCORES`, and enum names within the same enum must use the same prefix, defaulting to `ST_`.

### 3.4 Signal Instantiation

Always remember the key principle: signal naming should reflect its logical semantics, not try to determine the hardware implementation. Avoid letting procedural refactoring affect signal naming in reverse.

- **Hierarchical Consistency**: Keep signal names consistent across different levels of hierarchy. Minimize renaming a signal just because it crosses a module boundary.
- **Signal Grouping**: For discrete signals with strong functional correlation (e.g., `tx_valid`, `tx_ready`, `tx_data`), they should share the same prefix or be put into a `struct`.
- **Active-Low**: Any active-low signal should end with `_n`.
- **Clocks**: Usually named `clk`.
- **Resets**: Usually named `rst_n`. Unless defined by the protocol, such as AMBA's `aresetn` or `presetn`.
- **Pipeline Staging**: For long pipelines, use `_s{n}` to denote the stage where the signal is computed or used, forming excellent rules:
  - Combinational logic: `yyy_s{k} = f(xxx_s{k})`.
  - Registers: `zzz_s{k+1} <= zzz_s{k}`.
  - RAM: `read_addr{k}` -> `read_data{k+1}`

Avoid some practices praised by Verilog-style code but are not good ideas:

- **Avoid IO Suffixes**: Recommended to avoid adding `_i` and `_o` suffixes for module ports. This practice conflicts with hierarchical consistency.
- **Avoid `_d` / `_q` / `_reg`**: Recommended to avoid adding `_d` and `_q` suffixes to signals. Declarations should not care about physical implementation. Forbid using the `_reg` suffix to prevent collisions with the backend flow.

### 3.5 Block Instantiation

- Module instantiation names should use the `U_` prefix.
- Generate block instantiation names should use the `G_` prefix.

## 4. FSMs and Logic Separation

### 4.1 Sequential vs. Combinational Logic

- **Cohesive Merging**: For simple logic (a few `if`s or `case`s), write the combinational logic directly inside the `always_ff` block.
- **More Decision Logic**: Extract logic with more conditions (lots of `if`s, massive `case` conditions, mixed decisions) into a separate `always_comb` or `assign` block.
- **Reusing Combinational Logic**: Extract frequently used complex logic into a separate `function`, and then call it in sequential or combinational logic.

### 4.2 Three-Segment FSMs

When implementing a true state machine (FSM), follow the 3-segment structure:

1. **State Type**: Define states using a typed enumeration: `typedef enum logic [x:0] {ST_IDLE, ST_RUN} state_e;`
2. **State Variables**: Use `state_e state;` and `state_e state_next;`.
3. **Structure**:
   - *Segment 1 (Sequential)*: `always_ff` updates `state <= state_next;`.
   - *Segment 2 (Combinational)*: `always_comb` computes `state_next` using `case (state)`.
   - *Segment 3 (Output)*: Logic computing outputs based on `state`.

## 5. Simulation and Synthesis Consistency

### 5.1 always_comb

**Must use `always_comb`; forbid using `always @*`**. `always @*` carries the risk of simulation/synthesis mismatches. For example, `always @* a = 1'b1;` may not trigger in some simulators.

### 5.2 Case Statements & Modifiers

- **Forbid `casex`/`casez`**: These cause severe **simulation/synthesis mismatches**. For example, in `casex(a)`, an `x` in signal `a` (like an uninitialized state) is treated as a wildcard, leading to dangerous unexpected matches in simulation that don't exist in hardware. Use `case (...) inside` combined with `?` to represent don't-care bits.
- **Explicit Modifiers**: Use `unique` (exactly 1 match), `priority` (at least 1 match), or `unique0` (0 or 1 match) to catch logic errors via tool warnings/errors rather than debugging simulation results.

### 5.3 X-Propagation

Beware of simulation/synthesis mismatches caused by control signals entering an X state within `case` and `if` constructs. Even SystemVerilog lacks a perfect solution at the syntax level. When simulating with EDA tools, ensure the X-Propagation option is enabled and an X-Pessimism mode is selected.

### 5.4 CDC

Clock domain crossing (CDC) requires asynchronous sampling circuits. In zero-delay RTL simulations, asynchronous sampling is always in an ideal state. Discovering CDC errors relies on:

1. Formal verification. Some linting tools that can directly check CDC circuit architectures.
2. Injecting mis-sampleings during simulation.

The latter requires forbidding "writing CDC circuits manually on the spot in the code". CDC circuits should instantiate modules from a mature CDC library, utilizing their standard forms and mis-sampleings injection capabilities. If such a CDC library cannot be provided, at the very least, asynchronous sampling should be written into a separate module.

## 6. ASIC PPA Optimization

Targeting ASIC designs, many best practices here might differ significantly from early FPGA recommendations.

- **Asynchronous Resets**: Default to asynchronous resets (`or negedge rst_n`). This not only significantly reduces the difficulty of ASIC backend physical design and saves area, but is also highly recommended in modern FPGA designs (asynchronous resets make setting false paths easier to avoid consuming dedicated resources like GBUF).
- **No Resets**: Data signals like `data` or `payload` that are qualified by control flags like `valid` generally **do not require resets**, which can significantly save ASIC area and routing resources. Registers inside RAM typically do not get reset either.
- **Fanout**: In massive module designs, avoid creating a super control signal (like a soft reset/switch) that directly drives all registers, as such massive fanout causes routing congestion.
  - A correct approach is to use these global signals to generate local secondary control signals via a small number of local registers.
  - Another correct approach is to have control signals propagate along with the data flow and pipeline.

## 7. Lint Cleanliness

- Always use `localparam` inside a `package`.
- The Lint dilemma of using a `case` statement inside `always_ff`: "incomplete case" triggers a warning, but adding `default: b <= b;` triggers a "missing enable" warning during low-power analysis.
  1. `unique0`: In `always_ff` blocks where a register only updates on specific matches (0 or 1 match), use `unique0 case`.
  2. `default: ;`: For scenarios allowing zero or more matches, simply write an empty default like this, or `default: begin end`.
  3. Alternatively, implement it using `if` statements.
- `function`s should explicitly annotate their lifetime as `automatic`.
- Use static casting to preemptively process signals involved in calculations, unifying their bit-widths and signs. This avoids many false Lint warnings.