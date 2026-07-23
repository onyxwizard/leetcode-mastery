### 📘 Chapter: Stack  
### 📌 Problem 6: Evaluate Reverse Polish Notation (LeetCode 150)

---

**Input**  
- `tokens`: an array of strings representing an arithmetic expression in **Reverse Polish Notation (postfix)**.

**Output**  
- An integer — the evaluated result of the expression.

**Constraints**  
- `1 <= tokens.length <= 10⁴`  
- `tokens[i]` is either an operator: `"+"`, `"-"`, `"*"`, `"/"`, or an integer in `[-200, 200]`.  
- The expression is always valid (no division by zero).  
- Integer division truncates toward zero.  
- All intermediate results fit in a 32-bit integer.

**Example**  
```
Input:  tokens = ["2","1","+","3","*"]
Output: 9
Explanation: (2 + 1) * 3 = 9

Input:  tokens = ["4","13","5","/","+"]
Output: 6
Explanation: 4 + (13 / 5) = 4 + 2 = 6

Input:  tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
Output: 22
Explanation: ((10 * (6 / ((9 + 3) * -11))) + 17) + 5
           = ((10 * (6 / (12 * -11))) + 17) + 5
           = ((10 * (6 / -132)) + 17) + 5
           = ((10 * 0) + 17) + 5
           = (0 + 17) + 5
           = 22
```

**Follow-up**  
- Not explicitly given. (Extensions: support more operators, evaluate infix expressions, handle unary minus.)

---

### 🧠 Core Idea

Reverse Polish Notation (postfix) is **explicitly designed** for stack-based evaluation.

- **Infix:** `2 + 1` (operator between operands — needs precedence rules).
- **Postfix:** `2 1 +` (operator after operands — no ambiguity, no precedence needed).

**Evaluation rule:**
- Read left to right.
- **Operand (number):** Push onto stack.
- **Operator:** Pop two operands (right first, then left), compute, push result.
- At the end, the stack contains exactly one element — the answer.

**Why a stack?** The LIFO property perfectly models how postfix "resolves" the most recent operands first. When we see an operator, it always applies to the **two most recently seen unresolved values** — exactly what a stack gives us.

---

---

# 🔨 SECTION 1: BRUTE FORCE APPROACH

---

## 1A. Repeated Reduction — Scan and Replace (O(n²) Time)

**Idea:** Treat the expression as a mutable list. Repeatedly scan left-to-right for the first pattern `[operand, operand, operator]`. Replace those three tokens with the computed result. Continue until one token remains.

**Time:** O(n²) — each reduction scans up to n tokens and shifts the list.  
**Space:** O(n) — mutable list.

```java
import java.util.*;

public int evalRPN(String[] tokens) {
    List<String> list = new ArrayList<>(Arrays.asList(tokens));

    while (list.size() > 1) {
        for (int i = 2; i < list.size(); i++) {
            if (isOperator(list.get(i))) {
                int b = Integer.parseInt(list.get(i - 1));
                int a = Integer.parseInt(list.get(i - 2));
                int result = applyOp(a, b, list.get(i));

                // Replace three tokens with result
                list.set(i - 2, String.valueOf(result));
                list.remove(i);      // remove operator
                list.remove(i - 1);  // remove second operand
                break;               // restart scan
            }
        }
    }

    return Integer.parseInt(list.get(0));
}

private boolean isOperator(String s) {
    return s.equals("+") || s.equals("-") || s.equals("*") || s.equals("/");
}

private int applyOp(int a, int b, String op) {
    switch (op) {
        case "+": return a + b;
        case "-": return a - b;
        case "*": return a * b;
        case "/": return a / b;
        default: throw new IllegalArgumentException();
    }
}
```

### 🔍 Sample Iteration

**Input:** `tokens = ["2", "1", "+", "3", "*"]`

| Pass | List state | First operator found at i | a, b | Result | List after reduction |
|------|-----------|--------------------------|------|--------|---------------------|
| 1 | `["2", "1", "+", "3", "*"]` | i=2 (`"+"`) | a=2, b=1 | 2+1=**3** | `["3", "3", "*"]` |
| 2 | `["3", "3", "*"]` | i=2 (`"*"`) | a=3, b=3 | 3×3=**9** | `["9"]` |
| 3 | `["9"]` | size==1 → **STOP** | — | — | — |

**Result:** `9` ✅

> ⚠️ Each pass scans the list and performs `remove()` operations (shifting elements). For n = 10⁴ tokens, this is ~n/2 reductions × O(n) scan/shift each = O(n²) ≈ 10⁸ operations. The stack approach does it in a single O(n) pass.

---

## 1B. Recursive Evaluation (Right-to-Left)

**Idea:** Process the expression from right to left recursively. When encountering an operator, recursively evaluate its two operands.

