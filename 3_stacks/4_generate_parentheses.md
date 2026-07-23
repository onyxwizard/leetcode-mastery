### 📘 Chapter: Stack  
### 📌 Problem 4: Generate Parentheses (LeetCode 22)

---

**Input**  
- `n`: an integer representing the number of pairs of parentheses.

**Output**  
- A list of all **well‑formed parentheses strings** that can be formed with exactly `n` pairs.

**Constraints**  
- `1 <= n <= 8`

**Example**  
```
Input:  n = 3
Output: ["((()))", "(()())", "(())()", "()(())", "()()()"]

Input:  n = 1
Output: ["()"]
```

---

### 🧠 Core Idea

The problem asks for **all** valid combinations of `n` pairs of parentheses.

- **Brute force:** Generate **all** `2^(2n)` possible strings of `'('` and `')'`, then validate each one. Most are invalid — enormous waste.
- **Optimal (Pruning):** Build strings character by character, applying two rules:
  - Add `'('` only if `open < n`.
  - Add `')'` only if `close < open`.
  
  This generates **only** valid strings (Catalan number ≈ `4^n / n^(3/2)`). Zero waste.

We explore this through **Iterative** (BFS & DFS) and **Recursive Backtracking** approaches.

---

---

# 🔄 SECTION 1: ITERATIVE APPROACHES

---

## 1A. Brute Force BFS (Generate All → Validate)

**Idea:** Use a Queue. At every level, append **both** `'('` and `')'` to every string — **no pruning**. When a string hits length `2n`, validate it with a balance counter.

**Time:** O(2^(2n) × n)  
**Space:** O(2^(2n)) — queue holds up to half of all strings at the widest level.

```java
import java.util.*;

public class Solution {

    public List<String> generateParenthesis(int n) {
        List<String> result = new ArrayList<>();
        Queue<String> queue = new LinkedList<>();
        queue.add("");

        while (!queue.isEmpty()) {
            String current = queue.poll();

            if (current.length() == 2 * n) {
                if (isValid(current)) {
                    result.add(current);
                }
                continue;
            }

            // NO PRUNING: blindly append both
            queue.add(current + "(");
            queue.add(current + ")");
        }

        return result;
    }

    private boolean isValid(String s) {
        int balance = 0;
        for (char c : s.toCharArray()) {
            if (c == '(') balance++;
            else balance--;
            if (balance < 0) return false;
        }
        return balance == 0;
    }
}
```

### 🔍 Sample Iteration (n = 2, target length = 4)

| Step | Queue (front → back) | Polled | Action |
|------|----------------------|--------|--------|
| 0 | `[""]` | `""` | len=0≠4. Add `"("`, `")"` |
| 1 | `["(", ")"]` | `"("` | len=1≠4. Add `"(("`, `"()"` |
| 2 | `[")", "((", "()"]` | `")"` | len=1≠4. Add `")("`, `"))"` |
| 3 | `["((", "()", ")(", "))"]` | `"(("` | len=2≠4. Add `"((("`, `"(()"` |
| 4 | `["()", ")(", "))", "(((", "(()"]` | `"()"` | len=2≠4. Add `"()("`, `"())"` |
| 5 | `[")(", "))", "(((", "(()", "()(", "())"]` | `")("` | len=2≠4. Add `")(("`, `")()"` |
| 6 | `["))", "(((", "(()", "()(", "())", ")((", ")()"]` | `"))"` | len=2≠4. Add `"))("`, `")))"` |
| 7–14 | *(8 strings of length 3)* | each | len=3≠4. Each spawns 2 children → 16 strings of length 4 |
| 15–30 | *(16 strings of length 4)* | each | len=4. **Validate each.** |

**Validation of all 16 candidates:**

| String | Balance Trace | Valid? |
|--------|--------------|--------|
| `(((("` | 1→2→3→4 (ends≠0) | ❌ |
| `((()"` | 1→2→3→2 (ends≠0) | ❌ |
| `(()("` | 1→2→1→2 (ends≠0) | ❌ |
| **`(())"`** | **1→2→1→0 (never <0, ends=0)** | **✅** |
| `()(("` | 1→0→1→2 (ends≠0) | ❌ |
| **`()()"`** | **1→0→1→0 (never <0, ends=0)** | **✅** |
| `())("` | 1→0→**-1** | ❌ |
| `()))"` | 1→0→**-1** | ❌ |
| `)((("` | **-1** | ❌ |
| `)(()"` | **-1** | ❌ |
| `)()("` | **-1** | ❌ |
| `)())"` | **-1** | ❌ |
| `))(("` | **-1** | ❌ |
| `))()"` | **-1** | ❌ |
| `)))(`| **-1** | ❌ |
| `))))"` | **-1** | ❌ |

