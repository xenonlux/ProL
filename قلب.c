#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdint.h>

// ============================================
// ١. قاموس اللغة العربية
// ============================================
typedef struct {
    char *ar;
    int op;
} Cmd;

#define OP_LOAD 1
#define OP_ADD  2
#define OP_SUB  3
#define OP_MUL  4
#define OP_DIV  5
#define OP_PRT  6
#define OP_HALT 7
#define OP_SQRT 8
#define OP_POW  9
#define OP_CMP  10
#define OP_JMP  11
#define OP_JZ   12
#define OP_LOOP 13
#define OP_RUN  14
#define OP_TRAIN 15
#define OP_BUILD 16

Cmd dict[] = {
    {"شغل", OP_RUN}, {"شغّل", OP_RUN}, {"نفذ", OP_RUN},
    {"درب", OP_TRAIN}, {"درّب", OP_TRAIN}, {"علم", OP_TRAIN},
    {"ابنِ", OP_BUILD}, {"ابني", OP_BUILD}, {"أنشئ", OP_BUILD},
    {"اجمع", OP_ADD}, {"اطرح", OP_SUB}, {"اضرب", OP_MUL}, {"اقسم", OP_DIV},
    {"قارن", OP_CMP}, {"جذر", OP_SQRT}, {"قوة", OP_POW},
    {"كرر", OP_LOOP}, {"اعرض", OP_PRT},
    {NULL, 0}
};

// ============================================
// ٢. الآلة الافتراضية (VM)
// ============================================
typedef struct {
    uint8_t *code;
    int len;
    int ip;
    int regs[4];
    int flag_z;
    int running;
} VM;

void vm_init(VM *vm, uint8_t *code, int len) {
    vm->code = code;
    vm->len = len;
    vm->ip = 0;
    vm->regs[0] = 0; vm->regs[1] = 0;
    vm->regs[2] = 0; vm->regs[3] = 0;
    vm->flag_z = 0;
    vm->running = 1;
}

int vm_run(VM *vm) {
    while (vm->running && vm->ip < vm->len) {
        uint8_t op = vm->code[vm->ip++];
        switch (op) {
            case OP_LOAD:
                vm->regs[0] = vm->code[vm->ip++];
                break;
            case OP_ADD:
                vm->regs[0] += vm->code[vm->ip++];
                break;
            case OP_SUB:
                vm->regs[0] -= vm->code[vm->ip++];
                break;
            case OP_MUL:
                vm->regs[0] *= vm->code[vm->ip++];
                break;
            case OP_DIV:
                vm->regs[0] /= (vm->code[vm->ip++] ?: 1);
                break;
            case OP_SQRT:
                vm->regs[0] = (int)(sqrt(vm->regs[0]));
                break;
            case OP_POW:
                vm->regs[0] = vm->regs[0] * vm->regs[0];
                break;
            case OP_CMP:
                vm->flag_z = (vm->regs[0] == vm->code[vm->ip++]);
                break;
            case OP_PRT:
                printf("🖨️ %d\n", vm->regs[0]);
                break;
            case OP_LOOP: {
                int n = vm->code[vm->ip++];
                for (int i = 0; i < n; i++) printf("  ♻️ %d\n", i+1);
                vm->regs[0] = n;
                break;
            }
            case OP_HALT:
                vm->running = 0;
                return vm->regs[0];
            default:
                break;
        }
    }
    return vm->regs[0];
}

// ============================================
// ٣. المترجم: عربي → VM bytecode
// ============================================
int compile(char *src, uint8_t *out) {
    int pos = 0;
    char *word = strtok(src, " \n");
    int cmd = -1;
    int val = -1;
    
    while (word != NULL) {
        // بحث عن أمر
        for (int i = 0; dict[i].ar != NULL; i++) {
            if (strcmp(word, dict[i].ar) == 0) {
                cmd = dict[i].op;
                break;
            }
        }
        // رقم؟
        if (word[0] >= '0' && word[0] <= '9') val = atoi(word);
        word = strtok(NULL, " \n");
    }
    
    if (cmd == -1) return -1;
    
    switch (cmd) {
        case OP_ADD: out[pos++] = OP_LOAD; out[pos++] = val>0?val:0;
                      out[pos++] = OP_ADD; out[pos++] = val>0?val:0;
                      out[pos++] = OP_PRT; break;
        case OP_SUB: out[pos++] = OP_LOAD; out[pos++] = val>0?val:0;
                      out[pos++] = OP_SUB; out[pos++] = val>0?val:0;
                      out[pos++] = OP_PRT; break;
        case OP_MUL: out[pos++] = OP_LOAD; out[pos++] = val>0?val:0;
                      out[pos++] = OP_MUL; out[pos++] = val>0?val:0;
                      out[pos++] = OP_PRT; break;
        case OP_DIV: out[pos++] = OP_LOAD; out[pos++] = val>0?val:0;
                      out[pos++] = OP_DIV; out[pos++] = val>0?val:val?val:1;
                      out[pos++] = OP_PRT; break;
        case OP_SQRT: out[pos++] = OP_LOAD; out[pos++] = val>0?val:16;
                       out[pos++] = OP_SQRT; out[pos++] = OP_PRT; break;
        case OP_POW: out[pos++] = OP_LOAD; out[pos++] = val>0?val:2;
                      out[pos++] = OP_POW; out[pos++] = OP_PRT; break;
        case OP_CMP: out[pos++] = OP_LOAD; out[pos++] = val>0?val:0;
                      out[pos++] = OP_CMP; out[pos++] = val>0?val:0;
                      out[pos++] = OP_PRT; break;
        case OP_LOOP: out[pos++] = OP_LOOP; out[pos++] = val>0?val:3;
                       out[pos++] = OP_PRT; break;
        case OP_RUN: case OP_TRAIN: case OP_BUILD:
                      out[pos++] = OP_LOAD; out[pos++] = val>0?val:1;
                      out[pos++] = OP_PRT; break;
        case OP_PRT: out[pos++] = OP_LOAD; out[pos++] = val>0?val:0;
                      out[pos++] = OP_PRT; break;
        default: break;
    }
    out[pos++] = OP_HALT;
    return pos;
}

