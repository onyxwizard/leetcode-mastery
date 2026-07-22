### 📘 Chapter: Stack  
### 📌 Problem 2: Min Stack (LeetCode 155)

---

**Input**  
- A sequence of method calls on a `MinStack` object:  
  - `MinStack()` – initialises the stack.  
  - `push(int val)` – pushes `val` onto the stack.  
  - `pop()` – removes the top element.  
  - `top()` – returns the top element.  
  - `getMin()` – retrieves the current minimum element in the stack.

**Output**  
- For each method that returns a value (`top` and `getMin`), the corresponding integer output.

**Constraints**  
- `-2³¹ <= val <= 2³¹ - 1`  
- `pop`, `top`, and `getMin` are only called on a non‑empty stack.  
- At most `3 * 10⁴` total calls will be made.

**Follow‑up**  
- The problem already mandates **O(1) time for all operations**. The natural interview follow‑up is:  
  *Can you implement it using only one stack, or minimise extra space?*

---

### 🧠 Why this Data Structure?

We need to support normal stack operations (push, pop, top) **and** retrieve the minimum in **O(1)**.  
- A single stack alone cannot track the minimum efficiently — scanning the stack takes O(n).  
- The standard solution uses an **auxiliary stack (`minStack`)** that keeps track of the minimum value seen at each level of the main stack.  
  - When pushing, we also push the new value onto `minStack` if it is ≤ the current minimum.  
  - When popping, if the popped value equals the current minimum, we pop from `minStack` as well.  
  - This gives O(1) time for all operations, with O(n) extra space in the worst case.  
- An advanced space‑optimised version uses a **single stack + a variable** (`min`) and encodes the previous minimum inside the pushed value when a new minimum occurs (e.g., `stack.push(2*val - min)`). This still guarantees O(1) time and uses only one stack, but care must be taken with integer overflow.

---

### 🔨 Naive / Brute Force Approach (O(n) getMin)

**Method:**  
Use a normal stack (e.g., `ArrayList` or `ArrayDeque`). For `getMin()`, iterate through the entire stack to find the minimum.

**Time:** push/pop/top O(1), `getMin` O(n) – **fails the O(1) requirement**.  
**Space:** O(n) for the stack elements.

```java
// Not acceptable for the problem
class MinStack {
    private Deque<Integer> stack = new ArrayDeque<>();
    public void push(int val) { stack.push(val); }
    public void pop() { stack.pop(); }
    public int top() { return stack.peek(); }
    public int getMin() {
        int min = Integer.MAX_VALUE;
        for (int x : stack) min = Math.min(min, x);
        return min;
    }
}
```

---

### ⚡ Optimized Approach 1 – Two Stacks (Primary + minStack)

**Method:**  
- `stack` holds all elements.  
- `minStack` holds the **minimum value so far** at each push.  
  - `push(val)`: always push to `stack`. If `minStack` is empty or `val <= minStack.peek()`, push `val` onto `minStack`.  
  - `pop()`: pop `stack`. If the popped value equals `minStack.peek()`, pop `minStack` as well.  
  - `top()`: peek `stack`.  
  - `getMin()`: peek `minStack`.

**Time:** O(1) for all operations.  
**Space:** O(n) – in the worst case (decreasing values), `minStack` holds all `n` elements.

```java
import java.util.ArrayDeque;
import java.util.Deque;

class MinStack {
    private Deque<Integer> stack;
    private Deque<Integer> minStack;

    public MinStack() {
        stack = new ArrayDeque<>();
        minStack = new ArrayDeque<>();
    }

    public void push(int val) {
        stack.push(val);
        if (minStack.isEmpty() || val <= minStack.peek()) {
            minStack.push(val);
        }
    }

    public void pop() {
        int removed = stack.pop();
        if (removed == minStack.peek()) {
            minStack.pop();
        }
    }

    public int top() {
        return stack.peek();
    }

    public int getMin() {
        return minStack.peek();
    }
}
```

---

### ⚡ Optimized Approach 2 – Single Stack with Encoded Minimum (Space Optimisation)

**Method:**  
Use a single stack and a variable `min` to track the current minimum.  
- When pushing a new value `val` that is **≤ current `min`**, we first push the **old `min`** onto the stack (to remember it), then push `val`, and update `min = val`. Actually, a cleaner trick is to store a transformed value:  
  - If `val >= min`, push `val` normally.  
  - If `val < min`, push `2*val - min` (which is < val) and set `min = val`.  
