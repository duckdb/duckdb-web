---
layout: docu
title: Array Functions
---

<!-- markdownlint-disable MD001 -->

All [`LIST` functions]({% link docs/archive/1.1/sql/functions/list.md %}) work with the [`ARRAY` data type]({% link docs/archive/1.1/sql/data_types/array.md %}). Additionally, several `ARRAY`-native functions are also supported.

## Array-Native Functions

| Function | Description |
|----|-----|-------|---|
| [`array_value(index)`](#array_valueindex)                                                      | Create an `ARRAY` containing the argument values.                                                                                                                                                                                              |
| [`array_cross_product(array1, array2)`](#array_cross_productarray1-array2)                     | Compute the cross product of two arrays of size 3. The array elements can not be `NULL`.                                                                                                                                                       |
| [`array_cosine_similarity(array1, array2)`](#array_cosine_similarityarray1-array2)             | Compute the cosine similarity between two arrays of the same size. The array elements can not be `NULL`. The arrays can have any size as long as the size is the same for both arguments.                                                      |
| [`array_cosine_distance(array1, array2)`](#array_cosine_distancearray1-array2)                 | Compute the cosine distance between two arrays of the same size. The array elements can not be `NULL`. The arrays can have any size as long as the size is the same for both arguments. This is equivalent to `1.0 - array_cosine_similarity`. |
| [`array_distance(array1, array2)`](#array_distancearray1-array2)                               | Compute the distance between two arrays of the same size. The array elements can not be `NULL`. The arrays can have any size as long as the size is the same for both arguments.                                                               |
| [`array_inner_product(array1, array2)`](#array_inner_productarray1-array2)                     | Compute the inner product between two arrays of the same size. The array elements can not be `NULL`. The arrays can have any size as long as the size is the same for both arguments.                                                          |
| [`array_negative_inner_product(array1, array2)`](#array_negative_inner_productarray1-array2)   | Compute the negative inner product between two arrays of the same size. The array elements can not be `NULL`. The arrays can have any size as long as the size is the same for both arguments. This is equivalent to `-array_inner_product`.   |
| [`array_dot_product(array1, array2)`](#array_dot_productarray1-array2)                         | Alias for `array_inner_product(array1, array2)`.                                                                                                                                                                                               |
| [`array_negative_dot_product(array1, array2)`](#array_negative_dot_productarray1-array2)       | Alias for `array_negative_inner_product(array1, array2)`.                                                                                                                                                                                      |

#### `array_value(index)`

<div class="nostroke_table"></div>

| **Description** | Create an `ARRAY` containing the argument values. |
| **Example** | `array_value(1.0::FLOAT, 2.0::FLOAT, 3.0::FLOAT)` |
| **Result** | `[1.0, 2.0, 3.0]` |

#### `array_cross_product(array1, array2)`

<div class="nostroke_table"></div>

| **Description** | Compute the cross product of two arrays of size 3. The array elements can not be `NULL`. |
| **Example** | `array_cross_product(array_value(1.0::FLOAT, 2.0::FLOAT, 3.0::FLOAT), array_value(2.0::FLOAT, 3.0::FLOAT, 4.0::FLOAT))` |
| **Result** | `[-1.0, 2.0, -1.0]` |

#### `array_cosine_similarity(array1, array2)`

<div class="nostroke_table"></div>

| **Description** | Compute the cosine similarity between two arrays of the same size. The array elements can not be `NULL`. The arrays can have any size as long as the size is the same for both arguments. |
| **Example** | `array_cosine_similarity(array_value(1.0::FLOAT, 2.0::FLOAT, 3.0::FLOAT), array_value(2.0::FLOAT, 3.0::FLOAT, 4.0::FLOAT))` |
| **Result** | `0.9925833` |

#### `array_cosine_distance(array1, array2)`

<div class="nostroke_table"></div>

| **Description** | Compute the cosine distance between two arrays of the same size. The array elements can not be `NULL`. The arrays can have any size as long as the size is the same for both arguments. This is equivalent to `1.0 - array_cosine_similarity`. |
| **Example** | `array_cosine_distance(array_value(1.0::FLOAT, 2.0::FLOAT, 3.0::FLOAT), array_value(2.0::FLOAT, 3.0::FLOAT, 4.0::FLOAT))` |
| **Result** | `0.007416606` |

#### `array_distance(array1, array2)`

<div class="nostroke_table"></div>

| **Description** | Compute the distance between two arrays of the same size. The array elements can not be `NULL`. The arrays can have any size as long as the size is the same for both arguments. |
| **Example** | `array_distance(array_value(1.0::FLOAT, 2.0::FLOAT, 3.0::FLOAT), array_value(2.0::FLOAT, 3.0::FLOAT, 4.0::FLOAT))` |
| **Result** | `1.7320508` |

#### `array_inner_product(array1, array2)`

<div class="nostroke_table"></div>

| **Description** | Compute the inner product between two arrays of the same size. The array elements can not be `NULL`. The arrays can have any size as long as the size is the same for both arguments. |
| **Example** | `array_inner_product(array_value(1.0::FLOAT, 2.0::FLOAT, 3.0::FLOAT), array_value(2.0::FLOAT, 3.0::FLOAT, 4.0::FLOAT))` |
| **Result** | `20.0` |

#### `array_negative_inner_product(array1, array2)`

<div class="nostroke_table"></div>

| **Description** | Compute the negative inner product between two arrays of the same size. The array elements can not be `NULL`. The arrays can have any size as long as the size is the same for both arguments. This is equivalent to `-array_inner_product` |
| **Example** | `array_inner_product(array_value(1.0::FLOAT, 2.0::FLOAT, 3.0::FLOAT), array_value(2.0::FLOAT, 3.0::FLOAT, 4.0::FLOAT))` |
| **Result** | `-20.0` |

#### `array_dot_product(array1, array2)`

<div class="nostroke_table"></div>

| **Description** | Alias for `array_inner_product(array1, array2)`. |
| **Example** | `array_dot_product(l1, l2)` |
| **Result** | `20.0` |

#### `array_negative_dot_product(array1, array2)`

<div class="nostroke_table"></div>

| **Description** | Alias for `array_negative_inner_product(array1, array2)`. |
| **Example** | `array_negative_dot_product(l1, l2)` |
| **Result** | `-20.0` |