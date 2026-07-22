### 📘 Chapter: Arrays & Strings  
### 📌 Problem 6: Product of Array Except Self (LeetCode 238)

---

**Input**  
- `nums`: integer array

**Output**  
- `answer[]`: integer array where `answer[i]` is the product of all elements in `nums` except `nums[i]`

**Constraints**  
- `2 <= nums.length <= 10⁵`  
- `-30 <= nums[i] <= 30`  
- Product of any prefix/suffix fits in a 32‑bit integer (no overflow for intermediate steps if done correctly)  
- Division is **not allowed**.

**Follow-up**  
- Solve in **O(1) extra space** complexity. (The output array does **not** count as extra space.)

---

### 🧠 Why this Approach / Data Structure?

No special data structure beyond arrays is required. The core pattern is **Prefix and Suffix Products**.

- The answer for index `i` = (product of all elements before `i`) × (product of all elements after `i`).
- We can compute these in two passes:
  1. **Left pass**: Build an array where `answer[i]` = product of all elements left of `i`.
  2. **Right pass**: Multiply each `answer[i]` by a running product of all elements right of `i`.
- This gives **O(n) time** without division, and we can reuse the output array to keep **extra space O(1)**.

Why not division? It’s forbidden, and it would fail when zeros are present. The prefix‑suffix method handles zeros seamlessly.

---

### 🔨 Brute Force Approach

**Method:**  
For each index `i`, loop through the whole array and multiply all elements except `nums[i]`.

**Time:** O(n²)  
**Space:** O(1) (excluding output array, which is required anyways)

```java
public int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] answer = new int[n];
    for (int i = 0; i < n; i++) {
        int prod = 1;
        for (int j = 0; j < n; j++) {
            if (i != j) prod *= nums[j];
        }
        answer[i] = prod;
    }
    return answer;
}
```

Too slow for `n = 10⁵` — the O(n²) approach times out.

---

### ⚡ Optimized Approach 1 – Left & Right Product Arrays

**Method:**  
- Create two additional arrays: `left[i]` = product of all elements to the left of `i`; `right[i]` = product of all elements to the right of `i`.  
- Then `answer[i] = left[i] * right[i]`.

**Time:** O(n) – three passes (left, right, combine)  
**Space:** O(n) – two extra arrays of size n

```java
public int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] left = new int[n];
    int[] right = new int[n];
    int[] answer = new int[n];

    left[0] = 1;
    for (int i = 1; i < n; i++) {
        left[i] = left[i - 1] * nums[i - 1];
    }

    right[n - 1] = 1;
    for (int i = n - 2; i >= 0; i--) {
        right[i] = right[i + 1] * nums[i + 1];
    }

    for (int i = 0; i < n; i++) {
        answer[i] = left[i] * right[i];
    }
    return answer;
}
```

---

### ⚡ Optimized Approach 2 – O(1) Extra Space (Output Array Only)

**Method:**  
- Use the output array to store **prefix products** (equivalent to `left[]`).  
- Then traverse from the right, maintaining a `suffix` variable that holds the product of all elements seen so far on the right.  
- Multiply `answer[i]` by `suffix`, then update `suffix *= nums[i]`.

**Time:** O(n) – two passes  
**Space:** O(1) extra (the output array is not counted as extra space)

```java
public int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] answer = new int[n];

    // Left pass: answer[i] = product of all elements to the left of i
    answer[0] = 1;
    for (int i = 1; i < n; i++) {
        answer[i] = answer[i - 1] * nums[i - 1];
    }

    // Right pass: multiply by suffix product
    int suffix = 1;
    for (int i = n - 1; i >= 0; i--) {
        answer[i] *= suffix;
        suffix *= nums[i];
    }

    return answer;
}
```

---

### 📊 Solution Comparison & Trade-offs

| Solution                   | Time | Space (extra) | Meets Follow‑up? | Notes |
|----------------------------|------|---------------|------------------|-------|
| Brute force (nested loops) | O(n²) | O(1)          | ❌ No            | Fails for large inputs. |
| Left & Right arrays        | O(n)  | O(n)          | ❌ No            | Clear but uses extra arrays; good stepping stone. |
| Output array as left + suffix variable | O(n)  | O(1)    | ✅ Yes          | **Optimal** – uses only output array + one int. |

**Trade‑off:**  
The two‑array solution is more readable and separates the left/right logic cleanly. The O(1) space version is the elegant, production‑ready solution that the interviewer expects for the follow‑up. It is slightly more subtle but still straightforward.

---

### 🎯 What to Present to the Interviewer

1. Clarify that division is disallowed, and O(n) time is required.  
2. Start with the **left/right arrays** approach to demonstrate the prefix/suffix concept clearly.  
3. Then immediately transition to the **O(1) space** solution: use the output array to store left products and a running suffix variable to update in‑place.  
4. Walk through the code with an example.  
5. Emphasize that this meets the follow‑up and works correctly even when zeros are present.

**One‑sentence summary:**  
*Compute prefix products into the output array, then traverse backwards multiplying by a running suffix product — O(n) time, O(1) extra space, no division.*