---
title: "Linux Kernel Memory Management"
date: 2023-10-25
tags: ["linux", "kernel", "c"]
summary: "Notes on slab allocators."
---

Understanding `kmalloc` vs `vmalloc`.

`kmalloc` allocates physically contiguous memory. It is faster but limited in size.
`vmalloc` allocates virtually contiguous memory.

```c
void *ptr = kmalloc(size, GFP_KERNEL);
if (!ptr)
    return -ENOMEM;
```

