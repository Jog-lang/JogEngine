#version 450

// SDL_GPU SPIR-V fragment shader (Vulkan backend).
// Fragment samplers: set=2 binding=N (slot from BindGPUFragmentSamplers).

layout(location = 0) in vec2 frag_uv;
layout(location = 1) in vec3 frag_normal;

layout(set = 2, binding = 0) uniform sampler2D tex;

layout(location = 0) out vec4 fragColor;

void main() {
    vec3 N = normalize(frag_normal);
    vec3 L = normalize(vec3(0.4, 0.7, 0.35));
    float ndotl = max(dot(N, L), 0.0);
    vec4 albedo = texture(tex, frag_uv);
    float lighting = 0.25 + 0.75 * ndotl;
    fragColor = vec4(albedo.rgb * lighting, albedo.a);
}