**Time:** O(n).  
**Space:** O(n) — recursion stack depth.  
⚠️ Works but risks stack overflow for very deep expressions (n = 10⁴ is borderline safe in Java).

```java
private int pos;

public int evalRPN(String[] tokens) {
    pos = tokens.length - 1;
    return evaluate(tokens);
}

private int evaluate(String[] tokens) {
    String token = tokens[pos--];

    if (isOperator(token)) {
        int right = evaluate(tokens);  // right operand first (it's to the left in the array)
        int left = evaluate(tokens);   // left operand
        return applyOp(left, right, token);
    }

    return Integer.parseInt(token);
}
```

### 🔍 Sample Iteration (Call Stack)

**Input:** `tokens = ["2", "1", "+", "3", "*"]`, pos starts at 4.

```
evaluate(): token = tokens[4] = "*" → operator!
├─ right = evaluate(): token = tokens[3] = "3" → return 3
└─ left = evaluate(): token = tokens[2] = "+" → operator!
   ├─ right = evaluate(): token = tokens[1] = "1" → return 1
   └─ left = evaluate(): token = tokens[0] = "2" → return 2
   └─ return 2 + 1 = 3
└─ return 3 * 3 = 9 ✅
```

> 📌 Elegant but uses the call stack implicitly. For n = 10⁴, recursion depth could be ~5000 — safe in Java but not ideal. The explicit stack is preferred.

---

---

# ⚡ SECTION 2: OPTIMIZED APPROACH

---

## 2A. Stack-Based Evaluation (O(n) Time, O(n) Space) ✅

**Idea:**  
- Use a `Deque<Integer>` as the evaluation stack.  
- Iterate over each token left to right:  
  - **Number:** Parse and push.  
  - **Operator:** Pop `b` (top), pop `a` (next), compute `a op b`, push result.  
- Final answer = the sole element on the stack.

**Critical detail:** For `-` and `/`, order matters! Pop `b` first (it was pushed later), then `a`. Compute `a - b` and `a / b`.

**Time:** O(n) — each token processed exactly once.  
**Space:** O(n) — stack holds at most ~(n+1)/2 operands.

```java
import java.util.ArrayDeque;
import java.util.Deque;

public int evalRPN(String[] tokens) {
    Deque<Integer> stack = new ArrayDeque<>();

    for (String token : tokens) {
        switch (token) {
            case "+": {
                stack.push(stack.pop() + stack.pop());
                break;
            }
            case "-": {
                int b = stack.pop();
                int a = stack.pop();
                stack.push(a - b);
                break;
            }
            case "*": {
                stack.push(stack.pop() * stack.pop());
                break;
            }
            case "/": {
                int b = stack.pop();
                int a = stack.pop();
                stack.push(a / b);
                break;
            }
            default: {
                stack.push(Integer.parseInt(token));
            }
        }
    }

    return stack.peek();
}
```

### 🔍 Sample Iteration 1

**Input:** `tokens = ["2", "1", "+", "3", "*"]`  
**Infix equivalent:** `(2 + 1) * 3 = 9`

| Step | Token | Action | Stack (top → bottom) | Explanation |
|------|-------|--------|---------------------|-------------|
| 1 | `"2"` | Push 2 | `[2]` | Operand |
| 2 | `"1"` | Push 1 | `[1, 2]` | Operand |
| 3 | `"+"` | Pop b=1, pop a=2. Push 2+1=3. | `[3]` | Operator: 2+1=3 |
| 4 | `"3"` | Push 3 | `[3, 3]` | Operand |
| 5 | `"*"` | Pop b=3, pop a=3. Push 3×3=9. | `[9]` | Operator: 3×3=9 |
| END | — | Return stack.peek() | `[9]` | **Result: 9** ✅ |

---

### 🔍 Visual Stack Trace 1

```
tokens = ["2", "1", "+", "3", "*"]

Step 1: "2" → push
  ┌───┐
  │ 2 │
  └───┘

Step 2: "1" → push
  ┌───┐
  │ 1 │ ← top
  ├───┤
  │ 2 │
  └───┘

Step 3: "+" → pop 1, pop 2, push 2+1=3
  ┌───┐
  │ 3 │ ← result of 2+1
  └───┘

Step 4: "3" → push
  ┌───┐
  │ 3 │ ← top
  ├───┤
  │ 3 │
  └───┘

Step 5: "*" → pop 3, pop 3, push 3×3=9
  ┌───┐
  │ 9 │ ← FINAL ANSWER
  └───┘
```

---

### 🔍 Sample Iteration 2 (Division)

**Input:** `tokens = ["4", "13", "5", "/", "+"]`  
**Infix equivalent:** `4 + (13 / 5) = 4 + 2 = 6`

