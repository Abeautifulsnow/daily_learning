// Fuse.js 模糊搜索库封装, 安装完fuse.js和vue3之后，直接在项目中引用使用。
import Fuse from 'fuse.js'
import { unref, computed, ref, watch } from 'vue'
import type { ComputedRef, Ref } from 'vue'

/**
 * Maybe it's a ref, or a plain value
 *
 * ```ts
 * type MaybeRef<T> = T | Ref<T>
 * ```
 */
export type MaybeRef<T> = T | Ref<T>

/**
 * Maybe it's a computed ref, or a getter function
 *
 * ```ts
 * type MaybeReadonlyRef<T> = (() => T) | ComputedRef<T>
 * ```
 */
export type MaybeReadonlyRef<T> = (() => T) | ComputedRef<T>

/**
 * Maybe it's a ref, or a plain value, or a getter function
 *
 * ```ts
 * type MaybeComputedRef<T> = (() => T) | T | Ref<T> | ComputedRef<T>
 * ```
 */
export type MaybeComputedRef<T> = MaybeReadonlyRef<T> | MaybeRef<T>

/**
 * Get the value of value/ref/getter.
 */
export function resolveUnref<T>(f: MaybeComputedRef<T>): T {
  return typeof f === 'function' ? (f as any)() : unref(f)
}

export type FuseOptions<T> = Fuse.IFuseOptions<T>
export interface UseFuseOptions<T> {
  fuseOptions?: FuseOptions<T>
  resultLimit?: number
  matchAllWhenSearchEmpty?: boolean
}

export function useFuse<DataItem>(
  search: MaybeComputedRef<string>,
  data: MaybeComputedRef<DataItem[]>,
  options?: MaybeComputedRef<UseFuseOptions<DataItem>>,
) {
  const createFuse = () => {
    return new Fuse(
      resolveUnref(data) ?? [],
      resolveUnref(options)?.fuseOptions,
    )
  }

  const fuse = ref(createFuse())

  watch(
    () => resolveUnref(options)?.fuseOptions,
    () => {
      fuse.value = createFuse()
    },
    { deep: true },
  )

  watch(
    () => resolveUnref(data),
    (newData) => {
      fuse.value.setCollection(newData)
    },
    { deep: true },
  )

  const results: ComputedRef<Fuse.FuseResult<DataItem>[]> = computed(() => {
    const resolved = resolveUnref(options)

    if (resolved?.matchAllWhenSearchEmpty && !unref(search)) {
      return resolveUnref(data).map((item, index) => ({
        item,
        refIndex: index,
      }))
    }

    const limit = resolved?.resultLimit
    return fuse.value.search(
      resolveUnref(search),
      limit ? { limit } : undefined,
    )
  })

  return {
    fuse,
    results,
  }
}

export type UseFuseReturn = ReturnType<typeof useFuse>