**Result:** `["(())", "()()"]` — only **2 out of 16** valid. **87.5% wasted.**

---

## 1B. Optimized BFS with Pruning (Queue-Based)

**Idea:** Same Queue-based BFS, but each state carries `(string, openCount, closeCount)`. Apply pruning rules so **only valid prefixes** are ever enqueued. No validation needed at the end.

**Time:** O(4^n / n^(3/2)) — Catalan number  
**Space:** O(4^n / n^(3/2)) — queue width at the widest level

```java
import java.util.*;

public class Solution {

    private static class State {
        String str;
        int open;
        int close;

        State(String str, int open, int close) {
            this.str = str;
            this.open = open;
            this.close = close;
        }
    }

    public List<String> generateParenthesis(int n) {
        List<String> result = new ArrayList<>();
        Queue<State> queue = new LinkedList<>();
        queue.add(new State("", 0, 0));

        while (!queue.isEmpty()) {
            State current = queue.poll();

            if (current.str.length() == 2 * n) {
                result.add(current.str);  // guaranteed valid
                continue;
            }

            // Rule 1: add '(' only if open < n
            if (current.open < n) {
                queue.add(new State(current.str + "(", current.open + 1, current.close));
            }

            // Rule 2: add ')' only if close < open
            if (current.close < current.open) {
                queue.add(new State(current.str + ")", current.open, current.close + 1));
            }
        }

        return result;
    }
}
```

### 🔍 Sample Iteration (n = 2, target length = 4)

| Step | Queue (front → back) | Polled | Action |
|------|----------------------|--------|--------|
| 0 | `["",0,0]` | `("",0,0)` | len=0≠4. open(0)<2→add `"("`. close(0)<open(0)? **No**. |
| 1 | `["(",1,0]` | `("(",1,0)` | len=1≠4. open(1)<2→add `"(("`. close(0)<open(1)→add `"()"`. |
| 2 | `["((",2,0], ["()",1,1]` | `("((",2,0)` | len=2≠4. open(2)<2? **No**. close(0)<open(2)→add `"(()"`. |
| 3 | `["()",1,1], ["(()",2,1]` | `("()",1,1)` | len=2≠4. open(1)<2→add `"()("`. close(1)<open(1)? **No**. |
| 4 | `["(()",2,1], ["()(",2,1]` | `("(()",2,1)` | len=3≠4. open(2)<2? **No**. close(1)<open(2)→add `"(())"`. |
| 5 | `["()(",2,1], ["(())",2,2]` | `("()(",2,1)` | len=3≠4. open(2)<2? **No**. close(1)<open(2)→add `"()()"`. |
| 6 | `["(())",2,2], ["()()",2,2]` | `("(())",2,2)` | len=4 ✅ | result=`["(())"]` |
| 7 | `["()()",2,2]` | `("()()",2,2)` | len=4 ✅ | result=`["(())","()()"]` |
| 8 | `[]` | — | Queue empty. Done. | **Return `["(())","()()"]`** |

> 📌 Only **6 states** ever entered the queue (vs 30 in brute force). Zero invalid strings generated.

---

## 1C. Brute Force DFS (Generate All → Validate)

**Idea:** Use an explicit **Stack**. At every step, push **both** `'('` and `')'` — **no pruning**. When a string hits length `2n`, validate it.

**Time:** O(2^(2n) × n)  
**Space:** O(2^(2n)) — stack can grow large (though typically less than BFS peak).

```java
import java.util.*;

public class Solution {

    public List<String> generateParenthesis(int n) {
        List<String> result = new ArrayList<>();
        Deque<String> stack = new ArrayDeque<>();
        stack.push("");

        while (!stack.isEmpty()) {
            String current = stack.pop();

            if (current.length() == 2 * n) {
                if (isValid(current)) {
                    result.add(current);
                }
                continue;
            }

            // NO PRUNING: push both (push ')' first so '(' is processed first)
            stack.push(current + ")");
            stack.push(current + "(");
        }

        return result;
    }

    private boolean isValid(String s) {
        int balance = 0;
        for (char c : s.toCharArray()) {
            if (c == '(') balance++;
            else balance--;
            if (balance < 0) return false;
        }
        return balance == 0;
    }
}
```

