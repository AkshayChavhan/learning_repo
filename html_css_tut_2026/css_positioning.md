Here's a quick comparison of all five positions.

## Complete CSS Positioning Comparison

This table covers all five CSS positioning properties and their important characteristics.

| Characteristics | Static | Relative | Absolute | Fixed | Sticky |
|---|---|---|---|---|---|
| Default position | Yes | No | No | No | No |
| Normal document flow | Yes | Yes | No | No | Yes |
| Reserves original space | Yes | Yes | No | No | Yes |
| Can use top | No effect | Yes | Yes | Yes | Yes |
| Can use bottom | No effect | Yes | Yes | Yes | Yes |
| Can use left | No effect | Yes | Yes | Yes | Yes |
| Can use right | No effect | Yes | Yes | Yes | Yes |
| Moves on scrolling | Normally | Normally | With its containing block | Stays fixed | Until it sticks |
| Reference point | Normal layout | Its original position | Nearest positioned ancestor | Usually viewport | Nearest scrollport |
| Parent position matters | No | No | Yes | Usually no | Scroll container matters |

### 1. Individual behaviour

| Position | Behaviour |
|---|---|
| `static` | Default behaviour. Element stays in normal flow. |
| `relative` | Moves from its original position but keeps its original space. |
| `absolute` | Leaves normal flow and positions itself relative to its containing block. |
| `fixed` | Leaves normal flow and usually stays in the same position relative to the browser viewport while scrolling. |
| `sticky` | Stays in normal flow, scrolls normally, and sticks when it reaches its specified threshold. |

### 2. Parent and child combinations

| Parent | Child | What happens? |
|---|---|---|
| Static | Static | Both stay in normal flow. |
| Static | Relative | Child moves from its original position. |
| Static | Absolute | Child looks for another positioned ancestor. |
| Static | Fixed | Child usually references viewport. |
| Static | Sticky | Child sticks within its scroll container. |
| Relative | Relative | Both stay in normal flow. |
| Relative | Absolute | Child uses the relative parent as its containing block. |
| Relative | Fixed | Child usually references viewport. |
| Relative | Sticky | Child can stick within its scroll container. |
| Absolute | Absolute | Child can use the absolute parent as its containing block. |

### 3. Five important rules to remember

1. **Static:** Default positioning. Top, bottom, left and right have no effect.
2. **Relative:** Moves from its own original position. Original space remains reserved.
3. **Absolute:** Leaves normal flow. Original space is not reserved.
4. **Fixed:** Usually stays attached to the viewport, even when scrolling.
5. **Sticky:** Scrolls normally first, then sticks at the specified threshold.

### 4. One important CSS example

```css
.parent {
  position: relative;
  height: 300px;
}

.child {
  position: absolute;
  top: 20px;
  right: 20px;
}
```

Here:

- Parent stays in normal flow.
- Parent reserves its space.
- Child leaves normal flow.
- Child positions itself 20px from the parent's top and right edges.

**My recommendation:** Remember these three differences particularly well:

- Relative = Original space remains.
- Absolute = Original space disappears.
- Sticky = Original space remains, but the element sticks during scrolling.

These are the foundations of CSS positioning.

Just focus on three big points: relative keeps its space, absolute loses its space, and sticky keeps its space but sticks while scrolling. For example, parent relative with height 300px, child absolute top 20, right 20. The parent keeps its space, the child does not, and sits inside the parent. Those three are the backbone, the rest builds on them.  
  
  
  
  
IN MY WORDS :-  
if element is static then it wont apply any css top,bottom,left,right values and it takes its own space, everything default is statuc  
If element is relative then it moves using css top,bottom,left,right values and it takes its own space and move reference with its own position.  
If element is absolute then it moves using css top,bottom,left,right values and it doesnt takes its own space and move reference with its nearest positioned parents.  
If element is fixed then it moves using css top,bottom,left,right values and it doesnt takes its own space and move reference with its main viewport.  
If element is sticky then it moves using css left,right values and use top,bottom to add threshord values reference to scrolling page , it doesnt takes its own space