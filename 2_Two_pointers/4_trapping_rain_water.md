### 📘 Chapter: Two Pointers  
### 📌 Problem 4: Trapping Rain Water (LeetCode 42)

---

**Input**  
- `height`: an integer array of `n` non‑negative integers representing the elevation map, each bar width = 1

**Output**  
- Total units of water trapped after raining (an integer)

**Constraints**  
- `n == height.length`  
- `1 <= n <= 2 * 10⁴`  
- `0 <= height[i] <= 10⁵`

**Follow-up**  
- Typically the interview follow‑up is to achieve **O(1) extra space** in addition to O(n) time.

---

### 🧠 Why this Approach / Data Structure?

The amount of water trapped at index `i` is determined by the **minimum of the maximum height to its left and the maximum height to its right**, minus the height at `i` (if positive).  

To compute this efficiently:

- **Prefix/Suffix arrays** (`leftMax[i]`, `rightMax[i]`) allow O(1) lookup per index after O(n) preprocessing. This uses **O(n) extra space** but is simple to understand.  
- **Two pointers** further reduce space to **O(1)** by maintaining the current left and right maximums and moving pointers inward based on which side is lower. This avoids storing the entire arrays.

Both methods run in O(n) time, but the two‑pointer approach is the gold standard for its minimal memory usage and elegant logic.

No complex data structures beyond arrays and variables are needed.

---

### 🔨 Brute Force Approach (O(n²))

**Method:**  
For each index `i`, scan the left side to find `maxLeft` and the right side to find `maxRight`.  
Water at `i` = `max(0, min(maxLeft, maxRight) - height[i])`.

**Time:** O(n²) – nested loops  
**Space:** O(1)

```java
public int trap(int[] height) {
    int n = height.length;
    int total = 0;
    for (int i = 0; i < n; i++) {
        int maxLeft = 0, maxRight = 0;
        for (int j = 0; j <= i; j++) maxLeft = Math.max(maxLeft, height[j]);
        for (int j = i; j < n; j++) maxRight = Math.max(maxRight, height[j]);
        total += Math.max(0, Math.min(maxLeft, maxRight) - height[i]);
    }
    return total;
}
```

---

### ⚡ Optimized Approach 1 – Prefix/Suffix Arrays (O(n) time, O(n) space)

**Method:**  
1. Precompute `leftMax[i]` = max height from left up to `i`.  
2. Precompute `rightMax[i]` = max height from right up to `i`.  
3. For each index, water = `min(leftMax[i], rightMax[i]) - height[i]`.

**Time:** O(n) – three passes (left, right, final)  
**Space:** O(n) – two extra arrays of size n

```java
public int trap(int[] height) {
    int n = height.length;
    if (n == 0) return 0;

    int[] leftMax = new int[n];
    int[] rightMax = new int[n];

    leftMax[0] = height[0];
    for (int i = 1; i < n; i++) {
        leftMax[i] = Math.max(leftMax[i - 1], height[i]);
    }

    rightMax[n - 1] = height[n - 1];
    for (int i = n - 2; i >= 0; i--) {
        rightMax[i] = Math.max(rightMax[i + 1], height[i]);
    }

    int total = 0;
    for (int i = 0; i < n; i++) {
        total += Math.min(leftMax[i], rightMax[i]) - height[i];
    }
    return total;
}
```

---

### ⚡ Optimized Approach 2 – Two Pointers (O(n) time, O(1) space)

**Method:**  
- Use `left = 0`, `right = n - 1`, and two variables `leftMax = 0`, `rightMax = 0`.  
- While `left < right`:  
  - If `height[left] < height[right]`:  
    - If `height[left] >= leftMax` update `leftMax`, else add `leftMax - height[left]` to total.  
    - `left++`  
  - Else:  
    - If `height[right] >= rightMax` update `rightMax`, else add `rightMax - height[right]` to total.  
    - `right--`

**Why it works:**  
At each step, the lower of `height[left]` and `height[right]` determines the trapped water because the water level is bounded by the shorter side. The pointer with the smaller height is processed and moved inward, using the appropriate `max` value seen so far.

**Time:** O(n) – single pass  
**Space:** O(1)

```java
public int trap(int[] height) {
    int left = 0, right = height.length - 1;
    int leftMax = 0, rightMax = 0;
    int total = 0;

    while (left < right) {
        if (height[left] < height[right]) {
            if (height[left] >= leftMax) {
                leftMax = height[left];
            } else {
                total += leftMax - height[left];
            }
            left++;
        } else {
            if (height[right] >= rightMax) {
                rightMax = height[right];
            } else {
                total += rightMax - height[right];
            }
            right--;
        }
    }
    return total;
}
```

---

### 📊 Solution Comparison & Trade‑offs

| Solution                   | Time   | Space | Notes |
|----------------------------|--------|-------|-------|
| Brute force (nested loops) | O(n²)  | O(1)  | Too slow for n=2·10⁴. |
| Prefix/Suffix arrays       | O(n)   | O(n)  | Straightforward, easy to code; uses two extra arrays. |
| Two pointers               | O(n)   | O(1)  | **Optimal space**; elegant but requires a clear understanding of the water‑bounding logic. |

**Trade‑off:**  
- The prefix array approach is a great stepping stone and shows the candidate can think in terms of precomputation.  
- The two‑pointer method is the interview favorite because it achieves O(1) space and demonstrates deeper insight into the problem’s structure.

---

### 🎯 What to Present to the Interviewer

1. Start by explaining the water‑trapping formula: `min(maxLeft, maxRight) - height[i]`.  
2. Present the **prefix/suffix arrays** solution first – clear and easy to reason about, O(n) time and O(n) space.  
3. Then, mention the **follow‑up** to optimize space, leading to the **two‑pointer** approach.  
4. Walk through the two‑pointer algorithm carefully, highlighting the key decision: process the smaller side because the water level on that side is already bounded by the current `leftMax` or `rightMax`.  
5. Write the two‑pointer code cleanly.  
6. Conclude with complexity analysis (O(n) time, O(1) space) and note that this is the optimal solution.

**One‑sentence summary:**  
*Compute trapped water using two pointers that move inward based on the smaller height, maintaining running left and right maximums to calculate water added at each step in O(n) time and O(1) space.*