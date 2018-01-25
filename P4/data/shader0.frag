#define PROCESSING_COLOR_SHADER

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

varying vec4 vertColor;
varying vec4 vertTexCoord;

void main() {

    // create an array that holds all of the circle centers
    vec2 array[9] = vec2[] (vec2(0.2, 0.8), vec2(0.5, 0.8), vec2(0.8, 0.8),
                            vec2(0.2, 0.5), vec2(0.5, 0.5), vec2(0.8, 0.5),
                            vec2(0.2, 0.2), vec2(0.5, 0.2), vec2(0.8, 0.2));

    for(int i = 0; i < 9; i++) {
        if(pow(array[i].x - vertTexCoord.x, 2) + pow(array[i].y - vertTexCoord.y, 2) < pow(0.1, 2)) {
            gl_FragColor = vec4(0.2, 0.4, 1.0, 0.0);
            return;
        } else {
            gl_FragColor = vec4(0.2, 0.4, 1.0, 0.8);
        }
    }

}