- When popping:  
  - If the top value `t` is < `min`, then the actual value is `min`, and we need to restore the previous `min = 2*min - t`.  
  - Else, the actual value is `t`.  
- This uses only one stack and avoids a second stack entirely, but careful with overflow: use `long` for intermediate multiplication or ensure values are within bounds where `2*val - min` fits in an `int`. The constraints allow `-2^31` to `2^31-1`, so overflow is possible. A safer version pushes the old `min` explicitly before the new value instead of encoding; that still uses a single stack but effectively stores two values per minimum change.  

*For interview clarity, the two‑stack version is almost always sufficient.* The encoded version shows deeper understanding, but you must mention overflow handling.

```java
// Encoding version (with overflow caution using long)
class MinStack {
    private Deque<Long> stack;
    private long min;

    public MinStack() {
        stack = new ArrayDeque<>();
    }

    public void push(int val) {
        long v = (long) val;
        if (stack.isEmpty()) {
            stack.push(v);
            min = v;
        } else if (v >= min) {
            stack.push(v);
        } else {
            // val < min
            stack.push(2 * v - min); // encoded value, less than new min
            min = v;
        }
    }

    public void pop() {
        long top = stack.pop();
        if (top < min) {
            // top is encoded, restore previous min
            min = 2 * min - top;
        }
        // If top >= min, the actual value is top, no change to min
    }

    public int top() {
        long top = stack.peek();
        if (top < min) {
            return (int) min;
        } else {
            return (int) top;
        }
    }

    public int getMin() {
        return (int) min;
    }
}
```
*Note: The safer and more commonly presented single-stack approach is to push the old min explicitly before the new min whenever the min changes. That avoids overflow entirely:*

```java
class MinStack {
    private Deque<Integer> stack;
    private int min;

    public MinStack() { stack = new ArrayDeque<>(); min = Integer.MAX_VALUE; }

    public void push(int val) {
        if (val <= min) {
            stack.push(min); // store old min
            min = val;
        }
        stack.push(val);
    }

    public void pop() {
        if (stack.pop() == min) {
            min = stack.pop(); // retrieve old min
        }
    }

    public int top() { return stack.peek(); }
    public int getMin() { return min; }
}
```
This version uses only one stack and no overflow worries; it pushes two elements when the min changes, so space is still O(n).

---

### 📊 Solution Comparison & Trade‑offs

| Solution                       | Time per op | Space (extra) | Notes |
|--------------------------------|-------------|---------------|-------|
| Scan stack for min             | O(n) getMin | O(n) total    | Fails O(1) requirement. |
| Two stacks (primary + minStack)| O(1)        | O(n) worst-case| **Simplest, safest**; interview standard. |
| Single stack + encoding        | O(1)        | O(n) total, no separate minStack | Saves a few bytes; overflow risk; harder to explain. |
| Single stack + push old min    | O(1)        | O(n) total, but extra pushes when min changes | Avoids overflow, still one stack. |

**Trade‑off:**  
The two‑stack approach is the clearest and most maintainable; it’s the first choice in an interview. The single‑stack with explicit old‑min push is an elegant space micro‑optimisation that still uses O(n) space in the worst case. The encoding trick is clever but can overflow without careful `long` usage. I recommend presenting the two‑stack solution, then mentioning the single‑stack variant if the interviewer pushes for space optimisation.

---

### 🎯 What to Present to the Interviewer

1. Clarify that all operations must be O(1).  
2. Explain that a simple stack + O(n) scan fails; we need auxiliary storage.  
3. Introduce the **two‑stack approach**: one for elements, one for the running minimum.  
4. Walk through the code, especially the `push` (check if new value ≤ minStack top) and `pop` (synchronise minStack when the minimum is removed).  
5. Analyse time and space: O(1) per op, O(n) extra space.  
6. If asked about space, present the **single‑stack with old‑min push** variant. Briefly mention the encoding method but note the overflow risk.  
7. Conclude that the two‑stack solution is robust and meets all constraints perfectly.

**One‑sentence summary:**  
*Use an auxiliary min‑stack that tracks the minimum at each depth; synchronise it with the main stack during push and pop to deliver O(1) getMin, top, push, and pop.*