### 🔍 Sample Iteration (n = 2, target length = 4)

| Step | Stack (top → bottom) | Popped | Action |
|------|----------------------|--------|--------|
| 0 | `[""]` | `""` | len=0≠4. Push `")"`, then `"("`. |
| 1 | `["(", ")"]` | `"("` | len=1≠4. Push `"()"`, then `"(("`. |
| 2 | `["((", "()", ")"]` | `"(("` | len=2≠4. Push `"(()"`, then `"((("`. |
| 3 | `["(((", "(()", "()", ")"]` | `"((("` | len=3≠4. Push `"((()"`, then `"(((("`. |
| 4 | `["((((", "((()", "(()", "()", ")"]` | `"(((("` | len=4. Validate: 1→2→3→4 ≠ 0. ❌ |
| 5 | `["((()", "(()", "()", ")"]` | `"((()"` | len=4. Validate: 1→2→3→2 ≠ 0. ❌ |
| 6 | `["(()", "()", ")"]` | `"(()"` | len=3≠4. Push `"(()("`, then `"(())"`. |
| 7 | `["(())", "(()(", "()", ")"]` | `"(())"` | len=4. Validate: 1→2→1→0. ✅ | result=`["(())"]` |
| 8 | `["(()(", "()", ")"]` | `"(()("` | len=4. Validate: 1→2→1→2 ≠ 0. ❌ |
| 9 | `["()", ")"]` | `"()"` | len=2≠4. Push `"())"`, then `"()("`. |
| 10 | `["()(", "())", ")"]` | `"()("` | len=3≠4. Push `"()()"`, then `"()(("`. |
| 11 | `["()((", "()()", "())", ")"]` | `"()(("` | len=4. Validate: 1→0→1→2 ≠ 0. ❌ |
| 12 | `["()()", "())", ")"]` | `"()()"` | len=4. Validate: 1→0→1→0. ✅ | result=`["(())","()()"]` |
| 13 | `["())", ")"]` | `"())"` | len=3≠4. Push `"()))"`, then `"())("`. |
| 14 | `["())(", "()))", ")"]` | `"())("` | len=4. Validate: 1→0→-1. ❌ |
| 15 | `["()))", ")"]` | `"()))"` | len=4. Validate: 1→0→-1. ❌ |
| 16 | `[")"]` | `")"` | len=1≠4. Push `"))"`, then `")("`. |
| 17–22 | *(continues...)* | `")("`, `"))"`, etc. | All start with `)` → balance goes -1 immediately. All ❌. |
| Final | `[]` | — | Stack empty. | **Return `["(())","()()"]`** |

> ⚠️ **16 strings** of length 4 were generated and validated. Only 2 were valid. Same waste as brute force BFS, just different traversal order.

---

## 1D. Optimized DFS with Pruning (Stack-Based)

**Idea:** Same explicit Stack, but each state carries `(string, openCount, closeCount)`. Apply pruning rules. **No validation needed.** Push `')'` first, then `'('`, so `'('` is processed first (LIFO) — mimics recursive backtracking order.

**Time:** O(4^n / n^(3/2)) — Catalan number  
**Space:** O(n) — peak stack depth is at most ~2n entries.

```java
import java.util.*;

public class Solution {

    private static class State {
        String str;
        int open;
        int close;

        State(String str, int open, int close) {
            this.str = str;
            this.open = open;
            this.close = close;
        }
    }

    public List<String> generateParenthesis(int n) {
        List<String> result = new ArrayList<>();
        Deque<State> stack = new ArrayDeque<>();
        stack.push(new State("", 0, 0));

        while (!stack.isEmpty()) {
            State current = stack.pop();

            if (current.str.length() == 2 * n) {
                result.add(current.str);  // guaranteed valid
                continue;
            }

            // Push ')' FIRST so '(' is popped first (LIFO)
            if (current.close < current.open) {
                stack.push(new State(current.str + ")", current.open, current.close + 1));
            }

            // Push '(' SECOND (popped first)
            if (current.open < n) {
                stack.push(new State(current.str + "(", current.open + 1, current.close));
            }
        }

        return result;
    }
}
```

