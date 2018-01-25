#define PROCESSING_TEXTURE_SHADER

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

uniform sampler2D texture;

varying vec4 vertColor;
varying vec4 vertTexCoord;

void main() {
  vec4 diffuse_color = texture2D(texture, vertTexCoord.xy);

  float shift = 1.0 / 256.0;

  // finds the 4 surrounding pixels
  vec2 left = vec2(vertTexCoord.x - shift, vertTexCoord.y);
  vec2 right = vec2(vertTexCoord.x + shift, vertTexCoord.y);
  vec2 up = vec2(vertTexCoord.x, vertTexCoord.y + shift);
  vec2 down = vec2(vertTexCoord.x, vertTexCoord.y - shift);

  // gets the color of the surrounding pixels
  vec4 leftColor = texture2D(texture, left);
  vec4 rightColor = texture2D(texture, right);
  vec4 upColor = texture2D(texture, up);
  vec4 downColor = texture2D(texture, down);

  // convert all color to greyscale
  float centerGrey = (diffuse_color.r * 0.3) + (diffuse_color.g * 0.6) + (diffuse_color.b * 0.1);
  float leftGrey = (leftColor.r * 0.3) + (leftColor.g * 0.6) + (leftColor.b * 0.1);
  float rightGrey = (rightColor.r * 0.3) + (rightColor.g * 0.6) + (rightColor.b * 0.1);
  float upGrey = (upColor.r * 0.3) + (upColor.g * 0.6) + (upColor.b * 0.1);
  float downGrey = (downColor.r * 0.3) + (downColor.g * 0.6) + (downColor.b * 0.1);

  float finalColor = (leftGrey + rightGrey + upGrey + downGrey) - (4 * centerGrey);
  // scales the color so edges can be seen more easily
  finalColor *= 8;

  gl_FragColor = vec4(finalColor, finalColor, finalColor, 1.0);
}
