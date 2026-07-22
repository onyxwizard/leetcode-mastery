### 📘 Chapter: Stack  
### 📌 Problem 6: Evaluate Reverse Polish Notation (LeetCode 150)

---

**Input**  
- `tokens`: an array of strings representing an arithmetic expression in **Reverse Polish Notation (postfix)**.

**Output**  
- An integer – the evaluated result of the expression.

**Constraints**  
- `1 <= tokens.length <= 10⁴`  
- `tokens[i]` is either an operator: `"+"`, `"-"`, `"*"`, `"/"`, or an integer in the range `[-200, 200]`.  
- The expression is always valid (no division by zero, integer division truncates toward zero).  
- All intermediate results fit in a 32‑bit integer.

**Follow‑up**  
- Not explicitly given. (A typical extension might be to support more operators or to evaluate infix expressions.)

---

### 🧠 Why this Data Structure?

Reverse Polish Notation is explicitly designed to be evaluated with a **stack**.  
- The evaluation rule is straightforward:  
  - Read the expression left to right.  
  - When an **operand** (number) is encountered, push it onto the stack.  
  - When an **operator** is encountered, pop the required two operands (the right operand first, then the left), apply the operator, and push the result back.  
- The stack’s **LIFO** nature perfectly models the postfix order.  
- This yields an **O(n)** time and **O(n)** space solution in a single pass, which is optimal for this problem.

---

### 🔨 Brute Force / Naive Approach (Repeated Reduction)

**Method:**  
Instead of a stack, we can treat the expression as a list and repeatedly scan to find the first occurrence of the pattern `operand, operand, operator`. Replace those three tokens with the computed result (as a string), shortening the list. Continue until only one token remains.  

**Time:** O(n²) – each reduction requires scanning and removing elements (shifting the rest).  
**Space:** O(n) – for the mutable list.

```java
// Pseudo-concept (not efficient)
List<String> list = new ArrayList<>(Arrays.asList(tokens));
while (list.size() > 1) {
    for (int i = 0; i < list.size(); i++) {
        if (isOperator(list.get(i)) && i >= 2 
            && isOperand(list.get(i-1)) && isOperand(list.get(i-2))) {
            int b = Integer.parseInt(list.get(i-1));
            int a = Integer.parseInt(list.get(i-2));
            int res = apply(a, b, list.get(i));
            // replace the three tokens with res
            list.set(i-2, String.valueOf(res));
            list.remove(i);   // remove operator and operand
            list.remove(i-1);
            break;
        }
    }
}
return Integer.parseInt(list.get(0));
```
This approach is unnecessarily complex and slow; the stack is the natural tool.

---

### ⚡ Optimized Approach – Stack (O(n) time, O(n) space)

**Method:**  
- Use a `Deque<Integer>` (or `Stack<Integer>`) as the evaluation stack.  
- Iterate over each token:  
  - If the token is an **operator** (`+`, `-`, `*`, `/`):  
    - Pop the top two elements (`b = stack.pop()`, `a = stack.pop()`).  
    - Compute `a op b` (note the order: left operand `a`, right operand `b`).  
    - Push the result.  
  - Else (token is an integer): parse it and push onto the stack.  
- After processing all tokens, the final result is the sole element left on the stack.

**Time:** O(n) – each token processed once.  
**Space:** O(n) – stack can grow up to about n/2.

```java
import java.util.ArrayDeque;
import java.util.Deque;

public int evalRPN(String[] tokens) {
    Deque<Integer> stack = new ArrayDeque<>();
    for (String token : tokens) {
        switch (token) {
            case "+":
                stack.push(stack.pop() + stack.pop());
                break;
            case "-": {
                int b = stack.pop();
                int a = stack.pop();
                stack.push(a - b);
                break;
            }
            case "*":
                stack.push(stack.pop() * stack.pop());
                break;
            case "/": {
                int b = stack.pop();
                int a = stack.pop();
                stack.push(a / b);
                break;
            }
            default:
                stack.push(Integer.parseInt(token));
        }
    }
    return stack.peek();
}
```

*Note:* For `-` and `/`, the order of operands matters – we pop the second operand first, then the first, to preserve left‑to‑right evaluation.

---

### 📊 Solution Comparison & Trade‑offs

| Solution                     | Time   | Space | Notes |
|------------------------------|--------|-------|-------|
| Repeated reduction (list)    | O(n²)  | O(n)  | Conceptually follows the definition but inefficient. |
| Stack (single pass)          | O(n)   | O(n)  | **Optimal and standard** – exactly matches the postfix evaluation algorithm. |

**Trade‑off:**  
There is no meaningful trade‑off: the stack solution is always preferred. A recursive approach (processing from right to left) is possible but effectively uses the call stack similarly, and may be less intuitive. The explicit stack is the cleanest.

---

### 🎯 What to Present to the Interviewer

1. Explain that RPN is evaluated with a stack – push operands, pop for operators.  
2. Write the stack‑based solution in Java, being careful about the order of operands for subtraction and division.  
3. Walk through a simple example (e.g., `["2","1","+","3","*"]`).  
4. Discuss integer division truncation toward zero (Java’s `/` already does this for integers).  
5. State complexities: O(n) time, O(n) space – optimal.  
6. If asked, mention that recursion from the end of the expression is an alternative but the stack is more direct and avoids recursion depth issues for very large input (though constraints are safe).

**One‑sentence summary:**  
*Use a stack to evaluate the postfix expression in one pass: push numbers, and for each operator pop the required operands, apply the operator, and push the result, achieving O(n) time.*