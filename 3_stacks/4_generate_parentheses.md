### 📘 Chapter: Stack  
### 📌 Problem 4: Generate Parentheses (LeetCode 22)

---

**Input**  
- `n`: an integer representing the number of pairs of parentheses.

**Output**  
- A list of all **well‑formed parentheses strings** that can be formed with exactly `n` pairs.

**Constraints**  
- `1 <= n <= 8`

**Follow‑up**  
- Not explicitly given. (Common extensions: what if the number of pairs is larger? How does the time complexity grow? Can you generate them in lexicographical order? The Catalan number limits scalability.)

---

### 🧠 Why this Approach / Data Structure?

The problem asks for **all** valid combinations.  
- **Brute force:** generate **all** possible strings of length `2n` consisting of `'('` and `')'`, then filter each with a **stack** (or a balance counter) to check validity. This generates `2^(2n)` strings, many of which are invalid.  
- **Backtracking (optimal):** Instead of blindly generating all strings, we build the string character by character, respecting two simple rules:  
  - We can add an opening parenthesis `'('` if the number of `'('` used so far is less than `n`.  
  - We can add a closing parenthesis `')'` if the number of `')'` used so far is less than the number of `'('` used (ensuring we never close an unopened bracket).  
  This **directly** generates only valid sequences, dramatically reducing the search space. The number of valid strings is the nth Catalan number, which is approximately `O(4^n / (n^(3/2)))`, and we can’t do better than that because we must generate all of them.  
- No explicit stack is needed; the balance condition (`open > close`) guarantees validity.

---

### 🔨 Brute Force Approach (Generate All, Then Validate)

**Method:**  
- Generate all possible strings of length `2n` with `'('` and `')'` using recursion or bitmask.  
- For each string, check if it is a valid parentheses sequence using a **balance counter** (or stack).  
- A valid sequence has a running balance that never goes negative and ends at zero.

**Time:** O(2^(2n) * n) – `2^(2n)` strings, each validation O(n).  
**Space:** O(n) recursion depth (excluding output).

```java
public List<String> generateParenthesis(int n) {
    List<String> result = new ArrayList<>();
    generateAll(new char[2 * n], 0, result);
    return result;
}

private void generateAll(char[] current, int pos, List<String> result) {
    if (pos == current.length) {
        if (valid(current)) result.add(new String(current));
    } else {
        current[pos] = '(';
        generateAll(current, pos + 1, result);
        current[pos] = ')';
        generateAll(current, pos + 1, result);
    }
}

private boolean valid(char[] current) {
    int balance = 0;
    for (char c : current) {
        if (c == '(') balance++;
        else balance--;
        if (balance < 0) return false;
    }
    return balance == 0;
}
```

Too slow even for `n=8` (2^16 = 65,536 strings, still okay for n=8? Actually n=8 => 2^16=65536, each validation O(16) = ~1M ops, maybe acceptable for small n, but not general. However, it wastes work generating many invalid strings.)

---

### ⚡ Optimized Approach – Backtracking (Only Valid Sequences)

**Method:**  
- Use a recursive `backtrack` function that builds the string and keeps track of counts of `open` and `close` parentheses used.  
- At each step:  
  - If `open < n`, we can add `'('` and recurse with `open+1`.  
  - If `close < open`, we can add `')'` and recurse with `close+1`.  
- When `open == n` and `close == n`, add the built string to result.

**Time:** O(4^n / sqrt(n)) – the number of valid parentheses strings (Catalan number). This is optimal because we must generate all of them.  
**Space:** O(n) recursion depth (and output storage).

```java
import java.util.*;

public List<String> generateParenthesis(int n) {
    List<String> result = new ArrayList<>();
    backtrack(result, new StringBuilder(), 0, 0, n);
    return result;
}

private void backtrack(List<String> result, StringBuilder sb, int open, int close, int max) {
    if (sb.length() == max * 2) {
        result.add(sb.toString());
        return;
    }
    if (open < max) {
        sb.append('(');
        backtrack(result, sb, open + 1, close, max);
        sb.deleteCharAt(sb.length() - 1);
    }
    if (close < open) {
        sb.append(')');
        backtrack(result, sb, open, close + 1, max);
        sb.deleteCharAt(sb.length() - 1);
    }
}
```

---

### 📊 Solution Comparison & Trade‑offs

| Solution                     | Time (worst‑case)       | Space   | Approach |
|------------------------------|-------------------------|---------|----------|
| Brute force (generate + filter) | O(2^(2n) * n)        | O(n)    | Very simple, but wastes effort on invalid strings. |
| Backtracking                 | O(Catalan number) ≈ O(4^n / n^(3/2)) | O(n) recursion | **Optimal**; directly builds only valid strings. |

**Trade‑off:**  
- Brute force is easy to conceive but does not scale; it is only mentioned as a stepping stone.  
- Backtracking is the **standard and expected** solution; it prunes the search space based on the simple balance rule.  
- Another approach (Closure Number / DP) builds valid strings from smaller valid sub‑problems: `"(" + left + ")" + right`. It has the same asymptotic time but often uses more memory due to storing intermediate lists. It’s nice to mention as an alternative view, but backtracking is the most direct.

---

### 🎯 What to Present to the Interviewer

1. Recognise that this is a combinatorics generation problem; the output size is Catalan number, so we can’t do better than exponential in n.  
2. Briefly sketch the brute‑force method (generate all then validate) to show the baseline.  
3. Propose the **backtracking** method: maintain counts of `open` and `close` used, only add paren when it keeps the sequence valid.  
4. Walk through the recursive algorithm, explaining why we never need an explicit stack to check validity (the balance is encoded in the counts).  
5. Write the clean Java code with `StringBuilder` for efficiency and proper backtracking (append then deleteCharAt).  
6. Analyse complexity: time proportional to the nth Catalan number, space O(n) for recursion depth.  
7. If asked, mention the DP / closure number approach as an alternative, but state that backtracking is simpler and optimal.

**One‑sentence summary:**  
*Use backtracking to build valid strings character by character, only adding `'('` if the count of opens is less than `n`, and `')'` if closes are fewer than opens, thereby generating all well‑formed parentheses directly in O(Catalan) time.*