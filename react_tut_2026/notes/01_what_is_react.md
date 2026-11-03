# 01: What is React?

> **React** is a declarative JavaScript library for building user interfaces, maintained by **Meta** (formerly Facebook).
> You describe **what the UI should look like** for a given state. React works out **how to update the screen** when that state changes.

---

## 📌 Quick Reference

| Term | One-line definition |
|---|---|
| **Component** | A function that returns JSX (a description of UI) |
| **Virtual DOM** | A lightweight tree of JavaScript objects that represents the UI, kept in memory |
| **Re-rendering** | React calling your component function again to get a new UI description |
| **Diffing** | Comparing the new tree with the old tree |
| **Reconciliation** | The whole process: diff + deciding how to add, update, or remove DOM nodes |
| **Fiber** | React's scheduler: splits work into small, pausable units |

---

## 🟢 Beginner

### What React does

You write a component. React runs it, shows the result, and runs it again when state changes.

```jsx
function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Clicked {count} times
    </button>
  );
}
```

**Output on the screen:**

```text
Clicked 0 times   → user clicks →   Clicked 1 times   → user clicks →   Clicked 2 times
```

> You never change the button's text yourself. You only describe it for each state.

### Key terms

| Part | What it is |
|---|---|
| **Component** | A function that returns JSX |
| **JSX** | HTML-like syntax inside JavaScript that describes UI |
| **State** | Data that can change over time (`count` above) |

---

## 🟡 Intermediate

### The Virtual DOM

| | Real DOM | Virtual DOM |
|---|---|---|
| What it is | The page the user actually sees, owned by the browser | A tree of plain JavaScript objects that represents the UI |
| Speed to change | **Slow** | **Fast** (just JavaScript objects in memory) |
| Who uses it | The browser | React, for comparison |

> **Why React uses it:** touching the real DOM is slow. React compares trees in memory and changes only what is needed.

### How an update flows

```text
State changes
     │
     ▼
Re-render: component function runs again → new Virtual DOM tree
     │
     ▼
Diffing: compare new tree vs previous tree
     │
     ▼
Reconciliation: decide what to add / update / remove
     │
     ▼
Commit: apply the changes to the real DOM in one batch
```

**Key point:** React keeps the previous tree as a reference. After each update, the new tree becomes the "previous" one for the next comparison.

### Re-rendering is not redrawing

| Myth | Reality |
|---|---|
| "React redraws the whole page" | React re-runs the **component function** only |
| "Re-render means DOM update" | Re-render produces a new description. The DOM changes only where a diff found a difference |

---

## 🔴 Expert

### Fiber

**Before Fiber:** reconciliation was one long, uninterrupted job. A big update could freeze the page.

**With Fiber:** the work is split into **fibers**, one unit per component. Each fiber is a JavaScript object with:

- its **type** and **props**
- links to its **parent**, **child**, and **sibling** fibers

Because the units are small, React can **pause, resume, or discard** work in progress.

### Priorities

| Update type | Priority | What React does |
|---|---|---|
| User input (typing, clicking) | **High / urgent** | Interrupts lower-priority rendering |
| Transition (`startTransition`) | **Low** | Can be paused while urgent updates run |
| Stale render (a newer update arrived) | — | Throws away the in-progress work and starts over |

```jsx
// Mark a slow, non-urgent update as a transition
startTransition(() => {
  setFilteredList(bigList.filter(matches));
});
```

> Typing in the input stays responsive, even while the large list updates in the background.

---

## ⚠️ Common Misconceptions

| Misconception | Correct understanding |
|---|---|
| "Virtual DOM is always faster than the real DOM" | It avoids unnecessary DOM work. It is not faster than doing the minimum change directly |
| "Virtual DOM is a copy of what the user sees" | It is a tree of JavaScript objects. The real DOM is what the user sees |
| "Re-render = browser repaint" | Re-render runs your function. The browser only repaints if the DOM changed |
| "Diffing and reconciliation are the same" | Diffing is the comparing step. Reconciliation is the whole process around it |

---

## 🎯 Interview Quick Answers

| Question | Short answer |
|---|---|
| What is React? | A declarative JavaScript library for building UIs from components, maintained by Meta. "Declarative" means you describe the UI for a state, and React handles the DOM steps. |
| What is the Virtual DOM, and why use it? | A lightweight JavaScript object tree representing the UI. React compares trees in memory so the real DOM changes only where needed, because real DOM work is slow. |
| Reconciliation vs re-rendering? | **Re-rendering** is the trigger: React calls the component again. **Diffing** compares the old and new trees. **Reconciliation** is the full process of deciding and applying the changes. Re-rendering alone does not touch the real DOM. |
| What does Fiber do, and why? | Breaks the update into small units so React can pause, resume, or cancel work. Before Fiber, a long update blocked the page. |
| How does the Virtual DOM update the real DOM? | Updates produce a new tree, diffing finds the differences, and reconciliation applies them to the real DOM in one batch. |

---

## ✅ Key Takeaways

- React = **components** + **state** → **UI description**.
- Update flow: **re-render → diff → reconcile → batch-patch the real DOM**.
- **Fiber** lets React pause urgent work (typing) ahead of slower work (large renders).
