### 📘 Chapter: Arrays & Strings  
### 📌 Problem 9: Encode and Decode Strings (LeetCode 271)

---

**Input**  
- `encode`: a list of strings `strs`  
- `decode`: a single `String` (the encoded form)

**Output**  
- `encode` returns a single `String`  
- `decode` returns the original `List<String>`

**Constraints**  
- `0 <= strs.length < 100`  
- `0 <= strs[i].length < 200`  
- `strs[i]` may contain **any** character from the 256 valid ASCII characters (including special chars like `#`, `,`, `\n`, etc.)

**Follow-up**  
- Could you write a generalized algorithm to work on **any possible set of characters** (e.g., full Unicode)?

---

### 🧠 Why this Approach / Encoding Scheme?

The key challenge: strings can contain **any** character, so we cannot choose a single delimiter character that is guaranteed never to appear inside a string.

The standard robust solution is **length‑prefixing**:
- For each string, we prepend its length, followed by a delimiter that we **only** parse as a separator between length and string (e.g., `#`), then the string itself.
- Example: `["Hello", "World"]` → `"5#Hello5#World"`.
- During decoding, we scan for `#`, parse the preceding number as the length, then read exactly that many characters.  
- This works because we **never interpret the string’s contents** – we use the length to jump to the end of the string.

**Why not a simple delimiter?**  
If we pick `#` as a separator, the encoded form might be `"Hello#World"`, but how do we know if the original was `["Hello", "World"]` or `["Hello#World"]`? The delimiter is ambiguous.

**Why not use a non‑ASCII delimiter?**  
The input is restricted to 256 ASCII characters, but the follow‑up asks for a solution that handles **any** characters. Relying on a “safe” character (e.g., a Unicode char) is not future‑proof and not general. The length‑prefix method is independent of character set and is the definitive answer.

**Data structure:** Just a `StringBuilder` for encoding and simple index‑parsing for decoding – no complex data structures needed.

---

### 🔨 Naive / Simple Approach (Unsafe Delimiter)

**Method:**  
Choose a delimiter (e.g., `"#,#"`) and join strings. Hope that the delimiter never appears inside any string.

**Time:** O(n) for join/split  
**Space:** O(n)  
❌ **Not safe** for arbitrary ASCII strings, and certainly not generalizable. This fails silently if a string contains the delimiter.

```java
// NOT a valid solution for the problem constraints
public String encode(List<String> strs) {
    return String.join("#,#", strs);
}
public List<String> decode(String s) {
    return Arrays.asList(s.split("#,#"));
}
```
This is only for illustration – it would not pass an interview for this problem.

---

### ⚡ Optimized Approach – Length‑Prefix Encoding

**Encoding scheme:**  
`length + "#" + string` for each string, concatenated.

**Encoding method:**
- Use a `StringBuilder`.
- For each string in the list, append `str.length()`, then `'#'`, then the string itself.

**Decoding method:**
- Iterate through the encoded string with a pointer `i`.
- Find the next `'#'` starting at `i`.
- The substring from `i` to `'#'` is the length as a string – parse it to `len`.
- The actual string is the next `len` characters after `'#'`.
- Add it to the result, advance `i` to the position after that string.

**Time:** O(n) – each character of all strings is processed exactly once during encoding and once during decoding.  
**Space:** O(n) – for the encoded string and the output list.

```java
import java.util.*;

public class Codec {

    // Encodes a list of strings to a single string.
    public String encode(List<String> strs) {
        StringBuilder sb = new StringBuilder();
        for (String s : strs) {
            sb.append(s.length()).append('#').append(s);
        }
        return sb.toString();
    }

    // Decodes a single string to a list of strings.
    public List<String> decode(String s) {
        List<String> result = new ArrayList<>();
        int i = 0;
        while (i < s.length()) {
            // find the delimiter
            int j = i;
            while (s.charAt(j) != '#') j++;
            int len = Integer.parseInt(s.substring(i, j)); // length of next string
            i = j + 1; // skip '#'
            String str = s.substring(i, i + len);
            result.add(str);
            i += len; // move past the string
        }
        return result;
    }
}
```

**Handling of empty strings:**  
If a string is `""`, its encoded form is `"0#"`, and during decoding `len = 0`, so the substring from `i` to `i+0` is `""` – correct.

---

### 🌍 Follow‑up: Generalizing for Any Character Set (Unicode)

The length‑prefix method **already works for any possible set of characters** because:
- We only treat the **length part** as a numeric string followed by a known delimiter (`#`).
- The string portion is read byte‑by‑byte (or `char` by `char` in Java, which covers UTF‑16) exactly `len` times, without interpreting its content.
- Therefore, the algorithm is immediately applicable to Unicode strings, emojis, or any binary data represented as a string of characters.

No modification is needed. The interviewer might want you to state that this approach is inherently character‑set‑agnostic.

---

### 📊 Comparison & Trade‑offs

| Encoding Strategy        | Handles all ASCII? | Handles Unicode? | Robust? | Complexity |
|--------------------------|--------------------|-------------------|---------|------------|
| Simple delimiter (e.g., `","`) | ❌ No (if delimiter appears in strings) | ❌ No | Fragile | Trivial |
| Non‑ASCII delimiter      | ⚠️ Only ASCII | ❌ No (delimiter could appear in Unicode) | Not general | Simple |
| **Length‑prefix**        | ✅ Yes            | ✅ Yes            | ✅ Rock‑solid | Standard |

**Trade‑off:**  
- Length‑prefixing uses a small amount of extra space for the length and delimiter (at most `log₁₀(len)+1` chars per string).  
- It is extremely simple to implement and is the **industry standard** for serialising strings with arbitrary content (e.g., in protocols like Netstring, Redis’s bulk strings).

---

### 🎯 What to Present to the Interviewer

1. Immediately recognize the core problem: **no safe delimiter** because strings can contain any character.  
2. Propose **length‑prefixing**: `length + '#' + string`.  
3. Walk through the `encode` method with a `StringBuilder`.  
4. Walk through the `decode` method, showing how you locate `#`, parse the length, extract exactly that many characters, and advance the pointer.  
5. Explain that this handles empty strings, any ASCII, and naturally generalises to Unicode – answering the follow‑up before it’s even asked.  
6. Briefly contrast with unsafe delimiter approaches to show you understand why they fail.

**One‑sentence summary:**  
*Prefix each string with its length and a delimiter (`length#string`) so the decoder knows exactly how many characters to read, making the encoding safe for any character set.*