### 📘 Chapter: Two Pointers  
### 📌 Problem 5: Two Sum II – Input Array Is Sorted (LeetCode 167)

---

**Input**  
- `numbers`: a **1‑indexed** integer array sorted in **non‑decreasing order**  
- `target`: an integer

**Output**  
- A 2‑element array `[index1, index2]` containing the **1‑based indices** of the two numbers that sum to `target`.  
- `1 <= index1 < index2 <= numbers.length`. Exactly one solution exists.

**Constraints**  
- `2 <= numbers.length <= 3 * 10⁴`  
- `-1000 <= numbers[i] <= 1000`  
- `-1000 <= target <= 1000`  
- The array is sorted in non‑decreasing order.  
- The tests are generated such that there is exactly one solution.  
- **Your solution must use only constant extra space.**

**Follow-up**  
- The “constant extra space” restriction is the built‑in follow‑up from the original Two Sum (which allowed O(n) space with a HashMap).

---

### 🧠 Why this Approach (Two Pointers)?

- The array is **sorted**. This is the key property that lets us use the **two‑pointer technique** to find a pair that sums to a target in O(n) time and O(1) space.  
- **Why not a HashMap?**  
  A HashMap would give O(n) time, but O(n) space – violating the explicit “constant extra space” requirement. Hence two‑pointer is the intended optimal solution.  
- **How it works:**  
  Start with `left = 0` and `right = n‑1`.  
  - If `numbers[left] + numbers[right] == target`, return `[left+1, right+1]` (1‑based).  
  - If the sum is **less than** target, move `left` forward (we need a larger sum).  
  - If the sum is **greater**, move `right` backward (we need a smaller sum).  
  This converges in O(n) because each step discards one element, and no extra memory is used beyond two index variables.

---

### 🔨 Brute Force Approach (Not using the sorted property)

**Method:**  
Nested loops over all pairs `(i, j)` with `i < j`. If `numbers[i] + numbers[j] == target`, return `[i+1, j+1]`.

**Time:** O(n²)  
**Space:** O(1)

```java
public int[] twoSum(int[] numbers, int target) {
    int n = numbers.length;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (numbers[i] + numbers[j] == target) {
                return new int[] { i + 1, j + 1 };
            }
        }
    }
    return new int[] {}; // unreachable
}
```

Too slow for `n = 3×10⁴`.

---

### ⚡ Optimized Approach – Two Pointers (O(n) time, O(1) space)

**Method:**  
- `left = 0, right = numbers.length - 1`.  
- While `left < right`:  
  - `sum = numbers[left] + numbers[right]`.  
  - If `sum == target`, return `new int[]{left+1, right+1}`.  
  - If `sum < target`, `left++`.  
  - Else, `right--`.

**Time:** O(n) – each element visited at most once.  
**Space:** O(1) – only two variables.

```java
public int[] twoSum(int[] numbers, int target) {
    int left = 0, right = numbers.length - 1;
    while (left < right) {
        int sum = numbers[left] + numbers[right];
        if (sum == target) {
            return new int[] { left + 1, right + 1 };
        } else if (sum < target) {
            left++;
        } else {
            right--;
        }
    }
    return new int[] {}; // unreachable
}
```

---

### 📊 Solution Comparison & Trade‑offs

| Solution          | Time   | Space | Meets constant space? | Notes |
|-------------------|--------|-------|-----------------------|-------|
| Brute force       | O(n²)  | O(1)  | ✅ Yes (space) but too slow. | Simple, but fails for larger inputs. |
| Two pointers      | O(n)   | O(1)  | ✅ Yes                  | **Optimal**; exploits sorted order. |
| HashMap (not applicable) | O(n) | O(n) | ❌ No                   | Violates the “constant extra space” constraint; do not present as a solution. |

**Trade‑off:**  
The two‑pointer method sacrifices nothing – it’s both faster (linear) and uses constant space. The only reason to mention brute force is to show you can derive the linear approach from the sorted property.

---

### 🎯 What to Present to the Interviewer

1. Acknowledge the sorted input and the “constant extra space” requirement immediately.  
2. Dismiss the HashMap solution because it uses O(n) space.  
3. Propose the **two‑pointer technique** as the natural fit: start from both ends, adjust based on the sum compared to target.  
4. Walk through the algorithm with an example, showing why it works (the sorted property guarantees that moving the correct pointer won’t skip the solution).  
5. Write the concise Java code.  
6. Conclude with O(n) time, O(1) space – optimal and meets all constraints.

**One‑sentence summary:**  
*Since the array is sorted, two pointers converging from both ends find the target pair in O(n) time and O(1) space, meeting the constant‑space requirement perfectly.*