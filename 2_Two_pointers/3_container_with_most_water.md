### 📘 Chapter: Two Pointers  
### 📌 Problem 3: Container With Most Water (LeetCode 11)

---

**Input**  
- `height`: an integer array of length `n`, where `height[i]` represents the height of a vertical line at index `i`

**Output**  
- The maximum amount of water (integer area) that can be contained between any two lines, with the x‑axis forming the bottom.

**Constraints**  
- `n == height.length`  
- `2 <= n <= 10⁵`  
- `0 <= height[i] <= 10⁴`

**Follow-up**  
- None explicitly stated; the optimal solution is expected to run in **O(n) time** and **O(1) space**.

---

### 🧠 Why this Approach (Two Pointers)?

The problem asks for the maximum area formed by a pair of lines. The area between lines at indices `i` and `j` is:  
`area = min(height[i], height[j]) * (j - i)`.

- The **brute force** O(n²) checks all pairs.  
- **Two‑pointer** technique leverages a key insight:  
  The area is limited by the **shorter** line. If we start with the widest possible container (`left = 0, right = n-1`), the only way to potentially get a larger area is to discard the shorter line and move its pointer inward.  
  - If `height[left] < height[right]`, moving `right` leftward cannot increase the height because the new right height is still ≤ old right? Actually, if we move the taller one, the width decreases, and the height can't exceed the original shorter line (since the shorter line still limits). So the area can only decrease or stay the same. Therefore, moving the **shorter** pointer is the only chance to find a taller line and compensate for the width reduction.  
- This single pass yields O(n) time and O(1) space – optimal.

No auxiliary data structure is needed; just two pointers and a variable for the maximum area.

---

### 🔨 Brute Force Approach (All Pairs)

**Method:**  
Nested loops over all pairs `(i, j)` with `i < j`. Compute `min(height[i], height[j]) * (j - i)` and update the maximum.

**Time:** O(n²)  
**Space:** O(1)

```java
public int maxArea(int[] height) {
    int n = height.length;
    int maxArea = 0;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            int area = Math.min(height[i], height[j]) * (j - i);
            maxArea = Math.max(maxArea, area);
        }
    }
    return maxArea;
}
```

---

### ⚡ Optimized Approach – Two Pointers (O(n) time, O(1) space)

**Method:**  
- Initialize `left = 0`, `right = n - 1`, `maxArea = 0`.  
- While `left < right`:  
  - Compute area with current `left` and `right`.  
  - Update `maxArea`.  
  - Move the pointer with the **smaller height** one step inward (if equal, moving either is fine).  
- Return `maxArea`.

**Time:** O(n) – each element visited at most once  
**Space:** O(1)

```java
public int maxArea(int[] height) {
    int left = 0, right = height.length - 1;
    int maxArea = 0;

    while (left < right) {
        int width = right - left;
        int h = Math.min(height[left], height[right]);
        maxArea = Math.max(maxArea, h * width);

        // move the shorter line
        if (height[left] < height[right]) {
            left++;
        } else {
            right--;
        }
    }
    return maxArea;
}
```

---

### 📊 Two‑Solution Comparison & Trade‑offs

| Solution            | Time   | Space | Notes |
|---------------------|--------|-------|-------|
| Brute force (all pairs) | O(n²) | O(1)  | Simple but impractical for n=10⁵; wastes time checking doomed containers. |
| Two pointers        | O(n)   | O(1)  | **Optimal**; uses the property that moving the shorter line is the only way to increase area. |

**Trade‑off:**  
There is only one truly optimal solution for this problem – the two‑pointer method. The brute force is just the baseline. No other data structure (like hash map) applies. The insight is purely logical: width is maxed at the start, and height can only improve by abandoning the shorter line. The algorithm is a classic greedy/two‑pointer example.

---

### 🎯 What to Present to the Interviewer

1. Start by explaining the area formula and the O(n²) brute force approach.  
2. Then introduce the key insight: the area is limited by the shorter line. With the widest width, the only way to find a larger area is to move the shorter line inward in hope of a taller line.  
3. Walk through the **two‑pointer algorithm** step by step: initialize at extremes, compute area, move the pointer with the smaller height.  
4. Emphasize that this greedy elimination is safe because any container involving the shorter line and any inner line will have ≤ current area.  
5. Code the solution clearly.  
6. State the time and space complexities: O(n) time, O(1) space.

**One‑sentence summary:**  
*Start with the widest container and narrow it by always moving the pointer at the shorter line, because the only chance to beat the current area is to find a taller boundary, achieving O(n) time and O(1) space.*