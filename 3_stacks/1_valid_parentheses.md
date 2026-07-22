### 📘 Chapter: Stack  
### 📌 Problem 1: Valid Parentheses (LeetCode 20)

---

**Input**  
- `s`: a string containing only the characters `'('`, `')'`, `'{'`, `'}'`, `'['`, `']'`

**Output**  
- `true` if the input string is valid according to the following rules; `false` otherwise:  
  1. Open brackets must be closed by the same type of brackets.  
  2. Open brackets must be closed in the correct order.  
  3. Every close bracket has a corresponding open bracket of the same type.

**Constraints**  
- `1 <= s.length <= 10⁴`  
- `s` consists of parentheses only `'()[]{}'`.

**Follow-up**  
- None explicitly. (A common extension is to handle other types of brackets or to find the longest valid parentheses substring, but not for this problem.)

---

### 🧠 Why this Data Structure?

The problem demands that the **most recently opened unmatched bracket** must be the first one to be closed — this is exactly **Last‑In‑First‑Out (LIFO)** behavior.  

- A **Stack** (via `java.util.ArrayDeque` or `LinkedList`) is the natural choice.  
- As we traverse the string:
  - When we encounter an opening bracket, we push it onto the stack.
  - When we encounter a closing bracket, we check if the stack is non‑empty and the top element matches the corresponding opening bracket; if yes, we pop it. Otherwise, the string is invalid.
- At the end, the stack must be empty (all brackets matched).

Any solution without a stack (e.g., counting) cannot correctly handle cases like `"([)]"` where order matters across bracket types, because counts alone don't enforce the nesting order.

---

### 🔨 Brute Force Approach (Repeated Replacement)

**Method:**  
Continuously remove the innermost matching pairs `"()"`, `"{}"`, `"[]"` until the string becomes empty or unchanged.  
If the string eventually becomes empty, it was valid; if it stops shrinking while still non‑empty, it’s invalid.

**Time:** O(n²) – each pass scans the string and creates a new string (or shifts characters), and in the worst case (e.g., `"(((...)))"`) we need O(n) passes.  
**Space:** O(n) – for the intermediate string.

```java
public boolean isValid(String s) {
    String prev = "";
    while (!s.equals(prev)) {
        prev = s;
        s = s.replace("()", "").replace("{}", "").replace("[]", "");
    }
    return s.isEmpty();
}
```

This is simple but inefficient and not optimal for large inputs.

---

### ⚡ Optimized Approach – Stack (O(n) time, O(n) space)

**Method:**  
1. Initialize an empty stack of characters.  
2. Iterate over each character `c` in `s`:  
   - If `c` is an opening bracket `'(', '{', '['`, push it onto the stack.  
   - If `c` is a closing bracket:  
     - If the stack is empty → invalid (no matching open).  
     - Pop the top element and check if it is the corresponding opening bracket for `c`. If not → invalid.  
3. After the loop, return `true` if the stack is empty; otherwise, `false`.

**Time:** O(n) – single pass, each character pushed/popped at most once.  
**Space:** O(n) – in worst case (all opening brackets) the stack grows to `n`.

```java
import java.util.ArrayDeque;
import java.util.Deque;

public boolean isValid(String s) {
    Deque<Character> stack = new ArrayDeque<>();
    for (char c : s.toCharArray()) {
        if (c == '(' || c == '{' || c == '[') {
            stack.push(c);
        } else {
            if (stack.isEmpty()) return false;
            char top = stack.pop();
            if ((c == ')' && top != '(') ||
                (c == '}' && top != '{') ||
                (c == ']' && top != '[')) {
                return false;
            }
        }
    }
    return stack.isEmpty();
}
```

**Alternative mapping:** Use a `HashMap<Character, Character>` to map closing brackets to their opening counterparts for cleaner code.

```java
// Variation with map
Map<Character, Character> map = Map.of(')', '(', '}', '{', ']', '[');
Deque<Character> stack = new ArrayDeque<>();
for (char c : s.toCharArray()) {
    if (map.containsValue(c)) { // opening bracket
        stack.push(c);
    } else { // closing bracket
        if (stack.isEmpty() || stack.pop() != map.get(c)) return false;
    }
}
return stack.isEmpty();
```

---

### 📊 Solution Comparison & Trade‑offs

| Solution               | Time   | Space | Correctness for nested/mixed brackets | Notes |
|------------------------|--------|-------|---------------------------------------|-------|
| Repeated replacement   | O(n²)  | O(n)  | ✅ Works, but slow                     | Only as a conceptual baseline. |
| Stack (explicit)       | O(n)   | O(n)  | ✅ Yes (perfect LIFO)                  | **Industry standard**; the only correct optimal solution for this problem. |

**Trade‑off:**  
There is no serious trade‑off. The stack is the only data structure that can naturally handle multiple bracket types with correct nesting order in linear time. The brute‑force replacement is a novelty, not a practical alternative.

---

### 🎯 What to Present to the Interviewer

1. Immediately recognize that this is a classic **stack problem**.  
2. Explain the LIFO property required for bracket matching.  
3. Propose the **stack approach**: push openings, pop on closings, check matches.  
4. Walk through the code, emphasizing the use of a `Deque` (e.g., `ArrayDeque`) as the modern Java stack (avoiding `java.util.Stack` which is synchronized and legacy).  
5. Discuss early exit conditions: if a closing bracket appears and the stack is empty or mismatched, return `false`.  
6. At the end, verify that the stack is empty.  
7. State complexities: O(n) time, O(n) space (optimal).  
8. Optionally show the HashMap variation for elegance and extensibility (if more bracket types were added).

**One‑sentence summary:**  
*Use a stack to enforce that the most recently opened bracket is closed first; push opening brackets and pop on matching closings, returning false on any mismatch or if the stack is not empty at the end, all in O(n) time.*