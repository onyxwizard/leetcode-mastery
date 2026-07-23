### 📘 Chapter: Stack  
### 📌 Problem 8: Asteroid Collision (LeetCode 735)

---

**Input**  
- `asteroids`: an integer array representing asteroids in a row.  
  - **Absolute value** = size of the asteroid.  
  - **Sign** = direction: positive → moving **right** (→), negative → moving **left** (←).  
  - All asteroids move at the **same speed**.

**Output**  
- The state of asteroids after **all collisions** are resolved.  
  - Two asteroids collide only if the left one moves right (+) and the right one moves left (−).  
  - The **smaller** one explodes.  
  - If **equal size**, both explode.  
  - Same-direction asteroids never meet.

**Constraints**  
- `2 <= asteroids.length <= 10⁴`  
- `-1000 <= asteroids[i] <= 1000`, `asteroids[i] != 0`

**Example**  
```
Input:  asteroids = [5, 10, -5]
Output: [5, 10]
Explanation: 10 and -5 collide → 10 survives (10 > 5). 5 and 10 never collide (both right).

Input:  asteroids = [8, -8]
Output: []
Explanation: 8 and -8 collide → equal size → both explode.

Input:  asteroids = [10, 2, -5]
Output: [10]
Explanation: 2 and -5 collide → -5 wins (5 > 2). Then 10 and -5 collide → 10 wins (10 > 5).

Input:  asteroids = [-2, -1, 1, 2]
Output: [-2, -1, 1, 2]
Explanation: No collisions possible (left-moving are on the left, right-moving on the right).
```

**Follow-up**  
- Achieve O(n) time and O(n) space. (Standard expectation.)

---

### 🧠 Core Idea

Collisions **only** happen when a right-moving asteroid (+) is immediately to the **left** of a left-moving asteroid (−):

```
Collision possible:    →  ←     (positive followed by negative)
No collision:          →  →     (both right)
No collision:          ←  ←     (both left)
No collision:          ←  →     (moving apart)
```

**Why a stack?**  
When a left-moving asteroid appears, it collides with the **nearest surviving right-moving asteroid** to its left — which is the **top of the stack** (LIFO). The stack naturally maintains the chain of surviving asteroids in order.

**Processing rules for a left-moving asteroid (`ast < 0`):**
1. While stack top is positive AND smaller than `|ast|` → pop (top explodes).
2. After the while loop:
   - Stack empty or top is negative → push `ast` (survives, no more collisions).
   - Top is positive AND equal to `|ast|` → pop (both explode), don't push.
   - Top is positive AND larger than `|ast|` → do nothing (`ast` explodes).

**Right-moving asteroids (`ast > 0`):** Always push (no immediate collision; may collide with a future left-moving asteroid).

---

---

# 🔨 SECTION 1: BRUTE FORCE APPROACH

---

## 1A. Repeated Pairwise Scan (O(n²) Time)

**Idea:** Use a mutable list. Repeatedly scan left-to-right for adjacent pairs where `left > 0` and `right < 0` (collision). Apply collision rules, remove destroyed asteroid(s). Repeat until no collisions remain.

**Time:** O(n²) — up to n passes, each scanning O(n) elements.  
**Space:** O(n) — mutable list.

```java
import java.util.*;

public int[] asteroidCollision(int[] asteroids) {
    List<Integer> list = new ArrayList<>();
    for (int a : asteroids) list.add(a);

    boolean changed = true;
    while (changed) {
        changed = false;
        for (int i = 0; i < list.size() - 1; ) {
            int left = list.get(i);
            int right = list.get(i + 1);

            if (left > 0 && right < 0) {  // collision!
                changed = true;
                if (Math.abs(left) > Math.abs(right)) {
                    list.remove(i + 1);  // right explodes
                } else if (Math.abs(left) < Math.abs(right)) {
                    list.remove(i);      // left explodes
                } else {
                    list.remove(i);      // both explode
                    list.remove(i);      // (after removing i, the old i+1 is now at i)
                }
                // don't increment i — recheck this position
            } else {
                i++;
            }
        }
    }

    return list.stream().mapToInt(Integer::intValue).toArray();
}
```

