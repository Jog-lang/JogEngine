#version 450

// SDL_GPU SPIR-V vertex shader (Vulkan backend).
// Vertex uniforms: set=1 binding=N (slot_index from PushGPUVertexUniformData).
// Prefer a single 64-byte push: column-major mat4 mvp.

layout(location = 0) in vec3 in_position;
layout(location = 1) in vec2 in_uv;
layout(location = 2) in vec3 in_normal;

layout(set = 1, binding = 0) uniform VertexUniforms {
    mat4 mvp;
};

layout(location = 0) out vec2 frag_uv;
layout(location = 1) out vec3 frag_normal;

void main() {
    frag_uv = in_uv;
    // Model-space normals; host can bake world normals into the buffer later.
    frag_normal = in_normal;
    gl_Position = mvp * vec4(in_position, 1.0);
}
