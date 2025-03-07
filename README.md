# Rotate 4D
A simple stereographic projection of a tesseract onto 3-space

## TODO
- [ ] Refactor code into distinct components
    - [ ] Shell
        - [ ] Have terminal read pressed keys in real time
    - [ ] Math
        - [ ] Better math processing (maybe C?)
    - [ ] Drawing
        - [ ] Implement in OpenGL. Note that this requires another projection
        - [ ] Explore matplotlib animation library


## Distinct Component Notes
### Shell
How the user sends inputs to the program. This includes changing 4D rotation angle, (if rendering in 2D) 3D viewing angle, and stereographic projection distance.
### Math
Manages everything that is not directly drawn on screen. This includes the stereographic projection. The Drawing component should be able to directly use the output of this component to draw.
### Drawing
Is given a set of points, and draws them on the screen. If this component leverages something like matplotlib that provides 3D graphing tools, then this component should receive coordinates in 3-space. If this component fully implements its own rendering process (like with OpenGL), then this component should receive coordinates in 2-space (a computer screen or window is only 2D).
