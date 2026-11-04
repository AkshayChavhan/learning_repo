# 15: Higher-Order Components (HOC)

> A **higher-order component** is a **function** that **takes a component** and **returns a new component** with extra behavior.
> It is a **pattern**, not a React API. You write it yourself.

```text
withSomething(Component)  →  returns  NewComponent  (same props, extra behavior)
```

---

## 📌 Quick Reference

| Term | One-line definition |
|---|---|
| **HOC** | A function that takes a component and returns an enhanced component |
| **Wrapped component** | The original component passed into the HOC |
| **Naming convention** | HOCs start with `with`, like `withAuth` or `withLogging` |
| **Prop pass-through** | The HOC forwards its props to the wrapped component with `{...props}` |

---

## 🟢 Beginner

### The idea: a wrapper factory

You give it a component. It gives back a version with extra behavior.

### Example: log every render

```jsx
function withLogging(WrappedComponent) {
  return function LoggedComponent(props) {
    console.log("Rendering", WrappedComponent.name);
    return <WrappedComponent {...props} />;   // pass props through
  };
}

const LoggedButton = withLogging(Button);
```

```text
Rendering Button     ← logged on each render of LoggedButton
```

- `LoggedButton` looks and works like `Button`.
- The `{...props}` spread passes every prop through, so nothing is lost.

---

## 🟡 Intermediate

### Example: show content only to logged-in users

```jsx
function withAuth(WrappedComponent) {
  return function AuthenticatedComponent(props) {
    if (!props.user) {
      return <p>Please log in</p>;            // stop here
    }
    return <WrappedComponent {...props} />;   // otherwise render the original
  };
}

const ProfileWithAuth = withAuth(Profile);
```

```text
user = null       →  Please log in
user = { ... }    →  Profile is rendered with all its props
```

> Use `!props.user` rather than `props.user !== null`. The first also handles `undefined`.

### What HOCs are good for

| Use case | Example |
|---|---|
| Access control | `withAuth` |
| Loading or error states | `withLoading`, `withErrorHandling` |
| Logging or analytics | `withLogging` |
| Injecting shared data | `withTheme` |

### Rules to follow

| Rule | Why |
|---|---|
| **Pass props through** with `{...props}` | Otherwise the wrapped component loses data |
| **Start the name with `with`** | Makes it easy to recognize a HOC |
| **Set a `displayName`** | Shows a readable name in React DevTools |
| **Don't mutate the wrapped component** | Return a new component, don't change the original |

```jsx
LoggedButton.displayName = `withLogging(${Button.displayName || Button.name})`;
```

> `WrappedComponent.name` can be empty for anonymous components. `displayName` is more reliable.

---

## 🔴 Expert

### Refs don't pass through

`ref` is not a normal prop. A HOC must use `forwardRef` to pass it to the wrapped component:

```jsx
function withFocus(WrappedComponent) {
  return forwardRef(function WithFocus(props, ref) {
    return <WrappedComponent {...props} ref={ref} />;
  });
}
```

> In React 19, `ref` is a regular prop, so this is no longer needed for function components.

### Name collisions

If the HOC adds a prop with the same name as one the user passes, one of them is lost:

```jsx
// The HOC adds `user`, and the caller also passes `user`
<ProfileWithAuth user={currentUser} />
// Rule: pick unique names, or make the HOC's prop explicit
```

### Static properties are not copied

Static properties on the original (like `Profile.getLayout`) don't exist on the wrapper. Copy them yourself, or use a library such as `hoist-non-react-statics`.

### Don't define a HOC inside a component

```jsx
// ❌ A new component type on every render: the child remounts and loses state
function Parent() {
  const Wrapped = withLogging(Button);
  return <Wrapped />;
}

// ✅ Create it once, at the module level
const LoggedButton = withLogging(Button);
function Parent() {
  return <LoggedButton />;
}
```

> Same rule as defining components inside components (see note 03).

### Wrapper nesting

Stacking HOCs adds layers to the component tree, which makes DevTools harder to read:

```jsx
const Enhanced = withAuth(withLogging(withTheme(Profile)));
```

---

## ⚠️ Common Mistakes

| Mistake | Fix |
|---|---|
| Forgetting `{...props}` | Pass the props through |
| Defining the HOC call inside render | Create it at module level |
| Losing `ref` | Use `forwardRef` (React 18) |
| Prop name collision | Use unique prop names |
| Anonymous wrapper in DevTools | Set `displayName` |
| `return Please log in` (text without a tag) | Wrap text in JSX, like `<p>...</p>` |

---

## 🎯 Modern Alternative: custom hooks

Most HOC jobs (auth checks, logging, shared data) can now be done with a **custom hook**, which is easier to read and doesn't add wrapper layers:

```jsx
// HOC version
const ProfileWithAuth = withAuth(Profile);

// Hook version
function Profile() {
  const { user } = useAuth();
  if (!user) return <p>Please log in</p>;
  return <h1>{user.name}</h1>;
}
```

> HOCs are still common in older code and in some libraries. `React.memo` is also a HOC.

---

## 🎯 Interview Quick Answers

| Question | Short answer |
|---|---|
| What is a HOC? | A function that takes a component and returns a new component with added behavior. |
| What is it used for? | Sharing behavior like auth, logging, or loading states across components. |
| Why pass props through? | So the wrapped component still gets its data. |
| Why use `with` in the name? | It's the convention, so HOCs are easy to spot. |
| What is a problem with refs? | `ref` isn't a normal prop, so it must be forwarded with `forwardRef` (React 18). |
| HOC vs custom hook? | A HOC wraps the component. A hook shares logic inside it, without an extra layer. Hooks are the modern choice. |

---

## ✅ Key Takeaways

- **HOC** = `withX(Component)` → **new component** with extra behavior.
- **Always pass props through** with `{...props}`.
- Watch out for **refs**, **name collisions**, and **static properties**.
- Create HOCs at **module level**, never inside render.
- **Custom hooks** are usually the simpler modern option.