### 🔍 Sample Iteration (n = 2, target length = 4)

| Step | Stack (top → bottom) | Popped | Action |
|------|----------------------|--------|--------|
| 0 | `["",0,0]` | `("",0,0)` | len=0≠4. close(0)<open(0)? **No**. open(0)<2→push `"("`. |
| 1 | `["(",1,0]` | `("(",1,0)` | len=1≠4. close(0)<open(1)→push `"()"`. open(1)<2→push `"(("`. |
| 2 | `["((",2,0], ["()",1,1]` | `("((",2,0)` | len=2≠4. close(0)<open(2)→push `"(()"`. open(2)<2? **No**. |
| 3 | `["(()",2,1], ["()",1,1]` | `("(()",2,1)` | len=3≠4. close(1)<open(2)→push `"(())"`. open(2)<2? **No**. |
| 4 | `["(())",2,2], ["()",1,1]` | `("(())",2,2)` | len=4 ✅ | result=`["(())"]` |
| 5 | `["()",1,1]` | `("()",1,1)` | len=2≠4. close(1)<open(1)? **No**. open(1)<2→push `"()("`. |
| 6 | `["()(",2,1]` | `("()(",2,1)` | len=3≠4. close(1)<open(2)→push `"()()"`. open(2)<2? **No**. |
| 7 | `["()()",2,2]` | `("()()",2,2)` | len=4 ✅ | result=`["(())","()()"]` |
| 8 | `[]` | — | Stack empty. Done. | **Return `["(())","()()"]`** |

> 📌 Only **6 states** ever touched the stack. Same efficiency as optimized BFS, but **peak stack size never exceeded 2** (vs BFS queue holding 2–3 at widest). Traversal order matches recursive backtracking exactly.

---

---

# 🔁 SECTION 2: RECURSIVE / BACKTRACKING APPROACHES

---

## 2A. Brute Force Recursive (Generate All → Validate)

**Idea:** Recursively build every possible string of length `2n` by choosing `'('` or `')'` at each position. At the leaf, validate with a balance counter.

**Time:** O(2^(2n) × n)  
**Space:** O(n) recursion depth + O(2^(2n)) output filtering.

```java
import java.util.*;

public class Solution {

    public List<String> generateParenthesis(int n) {
        List<String> result = new ArrayList<>();
        generateAll(new char[2 * n], 0, result);
        return result;
    }

    private void generateAll(char[] current, int pos, List<String> result) {
        if (pos == current.length) {
            if (isValid(current)) {
                result.add(new String(current));
            }
            return;
        }
        current[pos] = '(';
        generateAll(current, pos + 1, result);
        current[pos] = ')';
        generateAll(current, pos + 1, result);
    }

    private boolean isValid(char[] current) {
        int balance = 0;
        for (char c : current) {
            if (c == '(') balance++;
            else balance--;
            if (balance < 0) return false;
        }
        return balance == 0;
    }
}
```

### 🔍 Sample Recursion Tree (n = 2, target length = 4)

```
generateAll(pos=0)
├─ current[0]='(' → generateAll(pos=1)
│  ├─ current[1]='(' → generateAll(pos=2)
│  │  ├─ current[2]='(' → generateAll(pos=3)
│  │  │  ├─ current[3]='(' → "((((" → validate: 1,2,3,4 → ❌
│  │  │  └─ current[3]=')' → "((()" → validate: 1,2,3,2 → ❌
│  │  └─ current[2]=')' → generateAll(pos=3)
│  │     ├─ current[3]='(' → "(()(" → validate: 1,2,1,2 → ❌
│  │     └─ current[3]=')' → "(())" → validate: 1,2,1,0 → ✅ ADD
│  └─ current[1]=')' → generateAll(pos=2)
│     ├─ current[2]='(' → generateAll(pos=3)
│     │  ├─ current[3]='(' → "()((" → validate: 1,0,1,2 → ❌
│     │  └─ current[3]=')' → "()()" → validate: 1,0,1,0 → ✅ ADD
│     └─ current[2]=')' → generateAll(pos=3)
│        ├─ current[3]='(' → "())(" → validate: 1,0,-1 → ❌
│        └─ current[3]=')' → "()))" → validate: 1,0,-1 → ❌
└─ current[0]=')' → generateAll(pos=1)
   ├─ ... (all 8 strings starting with ')') → ALL ❌ (balance goes -1 immediately)
   └─ ...

Total leaves explored: 16
Valid: 2
Result: ["(())", "()()"]
```

