### 📘 Chapter: Stack  
### 📌 Problem 3: Daily Temperatures (LeetCode 739)

---

**Input**  
- `temperatures`: integer array of daily temperatures.

**Output**  
- `answer[i]`: number of days you have to wait **after** day `i` to get a warmer temperature.  
- If there is no future warmer day, `answer[i] = 0`.

**Constraints**  
- `1 <= temperatures.length <= 10⁵`  
- `30 <= temperatures[i] <= 100`

**Follow‑up**  
- The problem’s natural follow‑up is **space optimization**: can you solve it with **O(1) extra space** (or very little extra memory) by exploiting the limited temperature range?

---

### 🧠 Why this Data Structure / Approach?

We need the **first greater element to the right** for every index.  
- **Monotonic Stack** (decreasing order) is the classic tool for “Next Greater Element” problems.  
  - We store indices of days that haven’t found a warmer day yet, and the stack maintains decreasing temperatures.  
  - When a warmer day arrives, it resolves all the previously colder days in one go.  
  - This yields **O(n) time** and **O(n) space**.  

- **Alternative optimized** (exploiting the small temperature range 30–100):  
  - We can use an array `next[101]` where `next[t]` holds the **earliest index** (from the right) of temperature `t`.  
  - Traverse from right to left; for the current temperature, the answer is the minimum index among all `next[t]` for `t > currentTemp` (if any). Then update `next[currentTemp] = i`.  
  - This uses **O(1) extra space** (only 101 integers) and **O(n * 70) ≈ O(n)** time. It’s a clever, constraint‑specific optimization.

---

### 🔨 Brute Force Approach (Nested Loops)

**Method:**  
For each day `i`, scan forward to find the first day `j > i` with `temperatures[j] > temperatures[i]`. Set `answer[i] = j - i`. If none found, `answer[i] = 0`.

**Time:** O(n²) – in worst case (descending temperatures), we scan to the end for every element.  
**Space:** O(1) – only the output array (required).

```java
public int[] dailyTemperatures(int[] temperatures) {
    int n = temperatures.length;
    int[] answer = new int[n];
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (temperatures[j] > temperatures[i]) {
                answer[i] = j - i;
                break;
            }
        }
    }
    return answer;
}
```

Too slow for `n = 10⁵`.

---

### ⚡ Optimized Approach 1 – Monotonic Stack (O(n) time, O(n) space)

**Method:**  
- Use a stack to store **indices** of days that haven’t found a warmer day yet.  
- The stack is **monotonically decreasing** in temperature: the temperature at the top is the coldest among the unresolved days.  
- Iterate `i` from 0 to `n-1`:  
  - While stack is not empty and `temperatures[i] > temperatures[stack.peek()]`:  
    - Pop the index `prev`, set `answer[prev] = i - prev`.  
  - Push `i` onto the stack.  
- Days left in the stack have no future warmer day, so their answer remains 0 (default).

**Time:** O(n) – each index pushed and popped at most once.  
**Space:** O(n) – stack holds at most `n` indices.

```java
import java.util.ArrayDeque;
import java.util.Deque;

public int[] dailyTemperatures(int[] temperatures) {
    int n = temperatures.length;
    int[] answer = new int[n];
    Deque<Integer> stack = new ArrayDeque<>(); // stores indices

    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && temperatures[i] > temperatures[stack.peek()]) {
            int prev = stack.pop();
            answer[prev] = i - prev;
        }
        stack.push(i);
    }
    return answer;
}
```

---

### ⚡ Optimized Approach 2 – Reverse Traversal with "Next Warmer" Array (O(n) time, O(1) extra space)

**Method:**  
Leverage the constraint `30 ≤ temperatures[i] ≤ 100`.  
- Create an array `next` of size 101, initialized to `Integer.MAX_VALUE`. `next[t]` will store the earliest index (from the right) where temperature `t` has been seen.  
- Traverse from right to left (`i` from `n-1` down to `0`):  
  - For `temp = temperatures[i]`, find the **minimum index** among `next[t]` for all `t > temp` (i.e., warmer temperatures).  
  - If found, `answer[i] = minIndex - i`.  
  - Update `next[temp] = i` (overwrite, because we want the earliest index from the right, i.e., the smallest index).  

**Time:** O(n * 70) ≈ O(n) – inner loop over at most 70 warmer temperatures.  
**Space:** O(1) extra – `next` array of fixed size 101.

```java
public int[] dailyTemperatures(int[] temperatures) {
    int n = temperatures.length;
    int[] answer = new int[n];
    int[] next = new int[101]; // temperatures 0..100, but only 30..100 used
    Arrays.fill(next, Integer.MAX_VALUE);

    for (int i = n - 1; i >= 0; i--) {
        int temp = temperatures[i];
        int minIndex = Integer.MAX_VALUE;
        // find the earliest warmer day
        for (int t = temp + 1; t <= 100; t++) {
            if (next[t] < minIndex) {
                minIndex = next[t];
            }
        }
        if (minIndex != Integer.MAX_VALUE) {
            answer[i] = minIndex - i;
        }
        next[temp] = i; // update current temp's earliest index
    }
    return answer;
}
```

---

### 📊 Solution Comparison & Trade‑offs

| Solution                    | Time   | Extra Space | When to Use |
|-----------------------------|--------|-------------|-------------|
| Brute force (nested loops)  | O(n²)  | O(1)        | Only for tiny input. |
| Monotonic stack             | O(n)   | O(n)        | **General**, works for any value range. Clean and typical. |
| Reverse + next warmer array | O(n·k) (k=71) ≈ O(n) | O(1) fixed  | **Exploit constraint** (small temp range). Space‑optimal. |

**Trade‑off:**  
- The stack approach is universal and doesn’t depend on the value range. It’s the expected interview answer for its clarity.  
- The reverse array approach uses **truly constant extra space** (only a fixed 101‑slot array) and is faster in practice because of array access, but it only works because temperatures are bounded to [30,100]. It shows ability to optimise using given constraints.

---

### 🎯 What to Present to the Interviewer

1. Start by noting this is a “Next Greater Element” variant, naturally solved with a **monotonic stack**.  
2. Quickly mention the O(n²) brute force as the baseline.  
3. Introduce the **stack of indices**, explain the decreasing order property: we only pop when a warmer day resolves previous days.  
4. Walk through the stack‑based Java code, showing O(n) time and O(n) space.  
5. After the interviewer is satisfied, point out the **small temperature range** constraint and offer the **O(1) extra space** solution using the `next` array. Explain the reverse traversal and searching only warmer buckets.  
6. Discuss trade‑offs: the stack is general; the array method is a nice space optimisation tailored to the constraints.  
7. Conclude that both are linear‑time, and the stack is the go‑to solution, while the constant‑space approach shows deep constraint awareness.

**One‑sentence summary:**  
*Use a monotonic decreasing stack to find the next warmer day for each temperature in O(n) time, or exploit the bounded temperature range to achieve O(1) extra space with a reverse‑traversal array lookup.*