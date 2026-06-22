import { createSlice, configureStore, createAsyncThunk } from "@reduxjs/toolkit";
import { Provider, useSelector, useDispatch } from "react-redux";

// ══════════════════════════════════════════════════════════════
// FILE: store/thunks/productThunks.js
// Purpose: All async API calls using createAsyncThunk
// ══════════════════════════════════════════════════════════════

export const fetchProducts = createAsyncThunk(
  "products/fetchAll",                        // action type prefix
  async (_, { rejectWithValue }) => {         // _ means no argument passed
    try {
      const res = await fetch("https://fakestoreapi.com/products?limit=5");
      if (!res.ok) throw new Error("Failed to fetch");
      const data = await res.json();
      return data.map(p => ({
        id:    p.id,
        name:  p.title,
        price: Math.round(p.price * 80),      // convert $ → ₹
        image: p.image,
      }));
    } catch (err) {
      return rejectWithValue(err.message);    // sends error to rejected case
    }
  }
);


// ══════════════════════════════════════════════════════════════
// FILE: store/slices/cartSlice.js
// Purpose: Cart state — add, remove, clear
// Exports:  cartSlice.reducer  → goes into store
//           cartSlice.actions  → used in components via dispatch
// ══════════════════════════════════════════════════════════════

const cartSlice = createSlice({
  name: "cart",
  initialState: { items: [] },
  reducers: {

    addToCart: (state, action) => {
      const exists = state.items.find(i => i.id === action.payload.id);
      if (exists) {
        exists.qty += 1;                      // immer — mutate directly, RTK handles immutability
      } else {
        state.items.push({ ...action.payload, qty: 1 });
      }
    },

    removeFromCart: (state, action) => {
      state.items = state.items.filter(i => i.id !== action.payload);
    },

    clearCart: (state) => {
      state.items = [];
    },

  },
});


// ══════════════════════════════════════════════════════════════
// FILE: store/slices/productsSlice.js
// Purpose: Products state — fetched from API
// extraReducers: listens to fetchProducts thunk (from another file)
// ══════════════════════════════════════════════════════════════

const productsSlice = createSlice({
  name: "products",
  initialState: { list: [], loading: false, error: null },
  reducers: {},                               // no sync reducers needed here
  extraReducers: (builder) => {
    builder
      .addCase(fetchProducts.pending,   (state) => {
        state.loading = true;
        state.error   = null;
      })
      .addCase(fetchProducts.fulfilled, (state, action) => {
        state.loading = false;
        state.list    = action.payload;       // action.payload = returned value from thunk
      })
      .addCase(fetchProducts.rejected,  (state, action) => {
        state.loading = false;
        state.error   = action.payload;       // action.payload = rejectWithValue(err.message)
      });
  },
});


// ══════════════════════════════════════════════════════════════
// FILE: store/store.js
// Purpose: Create and export the single Redux store
//          Import this in your root _app.tsx or layout.tsx
// ══════════════════════════════════════════════════════════════

const store = configureStore({
  reducer: {
    cart:     cartSlice.reducer,             // state.cart
    products: productsSlice.reducer,         // state.products
  },
});


// ══════════════════════════════════════════════════════════════
// FILE: store/slices/cartSlice.js  (bottom of same file)
// Purpose: Export actions so components can dispatch them
// Usage:   dispatch(addToCart(product))
// ══════════════════════════════════════════════════════════════

const { addToCart, removeFromCart, clearCart } = cartSlice.actions;


// ══════════════════════════════════════════════════════════════
// FILE: store/selectors/cartSelectors.js
// Purpose: All cart-related selectors in one place
//          Keeps components clean — no state shape logic inside components
// ══════════════════════════════════════════════════════════════

const selectCartItems = (state) => state.cart.items;

const selectCartTotal = (state) =>
  state.cart.items.reduce((sum, i) => sum + i.price * i.qty, 0);

