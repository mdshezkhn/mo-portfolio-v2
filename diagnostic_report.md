# Forensic CSS/DOM Geometry Comparison

## 1. Overall Body Height
- Manual: 2278.875px
- Generated: 1245.9375px
- Difference: -1032.9375px

## 2. Cumulative Spacing Analysis
| Property | Manual Total | Generated Total | Diff |
| --- | --- | --- | --- |
| marginTop | 591.0px | 257.0px | -333.9px |
| marginBottom | 591.0px | 257.0px | -333.9px |
| paddingTop | 0.0px | 0.0px | 0.0px |
| paddingBottom | 0.0px | 0.0px | 0.0px |

## 3. Section Analysis
- Manual CV has 6 `<section>` elements.
- Generated CV has 5 `<section>` elements.

### Major Block Divergences
- Manual CV `.role` / `.education` blocks count: 11
- Generated CV `.entry` blocks count: 16

**Average Margins for manual `.role` vs generated `.entry`:**
- Manual Margin: Top 0.0px, Bottom 0.0px
- Generated Margin: Top 0.0px, Bottom 0.0px

## 4. Specific CSS Rules Missing
- Manual Avg Line Height: 0.0px
- Generated Avg Line Height: 0.0px