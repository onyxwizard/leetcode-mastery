### 📘 Chapter: Arrays & Strings  
### 📌 Problem 1: Two Sum (LeetCode 1)

---

**Input**  
- `nums`: integer array (`int[]`)  
- `target`: integer (`int`)

**Output**  
- Indices of the two numbers that sum to `target`, returned as `int[]` (any order).

**Constraints**  
- `2 <= nums.length <= 10⁴`  
- `-10⁹ <= nums[i] <= 10⁹`  
- `-10⁹ <= target <= 10⁹`  
- Exactly one valid answer exists; same element cannot be used twice.

**Follow-up**  
- Can you devise an algorithm with time complexity better than O(n²)?

---

### 🧠 Why this Data Structure?

**HashMap** (`java.util.HashMap<Integer, Integer>`)  
The core operation is checking whether the complement (`target - current number`) has already been seen.  
- A `HashMap` provides **O(1) average** time for `containsKey()` and `put()`.  
- It maps each number (key) to its index (value).  
- This directly replaces the nested loop, reducing time from O(n²) to O(n).

*Alternative considered:* Sorting + two pointers. Sorting would require storing (value, original index) pairs, then sorting by value – still O(n log n) time and more code. The `HashMap` approach is simpler and optimal when original indices must be returned.

---

### 🔨 Brute Force Approach

**Method:** Nested loops  
Check every pair `(i, j)` with `i < j`. If `nums[i] + nums[j] == target`, return `new int[] {i, j}`.

**Time:** O(n²)  
**Space:** O(1)

```java
public int[] twoSum(int[] nums, int target) {
    int n = nums.length;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (nums[i] + nums[j] == target) {
                return new int[] {i, j};
            }
        }
    }
    return new int[] {}; // unreachable due to constraints
}
```

---

### ⚡ Optimized Approach (HashMap – One Pass)

**Method:**  
Iterate once. For each number, compute its complement.  
- If complement exists in the map, return `new int[] {stored index, current index}`.  
- Otherwise, store `(current number, current index)` in the map.

**Time:** O(n) – single pass  
**Space:** O(n) – `HashMap` stores at most `n` entries

```java
import java.util.HashMap;
import java.util.Map;

public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int comp = target - nums[i];
        if (seen.containsKey(comp)) {
            return new int[] { seen.get(comp), i };
        }
        seen.put(nums[i], i);
    }
    return new int[] {}; // unreachable
}
```

---

### 📊 Two-Solution Comparison & Trade-offs

| Solution               | Time   | Space  | Notes                                 |
|------------------------|--------|--------|---------------------------------------|
| Brute force (nested)   | O(n²)  | O(1)   | Simple, no extra memory, too slow for large `n`. |
| HashMap (one-pass)     | O(n)   | O(n)   | **Interview standard** for returning indices; trades space for speed. |

*(Two-pointer on a sorted array is omitted here because it cannot return original indices without extra work; it’s more appropriate for value‑only or boolean return variants.)*

---

### 🎯 What to Present to the Interviewer

- Start by stating the brute‑force O(n²) solution to show you understand the baseline.  
- Immediately propose the **O(n)** hash map approach to meet the follow‑up requirement.  
- Implement the **one‑pass `HashMap`** solution cleanly in Java.  
- Discuss time/space trade‑off: O(n) time achieved by using O(n) space.  
- Mention that if only values (not indices) were needed, sorting + two pointers (O(n log n), O(1) space) would be a space‑optimised alternative, but for indices the `HashMap` is optimal.

**One‑sentence summary:**  
*Use a `HashMap<Integer, Integer>` to remember seen numbers and their indices, enabling O(n) time by checking for the complement in O(1).*