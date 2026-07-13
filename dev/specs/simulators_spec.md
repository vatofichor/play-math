# Simulators Implementation & Library Specification

This document defines where simulator code lives, standard third-party libraries permitted, coordinate-mapping standards, and rendering loop choices across play-math.

---

## 1. Core Codebase Location
To enforce isolation and run-anywhere modularity:
- **Zero-Dependency Components**: For arithmetic, basic algebra, and fundamental geometry, simulator logic must live **directly inline** inside the subtopic's [index.html](file:///d:/Dev/play-math/01_arithmetic_number_sense/basic_operations/index.html) page within standard `<script>` tags at the bottom of the body.
- **Dynamic Assets**: Global styles and navbar injection reside in the root [shared.css](file:///d:/Dev/play-math/shared.css) and [shared.js](file:///d:/Dev/play-math/shared.js) files respectively. No duplicate navigation markup or basic style declarations are allowed in topic folders.

---

## 2. Library Selection Policy
The project mandates a **Vanilla-First** approach to performance and independence.

```
       [ Mathematical Roadmap Simulators ]
                       |
        +--------------+--------------+
        |                             |
[ Steps 1 - 6 ]                 [ Step 7: Computational ]
- Native HTML5 Canvas 2D        - JupyterLab (Sandbox Embeds)
- Vanilla DOM API               - NumPy / Pandas / Matplotlib (Python)
- No Render Wrappers            - D3.js / Math.js / Chart.js (Optional JS)
```

1. **Steps 1 through 6 (Arithmetic, Algebra, Geometry, Trig, Calculus, Stats)**:
   - **No Heavy Render Engines**: Standard rendering wrappers (e.g., Three.js, p5.js, PixiJS) are **strictly forbidden** to prevent layout lag, frame overhead, and network dependency issues.
   - **Canvas 2D Context**: Use raw HTML5 Canvas 2D context (`canvas.getContext('2d')`) for visual simulations, graphs, geometries, and vector systems.
   
2. **Step 7 (Computational Math)**:
   - Permissible standard data science and computing runtimes include **Python** (NumPy, Pandas, Matplotlib) and client-side computational utilities like **Math.js** (for symbolic execution) and **D3.js** (for advanced complex-data graphing).

---

## 3. Project-Wide Simulator Standards

### Dynamic Canvas Sizing & Redrawing
To align with the glassmorphic layout and collapsible sidebar drawer, all canvas elements must use reactive, container-bound scaling.
- **Autosizing Function**:
  ```javascript
  function resizeCanvas(canvasElement) {
      const container = canvasElement.parentElement;
      canvasElement.width = container.clientWidth;
      canvasElement.height = container.clientHeight;
  }
  ```
- **Redraw Events**: Since layout resizing transitions take time (matching CSS transition rules of `0.3s`), listeners must capture window `resize` events and fire drawing updates after a delay:
  ```javascript
  window.addEventListener('resize', () => {
      setTimeout(() => {
          resizeCanvas(canvas);
          drawSimulation();
      }, 300);
  });
  ```

### Cartesian Coordinate Mapping (Algebra, Trig & Calculus)
When drawing function plots, systems of equations, or trigonometric waves, simulators must convert math coordinates (Cartesian space) to screen pixels:
- **Standard Mapping Utility**:
  ```javascript
  // Map mathematical (x, y) to Screen Canvas (px, py)
  function mapToScreen(x, y, mathBounds, canvasWidth, canvasHeight) {
      const { minX, maxX, minY, maxY } = mathBounds;
      const px = ((x - minX) / (maxX - minX)) * canvasWidth;
      const py = canvasHeight - ((y - minY) / (maxY - minY)) * canvasHeight; // Inverted Y axis
      return { x: px, y: py };
  }
  ```

### Animation and Rendering Loops
- **Static/Reactive Simulators**: For components changing solely via slider inputs (e.g., operator grids, matrix steps, place value columns), draw calls must be triggered **directly inside the event listeners** rather than consuming clock cycles with continuous loops.
- **Continuous Physics/Time Loops**: For continuous waves, vector flow fields, or limits animations, utilize `requestAnimationFrame()` for performance conservation and smooth rendering.
  ```javascript
  let animationFrameId;
  function loop() {
      updatePhysics();
      drawSimulation();
      animationFrameId = requestAnimationFrame(loop);
  }
  ```

---

## 4. Specifications for Core Built Simulators

The following specifications detail the HTML5 canvas layout, coordinate spaces, HSL accent themes, and interactive controls for the built subtopics in the roadmap:

### Phase 1: Foundational Quantities & Cartesian Space

1. **Negative Numbers & Directed Number Line** (`01_arithmetic_number_sense/negative_numbers`)
   - **Theme Accent**: Cyan (`--color-primary: #38bdf8`)
   - **Canvas Layout**: Horizontal splitting grid (60% Canvas / 40% Control Panel). Canvas renders a horizontal sea-level cross-section (above-water sky, below-water deep blue ocean).
   - **Mathematical Bounds**: Altimeter Y-axis from -100 meters (abyssal ocean floor) to +100 meters (sky level).
   - **Controls**: Vertical slider representing submarine ballast controls. Renders a submarine sprite translating vertically on the canvas.
   - **Logic/Visuals**: Displays positive numbers in sky-blue altitude markers and negative numbers in submarine depth markings. A numerical readout calculates absolute value distance from sea level.

2. **Four-Quadrant Coordinate Plane** (`03_geometry_measurement/coordinate_plane_four_quadrants`)
   - **Theme Accent**: Emerald (`--color-primary: #10b981`)
   - **Canvas Layout**: Dual Panel. Canvas renders a high-density sonar/radar sweep screen centered at (0, 0).
   - **Mathematical Bounds**: x in [-10, 10], y in [-10, 10].
   - **Controls**: Two sliders (X coordinate, Y coordinate) and a mode toggle (Rectangular vs. Polar radar tracking).
   - **Logic/Visuals**: A sweeping vector radar line highlights a moving airplane sprite. Selecting coordinates draws dashed projection lines to the horizontal and vertical axes, highlighting the sign rules of Quadrants I, II, III, and IV.

### Phase 2: Inequalities & Spatial Transformation

3. **Inequalities & Balance Bridges** (`02_algebra/inequalities`)
   - **Theme Accent**: Rose (`--color-primary: #f43f5e`)
   - **Canvas Layout**: Top-bottom split. Top canvas renders a bridge carrying a vehicle. Bottom panel houses inequalities configurations.
   - **Mathematical Bounds**: Limit threshold variable L and current mass variable W.
   - **Controls**: Mass load slider (W in [0, 150] tons) and limit threshold slider (L in [20, 120] tons). Inequality operator selector (<, >, <=, >=).
   - **Logic/Visuals**: If the selection yields a false inequality (e.g. W > L when limit is breached), the bridge structural struts flash red and collapse, dropping the vehicle. Shows the inequality statement dynamically on a real-time number line.

4. **Geometric Transformations** (`03_geometry_measurement/geometric_transformations`)
   - **Theme Accent**: Emerald (`--color-primary: #10b981`)
   - **Canvas Layout**: Interactive grid canvas. Left panel for stamp selection (triangle, F-shape, star), right panel for action matrix.
   - **Mathematical Bounds**: Grid of 20 x 20 units.
   - **Controls**: Translation vectors (dx, dy) sliders, Rotation angle theta slider, Reflection axis toggle (X-axis, Y-axis, or y=x), Dilation scale factor s slider. Action buttons: "Translate", "Rotate", "Reflect", "Dilate".
   - **Logic/Visuals**: Renders a primary shape (green translucent). Applying transformations draws path vectors to show the transition of vertices to their secondary mapped coordinates (blue translucent stamp).

5. **Similarity, Congruence & Scale Factor** (`03_geometry_measurement/similarity_congruence`)
   - **Theme Accent**: Emerald (`--color-primary: #10b981`)
   - **Canvas Layout**: Shadow projection chamber mockup. Canvas displays a light source casting a shape's shadow onto a screen.
   - **Mathematical Bounds**: Distance variables mapping light source, object location, and screen height.
   - **Controls**: Draggable light source slider, draggable object slider, scale factor numeric input.
   - **Logic/Visuals**: Compares original object dimensions to shadow size. Visualizes how increasing distance from the light source alters shadow scale proportionally (maintaining similar angles, proving congruent shape profile but scaled area).

### Phase 3: Discrete Logic & Counting

6. **Set Theory & Venn Diagrams** (`06_data_science_statistics/set_theory_venn`)
   - **Theme Accent**: Purple (`--color-primary: #a855f7`)
   - **Canvas Layout**: Overlapping lens diagram canvas.
   - **Mathematical Bounds**: Two or three circles forming Set A, B, and C.
   - **Controls**: Set operation selectors (A intersects B, A union B, A minus B, A delta B).
   - **Logic/Visuals**: Drag-and-drop colorful geometric shapes with specific properties (e.g. "Red Circle", "Blue Triangle") onto the sorting field. Shapes snap to corresponding overlapping intersections based on active criteria, shading selected intersections in neon glow colors.

7. **Combinatorics & Permutations** (`06_data_science_statistics/combinatorics_counting`)
   - **Theme Accent**: Purple (`--color-primary: #a855f7`)
   - **Canvas Layout**: Safe dial vault lock mockup.
   - **Mathematical Bounds**: Number of dials n in [1, 5] and number of symbols per dial r in [2, 10].
   - **Controls**: Dial count incrementor, symbol size selector, toggle for "Permutations (Order matters)" vs. "Combinations (Order irrelevant)".
   - **Logic/Visuals**: Renders spinning cylinder lock wheels. Explores the combination tree space visually. Displays a tree graph connecting branches of possible secret codes to emphasize the exponential growth of permutations (n! and n^r).

### Phase 4: Higher-Order Curves & Asymptotes

8. **Polynomial Families & Extrema** (`02_algebra/polynomial_families`)
   - **Theme Accent**: Rose (`--color-primary: #f43f5e`)
   - **Canvas Layout**: Function plot grid with draggable coordinate pegs.
   - **Mathematical Bounds**: x in [-5, 5], y in [-15, 15].
   - **Controls**: Degree selection tabs (x^2, x^3, x^4) and coordinate peg controls.
   - **Logic/Visuals**: The function curve behaves like a flexible rubber string. Draggable vertex points (local extrema) deform the curve equation coefficients dynamically, computing turning points (extrema) and roots (x-intercepts) in real-time.

9. **Asymptotes & Rational Functions** (`02_algebra/rational_functions`)
   - **Theme Accent**: Rose (`--color-primary: #f43f5e`)
   - **Canvas Layout**: Coordinate space containing vertical/horizontal barrier walls and a moving charge particle.
   - **Mathematical Bounds**: f(x) = a / (x - h) + k.
   - **Controls**: Coefficients sliders (a, h, k) and a mouse/touch probe tracking tool.
   - **Logic/Visuals**: Draws vertical asymptote x = h (as a red dashed magnetic fence) and horizontal asymptote y = k. A draggable test particle is pulled by a cursor towards the barrier; as it approaches x -> h, the particle gets deflected and accelerates off screen to infinity, illustrating rational limits.

### Phase 5: Continuous Limits & Directional Fields

10. **Infinite Sequences & Series** (`05_calculus/sequences_series`)
    - **Theme Accent**: Indigo (`--color-primary: #6366f1`)
    - **Canvas Layout**: Infinite slicing grid mapping the geometric sum sum( (1/2)^n ) = 1.
    - **Mathematical Bounds**: Sum limit tracking between 0 and 1.
    - **Controls**: Term iteration slider (n in [1, 20]), sequence type toggle (Arithmetic, Geometric, Harmonic).
    - **Logic/Visuals**: Renders a large unit square. Each slider step cuts the remaining unshaded area in half and fills it with translucent colored patterns. Illustrates how infinite summation fills the target bounds completely without ever spilling outside the boundary of 1.

11. **Vector Geometry & Fields** (`05_calculus/vectors_fields`)
    - **Theme Accent**: Indigo (`--color-primary: #6366f1`)
    - **Canvas Layout**: High-density flow field grid.
    - **Mathematical Bounds**: Field coordinates F(x, y) = P(x, y)i + Q(x, y)j.
    - **Controls**: Field type selector (Source, Sink, Rotational Vortex, Saddle), flow speed slider, draggable coordinate anchor.
    - **Logic/Visuals**: Renders a grid of tiny translucent arrows pointing in direction of velocity field. Draggable coordinate anchor calculates curl/divergence values. Releasing particle seeds animations tracing stream curves in real-time.

### Phase 6: Network Routing & Computational Systems

12. **Graph Theory & Networks** (`07_computational_math/graph_theory_networks`)
    - **Theme Accent**: Indigo (`--color-primary: #6366f1`)
    - **Canvas Layout**: Delivery map showing houses (nodes) and roads (edges) with weights.
    - **Mathematical Bounds**: Node count N in [5, 12], Edge weights represent travel time or cost.
    - **Controls**: Interactive click-to-connect nodes tool, routing algorithm tabs (Dijkstra's Shortest Path, Minimum Spanning Tree).
    - **Logic/Visuals**: The user plays a delivery truck dispatcher connecting delivery endpoints. Activating Dijkstra's visualizes distance updates scanning through nodes step-by-step, highlighting the optimal low-cost highway structure in bright neon lines.

### Phase 7: Data Science & Statistics (Completed Stats Modules)

13. **Probability & Likelihood** (`06_data_science_statistics/probability_and_likelihood`)
    - **Theme Accent**: Purple (`--color-primary: #a855f7`)
    - **Canvas Layout**: Spin-physics circular wheel with 4 wedges (Red, Blue, Green, Yellow) and a top pointer needle. Renders alongside a horizontal likelihood adjective bar (Impossible to Certain) and an LLN line graph.
    - **Controls**: Wedge allocation sliders (0-10 shares), spin trigger button, and batch generators (+10, +100, +1000).
    - **Logic/Visuals**: Evaluates spin outcomes, tracking experimental ratios converging onto the theoretical target line (Law of Large Numbers) over time.

14. **Probability Distributions** (`06_data_science_statistics/probability_distributions`)
    - **Theme Accent**: Purple (`--color-primary: #a855f7`)
    - **Canvas Layout**: Dual tab panel: Discrete sums (6x6 combinations matrix and frequency charts) vs. Continuous distributions (Normal bell curve with shaded boundaries).
    - **Controls**: Mean ($\mu$) and Std Dev ($\sigma$) sliders, draggable boundary sliders ($a$, $b$).
    - **Logic/Visuals**: Evaluates normal curves CDF integrals ($P(a \le X \le b)$) dynamically using Abramowitz-Stegun approximations.

15. **Recording Data** (`06_data_science_statistics/recording_data`)
    - **Theme Accent**: Purple (`--color-primary: #a855f7`)
    - **Canvas Layout**: Scrolling green ledger logger terminal alongside a Pictograph canvas drawing horizontal emoji icons.
    - **Controls**: Observations clicker buttons, key scale slider (1 to 4 units per icon), and preset switches (Pets vs. Weather).
    - **Logic/Visuals**: Handles dynamic emoji clipping vectors to draw partial half-icons when division remainders require fractional counts.

16. **Statistical Inference & Hypothesis Testing** (`06_data_science_statistics/statistical_inference_hypothesis_testing`)
    - **Theme Accent**: Purple (`--color-primary: #a855f7`)
    - **Canvas Layout**: Standard normal Z-distribution curve showing red rejection critical regions and vertical calculated test-statistic markers, alongside a Confidence Interval coordinate scale.
    - **Controls**: Sliders for sample mean, size, standard deviation, tail type selector, and significance level ($\alpha$).
    - **Logic/Visuals**: Computes Z-scores and P-values in real-time, flashing large decision banners showing rejection outcomes.

17. **Time Series Forecasting** (`06_data_science_statistics/time_series`)
    - **Theme Accent**: Purple (`--color-primary: #a855f7`)
    - **Canvas Layout**: 30-month coordinate timeline canvas showing historical data points and forecasted projection lines.
    - **Controls**: Direct coordinate vertical dragging handlers on historical points, presets (Seasonal, Cycles, Noise), and smoothing method selector (SMA vs. SES).
    - **Logic/Visuals**: Shows phase lag shifts when smoothing factors alter, calculating MAE and regression slope parameters dynamically.

18. **Trend Lines & Linear Models** (`06_data_science_statistics/trend_lines_and_linear_models`)
    - **Theme Accent**: Purple (`--color-primary: #a855f7`)
    - **Canvas Layout**: 2D scatter coordinates canvas with a manual trend line and the optimal Least Squares Regression Line.
    - **Controls**: Add/delete points by double/right clicking, dragging points, and dragging two manual line endpoints (Anchor 1 at X=1, Anchor 2 at X=9).
    - **Logic/Visuals**: Renders pink vertical residual stems, calculating and comparing user SSR against the mathematical minimum SSR in real-time.

19. **Two-Way Tables & Relative Frequency** (`06_data_science_statistics/two_way_tables_and_relative_frequency`)
    - **Theme Accent**: Purple (`--color-primary: #a855f7`)
    - **Canvas Layout**: Proportional frequency table grid with inline cell adjusters, rendering alongside a horizontal stacked percentage bar canvas.
    - **Controls**: Cell increment clickers (`+`/`-`), display mode tabs (counts, joint, row/col relative conditionals), and association presets.
    - **Logic/Visuals**: Evaluates conditional differentials between rows, flagging if a statistical dependency association exists.

---
# Copyright (c) 2026:
# vatofichor - Sebastian Mass     [>_<]
# & Assisted By Gemini Antigravity /|\