### 🔍 Sample Iteration

**Input:** `asteroids = [10, 2, -5]`

| Pass | List state | i | left, right | Collision? | Result | List after |
|------|-----------|---|-------------|------------|--------|-----------|
| 1 | `[10, 2, -5]` | 0 | 10, 2 | 10>0, 2>0 → No | i++ | — |
| 1 | `[10, 2, -5]` | 1 | 2, -5 | 2>0, -5<0 → **Yes!** | |2|<|-5| → left(2) explodes | `[10, -5]` |
| 2 | `[10, -5]` | 0 | 10, -5 | 10>0, -5<0 → **Yes!** | |10|>|-5| → right(-5) explodes | `[10]` |
| 3 | `[10]` | — | size=1 → no pairs | — | **STOP** | `[10]` |

**Result:** `[10]` ✅

> ⚠️ **3 passes** for n=3. For n=10⁴ with cascading collisions (e.g., `[1, 2, 3, ..., 5000, -10000]`), the large negative asteroid destroys all positives one by one, requiring ~5000 passes → O(n²).

---

---

# ⚡ SECTION 2: OPTIMIZED APPROACH

---

## 2A. Stack-Based Simulation (O(n) Time, O(n) Space) ✅

**Idea:**  
- Use a `Deque<Integer>` as a stack representing surviving asteroids (bottom = leftmost).  
- For each asteroid:  
  - **Positive (→):** Push immediately (no collision with what's below).  
  - **Negative (←):** Resolve collisions with the stack top:  
    - While top is positive and smaller → pop (top explodes).  
    - Then check: equal → pop (both explode); larger top → current explodes; empty/negative top → push current.  
- Convert stack to array (bottom-to-top order).

**Time:** O(n) — each asteroid pushed at most once, popped at most once.  
**Space:** O(n) — stack holds up to n elements.

```java
import java.util.*;

public int[] asteroidCollision(int[] asteroids) {
    Deque<Integer> stack = new ArrayDeque<>();

    for (int ast : asteroids) {
        if (ast > 0) {
            // Right-moving: always push (no immediate collision)
            stack.push(ast);
        } else {
            // Left-moving: resolve collisions with right-moving asteroids on the stack
            while (!stack.isEmpty() && stack.peek() > 0 && stack.peek() < -ast) {
                stack.pop();  // smaller right-moving asteroid explodes
            }

            if (stack.isEmpty() || stack.peek() < 0) {
                // No more right-moving asteroids to collide with → survives
                stack.push(ast);
            } else if (stack.peek() == -ast) {
                // Equal size → both explode
                stack.pop();
                // don't push current
            }
            // else: stack.peek() > -ast → current asteroid explodes (do nothing)
        }
    }

    // Build result array (bottom to top of stack = left to right)
    int[] result = new int[stack.size()];
    for (int i = result.length - 1; i >= 0; i--) {
        result[i] = stack.pop();
    }
    return result;
}
```

### 🔍 Sample Iteration 1

**Input:** `asteroids = [5, 10, -5]`

| Step | ast | Direction | Stack BEFORE (top→bottom) | Action | Stack AFTER |
|------|-----|-----------|---------------------------|--------|-------------|
| 1 | 5 | → (right) | `[]` | Push 5 | `[5]` |
| 2 | 10 | → (right) | `[5]` | Push 10 | `[10, 5]` |
| 3 | -5 | ← (left) | `[10, 5]` | Top=10 > 0. 10 < |-5|=5? **No** (10 > 5). Top > |ast| → current explodes. Do nothing. | `[10, 5]` |
| END | — | — | `[10, 5]` | Build result bottom→top | **`[5, 10]`** ✅ |

---

### 🔍 Visual Stack Trace 1

```
asteroids = [5, 10, -5]

Step 1: ast=5 (→)
  ┌────┐
  │ 5→ │
  └────┘

Step 2: ast=10 (→)
  ┌─────┐
  │ 10→ │ ← top
  ├─────┤
  │  5→ │
  └─────┘

Step 3: ast=-5 (←)
  Collides with top (10→). |10| > |-5| → -5 explodes!
  ┌─────┐
  │ 10→ │ ← top (survives)
  ├─────┤
  │  5→ │
  └─────┘

Result (bottom to top): [5, 10] ✅
```

---

### 🔍 Sample Iteration 2 (Both Explode)

**Input:** `asteroids = [8, -8]`

| Step | ast | Stack BEFORE | Action | Stack AFTER |
|------|-----|--------------|--------|-------------|
| 1 | 8 | `[]` | Push 8 | `[8]` |
| 2 | -8 | `[8]` | Top=8 > 0. 8 < 8? No. 8 == |-8|=8? **Yes** → pop (both explode). Don't push. | `[]` |
| END | — | `[]` | — | **`[]`** ✅ |

---

### 🔍 Sample Iteration 3 (Cascading Destruction)

**Input:** `asteroids = [10, 2, -5]`

| Step | ast | Stack BEFORE | Action | Stack AFTER |
|------|-----|--------------|--------|-------------|
| 1 | 10 | `[]` | Push 10 | `[10]` |
| 2 | 2 | `[10]` | Push 2 | `[2, 10]` |
| 3 | -5 | `[2, 10]` | Top=2 > 0. 2 < 5? **Yes** → pop 2 (explodes). Stack: `[10]`. Top=10 > 0. 10 < 5? **No**. 10 == 5? **No**. 10 > 5 → current (-5) explodes. | `[10]` |
| END | — | `[10]` | — | **`[10]`** ✅ |

---

### 🔍 Visual Stack Trace 3

```
asteroids = [10, 2, -5]

Step 1: ast=10 (→)
  ┌─────┐
  │ 10→ │
  └─────┘

Step 2: ast=2 (→)
  ┌────┐
  │ 2→ │ ← top
  ├────┤
  │10→ │
  └────┘

Step 3: ast=-5 (←)
  ┌────┐
  │ 2→ │ ← top. |2| < |-5| → 2 EXPLODES! Pop.
  ├────┤
  │10→ │
  └────┘
  
  Now top=10. |10| > |-5| → -5 EXPLODES! Don't push.
  
  ┌─────┐
  │ 10→ │ ← survives
  └─────┘

Result: [10] ✅
```

---

### 🔍 Sample Iteration 4 (No Collisions)

**Input:** `asteroids = [-2, -1, 1, 2]`

| Step | ast | Direction | Stack BEFORE | Action | Stack AFTER |
|------|-----|-----------|--------------|--------|-------------|
| 1 | -2 | ← | `[]` | Stack empty → push -2 | `[-2]` |
| 2 | -1 | ← | `[-2]` | Top=-2 < 0 → push -1 (both left, no collision) | `[-1, -2]` |
| 3 | 1 | → | `[-1, -2]` | Positive → push 1 | `[1, -1, -2]` |
| 4 | 2 | → | `[1, -1, -2]` | Positive → push 2 | `[2, 1, -1, -2]` |
| END | — | — | `[2, 1, -1, -2]` | Build result | **`[-2, -1, 1, 2]`** ✅ |

> 📌 No collisions because left-moving asteroids are on the LEFT and right-moving on the RIGHT — they're moving **apart**.

---

### 🔍 Sample Iteration 5 (Complex Cascading)

**Input:** `asteroids = [1, -2, -2, -2]`

| Step | ast | Stack BEFORE | Action | Stack AFTER |
|------|-----|--------------|--------|-------------|
| 1 | 1 | `[]` | Push 1 | `[1]` |
| 2 | -2 | `[1]` | Top=1 > 0. 1 < 2? **Yes** → pop 1. Stack empty → push -2. | `[-2]` |
| 3 | -2 | `[-2]` | Top=-2 < 0 → push -2 (both left) | `[-2, -2]` |
| 4 | -2 | `[-2, -2]` | Top=-2 < 0 → push -2 | `[-2, -2, -2]` |
| END | — | `[-2, -2, -2]` | — | **`[-2, -2, -2]`** ✅ |

---

### 🔍 Sample Iteration 6 (Multiple Collisions)

**Input:** `asteroids = [3, 5, -6, 2, -1]`

| Step | ast | Stack BEFORE | Action | Stack AFTER |
|------|-----|--------------|--------|-------------|
| 1 | 3 | `[]` | Push 3 | `[3]` |
| 2 | 5 | `[3]` | Push 5 | `[5, 3]` |
| 3 | -6 | `[5, 3]` | Top=5>0, 5<6 → pop 5. Top=3>0, 3<6 → pop 3. Stack empty → push -6. | `[-6]` |
| 4 | 2 | `[-6]` | Positive → push 2 | `[2, -6]` |
| 5 | -1 | `[2, -6]` | Top=2>0, 2<1? **No**. 2==1? **No**. 2>1 → -1 explodes. | `[2, -6]` |
| END | — | `[2, -6]` | Build result | **`[-6, 2]`** ✅ |

**Verification:**
```
[3, 5, -6, 2, -1]
 3→ 5→ ←6  2→ ←1

Step: 5→ collides ←6: |5|<|6| → 5 explodes. [3, -6, 2, -1]
Step: 3→ collides ←6: |3|<|6| → 3 explodes. [-6, 2, -1]
Step: 2→ collides ←1: |2|>|1| → -1 explodes. [-6, 2]
No more collisions. Result: [-6, 2] ✅
```

---

### 🔍 Decision Flowchart for Left-Moving Asteroid

```
ast < 0 (moving left ←)
│
├─ WHILE stack not empty AND top > 0 AND top < |ast|:
│     POP (top explodes — it's smaller)
│
├─ AFTER the while loop:
│   │
│   ├─ Stack empty OR top < 0?
│   │     → PUSH ast (no more right-moving asteroids to fight)
│   │
│   ├─ top == |ast|?
│   │     → POP top (both explode). DON'T push ast.
│   │
│   └─ top > |ast|?
│         → Do NOTHING (ast explodes against the bigger asteroid)
│
└─ (ast > 0 case: just PUSH, no collision possible right now)
```

---

### 🔍 Why Each Asteroid is Pushed/Popped At Most Once

```
Total operations:
  - Each asteroid is PUSHED onto the stack at most once → n pushes total.
  - Each asteroid is POPPED from the stack at most once → n pops total.
  - Total: 2n operations → O(n).

Even though there's a while loop inside the for loop, the while loop's total
iterations across ALL asteroids is bounded by n (total pops ≤ total pushes ≤ n).

This is the classic AMORTIZED O(n) argument for stack-based algorithms.
```

---

### 🔍 When Collisions CAN and CANNOT Happen

```
CAN collide (→ ←):     [5, -3]     5 moves right, -3 moves left → they approach
CANNOT collide (→ →):  [5, 3]      both move right → same direction, never meet
CANNOT collide (← ←):  [-5, -3]    both move left → same direction, never meet
CANNOT collide (← →):  [-5, 3]     -5 moves left, 3 moves right → moving APART

Key: collision ONLY when positive is to the LEFT of negative.
In stack terms: top is positive (+) and new asteroid is negative (-).
```

---

---

# 📊 SECTION 3: TRADE-OFFS & COMPARISONS

---

## Brute Force vs Stack

| Metric | Repeated Pairwise Scan | Stack (Single Pass) |
|--------|----------------------|---------------------|
| Time | O(n²) | **O(n)** |
| For n=10⁴ | ~10⁸ ops → slow | ~2×10⁴ ops → **instant** |
| Space | O(n) list | O(n) stack |
| Passes over data | Up to n passes | **1 pass** |
| Handles cascading collisions? | ✅ (but slowly) | **✅ (efficiently)** |
| Code complexity | Moderate (list removal) | Moderate (while + conditions) |
| Interview value | Baseline only | **Expected answer** |

---

## Why No Other Approach Works Better

| Alternative | Why it doesn't apply |
|-------------|---------------------|
| Sorting | Would destroy positional order (collision depends on adjacency) |
| HashMap | No "lookup" operation; collisions are sequential |
| Two pointers | Collisions cascade backward (need LIFO, not converging pointers) |
| Queue (FIFO) | Wrong order — we need to interact with the MOST RECENT survivor |
| **Stack (LIFO)** | **Perfect fit — most recent right-moving asteroid is on top** |

---

## Stack vs In-Place Array Modification

| Metric | Stack (Deque) | In-Place Array |
|--------|--------------|----------------|
| Time | O(n) | O(n) |
| Space | O(n) | O(1) extra |
| Code clarity | **Clean, readable** | Complex (index management) |
| Correctness risk | Low | Higher (off-by-one errors) |
| Interview preference | **Standard, expected** | Bonus optimization |

In-place version (for reference):
```java
public int[] asteroidCollision(int[] asteroids) {
    int top = -1;  // acts as stack pointer
    for (int ast : asteroids) {
        if (ast > 0) {
            asteroids[++top] = ast;
        } else {
            while (top >= 0 && asteroids[top] > 0 && asteroids[top] < -ast) {
                top--;  // pop
            }
            if (top < 0 || asteroids[top] < 0) {
                asteroids[++top] = ast;
            } else if (asteroids[top] == -ast) {
                top--;  // both explode
            }
        }
    }
    return Arrays.copyOf(asteroids, top + 1);
}
```

> 📌 Same logic, O(1) extra space (reuses input array as the stack). Mention as an optimization after presenting the clean stack version.

---

## 🏁 Final Master Comparison Table

| Approach | Time | Space | Passes | Key Insight |
|----------|------|-------|--------|-------------|
| Repeated Scan | O(n²) | O(n) | Up to n | Find and resolve one collision per pass |
| **Stack (Deque)** | **O(n)** | **O(n)** | **1** | **LIFO matches "nearest right-moving asteroid" lookup** |
| In-Place Array | O(n) | O(1) | 1 | Use input array as stack (index as top) |

---

### 🎯 What to Present to the Interviewer

1. **Clarify collision rules:** "Only → followed by ← can collide. Same direction or moving apart = no collision."
2. **Explain why a stack fits:** "When a left-moving asteroid appears, it fights the nearest surviving right-moving asteroid to its left. That's the top of the stack (LIFO)."
3. **Walk through the algorithm:**
   - Positive → push.
   - Negative → while top is positive and smaller, pop. Then: equal → pop (both die); larger top → current dies; empty/negative → push.
4. **Walk through** `[10, 2, -5]`:
   - Push 10, push 2.
   - -5 arrives: top=2, |2|<5 → pop 2. Top=10, |10|>5 → -5 explodes.
   - Result: [10].
5. **Emphasize amortized O(n):** "Each asteroid is pushed once and popped at most once. Total operations = 2n."
6. **Write clean code** with `ArrayDeque<Integer>`.
7. **Mention in-place optimization:** "We can reuse the input array as the stack with an index pointer, achieving O(1) extra space."
8. **State complexity:** O(n) time, O(n) space (or O(1) extra with in-place).

**One‑sentence summary:**  
*Use a stack to simulate asteroid collisions in a single left-to-right pass: push right-moving asteroids, and when a left-moving asteroid arrives, pop smaller right-moving ones from the top until it either survives (push), mutually destroys (pop equal), or is destroyed (larger top remains) — achieving O(n) time via amortized analysis.*