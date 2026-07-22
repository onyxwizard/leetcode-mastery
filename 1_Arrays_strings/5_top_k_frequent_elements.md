### 📘 Chapter: Arrays & Strings  
### 📌 Problem 5: Top K Frequent Elements (LeetCode 347)

---

**Input**  
- `nums`: integer array  
- `k`: integer – number of most frequent elements to return

**Output**  
- An array/list of the `k` most frequent elements (any order).

**Constraints**  
- `1 <= nums.length <= 10⁵`  
- `-10⁴ <= nums[i] <= 10⁴`  
- `1 <= k <= number of unique elements in nums`  
- The answer is guaranteed to be unique.

**Follow-up**  
- Your algorithm’s time complexity must be **better than O(n log n)**, where `n` is the array’s length.

---

### 🧠 Why this Data Structure?

1. **HashMap** – Counts frequencies of each number in O(n) time.  
2. For extracting the top `k` elements while beating O(n log n):  
   - **Min‑Heap (PriorityQueue)** of size `k` – gives O(n log k) average time.  
   - **Bucket sort** (array of lists indexed by frequency) – gives a strict O(n) time, no sorting at all.

The heap is classic, but bucket sort is the definitive answer to the follow‑up, as it guarantees O(n) time regardless of `k`.

---

### 🔨 Brute Force Approach (Sorting by Frequency)

**Method:**  
- Build a `HashMap` of frequencies.  
- Convert key set to a list, sort it by frequency descending using a custom comparator.  
- Take the first `k` elements.

**Time:** O(n + u log u) ≈ O(n log n) (where u ≤ n is the number of distinct elements)  
**Space:** O(n)  
❌ Does not meet follow‑up because `u log u` is O(n log n) in the worst case.

```java
// Not recommended for follow-up
public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int num : nums) freq.put(num, freq.getOrDefault(num, 0) + 1);
    List<Integer> unique = new ArrayList<>(freq.keySet());
    unique.sort((a, b) -> freq.get(b) - freq.get(a));
    int[] res = new int[k];
    for (int i = 0; i < k; i++) res[i] = unique.get(i);
    return res;
}
```

---

### ⚡ Optimized Approach 1 – Min‑Heap (PriorityQueue)

**Method:**  
- Count frequencies using a `HashMap`.  
- Use a min‑heap of size `k` (keeping the **k largest** frequencies).  
- Iterate through the map entries; offer to heap. If heap size exceeds `k`, poll the smallest frequency.  
- At the end, the heap contains the top `k` frequent elements.

**Time:** O(n log k) – when k ≪ n, it’s much faster than O(n log n).  
**Space:** O(n) for the map + O(k) for the heap.

```java
import java.util.*;

public int[] topKFrequent(int[] nums, int k) {
    // 1. Frequency map
    Map<Integer, Integer> freq = new HashMap<>();
    for (int num : nums) {
        freq.put(num, freq.getOrDefault(num, 0) + 1);
    }

    // 2. Min-heap by frequency
    PriorityQueue<Integer> heap = new PriorityQueue<>((a, b) -> freq.get(a) - freq.get(b));
    for (int num : freq.keySet()) {
        heap.offer(num);
        if (heap.size() > k) {
            heap.poll();
        }
    }

    // 3. Build result
    int[] res = new int[k];
    for (int i = 0; i < k; i++) {
        res[i] = heap.poll();   // order doesn't matter; poll yields ascending freq
    }
    return res;
}
```

---

### ⚡ Optimized Approach 2 – Bucket Sort (True O(n))

**Method:**  
- Count frequencies with `HashMap`.  
- Create an array of lists `buckets[]` where index = frequency. Max frequency ≤ `n`, so size `n+1`.  
- Place each number into the bucket corresponding to its frequency.  
- Iterate buckets from the highest frequency downwards, collecting numbers until we have `k` elements.

**Time:** O(n) – building map, filling buckets, and collecting results all linear.  
**Space:** O(n) – frequency map + bucket list array.

```java
public int[] topKFrequent(int[] nums, int k) {
    // 1. Frequency map
    Map<Integer, Integer> freq = new HashMap<>();
    for (int num : nums) {
        freq.put(num, freq.getOrDefault(num, 0) + 1);
    }

    // 2. Buckets: index = frequency
    List<Integer>[] buckets = new List[nums.length + 1];
    for (int key : freq.keySet()) {
        int f = freq.get(key);
        if (buckets[f] == null) {
            buckets[f] = new ArrayList<>();
        }
        buckets[f].add(key);
    }

    // 3. Gather top k from highest frequencies
    int[] res = new int[k];
    int idx = 0;
    for (int i = buckets.length - 1; i >= 0 && idx < k; i--) {
        if (buckets[i] != null) {
            for (int num : buckets[i]) {
                res[idx++] = num;
                if (idx == k) break;
            }
        }
    }
    return res;
}
```

---

### 📊 Solution Comparison & Trade-offs

| Solution             | Time      | Space   | Meets follow‑up? | Notes |
|----------------------|-----------|---------|------------------|-------|
| Sort by frequency    | O(n log n)| O(n)    | ❌ No            | Brute force, simple but too slow. |
| Min‑Heap (size k)    | O(n log k)| O(n)    | ⚠️ Not always    | Good when k ≪ n. Worst‑case k ≈ n gives O(n log n). |
| Bucket sort          | O(n)      | O(n)    | ✅ Yes           | **Strictly linear**, always meets follow‑up. |

**Trade‑off:**  
- **Min‑Heap** uses less extra memory for the top‑k structure (only `k` elements), and in many practical cases (`k` small) it’s very efficient. However, it still has a logarithmic factor.  
- **Bucket sort** is truly O(n) and is the only approach that **provably** beats O(n log n) for all inputs. It uses a full array of length `n+1` which might be slightly more memory, but it’s the safest answer for the follow‑up.

---

### 🎯 What to Present to the Interviewer

1. Start by counting frequencies with a `HashMap` – O(n).  
2. Explain the need to avoid a full sort (to beat O(n log n)).  
3. First, present the **min‑heap** solution (O(n log k)). Acknowledge that while it often beats O(n log n), worst‑case `k ≈ n` can still touch O(n log n).  
4. Then, present the **bucket sort** solution as the optimal answer. Emphasize that it’s O(n) time and O(n) space, fully meeting the follow‑up.  
5. Discuss space trade‑offs and when each might be preferred.

**One‑sentence summary:**  
*Count frequencies with a HashMap, then avoid full sorting by using either a size‑k min‑heap (O(n log k)) or bucket sort (O(n)) to extract the top k elements.*