> ⚠️ All 16 leaves visited. 14 were invalid. Same waste as iterative brute force.

---

## 2B. Optimized Backtracking (Pruned Recursive DFS)

**Idea:** Recursively build the string, but **prune** at every step:
- Add `'('` only if `open < n`.
- Add `')'` only if `close < open`.

When length = `2n`, the string is **guaranteed valid**. Use `StringBuilder` for O(1) append/delete.

**Time:** O(4^n / n^(3/2)) — Catalan number (optimal)  
**Space:** O(n) recursion depth.

```java
import java.util.*;

public class Solution {

    public List<String> generateParenthesis(int n) {
        List<String> result = new ArrayList<>();
        backtrack(result, new StringBuilder(), 0, 0, n);
        return result;
    }

    private void backtrack(List<String> result, StringBuilder sb, int open, int close, int max) {
        // Base case: all 2n characters placed
        if (sb.length() == max * 2) {
            result.add(sb.toString());
            return;
        }

        // Choice 1: Add '(' if we still have opening brackets available
        if (open < max) {
            sb.append('(');
            backtrack(result, sb, open + 1, close, max);
            sb.deleteCharAt(sb.length() - 1);  // UNDO (backtrack)
        }

        // Choice 2: Add ')' only if it won't exceed the number of '('
        if (close < open) {
            sb.append(')');
            backtrack(result, sb, open, close + 1, max);
            sb.deleteCharAt(sb.length() - 1);  // UNDO (backtrack)
        }
    }
}
```

### 🔍 Sample Recursion Tree (n = 2, target length = 4)

```
backtrack(sb="", open=0, close=0)
│
├─ open(0)<2 → append '(' → sb="("
│  backtrack(sb="(", open=1, close=0)
│  │
│  ├─ open(1)<2 → append '(' → sb="(("
│  │  backtrack(sb="((", open=2, close=0)
│  │  │
│  │  ├─ open(2)<2? NO ← pruned!
│  │  └─ close(0)<open(2) → append ')' → sb="(()"
│  │     backtrack(sb="(()", open=2, close=1)
│  │     │
│  │     ├─ open(2)<2? NO ← pruned!
│  │     └─ close(1)<open(2) → append ')' → sb="(())"
│  │        backtrack(sb="(())", open=2, close=2)
│  │        │
│  │        └─ len==4 ✅ → result.add("(())")
│  │           ← deleteCharAt → sb="(()"
│  │        ← deleteCharAt → sb="(("
│  │     ← deleteCharAt → sb="("
│  │
│  └─ close(0)<open(1) → append ')' → sb="()"
│     backtrack(sb="()", open=1, close=1)
│     │
│     ├─ open(1)<2 → append '(' → sb="()("
│     │  backtrack(sb="()(", open=2, close=1)
│     │  │
│     │  ├─ open(2)<2? NO ← pruned!
│     │  └─ close(1)<open(2) → append ')' → sb="()()"
│     │     backtrack(sb="()()", open=2, close=2)
│     │     │
│     │     └─ len==4 ✅ → result.add("()()")
│     │        ← deleteCharAt → sb="()("
│     │     ← deleteCharAt → sb="()"
│     │
│     └─ close(1)<open(1)? NO ← pruned!
│        ← deleteCharAt → sb="("
│  ← deleteCharAt → sb=""
│
└─ close(0)<open(0)? NO ← pruned! (never even tries starting with ')')

Final result: ["(())", "()()"]
```

> 📌 Only **6 recursive calls** made (vs 16 leaves in brute force). The `← deleteCharAt` is the **backtrack** step — restoring `StringBuilder` for the next branch. This is what keeps space at O(n).

---

---

# 📊 SECTION 3: TRADE-OFFS & COMPARISONS

---

## Iterative BFS vs Iterative DFS (Both Optimized)

