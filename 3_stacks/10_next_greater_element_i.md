### 📘 Chapter: Stack  
### 📌 Problem 10: Next Greater Element I (LeetCode 496)

---

**Input**  
- `nums1`: an array of unique integers, which is a subset of `nums2`.  
- `nums2`: an array of unique integers that contains all elements of `nums1`.

**Output**  
- An array `ans` of length `nums1.length` where `ans[i]` is the **next greater element** for `nums1[i]` as found in `nums2`.  
- The next greater element of a value `x` in `nums2` is the first element to the right of `x` in `nums2` that is **greater than `x`**.  
- If no such element exists, the answer is `-1`.

**Constraints**  
- `1 <= nums1.length <= nums2.length <= 1000`  
- `0 <= nums1[i], nums2[i] <= 10⁴`  
- All integers in `nums1` and `nums2` are unique.  
- Every element of `nums1` appears in `nums2`.

**Follow‑up**  
- Could you find an **O(nums1.length + nums2.length)** solution?

---

### 🧠 Why this Data Structure (Monotonic Stack + HashMap)?

The core task is to find the **next greater element** for every element in `nums2`, then quickly look up the answers for the subset `nums1`.  

- **Monotonic decreasing stack** is the classic tool for “Next Greater Element” problems:  
  - We traverse `nums2` from left to right.  
  - While the stack is not empty and the current element is greater than the top element on the stack, we pop the top element — its **next greater element** is the current element.  
  - We record this mapping in a `HashMap`.  
  - After checking, we push the current element onto the stack.  
  - Elements left in the stack after the traversal have no next greater element, mapping to `-1`.  
- This processes each element of `nums2` once (push and pop at most once) → **O(n)** time where n = `nums2.length`.  
- The `HashMap` then allows O(1) lookup for each element in `nums1`, giving total time **O(n + m)** meeting the follow‑up.

---

### 🔨 Brute Force Approach (Direct Search for Each Element)

**Method:**  
For each element `val` in `nums1`, find its index in `nums2`, then scan to the right looking for the first larger element.

**Time:** O(m * n) where `m = nums1.length`, `n = nums2.length`. In worst case, `m ≈ n`, so O(n²).  
**Space:** O(1) extra (excluding output array).

```java
public int[] nextGreaterElement(int[] nums1, int[] nums2) {
    int[] ans = new int[nums1.length];
    for (int i = 0; i < nums1.length; i++) {
        int val = nums1[i];
        int j = 0;
        // find index of val in nums2
        while (nums2[j] != val) j++;
        // search for next greater
        int nextGreater = -1;
        for (int k = j + 1; k < nums2.length; k++) {
            if (nums2[k] > val) {
                nextGreater = nums2[k];
                break;
            }
        }
        ans[i] = nextGreater;
    }
    return ans;
}
```

---

### ⚡ Optimized Approach – Monotonic Stack + HashMap (O(n + m) time)

**Method:**  
1. Initialize a `HashMap<Integer, Integer>` to store the next greater element for each number in `nums2`.  
2. Use a `Deque<Integer>` (stack) that stores numbers in a **monotonically decreasing** order (from bottom to top).  
3. Iterate over `nums2`:
   - While stack is not empty and `current > stack.peek()`:
     - Pop the top and put `(popped, current)` into the map.  
   - Push `current`.  
4. After the loop, any numbers remaining in the stack have no next greater element — they implicitly map to `-1`.  
5. Build the result for `nums1` by looking up each element in the map; if not present, use `-1`.

**Time:** O(n + m) — `nums2` processed once, `nums1` looked up once.  
**Space:** O(n) — for the stack and the hashmap.

```java
import java.util.*;

public int[] nextGreaterElement(int[] nums1, int[] nums2) {
    Map<Integer, Integer> nextGreater = new HashMap<>();
    Deque<Integer> stack = new ArrayDeque<>();

    for (int num : nums2) {
        while (!stack.isEmpty() && stack.peek() < num) {
            nextGreater.put(stack.pop(), num);
        }
        stack.push(num);
    }
    // elements left in stack have no next greater element, 
    // they are implicitly -1, so we don't need to store them.

    int[] ans = new int[nums1.length];
    for (int i = 0; i < nums1.length; i++) {
        ans[i] = nextGreater.getOrDefault(nums1[i], -1);
    }
    return ans;
}
```

---

### 📊 Solution Comparison & Trade‑offs

| Solution                      | Time   | Space  | Follow‑up? |
|-------------------------------|--------|--------|------------|
| Brute force (scan per element)| O(m·n) | O(1)   | ❌ No      |
| Monotonic stack + HashMap     | O(n+m) | O(n)   | ✅ Yes     |

**Trade‑off:**  
- The brute force is simple but quadratic in worst case.  
- The stack solution trades O(n) extra space for O(n) time, exactly meeting the follow‑up requirement.  
- Since the constraints here are small (≤1000), brute force is acceptable, but the stack method demonstrates the optimal pattern that extends to larger constraints.

---

### 🎯 What to Present to the Interviewer

1. Recognize this is the **Next Greater Element** problem, naturally solved by a **monotonic decreasing stack**.  
2. First, describe the straightforward O(m·n) brute force to establish the baseline.  
3. Then propose the optimal approach: preprocess `nums2` with a stack to compute the next greater element for all its numbers in **one pass**.  
4. Explain the algorithm step‑by‑step: maintain a decreasing stack; when a larger number appears, it resolves the next greater element for the popped smaller numbers.  
5. Use a `HashMap` to store these mappings, then simply query it for each element in `nums1`.  
6. Write the clean Java code.  
7. State complexities: O(n + m) time, O(n) space – satisfying the follow‑up.  
8. Mention that elements left in the stack have no next greater element, so they map to `-1`.

**One‑sentence summary:**  
*Use a monotonic decreasing stack to compute the next greater element for every element in `nums2` in one pass, store results in a HashMap, then answer queries for `nums1` in O(n + m) time.*