### 📘 Chapter: Stack  
### 📌 Problem 9: Remove K Digits (LeetCode 402)

---

**Input**  
- `num`: a string representing a non‑negative integer.  
- `k`: an integer – the number of digits to remove.

**Output**  
- The smallest possible integer (as a string) after removing exactly `k` digits from `num`.  
- The result must not contain leading zeros (except for "0" itself).

**Constraints**  
- `1 <= k <= num.length <= 10⁵`  
- `num` consists of only digits.  
- `num` has no leading zeros except for the zero itself.

**Follow‑up**  
- None explicitly. The classic extension is to minimise time complexity – we target **O(n) time** and **O(n) space**.

---

### 🧠 Why this Data Structure (Monotonic Stack)?

The problem is to make the number as **small as possible** by removing digits. The key insight:

- We want the most significant digits (leftmost) to be as small as possible.  
- If a digit is larger than the digit coming after it, removing the larger digit reduces the overall number more than removing a smaller one later.  
- Therefore, we can use a **monotonic increasing stack**:  
  - Scan the digits left to right.  
  - While the stack is not empty, the top of the stack is greater than the current digit, and we still have removals left (`k > 0`), pop the stack (remove the larger digit).  
  - Then push the current digit.

- This greedy strategy builds the smallest possible sequence because it eliminates “peaks” (digits that are larger than their successor) as early as possible.  
- If `k` removals remain after the scan, we remove digits from the end (the least significant side) – they are already in increasing order, so the last ones are the largest remaining.  
- Finally, we strip any leading zeros and handle the empty result case.

The stack is the natural choice for this “next smaller / previous larger” pattern in string manipulation – it’s a classic monotonic stack application.

---

### 🔨 Brute Force Approach (Recursive / Backtracking)

**Method:**  
Generate all possible subsequences of length `n - k` by trying to remove `k` digits in all possible ways, then pick the smallest numeric value.  

- For each position, we could either keep or drop a digit (ensuring exactly `k` are dropped).  
- This is a combinatorial explosion – C(n, k) possibilities, which is exponential in the worst case.

**Time:** O(2ⁿ) (exponential) – completely impractical.  
**Space:** O(n) recursion depth.

```java
// Pseudo-code (impractical)
String minNum = null;
void generate(int i, int removed, StringBuilder sb) {
    if (i == num.length()) {
        if (removed == k) {
            String candidate = sb.toString().replaceFirst("^0+", "");
            if (candidate.isEmpty()) candidate = "0";
            if (minNum == null || candidate.compareTo(minNum) < 0) minNum = candidate;
        }
        return;
    }
    // keep
    sb.append(num.charAt(i));
    generate(i+1, removed, sb);
    sb.deleteCharAt(sb.length()-1);
    // drop
    if (removed < k) generate(i+1, removed+1, sb);
}
```
Not usable; only for reference.

---

### ⚡ Optimized Approach – Greedy Monotonic Stack (O(n) time, O(n) space)

**Method:**  
1. Use a `Deque<Character>` (or `StringBuilder` as a pseudo-stack) to hold the digits of the result.  
2. Iterate over each digit `c` in `num`:  
   - While stack is not empty, `k > 0`, and `stack.peek() > c`:  
     - Pop the stack (remove the larger previous digit), decrement `k`.  
   - Push `c` onto the stack.  
3. If `k` still > 0 after processing all digits, remove the last `k` digits from the stack (they are the largest ones at the least significant positions).  
4. Construct the result string from the stack (bottom‑to‑top).  
5. Remove leading zeros. If the result is empty, return `"0"`.

**Time:** O(n) – each digit is pushed and popped at most once.  
**Space:** O(n) – stack/stringbuilder holds up to n digits.

```java
import java.util.*;

public String removeKdigits(String num, int k) {
    Deque<Character> stack = new ArrayDeque<>();
    for (char c : num.toCharArray()) {
        while (!stack.isEmpty() && k > 0 && stack.peek() > c) {
            stack.pop();
            k--;
        }
        stack.push(c);
    }
    // remove remaining k from the end
    while (k-- > 0 && !stack.isEmpty()) {
        stack.pop();
    }
    // build result and strip leading zeros
    StringBuilder sb = new StringBuilder();
    while (!stack.isEmpty()) {
        sb.append(stack.removeLast()); // get from bottom
    }
    // remove leading zeros
    int start = 0;
    while (start < sb.length() && sb.charAt(start) == '0') start++;
    return (start == sb.length()) ? "0" : sb.substring(start);
}
```

*Note:* The `Deque` is used as a stack (push/pop at head). For final output order, we can also use a `StringBuilder` directly and maintain it as a stack by treating the end as the top:

```java
public String removeKdigits(String num, int k) {
    StringBuilder sb = new StringBuilder(); // acts as stack (top at end)
    for (char c : num.toCharArray()) {
        while (sb.length() > 0 && k > 0 && sb.charAt(sb.length() - 1) > c) {
            sb.deleteCharAt(sb.length() - 1);
            k--;
        }
        sb.append(c);
    }
    while (k-- > 0 && sb.length() > 0) {
        sb.deleteCharAt(sb.length() - 1);
    }
    // trim leading zeros
    int start = 0;
    while (start < sb.length() && sb.charAt(start) == '0') start++;
    return (start == sb.length()) ? "0" : sb.substring(start);
}
```

This `StringBuilder` approach is even simpler and avoids explicit `Deque`, but both convey the same O(n) monotonic stack idea.

---

### 📊 Solution Comparison & Trade‑offs

| Solution              | Time    | Space | Notes |
|-----------------------|---------|-------|-------|
| Brute force (generate all) | Exponential | O(n) | Impossible for n=10⁵. |
| Greedy Monotonic Stack | O(n)    | O(n)  | **Optimal**; linear time, simple once the greedy property is understood. |

**Trade‑off:**  
- The brute force is only a baseline to highlight the need for a smarter approach.  
- The monotonic stack is the canonical solution; it’s essentially the standard algorithm for “smallest number after removing k digits”. The in‑place StringBuilder version reduces the memory constant factor but still O(n). No further optimisation possible – we must examine all digits.

---

### 🎯 What to Present to the Interviewer

1. Explain the greedy intuition: a smaller leftmost digit always yields a smaller number, so we want to remove larger digits when a smaller digit follows.  
2. Introduce the **monotonic increasing stack** concept to enforce that.  
3. Walk through an example like `"1432219"` with `k=3`, showing the stack evolution.  
4. Write the code (prefer the `StringBuilder` stack version for conciseness).  
5. Discuss edge cases:  
   - If `k` remains after the loop, remove trailing digits.  
   - Strip leading zeros; if result empty, return `"0"`.  
6. State time/space complexity: O(n).  
7. Optionally mention that the greedy choice property can be proved by contradiction – but the high‑level idea suffices.

**One‑sentence summary:**  
*Use a greedy monotonic stack (increasing) to drop larger digits whenever a smaller digit appears to the right, ensuring the smallest possible number after removing exactly k digits, all in O(n) time.*