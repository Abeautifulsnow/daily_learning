/**
 * Convert any integer to a base-based byte array.
 * @param number
 * @param radix
 * @returns
 */
export default function numToByte<T extends number>(
  number: T,
  radix: T
): string[] {
  if (Number.isNaN(number)) return [];

  let str = Math.abs(number).toString(radix);
  if (str.length % 2) str = str.padStart(str.length + 1, "0");

  return str.match(/(.{2})/g) ?? [];
}