| Step | Token | Action | Stack (top → bottom) |
|------|-------|--------|---------------------|
| 1 | `"4"` | Push 4 | `[4]` |
| 2 | `"13"` | Push 13 | `[13, 4]` |
| 3 | `"5"` | Push 5 | `[5, 13, 4]` |
| 4 | `"/"` | Pop b=5, pop a=13. Push 13/5=**2** (truncates toward 0). | `[2, 4]` |
| 5 | `"+"` | Pop b=2, pop a=4. Push 4+2=**6**. | `[6]` |
| END | — | Return 6 | **Result: 6** ✅ |

> 📌 Java's integer division `13 / 5 = 2` already truncates toward zero. For negative: `-7 / 2 = -3` (truncates toward zero, not floor). This matches the problem requirement.

---

### 🔍 Sample Iteration 3 (Complex Expression)

**Input:** `tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]`  
**Infix equivalent:** `((10 * (6 / ((9 + 3) * -11))) + 17) + 5 = 22`

| Step | Token | Action | Stack (top → bottom) |
|------|-------|--------|---------------------|
| 1 | `"10"` | Push 10 | `[10]` |
| 2 | `"6"` | Push 6 | `[6, 10]` |
| 3 | `"9"` | Push 9 | `[9, 6, 10]` |
| 4 | `"3"` | Push 3 | `[3, 9, 6, 10]` |
| 5 | `"+"` | Pop 3, pop 9. Push 9+3=**12**. | `[12, 6, 10]` |
| 6 | `"-11"` | Push -11 | `[-11, 12, 6, 10]` |
| 7 | `"*"` | Pop -11, pop 12. Push 12×(-11)=**-132**. | `[-132, 6, 10]` |
| 8 | `"/"` | Pop -132, pop 6. Push 6/(-132)=**0** (truncates). | `[0, 10]` |
| 9 | `"*"` | Pop 0, pop 10. Push 10×0=**0**. | `[0]` |
| 10 | `"17"` | Push 17 | `[17, 0]` |
| 11 | `"+"` | Pop 17, pop 0. Push 0+17=**17**. | `[17]` |
| 12 | `"5"` | Push 5 | `[5, 17]` |
| 13 | `"+"` | Pop 5, pop 17. Push 17+5=**22**. | `[22]` |
| END | — | Return 22 | **Result: 22** ✅ |

---

### 🔍 Visual Stack Trace 3 (Annotated)

```
tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]

"10" → [10]
"6"  → [6, 10]
"9"  → [9, 6, 10]
"3"  → [3, 9, 6, 10]
"+"  → [12, 6, 10]          ← 9+3=12
"-11"→ [-11, 12, 6, 10]
"*"  → [-132, 6, 10]        ← 12×(-11)=-132
"/"  → [0, 10]              ← 6÷(-132)=0 (truncated)
"*"  → [0]                  ← 10×0=0
"17" → [17, 0]
"+"  → [17]                 ← 0+17=17
"5"  → [5, 17]
"+"  → [22]                 ← 17+5=22 ★ ANSWER
```

---

### 🔍 Why Operand Order Matters for `-` and `/`

```
Stack before "-": [b, a, ...]  (b is on top, pushed AFTER a)

WRONG: stack.pop() - stack.pop()  →  b - a  ❌
RIGHT: int b = stack.pop();
       int a = stack.pop();
       a - b  ✅

Example: tokens = ["5", "3", "-"]  means 5 - 3 = 2
  Stack: [3, 5]  (3 on top)
  Pop b=3, pop a=5 → 5-3=2 ✅
  If we did pop()-pop() = 3-5 = -2 ❌
```

> 📌 For `+` and `*`, order doesn't matter (commutative), so `stack.pop() + stack.pop()` is safe. For `-` and `/`, we **must** pop into named variables to preserve order.

---

### 🔍 Edge Case: Single Number

**Input:** `tokens = ["42"]`

| Step | Token | Action | Stack |
|------|-------|--------|-------|
| 1 | `"42"` | Push 42 | `[42]` |
| END | — | Return 42 | **Result: 42** ✅ |

---

### 🔍 Edge Case: Negative Numbers

**Input:** `tokens = ["-3", "-2", "+"]` → means (-3) + (-2) = -5

| Step | Token | Action | Stack |
|------|-------|--------|-------|
| 1 | `"-3"` | `Integer.parseInt("-3")` = -3. Push. | `[-3]` |
| 2 | `"-2"` | `Integer.parseInt("-2")` = -2. Push. | `[-2, -3]` |
| 3 | `"+"` | Pop -2, pop -3. Push -3+(-2)=-5. | `[-5]` |

**Result:** `-5` ✅

> 📌 `Integer.parseInt()` handles negative number strings correctly. The `"-"` operator is a single character; `"-3"` is a multi-character number string. The `switch` on `token` distinguishes them because `"-3"` doesn't match `"-"`.