// Curried selector — takes dynamic arg (id), returns a selector function
// Usage: useSelector(selectIsInCart(product.id))
const selectIsInCart = (id) => (state) =>
  state.cart.items.some(i => i.id === id);


// ══════════════════════════════════════════════════════════════
// FILE: store/selectors/productSelectors.js
// Purpose: All product-related selectors
// ══════════════════════════════════════════════════════════════

const selectProducts = (state) => state.products.list;
const selectLoading  = (state) => state.products.loading;
const selectError    = (state) => state.products.error;


// ══════════════════════════════════════════════════════════════
// FILE: components/products/ProductList.jsx
// ══════════════════════════════════════════════════════════════

function ProductList() {
  const dispatch = useDispatch();
  const products = useSelector(selectProducts);
  const loading  = useSelector(selectLoading);
  const error    = useSelector(selectError);

  return (
    <div style={s.section}>
      <div style={s.sectionHead}>
        <span style={s.label}>PRODUCTS</span>
        <button style={s.btn} onClick={() => dispatch(fetchProducts())}>
          {loading ? "Loading…" : "Load Products"}
        </button>
      </div>
      {error    && <div style={s.error}>Error: {error}</div>}
      {!loading && products.map(p => <ProductCard key={p.id} product={p} />)}
    </div>
  );
}


// ══════════════════════════════════════════════════════════════
// FILE: components/products/ProductCard.jsx
// ══════════════════════════════════════════════════════════════

function ProductCard({ product }) {
  const dispatch = useDispatch();
  const isInCart = useSelector(selectIsInCart(product.id)); // curried selector

  return (
    <div style={s.card}>
      <div style={s.cardLeft}>
        <img src={product.image} alt={product.name} style={s.img} />
        <div>
          <div style={s.productName}>{product.name.slice(0, 28)}…</div>
          <div style={s.productPrice}>₹{product.price.toLocaleString()}</div>
        </div>
      </div>
      <button
        style={{ ...s.btn, ...(isInCart ? s.btnActive : {}) }}
        onClick={() => isInCart
          ? dispatch(removeFromCart(product.id))
          : dispatch(addToCart(product))
        }
      >
        {isInCart ? "Remove" : "Add"}
      </button>
    </div>
  );
}


// ══════════════════════════════════════════════════════════════
// FILE: components/cart/Cart.jsx
// ══════════════════════════════════════════════════════════════

function Cart() {
  const dispatch = useDispatch();
  const items    = useSelector(selectCartItems);
  const total    = useSelector(selectCartTotal);

  return (
    <div style={s.section}>
      <div style={s.sectionHead}>
        <span style={s.label}>CART ({items.length})</span>
        {items.length > 0 &&
          <button style={{ ...s.btn, ...s.btnDanger }} onClick={() => dispatch(clearCart())}>
            Clear
          </button>
        }
      </div>
      {items.length === 0
        ? <div style={s.empty}>Cart is empty</div>
        : <>
            {items.map(i => (
              <div key={i.id} style={s.cartRow}>
                <span style={s.cartName}>{i.name}</span>
                <span style={s.cartQty}>×{i.qty}</span>
                <span style={s.cartPrice}>₹{(i.price * i.qty).toLocaleString()}</span>
              </div>
            ))}
            <div style={s.total}>Total: ₹{total.toLocaleString()}</div>
          </>
      }
    </div>
  );
}


// ══════════════════════════════════════════════════════════════
// FILE: app/layout.tsx  (Next.js)  OR  src/main.jsx  (Vite)
// Purpose: Wrap entire app with <Provider> so all components
//          can access the Redux store via useSelector/useDispatch
// ══════════════════════════════════════════════════════════════