| Metric | Optimized BFS (Queue) | Optimized DFS (Stack) |
|--------|----------------------|----------------------|
| Traversal order | Level-by-level (breadth) | Deep-first (mimics recursion) |
| Peak memory | O(4^n / n^(3/2)) — wide queue at middle levels | O(n) — narrow stack |
| For n=8, peak states | ~1,430 in queue simultaneously | ~16 on stack simultaneously |
| String creation | New String at every enqueue | New String at every push |
| Result order | Grouped by length (all same-length together) | Same as recursive backtracking |
| Use case | When you need level-order generation | When memory is constrained |

**Verdict:** DFS (Stack) wins on memory. BFS wins if you need results grouped by string length.

---

## Brute Force vs Optimized (Within Each Category)

| Metric | Brute Force (BFS/DFS/Recursive) | Optimized (BFS/DFS/Backtracking) |
|--------|-------------------------------|----------------------------------|
| Strings generated | 2^(2n) = 4^n | Catalan(n) ≈ 4^n / n^(3/2) |
| For n=8 | 65,536 strings | 1,430 strings |
| Wasted work | ~97.8% invalid strings generated & validated | 0% — every string generated is valid |
| Validation needed? | Yes (O(n) per string) | No — pruning guarantees validity |
| Time complexity | O(4^n × n) | O(4^n / n^(3/2)) |

**Verdict:** Optimized is strictly better. Brute force is only a conceptual stepping stone.

---

## Iterative vs Recursive Backtracking (Both Optimized)

| Metric | Iterative DFS (Stack) | Recursive Backtracking |
|--------|----------------------|----------------------|
| Code clarity | Requires explicit `State` class | Clean, minimal code |
| Memory per state | New `String` object per push (garbage) | `StringBuilder` with O(1) append/delete |
| Peak space | O(n) stack entries × O(n) string each = O(n²) | O(n) recursion × O(1) StringBuilder = O(n) |
| Risk of StackOverflow | None (heap-allocated stack) | Yes for very large n (call stack limit) |
| Interview preference | Shows you understand the mechanics | **Standard expected answer** |
| Traversal order | Identical (if push order is correct) | Identical |

**Verdict:** Recursive backtracking is the **gold standard** for interviews — cleanest code, least memory. Iterative DFS is the answer when the interviewer says *"no recursion allowed"*.

---

## 🏁 Final Master Comparison Table

| Approach | Time | Space (peak) | Strings Generated | Validation? |
|----------|------|--------------|-------------------|-------------|
| Brute Force BFS | O(4^n × n) | O(4^n) | 4^n (all) | Yes |
| Brute Force DFS | O(4^n × n) | O(4^n) | 4^n (all) | Yes |
| Brute Force Recursive | O(4^n × n) | O(n) | 4^n (all) | Yes |
| **Optimized BFS** | **O(4^n / n^(3/2))** | **O(4^n / n^(3/2))** | **Catalan(n) only** | **No** |
| **Optimized DFS (Stack)** | **O(4^n / n^(3/2))** | **O(n)** | **Catalan(n) only** | **No** |
| **Backtracking (Recursive)** | **O(4^n / n^(3/2))** | **O(n)** | **Catalan(n) only** | **No** |

---

### 🎯 What to Present to the Interviewer

1. **Recognise** this is a combinatorics generation problem; output size = Catalan number → can't beat exponential.
2. **Sketch brute force** (generate all 4^n strings, validate each) to establish the baseline.
3. **Propose pruning rules:** add `'('` if `open < n`; add `')'` if `close < open`. This eliminates all invalid strings at birth.
4. **Write the recursive backtracking** solution with `StringBuilder` — cleanest and most expected.
5. **If asked for iterative:** present Stack-based DFS with explicit `State` objects. Mention BFS as alternative but note higher peak memory.
6. **Walk through** the recursion tree / stack trace for `n=2` to show only 6 states are visited.
7. **Analyse:** Time = O(Catalan) ≈ O(4^n / n^(3/2)), Space = O(n).
8. **If asked further:** mention DP / Closure Number (`"(" + left + ")" + right`) as an alternative view.

**One‑sentence summary:**  
*Use backtracking (or its iterative Stack equivalent) to build valid strings character by character, only adding `'('` if opens < n and `')'` if closes < opens, generating all well‑formed parentheses in O(Catalan) time with O(n) space — zero invalid strings ever created.*