---

### 🔍 How to Distinguish Operator "-" from Negative Number "-X"

```java
// The switch statement handles this naturally:
switch (token) {
    case "-":   // This ONLY matches the single character "-"
        ...
    default:    // "-3", "-200", etc. fall through to here
        stack.push(Integer.parseInt(token));  // parses "-3" → -3
}
```

> 📌 The token `"-"` (length 1) is the subtraction operator. The token `"-3"` (length 2) is a negative number. String equality in `switch` distinguishes them perfectly.

---

---

# 📊 SECTION 3: TRADE-OFFS & COMPARISONS

---

## Repeated Reduction vs Recursive vs Stack

| Metric | Repeated Reduction | Recursive (R→L) | Stack (L→R) |
|--------|-------------------|-----------------|-------------|
| Time | O(n²) | O(n) | **O(n)** |
| Space | O(n) list + O(n) shifts | O(n) call stack | **O(n) explicit stack** |
| Direction | Left-to-right (scan) | Right-to-left | **Left-to-right** |
| Overflow risk | None | Yes (deep recursion for n=10⁴) | **None** |
| Code clarity | Complex (list manipulation) | Elegant but non-obvious | **Clean, standard** |
| Interview value | Baseline only | Shows alternative thinking | **Expected answer** |

---

## Stack vs Recursive (Head-to-Head)

| Metric | Explicit Stack | Recursive |
|--------|---------------|-----------|
| Time | O(n) | O(n) |
| Space | O(n) heap | O(n) call stack |
| Stack overflow risk? | **No** (heap-allocated) | Yes (JVM call stack limit ~10⁴) |
| Code length | ~20 lines | ~12 lines |
| Intuitiveness | **Directly models the algorithm** | Requires right-to-left thinking |
| Debugging | Easy (inspect stack contents) | Harder (recursive calls) |
| When preferred | **Always for this problem** | Academic interest |

**Verdict:** The explicit stack is the **standard, expected solution**. It's iterative (no overflow risk), intuitive (left-to-right, matching how we read the expression), and easy to debug.

---

## Why Stack is the "Natural" Data Structure for RPN

```
Postfix: 2  1  +  3  *
         ─  ─  ─  ─  ─
         ↓  ↓  ↓  ↓  ↓
         push push OP push OP

The operator ALWAYS applies to the two MOST RECENT unresolved values.
"Most recent" = top of stack = LIFO.

Infix would need: precedence rules, parentheses tracking, shunting-yard algorithm.
Postfix + stack: zero ambiguity, zero precedence logic.
```

---

## 🏁 Final Master Comparison Table

| Approach | Time | Space | Direction | Practical? | Key Insight |
|----------|------|-------|-----------|------------|-------------|
| Repeated Reduction | O(n²) | O(n) | L→R (scan) | ❌ Slow | Find first `num num op`, replace |
| Recursive | O(n) | O(n) call stack | R→L | ⚠️ Overflow risk | Operator recursively evaluates its operands |
| **Stack (single pass)** | **O(n)** | **O(n)** | **L→R** | **✅ Optimal** | **Push numbers; pop-compute-push for operators** |

---

### 🎯 What to Present to the Interviewer

1. **Explain RPN:** "In postfix notation, every operator follows its operands. This eliminates the need for precedence rules or parentheses."
2. **State the stack algorithm:**
   - "Read left to right. Push numbers. When we hit an operator, pop two operands, compute, push the result."
   - "At the end, the stack has exactly one element — the answer."
3. **Emphasize operand order:** "For subtraction and division, we pop `b` first (top), then `a`. Compute `a - b` and `a / b`."
4. **Walk through** `["2","1","+","3","*"]`:
   - Push 2, push 1. See `+`: pop 1, pop 2, push 3.
   - Push 3. See `*`: pop 3, pop 3, push 9.
   - Return 9.
5. **Mention division truncation:** "Java's integer division already truncates toward zero: `6 / -132 = 0`, `13 / 5 = 2`."
6. **Handle negative numbers:** "`Integer.parseInt(\"-3\")` correctly parses negative number strings. The switch on `\"-\"` only matches the single-character operator."
7. **State complexity:** O(n) time (each token processed once), O(n) space (stack holds at most ~n/2 operands).
8. **If asked about alternatives:** Mention the recursive right-to-left approach (elegant but risks stack overflow) and the repeated-reduction approach (O(n²), impractical).

**One‑sentence summary:**  
*Use a stack to evaluate the postfix expression in a single left-to-right pass: push numbers, and for each operator pop the top two operands (right then left), apply the operation, and push the result back — achieving O(n) time and O(n) space with the stack's LIFO property perfectly matching postfix semantics.*