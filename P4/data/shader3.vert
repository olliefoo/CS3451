#define PROCESSING_TEXTURE_SHADER

uniform mat4 transform;
uniform mat4 texMatrix;

attribute vec4 position;
attribute vec4 color;
attribute vec3 normal;
attribute vec2 texCoord;

varying vec4 vertColor;
varying vec4 vertTexCoord;

uniform sampler2D texture;

void main() {
  vertColor = color;
  vertTexCoord = texMatrix * vec4(texCoord, 1.0, 1.0);

  vec4 textureColor = texture2D(texture, vertTexCoord.xy);
  float grey = (textureColor.r * 0.3) + (textureColor.g * 0.6) + (textureColor.b * 0.1);
  // scales the color for desired mountain height
  grey *= 200;

  // normal is vec3, so need to wrap it around vec4
  vec4 pos = position + vec4(grey*normal, 0.0);
  gl_Position = transform * pos;
}
