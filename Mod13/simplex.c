#include <stdio.h>


#define DEFAULT_CAPACITY 20

typedef struct {
	int rows;
	int columns;
	double** arr;
} Tab;


//
//
// void tab_add(StringBuffer* sb, char c) {
//
//     if (sb->count >= sb->capacity) {
//         // increase capacity of items by 2
//         size_t new_capacity;
//         if (sb->capacity == 0) {
//             new_capacity = DEFAULT_CAPACITY;
//         } else {
//             new_capacity = sb->capacity * 2;
//         }
//
//         sb->items = (char*)realloc(sb->items, sizeof(*sb->items) * new_capacity);
//         assert(sb->items != NULL && "String Buffer Overflow");
//     }
//     // sb->count++;
//     sb->items[sb->count++] = c;
// }

