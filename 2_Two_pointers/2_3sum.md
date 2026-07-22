### 📘 Chapter: Two Pointers  
### 📌 Problem 2: 3Sum (LeetCode 15)

---

**Input**  
- `nums`: integer array

**Output**  
- All unique triplets `[nums[i], nums[j], nums[k]]` such that `i != j != k` and `nums[i] + nums[j] + nums[k] == 0`. No duplicate triplets.

**Constraints**  
- `3 <= nums.length <= 3000`  
- `-10⁵ <= nums[i] <= 10⁵`

**Follow-up**  
- The problem inherently requires an algorithm better than O(n³). The standard follow‑up is to achieve **O(n²)** time and handle duplicate triplets correctly.

---

### 🧠 Why this Approach / Data Structure?

The problem is an extension of Two Sum, but with three numbers and the requirement to return **all unique triplets**.  

- **Sorting the array** first achieves two things:  
  1. It lets us use the **two‑pointer technique** to find a pair that sums to a target value in O(n) time.  
  2. It makes duplicate skipping easy – identical values become adjacent, so we can skip them while iterating.

- For each element `nums[i]` (acting as the first element), we set a target `-nums[i]` and use two pointers (`left = i+1`, `right = n-1`) to find pairs that sum to that target.  
- This reduces the time from O(n³) to **O(n²)**.  
- The two‑pointer approach uses **O(1) extra space** (ignoring the output list) because we only move indices.

- **Alternative (HashSet):** We could use a HashSet to store complements while iterating, but deduplication of triplets becomes tricky and often requires extra storage or sorting anyway. Sorting + two pointers is the gold standard.

---

### 🔨 Brute Force Approach (Three Nested Loops)

**Method:**  
Try all triplets `(i, j, k)` with `i < j < k`. If sum is zero, add to result. To avoid duplicate triplets, use a `Set<List<Integer>>` to store sorted triplets.

**Time:** O(n³) – checking all combinations  
**Space:** O(n) for the set of unique triplets

```java
public List<List<Integer>> threeSum(int[] nums) {
    int n = nums.length;
    Set<List<Integer>> resultSet = new HashSet<>();
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            for (int k = j + 1; k < n; k++) {
                if (nums[i] + nums[j] + nums[k] == 0) {
                    List<Integer> triplet = Arrays.asList(nums[i], nums[j], nums[k]);
                    Collections.sort(triplet);
                    resultSet.add(triplet);
                }
            }
        }
    }
    return new ArrayList<>(resultSet);
}
```

Too slow for `n = 3000`.

---

### ⚡ Optimized Approach 1 – Sorting + Two Pointers (O(n²))

**Method:**  
1. Sort `nums`.  
2. Iterate `i` from `0` to `n-3`. If `i > 0` and `nums[i] == nums[i-1]`, skip to avoid duplicate first elements.  
3. For each `i`, set `left = i+1`, `right = n-1`. While `left < right`:  
   - `sum = nums[i] + nums[left] + nums[right]`  
   - If `sum == 0`: add triplet, then skip duplicates for left and right by moving them until new values. Then `left++; right--`.  
   - If `sum < 0`: `left++`.  
   - If `sum > 0`: `right--`.

**Time:** O(n²) – outer loop O(n), inner two-pointer O(n)  
**Space:** O(1) extra (output list not counted) – sorting may use O(log n) stack, but typically considered O(1) extra in this context.

```java
public List<List<Integer>> threeSum(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    Arrays.sort(nums);
    int n = nums.length;

    for (int i = 0; i < n - 2; i++) {
        if (i > 0 && nums[i] == nums[i - 1]) continue; // skip duplicate i

        int left = i + 1, right = n - 1;
        int target = -nums[i];

        while (left < right) {
            int sum = nums[left] + nums[right];
            if (sum == target) {
                result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                // skip duplicates for left and right
                while (left < right && nums[left] == nums[left + 1]) left++;
                while (left < right && nums[right] == nums[right - 1]) right--;
                left++;
                right--;
            } else if (sum < target) {
                left++;
            } else {
                right--;
            }
        }
    }
    return result;
}
```

---

### ⚡ Optimized Approach 2 – HashSet (Still O(n²))

**Method:**  
- Sort the array (to help deduplicate easily) or use a HashSet for seen pairs.  
- For each `i`, use a HashSet to store numbers seen as we iterate `j` from `i+1` to end.  
- Compute complement `-nums[i] - nums[j]`. If it exists in set, we found a triplet.  
- To avoid duplicates, sort the triplet and use a `Set<List<Integer>>` (or use sorting of array and skip duplicate `i` and `j`).  

Usually less efficient than two-pointer due to hashing overhead and memory, but demonstrates alternative thinking.

**Time:** O(n²) on average  
**Space:** O(n) for the hashset + O(unique triplets) output.

```java
public List<List<Integer>> threeSum(int[] nums) {
    Set<List<Integer>> resultSet = new HashSet<>();
    Arrays.sort(nums); // helps deduplicate
    for (int i = 0; i < nums.length - 2; i++) {
        if (i > 0 && nums[i] == nums[i - 1]) continue;
        Set<Integer> seen = new HashSet<>();
        for (int j = i + 1; j < nums.length; j++) {
            int complement = -nums[i] - nums[j];
            if (seen.contains(complement)) {
                resultSet.add(Arrays.asList(nums[i], nums[j], complement));
                // still need to skip duplicate j manually? The set handles triplet dedup but not efficiently
            }
            seen.add(nums[j]);
        }
    }
    return new ArrayList<>(resultSet);
}
```
*Note:* This HashSet approach may still include duplicate triplets if not careful; sorting and skipping duplicate `j` values is needed, making it less clean.

---

### 📊 Two‑Solution Comparison & Trade‑offs

| Solution                    | Time   | Space (extra) | Duplicate Handling | Notes |
|-----------------------------|--------|---------------|-------------------|-------|
| Sorting + Two Pointers      | O(n²)  | O(1)          | Easy via skipping  | **Industry standard**; optimal memory. |
| HashSet (Two Sum on sorted) | O(n²)  | O(n)          | Requires a set or manual skip | Simpler logic but uses more memory; more edge cases. |

**Trade‑off:**  
- Sorting + two pointers is always preferred because it uses no extra storage and elegantly avoids duplicates by pointer skipping.  
- HashSet approach is a direct extension of Two Sum with a hash map, but managing duplicate triplets is messier and memory usage is higher.  
- In an interview, presenting the two‑pointer approach is expected; the HashSet can be mentioned as an alternative if you can’t initially think of two pointers.

---

### 🎯 What to Present to the Interviewer

1. First, state the O(n³) brute force to clarify the baseline.  
2. Propose **sorting** to enable the two‑pointer technique, which reduces Two Sum from O(n²) to O(n) per outer element.  
3. Walk through the **two‑pointer algorithm**: fix `i`, then adjust `left` and `right` based on the sum relative to target.  
4. Emphasize how duplicate handling works by skipping identical values for `i`, `left`, and `right`.  
5. Code the solution cleanly.  
6. If asked, contrast with the HashSet approach and explain why sorting+two-pointer is superior in space and code clarity.

**One‑sentence summary:**  
*Sort the array, then for each element use two pointers to find complementary pairs that sum to the negative of that element, skipping duplicates to collect all unique triplets in O(n²) time.*