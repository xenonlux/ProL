BITS 64
  org 0x400000

ehdr:
  db 0x7F,"ELF"
  db 2
  db 1
  db 1
  db 0
  db 0
  times 7 db 0
  dw 2
  dw 0x3E
  dd 1
  dq _start
  dq phdr - ehdr
  dq 0
  dd 0
  dw ehdrsize
  dw phdrsize
  dw 1
  dw 0
  dw 0
  dw 0
ehdrsize equ $ - ehdr

phdr:
  dd 1
  dd 7
  dq 0
  dq ehdr
  dq ehdr
  dq filesize
  dq filesize
  dq 0x1000
phdrsize equ $ - phdr

program:
  db 1, 10
  db 2, 5
  db 3, 3
  db 2, 30
  db 0

_start:
  xor rax, rax
  lea rbx, [rel program]

vm_loop:
  movzx ecx, byte [rbx]
  inc rbx

  cmp ecx, 1
  je op_load
  cmp ecx, 2
  je op_add
  cmp ecx, 3
  je op_sub
  cmp ecx, 0
  je op_halt

  mov edi, 255
  jmp do_exit

op_load:
  movzx eax, byte [rbx]
  inc rbx
  jmp vm_loop

op_add:
  movzx ecx, byte [rbx]
  add eax, ecx
  inc rbx
  jmp vm_loop

op_sub:
  movzx ecx, byte [rbx]
  sub eax, ecx
  inc rbx
  jmp vm_loop

op_halt:
  mov edi, eax

do_exit:
  mov eax, 60
  syscall

filesize equ $ - ehdr
