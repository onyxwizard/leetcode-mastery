### 📘 Chapter: Stack  
### 📌 Problem 5: Largest Rectangle in Histogram (LeetCode 84)

---

**Input**  
- `heights`: an array of integers representing the heights of histogram bars (width of each bar = 1).

**Output**  
- The area of the largest rectangle that can be formed within the histogram.

**Constraints**  
- `1 <= heights.length <= 10⁵`  
- `0 <= heights[i] <= 10⁴`

**Follow‑up**  
- Not explicitly given. The natural expectation is to achieve **O(n) time** and **O(n) space**, which is optimal.

---

### 🧠 Why this Data Structure / Approach?

For each bar, the largest rectangle using that bar as the **minimum height** extends to the left and right until it hits a shorter bar.  
- **Brute force:** For each bar, expand outwards to find the first shorter bar on each side → O(n²).  
- **Monotonic Stack (increasing):**  
  - We use a stack to keep track of indices of bars in **increasing order of height**.  
  - When we encounter a bar **shorter** than the bar at the top of the stack, it means the bar at the top cannot extend further to the right. We pop it, calculate its area using its height and the width determined by the new, smaller left boundary (the next element on the stack) and the current index as the right boundary.  
  - This processes each bar once when pushed and once when popped → O(n) time, O(n) space.

This stack approach is the classic optimal solution for this problem.

---

### 🔨 Brute Force Approach (Expand Around Each Bar)

**Method:**  
For each bar `i`, find the first shorter bar to the left (`left`) and to the right (`right`).  
The rectangle with height `heights[i]` spans width `(right - left - 1)`.  
Track the maximum area.

**Time:** O(n²) – for each bar, in worst case we scan all the way left and right.  
**Space:** O(1).

```java
public int largestRectangleArea(int[] heights) {
    int n = heights.length;
    int maxArea = 0;
    for (int i = 0; i < n; i++) {
        int left = i;
        while (left >= 0 && heights[left] >= heights[i]) left--;
        int right = i;
        while (right < n && heights[right] >= heights[i]) right++;
        int width = right - left - 1;
        maxArea = Math.max(maxArea, heights[i] * width);
    }
    return maxArea;
}
```

Too slow for `n = 10⁵`.

---

### ⚡ Optimized Approach – Monotonic Stack (O(n) time, O(n) space)

**Method:**  
- Use a stack that stores **indices** (not heights) of bars in increasing order of height.  
- We append a sentinel height `0` at the end to ensure all bars are popped and processed.  
- Iterate `i` from `0` to `n` (inclusive):  
  - While the stack is not empty and `heights[stack.peek()] > heights[i]`:  
    - Pop `h = heights[stack.pop()]`.  
    - Determine the width: if stack is empty, width = `i` (all bars to the left were taller); else width = `i - stack.peek() - 1`.  
    - Compute area = `h * width`, update `maxArea`.  
  - Push `i` onto the stack.  

**Time:** O(n) – each index pushed and popped at most once.  
**Space:** O(n) – stack holds at most `n` indices.

```java
import java.util.ArrayDeque;
import java.util.Deque;

public int largestRectangleArea(int[] heights) {
    int n = heights.length;
    Deque<Integer> stack = new ArrayDeque<>();
    int maxArea = 0;

    for (int i = 0; i <= n; i++) {
        int h = (i == n) ? 0 : heights[i];
        while (!stack.isEmpty() && h < heights[stack.peek()]) {
            int height = heights[stack.pop()];
            int width = stack.isEmpty() ? i : i - stack.peek() - 1;
            maxArea = Math.max(maxArea, height * width);
        }
        stack.push(i);
    }
    return maxArea;
}
```

---

### 📊 Solution Comparison & Trade‑offs

| Solution                 | Time | Space  | Notes |
|--------------------------|------|--------|-------|
| Brute force (expand)     | O(n²)| O(1)   | Simple but impractical for large `n`. |
| Monotonic stack          | O(n) | O(n)   | **Optimal**; linear time, one pass. |

**Trade‑off:**  
- The brute force is only for concept; the stack approach is always preferred.  
- A variant using a two‑pointer with precomputed left/right limits (using an array) also yields O(n) time and O(n) space, but the stack is more compact and elegant.  
- The stack solution is the definitive interview answer.

---

### 🎯 What to Present to the Interviewer

1. Start by explaining the logic: the maximum rectangle with a bar as the minimum height extends left until a smaller bar and right until a smaller bar.  
2. Present the O(n²) brute force briefly.  
3. Introduce the **monotonic increasing stack** concept: maintain indices of bars in increasing height; when a smaller bar arrives, the previous taller bars can’t extend further right, so we pop and calculate their maximum possible rectangle.  
4. Walk through the algorithm with an example (e.g., `[2,1,5,6,2,3]`).  
5. Write the clean code, highlighting the sentinel `0` trick to flush remaining bars.  
6. State complexities: O(n) time, O(n) space.  
7. Optionally mention the precomputed left/right boundaries method as an alternative but reaffirm the stack as the cleanest.

**One‑sentence summary:**  
*Use a monotonic increasing stack to track bar indices; when a smaller bar is encountered, pop and calculate the area using the popped bar as the shortest one, extending to the current index on the right and the new stack top on the left, achieving O(n) time.*