// ============================================
// ٤. مولد ELF x86-64 (من bytecode إلى كود آلة حقيقي)
// ============================================
void generate_elf(uint8_t *bytecode, int len, char *path) {
    FILE *f = fopen(path, "wb");
    
    // ELF Header
    uint8_t elf_hdr[64] = {
        0x7F,'E','L','F', 2,1,1,0, 0,0,0,0,0,0,0,0,
        2,0, 0x3E,0, 1,0,0,0,
        0x78,0x00,0x40,0x00,0x00,0x00,0x00,0x00, // entry
        0x40,0,0,0,0,0,0,0, // phoff
        0,0,0,0,0,0,0,0,    // shoff
        0,0,0,0,
        0x40,0, 0x38,0, 1,0,0,0, 0,0,0,0, 0,0,0,0
    };
    
    // Program Header
    uint8_t phdr[56] = {
        1,0,0,0, 7,0,0,0,
        0,0,0,0,0,0,0,0,   // offset
        0,0,0x40,0,0,0,0,0, // vaddr
        0,0,0x40,0,0,0,0,0, // paddr
        0,0,0,0,0,0,0,0,    // filesz
        0,0,0,0,0,0,0,0,    // memsz
        0,0x10,0,0,0,0,0,0  // align
    };
    
    // كود x86-64
    uint8_t code[256];
    int clen = 0;
    
    // mov eax, imm
    code[clen++] = 0xB8;
    code[clen++] = bytecode[1];
    code[clen++] = 0;
    code[clen++] = 0;
    code[clen++] = 0;
    
    // mov edi, eax
    code[clen++] = 0x89; code[clen++] = 0xC7;
    // mov eax, 60 (sys_exit)
    code[clen++] = 0xB8; code[clen++] = 0x3C;
    code[clen++] = 0; code[clen++] = 0; code[clen++] = 0;
    // syscall
    code[clen++] = 0x0F; code[clen++] = 0x05;
    
    int total = 64 + 56 + clen;
    uint64_t entry = 0x400000 + 64 + 56;
    uint64_t filesz = total;
    
    // Fixup
    memcpy(elf_hdr+24, &entry, 8);
    memcpy(phdr+32, &filesz, 8);
    memcpy(phdr+40, &filesz, 8);
    
    fwrite(elf_hdr, 1, 64, f);
    fwrite(phdr, 1, 56, f);
    fwrite(code, 1, clen, f);
    fclose(f);
    chmod(path, 0755);
}

// ============================================
// ٥. الرئيسي - مترجم كامل
// ============================================
int main(int argc, char **argv) {
    printf("🫀 القلب الناطق (C - مستقل)\n");
    
    char line[1024];
    uint8_t bytecode[256];
    
    if (argc > 1) {
        // ملف
        FILE *f = fopen(argv[1], "r");
        if (!f) { printf("❌ ملف غير موجود\n"); return 1; }
        while (fgets(line, 1024, f)) {
            line[strcspn(line, "\n")] = 0;
            printf("📝 %s\n", line);
            int len = compile(line, bytecode);
            if (len > 0) {
                VM vm;
                vm_init(&vm, bytecode, len);
                int r = vm_run(&vm);
                printf("✅ %d\n", r);
                
                // إنتاج ELF
                char elf_path[256];
                snprintf(elf_path, 256, "%s.elf", argv[1]);
                generate_elf(bytecode, len, elf_path);
                printf("📦 %s\n", elf_path);
            }
        }
        fclose(f);
    } else {
        // تفاعلي
        while (1) {
            printf("\n📝 > ");
            if (!fgets(line, 1024, stdin)) break;
            line[strcspn(line, "\n")] = 0;
            if (strcmp(line, "خروج") == 0) break;
            
            int len = compile(line, bytecode);
            if (len > 0) {
                VM vm;
                vm_init(&vm, bytecode, len);
                int r = vm_run(&vm);
                printf("✅ %d\n", r);
            } else {
                printf("❌ لم أفهم\n");
            }
        }
    }
    return 0;
}
