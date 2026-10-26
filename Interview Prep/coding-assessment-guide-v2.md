# Passing the Coding Assessment

- You'll be given a HackerRank assessment (which is like Leetcode, or the Revpro coding assessments) with one or more medium-difficulty problems. Medium usually involves arrays, strings, hashmaps, or basic algorithm logic.

- There will probably be edge cases they expect you to handle, and you'll be assessed on how many test cases you can pass
  - They're NOT expecting perfection, and you should be given a number of runs to see if your code compiles and passes tests.

**Common problem types at this level:**
- Finding duplicates, missing values, or occurrences in an array
- String manipulation (reversals, anagrams, substrings, palindromes)
- Simple sorting or searching logic
- Two-pointer or sliding window patterns
- Basic recursion or tree traversal (less common but possible)

---

## Before Writing Your Solution

- **Read the problem twice!!** Or more. The prompts can be obnoxiously long and convoluted. They kind of do it by design, to test your ability to critically think and fully assess the problem at hand.

- Ask yourself:
  - **What is the input? What is the expected output?**
    - HackerRank will likely give you examples.
    - Walk through the examples they give you by hand. If the example says `input: [1,2,3,4,5] // output: 9`, figure out why and how.
  - **Are there constraints?** (array size, value ranges, negative numbers?)
  - **What are some edge cases to account for?** (empty input, single element, all duplicates, zero, null?)

- Write something like this at the top of your file:
  ```java
  // Plan:
  // 1. Iterate through the array
  // 2. Track seen values in a HashSet
  // 3. If there's a duplicate, return it
  ```
  - This does two things: it forces you to think before you type, and if you run out of time, the interviewer can see your logic even if the code isn't complete.
  - **Don't optimize first.** Get a passing (or semi-passing) brute-force solution, THEN make it efficient and all-encompassing if you have time.

---

## Writing Your Solution

- Use **meaningful variable names**. Words, not letters. You want readable code that's easy to follow and debug.

- **Handle edge cases early** — at the top of your method, or as high as possible.

- **Don't delete code that isn't working yet.** Comment it out. You might come back to it.

- **Test as you go.** Use the sample inputs they give you in print statements before hitting submit for the final time.

- **If you're stuck, re-read the problem.**
  - Sounds pointless maybe, but you might catch something new that makes you think about the problem differently. It's also a way to reset your brain if you've been staring at the code for too long.
  - **WRITE SOME PSEUDOCODE!** It doesn't have to be "standard" pseudocode. Just write something that conveys what you want to do.
    - If you have absolutely no idea, write as much as you can — method signature, edge case handling, maybe a partial loop. Again, partial credit exists and you really don't want to leave these blank.

---

## Common Mistakes I See

- **Off-by-one errors.** Double-check your loop bounds.
  - Stuff like `i < arr.length` vs `i <= arr.length`
- **Not accounting for zero or negative numbers** in number problems.
- **Modifying an array while iterating over it.** Use a copy or a separate structure to store values during the loop.
- **Returning inside a loop when you should be returning after it** (or vice versa).
- **Forgetting to return anything.** I see people get stumped on why they can't compile after they calculated the return value but never actually returned it.
