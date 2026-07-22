### 📘 Chapter: Arrays & Strings  
### 📌 Problem 10: Majority Element (LeetCode 169)

---

**Input**  
- `nums`: integer array of size `n`

**Output**  
- The majority element — the element that appears **more than** `⌊n / 2⌋` times.

**Constraints**  
- `n == nums.length`  
- `1 <= n <= 5 * 10⁴`  
- `-10⁹ <= nums[i] <= 10⁹`  
- A majority element **always exists** in the input.

**Follow-up**  
- Can you solve the problem in **O(n) time** and **O(1) space**?

---

### 🧠 Why this Approach / Data Structure?

The core problem: find an element that appears more than half the time. Guarantee of existence allows some clever elimination.

- **HashMap**: Counting frequencies with a HashMap gives O(n) time but O(n) space. It’s straightforward and often the first instinct. However, it does not meet the O(1) space follow‑up.

- **Boyer‑Moore Voting Algorithm**: This is the **optimal** solution. It’s O(n) time and O(1) extra space.  
  - Idea: maintain a `candidate` and a `count`. Traverse the array; when `count == 0`, pick the current element as new candidate. Increment count if current element equals candidate, decrement otherwise.  
  - Because the majority element appears more than n/2 times, it will always survive the elimination process and end up as the final candidate.  
  - No extra data structure needed, just two variables.

---

### 🔨 Brute Force Approach (Nested Loops)

**Method:**  
For each element, count its occurrences by scanning the whole array. If any count > n/2, return it.

**Time:** O(n²)  
**Space:** O(1)

```java
public int majorityElement(int[] nums) {
    int n = nums.length;
    for (int i = 0; i < n; i++) {
        int count = 0;
        for (int j = 0; j < n; j++) {
            if (nums[j] == nums[i]) count++;
        }
        if (count > n / 2) return nums[i];
    }
    return -1; // unreachable
}
```

Too slow for `n = 5×10⁴`.

---

### ⚡ Optimized Approach 1 – HashMap (O(n) time, O(n) space)

**Method:**  
Count frequencies with a HashMap. Return the key whose frequency > n/2.

**Time:** O(n) – single pass  
**Space:** O(n) – worst case all distinct

```java
public int majorityElement(int[] nums) {
    Map<Integer, Integer> freq = new HashMap<>();
    int n = nums.length;
    for (int num : nums) {
        freq.put(num, freq.getOrDefault(num, 0) + 1);
        if (freq.get(num) > n / 2) return num; // early exit
    }
    return -1; // unreachable
}
```

---

### ⚡ Optimized Approach 2 – Boyer‑Moore Voting Algorithm (O(n) time, O(1) space)

**Method:**  
- Initialize `candidate = 0` and `count = 0`.  
- For each `num`: if `count == 0`, set `candidate = num`. Then `count += (num == candidate) ? 1 : -1`.  
- Return `candidate`.

**Time:** O(n) – one pass  
**Space:** O(1)

```java
public int majorityElement(int[] nums) {
    int candidate = 0, count = 0;
    for (int num : nums) {
        if (count == 0) {
            candidate = num;
        }
        count += (num == candidate) ? 1 : -1;
    }
    return candidate;
}
```

**Why it works:**  
Majority element appears more than n/2 times; every other element combined appears less than n/2 times. The algorithm cancels pairs of different elements; the majority element cannot be fully cancelled, so it survives.

---

### 📊 Two-Solution Comparison & Trade-offs

| Solution               | Time   | Space | Meets Follow‑up? | Notes |
|------------------------|--------|-------|------------------|-------|
| HashMap frequency      | O(n)   | O(n)  | ❌ No            | Simple, intuitive, useful when majority is not guaranteed. |
| Boyer‑Moore voting     | O(n)   | O(1)  | ✅ Yes           | Clever, space‑optimal, only works if majority element exists. |

**Trade‑off:**  
- HashMap works even without the existence guarantee (if we check at the end) and is easy to understand.  
- Boyer‑Moore is the **interview target** for this exact problem because of the existence guarantee and the O(1) space requirement. It’s a classic algorithm that shows problem‑solving flair.

---

### 🎯 What to Present to the Interviewer

1. First, mention the trivial HashMap counting solution: O(n) time, O(n) space.  
2. Quickly acknowledge that the follow‑up asks for O(1) space, leading to Boyer‑Moore.  
3. Explain the Boyer‑Moore algorithm intuitively: “we cancel out different elements, and the majority element survives”.  
4. Write the concise Boyer‑Moore code.  
5. Emphasize that it’s O(n) time and O(1) space.  
6. If asked about verification (when existence not guaranteed), note that a second pass can count the candidate to confirm it’s truly the majority – but not required here.

**One‑sentence summary:**  
*Use Boyer‑Moore Voting Algorithm to find the majority element in O(n) time and O(1) space by maintaining a candidate and cancelling out opposing pairs.*