export default function App() {
  return (
    <Provider store={store}>
      <div style={s.root}>

        <div style={s.header}>
          <span style={s.title}>Redux Toolkit</span>
          <span style={s.subtitle}>createSlice · createAsyncThunk · Selectors · Immer</span>
        </div>

        <div style={s.grid}>
          <ProductList />
          <Cart />
        </div>

        {/* File structure reference */}
        <div style={s.concepts}>
          {[
            ["store/thunks/",       "createAsyncThunk — all API calls live here"],
            ["store/slices/",       "createSlice — state + reducers + actions per feature"],
            ["store/store.js",      "configureStore — combines all slices into one store"],
            ["store/selectors/",    "All selectors — keeps state shape out of components"],
            ["app/layout.tsx",      "<Provider store={store}> — wraps the entire app"],
            ["any component",       "useSelector(selector) · useDispatch() — read & write store"],
            ["Immer (built-in)",    "Mutate state directly in reducers — RTK handles immutability"],
          ].map(([file, desc]) => (
            <div key={file} style={s.conceptRow}>
              <span style={s.conceptTerm}>{file}</span>
              <span style={s.conceptDesc}>{desc}</span>
            </div>
          ))}
        </div>

      </div>
    </Provider>
  );
}

const s = {
  root:        { fontFamily: "'DM Mono', monospace", maxWidth: 760, margin: "0 auto", padding: "16px", background: "#0f0f0f", minHeight: "100vh", color: "#e2e2e2" },
  header:      { marginBottom: 20, borderBottom: "1px solid #222", paddingBottom: 14 },
  title:       { display: "block", fontSize: 22, fontWeight: 700, color: "#a78bfa", letterSpacing: -0.5 },
  subtitle:    { display: "block", fontSize: 11, color: "#555", marginTop: 4, letterSpacing: 1 },
  grid:        { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 20 },
  section:     { background: "#161616", border: "1px solid #222", borderRadius: 10, padding: 16 },
  sectionHead: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 },
  label:       { fontSize: 10, fontWeight: 700, letterSpacing: 2, color: "#555" },
  card:        { display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 0", borderBottom: "1px solid #1e1e1e" },
  cardLeft:    { display: "flex", alignItems: "center", gap: 10 },
  img:         { width: 36, height: 36, objectFit: "contain", borderRadius: 6, background: "#fff", padding: 3 },
  productName: { fontSize: 13, color: "#e2e2e2", marginBottom: 2 },
  productPrice:{ fontSize: 11, color: "#6b7280" },
  btn:         { fontSize: 11, padding: "5px 12px", borderRadius: 6, border: "1px solid #333", background: "transparent", color: "#a78bfa", cursor: "pointer", fontFamily: "inherit" },
  btnActive:   { background: "#1e1a2e", borderColor: "#7c3aed", color: "#c4b5fd" },
  btnDanger:   { color: "#f87171", borderColor: "#3b1a1a" },
  cartRow:     { display: "flex", alignItems: "center", gap: 8, padding: "8px 0", borderBottom: "1px solid #1e1e1e" },
  cartName:    { flex: 1, fontSize: 12, color: "#e2e2e2" },
  cartQty:     { fontSize: 11, color: "#6b7280", minWidth: 24, textAlign: "center" },
  cartPrice:   { fontSize: 12, color: "#a78bfa", minWidth: 80, textAlign: "right" },
  total:       { marginTop: 12, textAlign: "right", fontSize: 14, fontWeight: 700, color: "#a78bfa" },
  empty:       { fontSize: 12, color: "#444", textAlign: "center", padding: "20px 0" },
  error:       { fontSize: 11, color: "#f87171", background: "#1a0f0f", padding: "8px 10px", borderRadius: 6, marginBottom: 10 },
  concepts:    { background: "#161616", border: "1px solid #222", borderRadius: 10, overflow: "hidden" },
  conceptRow:  { display: "flex", gap: 16, padding: "10px 16px", borderBottom: "1px solid #1a1a1a", alignItems: "flex-start" },
  conceptTerm: { fontSize: 11, fontWeight: 700, color: "#a78bfa", minWidth: 170, flexShrink: 0 },
  conceptDesc: { fontSize: 11, color: "#6b7280", lineHeight: 1.6 },
};
