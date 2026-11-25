# 10: useReducer

> **`useReducer`** manages **complex or related state** by **dispatching actions** to a **reducer** function.
> The reducer takes the current state and an action, and returns the **next state**.
> It is the same idea as Redux, built into React.

---

## 📌 Quick Reference

| Term | One-line definition |
|---|---|
| **Reducer** | A **pure** function `(state, action) → newState` |
| **Action** | A plain object describing what happened, like `{ type: "ADD_ITEM", payload: item }` |
| **`dispatch`** | Sends an action to the reducer. Triggers a re-render with the new state |
| **Action creator** | A function that returns an action object, to avoid typos in `type` strings |
| **Lazy init** | A third argument that computes the initial state only once |

---

## 🟢 Beginner

### The analogy: a TV remote

```text
Remote button  →  (action)  →  TV logic  →  (reducer)  →  new TV state
```

You don't change the TV directly. You **press a button** (dispatch an action), and the **logic** (reducer) decides the new state.

### Why it exists

Use `useState` when values **change independently**. Use `useReducer` when **several fields must change together**.

```jsx
// ❌ useState: easy to forget one setter
const [items, setItems] = useState([]);
const [total, setTotal] = useState(0);
const [discount, setDiscount] = useState(0);

function addItem(item) {
  setItems(prev => [...prev, item]);
  setTotal(prev => prev + item.price);
  setDiscount(0);          // easy to forget
}

// ✅ useReducer: one dispatch updates everything together
const [state, dispatch] = useReducer(cartReducer, initialState);

function addItem(item) {
  dispatch({ type: "ADD_ITEM", payload: item });
}
```

### The syntax: 4 parts

```jsx
const [state, dispatch] = useReducer(reducer, initialState);
//     ↑        ↑                    ↑         ↑
//  current   sends an          the function  starting
//  state     action            that decides  value
//                              new state
```

---

## 🟡 Intermediate

### Full example: shopping cart

**1. Initial state**

```jsx
const initialState = {
  items: [],
  discount: 0,      // percent, e.g. 10 means 10% off
};
```

**2. Reducer**: pure, returns a **new** object for every change

```jsx
function calcTotal(items, discount) {
  const subtotal = items.reduce((sum, item) => sum + item.price, 0);
  return subtotal - (subtotal * discount) / 100;
}

function cartReducer(state, action) {
  switch (action.type) {
    case "ADD_ITEM": {
      const items = [...state.items, action.payload];
      return { ...state, items, discount: 0 };      // reset discount on add
    }
    case "REMOVE_ITEM": {
      const items = state.items.filter(i => i.id !== action.payload);
      return { ...state, items };
    }
    case "APPLY_DISCOUNT":
      return { ...state, discount: action.payload };
    case "CLEAR_CART":
      return initialState;                          // reset everything
    default:
      return state;                                 // unknown action: no change
  }
}
```

> **Note:** the total is **derived** from `items` and `discount`, not stored. Storing it and updating it on each action makes it easy to get wrong. For example, applying a discount twice would compound it.

**3. Component**

```jsx
function ShoppingCart() {
  const [state, dispatch] = useReducer(cartReducer, initialState);
  const total = calcTotal(state.items, state.discount);

  return (
    <div>
      <p>Total: Rs.{total}</p>
      <p>Items: {state.items.length}</p>

      <button onClick={() => dispatch({
        type: "ADD_ITEM", payload: { id: 1, name: "Phone", price: 999 }
      })}>Add Phone</button>

      <button onClick={() => dispatch({ type: "REMOVE_ITEM", payload: 1 })}>
        Remove
      </button>

      <button onClick={() => dispatch({ type: "APPLY_DISCOUNT", payload: 10 })}>
        Apply 10% Off
      </button>

      <button onClick={() => dispatch({ type: "CLEAR_CART" })}>Clear Cart</button>
    </div>
  );
}
```

### `useState` vs `useReducer`

| Use `useState` when | Use `useReducer` when |
|---|---|
| 1–2 independent values | 3+ related values that update together |
| Simple toggle, string, or number | An object with several fields |
| The next state doesn't depend on other fields | Fields depend on each other |
| Update logic is simple | Update logic has many cases |
| No state-machine patterns | Finite-state-machine style transitions |

### Action creators: avoid typos

```jsx
// ❌ Raw strings: "REMOV_ITEM" compiles fine and fails silently
dispatch({ type: "REMOV_ITEM", payload: id });

// ✅ Action creators: one place for each type
const addItem = (item) => ({ type: "ADD_ITEM", payload: item });
const removeItem = (id) => ({ type: "REMOVE_ITEM", payload: id });
const clearCart = () => ({ type: "CLEAR_CART" });

dispatch(addItem(item));
dispatch(removeItem(1));
dispatch(clearCart());
```

### `useReducer` + `useContext`: mini Redux

Share state and dispatch across the app without a library:

