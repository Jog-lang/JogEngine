/* Host helper: f64 -> IEEE-754 f32 bit pattern (needed while gpu_present.jog is in the library). */
.globl jog_f32_bits
.type jog_f32_bits, @function
jog_f32_bits:
    cvtsd2ss %xmm0, %xmm0
    movd %xmm0, %eax
    ret
.size jog_f32_bits, .-jog_f32_bits
