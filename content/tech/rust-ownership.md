---
title: "Understanding Rust Ownership"
date: 2026-02-05
tags: ["rust", "memory"]
---

Ownership is Rust’s most unique feature. It enables memory safety without a garbage collector.

## The Rules
1. Each value in Rust has a variable that’s called its *owner*.
2. There can only be one owner at a time.
3. When the owner goes out of scope, the value will be dropped.

```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1; // s1 is moved to s2
    
    // println!("{}, world!", s1); // This would fail!
}
```

