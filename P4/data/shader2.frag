#define PROCESSING_COLOR_SHADER

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

varying vec4 vertColor;
varying vec4 vertTexCoord;

void main() {

    // original cx, cy is between [0, 1]. Need to convert the domain to become [-2.1, 0.9] and [-1.5, 1.5]
    float cx = (vertTexCoord.x * 3.0) - 2.1;
    float cy = (vertTexCoord.y * 3.0) - 1.5;

    float real = 0.0;
    float imag = 0.0;
    for(int i = 0; i < 20; i++) {
        float oldRealSquared = pow(real, 2) - pow(imag, 2);
        float oldImagSquared = 2 * real * imag;
        real = oldRealSquared + cx;
        imag = oldImagSquared + cy;

        if(pow(real, 2) + pow(imag, 2) < 4) {
            // if within radius of 2, then color it white
            gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
        } else {
            gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
        }
    }

}