```jsx
import { createContext, useContext, useMemo, useReducer } from "react";

const CartContext = createContext(null);

export function CartProvider({ children }) {
  const [state, dispatch] = useReducer(cartReducer, initialState);

  const value = useMemo(() => ({ state, dispatch }), [state]);
  // dispatch is stable, so it doesn't need to be in the array

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) throw new Error("useCart must be used inside CartProvider");
  return context;
}

// Any component can read state and dispatch
function ProductPage({ product }) {
  const { state, dispatch } = useCart();

  return (
    <div>
      <p>Cart: {state.items.length} items</p>
      <button onClick={() => dispatch(addItem(product))}>Add to Cart</button>
    </div>
  );
}
```

---

## 🔴 Expert

### `dispatch` is stable

React guarantees that `dispatch` keeps the **same reference** across renders. `useState`'s setter is also stable. The benefit of `dispatch` is different:

```jsx
// Setter from useState: the handler closes over `items`, so it must depend on it
const handleAdd = useCallback(() => setItems([...items, item]), [items, item]);

// dispatch: the handler only needs the action, so the dependency list stays short
const handleAdd = useCallback(() => dispatch(addItem(item)), [item]);
```

> **Correction to common notes:** `useState` setters are stable too. `useCallback` is needed only when a function's **captured values** change, not because of the setter itself.

### Lazy initialization

Pass an `init` function as the third argument. React calls it **once**, on mount.

```jsx
// ❌ expensiveCalc() runs on EVERY render (the result is ignored after mount)
const [state, dispatch] = useReducer(reducer, expensiveCalc());

// ✅ init runs ONCE, on mount
function init(initialCount) {
  return { count: initialCount, history: [] };
}
const [state, dispatch] = useReducer(reducer, 0, init);
//                                            ↑ passed to init(0) once
```

### Immer: write "mutating" code safely

Immer's `produce` lets you write code that looks like mutation. It builds the new immutable state for you. This helps with deeply nested state.

```jsx
import { produce } from "immer";

// ❌ Manual spread gets messy when nested
case "ADD_ITEM":
  return { ...state, cart: { ...state.cart, items: [...state.cart.items, action.payload] } };

// ✅ Immer: looks like mutation, produces a new immutable state
const cartReducer = produce((draft, action) => {
  switch (action.type) {
    case "ADD_ITEM":
      draft.cart.items.push(action.payload);
      break;
  }
});
```

### Performance: `useState` vs `useReducer`

| Question | Answer |
|---|---|
| Is `useReducer` heavy? | No. Its performance is the same as `useState` |
| Can I use it anywhere? | Yes, in small or large components, custom hooks, or several reducers in one component |
| How do you choose? | By **code clarity**, not speed |

> `useState` is essentially `useReducer` with a built-in reducer. Choose the one that makes your update logic easiest to read.

---

## ⚠️ Common Mistakes

| Mistake | Fix |
|---|---|
| Reducer mutates state (`state.items.push(...)`) | Return a new object and array. Or use Immer |
| Reducer has side effects (fetch, log, timers) | Keep reducers **pure**. Put side effects in event handlers or `useEffect` |
| No `default` case in the switch | Return `state` for unknown actions |
| Storing derived values (like `total`) in state | Calculate them from `items` and `discount` |
| Unknown or misspelled action type | Use action creators, and throw for unknown types during development |
| `REMOVE_ITEM` for an item that doesn't exist | Guard against `undefined` before using it |
| Using `useReducer` for one simple value | Use `useState` |

---

## 🎯 Decision Guide

| Situation | Best choice |
|---|---|
| 1–2 simple independent values | `useState` |
| Simple toggle, string, or number | `useState` |
| 3+ related fields that update together | `useReducer` |
| Fields depend on each other | `useReducer` |
| Complex transition logic | `useReducer` |
| Passing the update function to memoized children | `useReducer` (stable `dispatch`) |
| Global state without Redux | `useReducer` + `useContext` |
| Large app that needs DevTools or middleware | Redux or Zustand |

---

## 🎯 Interview Quick Answers

| Question | Short answer |
|---|---|
| What is `useReducer`? | A hook for complex state. You `dispatch` actions, and a pure reducer returns the new state. |
| When use it over `useState`? | Several related fields update together, the next state depends on several parts of the current state, or update logic is complex. |
| What is a reducer? | A **pure** function `(state, action) → newState`. It has no side effects, doesn't mutate, and always returns a new value. |
| What is dispatching? | Calling `dispatch({ type, payload })`. The `type` says what happened, and the `payload` carries the data. |
| Is `useReducer` slower? | No. Performance is the same as `useState`. Choose by clarity. |
| How do you combine it with context? | Put `useReducer` in a Provider, and pass `state` and `dispatch` as the context value. |
| Why is `dispatch` stable? | React guarantees the same reference across renders, so it doesn't need `useCallback` to avoid breaking memoized children. |
| What is lazy initialization? | `useReducer(reducer, arg, init)`. React calls `init(arg)` once, on mount. |
| `useReducer` vs Redux? | `useReducer` is built into React and needs no library. Redux adds middleware, DevTools, time-travel debugging, and strict conventions. |

---

## ✅ Key Takeaways

- **Action → reducer → new state.** The reducer is **pure**.
- Use `useReducer` for **related state** and **complex transitions**. Use `useState` for simple values.
- **Derive** values like totals instead of storing them.
- `dispatch` is **stable**. Combine it with context for mini Redux.
- Lazy init runs **once**. Pass the `init` function, not its result.
