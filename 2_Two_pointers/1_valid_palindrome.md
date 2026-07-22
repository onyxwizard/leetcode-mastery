### 📘 Chapter: Two Pointers  
### 📌 Problem 1: Valid Palindrome (LeetCode 125)

---

**Input**  
- `s`: a string containing printable ASCII characters

**Output**  
- `true` if after converting all uppercase letters to lowercase and removing all non‑alphanumeric characters, the string reads the same forward and backward; otherwise `false`.

**Constraints**  
- `1 <= s.length <= 2 * 10⁵`  
- `s` consists only of printable ASCII characters

**Follow-up**  
- None explicitly stated in the problem.

---

### 🧠 Why this Approach?

A palindrome check naturally uses **two pointers** starting from the ends and moving inward.  
However, the problem requires us to ignore non‑alphanumeric characters and treat letters case‑insensitively.  

- The key data structure is just the input string; no extra storage is needed.  
- Using two pointers **directly on the original string**, we can skip non‑alphanumeric characters on the fly using `Character.isLetterOrDigit()` and compare characters using `Character.toLowerCase()`.  
- This yields **O(1) extra space** and O(n) time, which is optimal.

**Alternative:** Build a cleaned version of the string first, then check palindrome. This is O(n) time but O(n) space. It’s simpler to code but not as space‑efficient. In interviews, the in‑place two‑pointer solution is expected.

---

### 🔨 Brute Force / Simpler Approach (Filtered String)

**Method:**  
1. Create a new `StringBuilder` (or `ArrayList<Character>`) and append only lowercase alphanumeric characters from `s`.  
2. Check if this cleaned string equals its reverse (or use two pointers on the cleaned string).

**Time:** O(n) – one pass to filter + one pass to compare  
**Space:** O(n) – storing the cleaned string

```java
public boolean isPalindrome(String s) {
    StringBuilder clean = new StringBuilder();
    for (char c : s.toCharArray()) {
        if (Character.isLetterOrDigit(c)) {
            clean.append(Character.toLowerCase(c));
        }
    }
    String cleanStr = clean.toString();
    int left = 0, right = cleanStr.length() - 1;
    while (left < right) {
        if (cleanStr.charAt(left) != cleanStr.charAt(right)) return false;
        left++;
        right--;
    }
    return true;
}
```

---

### ⚡ Optimized Approach – Two Pointers In‑place (O(1) Space)

**Method:**  
- Use two pointers `left = 0`, `right = s.length() - 1`.  
- While `left < right`:  
  - Advance `left` while it is not alphanumeric.  
  - Decrement `right` while it is not alphanumeric.  
  - If `Character.toLowerCase(s.charAt(left)) != Character.toLowerCase(s.charAt(right))`, return `false`.  
  - Else, move both pointers inward.

**Time:** O(n) – each character examined at most once  
**Space:** O(1) – no extra array or string

```java
public boolean isPalindrome(String s) {
    int left = 0, right = s.length() - 1;
    while (left < right) {
        // skip non-alphanumeric from left
        while (left < right && !Character.isLetterOrDigit(s.charAt(left))) {
            left++;
        }
        // skip non-alphanumeric from right
        while (left < right && !Character.isLetterOrDigit(s.charAt(right))) {
            right--;
        }
        // compare
        if (Character.toLowerCase(s.charAt(left)) != 
            Character.toLowerCase(s.charAt(right))) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}
```

---

### 📊 Two‑Solution Comparison & Trade-offs

| Solution                   | Time | Space | Notes |
|----------------------------|------|-------|-------|
| Filter + two‑pointer/reverse | O(n) | O(n)  | Very clear, but allocates extra string. |
| Direct two‑pointer on `s`  | O(n) | O(1)  | **Optimal space**, slightly more logic for skipping. Best answer. |

**Trade‑off:**  
The filtering approach is arguably easier to read, but the in‑place two‑pointer method demonstrates stronger mastery of constraints (large input size) and minimizes memory. In an interview, presenting the O(1) space version is the goal.

---

### 🎯 What to Present to the Interviewer

1. Start by explaining that a palindrome check suggests two pointers.  
2. Mention the filtering approach as a quick‑to‑code baseline with O(n) space.  
3. Then present the **two‑pointer in‑place** approach, step by step: skip non‑alphanumeric, compare case‑insensitively.  
4. Highlight that this uses O(1) extra space and O(n) time, which is ideal.  
5. Be ready to discuss Java’s `Character.isLetterOrDigit()` and `Character.toLowerCase()` methods.

**One‑sentence summary:**  
*Use two pointers to skip non‑alphanumeric characters and compare the lowercase letters directly in the original string for O(n) time and O(1) space.*