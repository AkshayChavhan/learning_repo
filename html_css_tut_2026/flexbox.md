## CSS Flexbox cheat sheet

| Property          | What it does                                   | Common values                                                                       | Applied to |
| ----------------- | ---------------------------------------------- | ----------------------------------------------------------------------------------- | ---------- |
| `display`         | Creates a flex container.                      | `flex`, `inline-flex`                                                               | Parent     |
| `flex-direction`  | Sets the direction of the items.               | `row`, `column`, `row-reverse`, `column-reverse`                                    | Parent     |
| `justify-content` | Aligns items along the main axis.              | `center`, `flex-start`, `flex-end`, `space-between`, `space-around`, `space-evenly` | Parent     |
| `align-items`     | Aligns items along the cross axis.             | `center`, `stretch`, `flex-start`, `flex-end`, `baseline`                           | Parent     |
| `align-self`      | Overrides alignment for one specific item.     | `auto`, `center`, `stretch`, `flex-start`, `flex-end`, `baseline`                   | Child      |
| `flex-wrap`       | Controls whether items move onto another line. | `nowrap`, `wrap`, `wrap-reverse`                                                    | Parent     |
| `flex-grow`       | Controls how much an item grows.               | `0`, `1`, `2`                                                                       | Child      |
| `flex-shrink`     | Controls how much an item shrinks.             | `0`, `1`, `2`                                                                       | Child      |
| `flex-basis`      | Sets an item's initial main-axis size.         | `auto`, `200px`, `30%`, `0`                                                         | Child      |

### Easy way to remember

Parent — Flex container

Controls the overall layout

- `display`
- `flex-direction`
- `justify-content`
- `align-items`
- `flex-wrap`

Child — Flex item

Controls individual items

- `align-self`
- `flex-grow`
- `flex-shrink`
- `flex-basis`

Important: The parent controls how the children are arranged. The child properties control how each individual item behaves within that layout.

You can use this as your updated Flexbox reference sheet while practicing CSS.