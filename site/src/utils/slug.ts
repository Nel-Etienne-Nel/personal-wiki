/**
 * Convert a Astro content collection entry `id` to a clean URL slug.
 *
 * Astro's glob loader (v6+) runs each path segment through github-slugger
 * before setting `note.id`, so the raw path "00 - Archive/Module 1 - The Setup/Lesson 1.1 - Welcome.md"
 * arrives here as "00---archive/module-1---the-setup/lesson-11---welcome.md".
 *
 * Transform order per segment:
 *   1. Collapse any run of non-alphanumeric chars to a single hyphen.
 *   2. Strip a leading digit-only prefix (e.g. "00-", "01-") produced by the folder number.
 *   3. Trim leading/trailing hyphens.
 */
export function toSlug(id: string): string {
  return id
    .replace(/\.md$/, '')
    .split('/')
    .map(part =>
      part
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')   // normalise separators first
        .replace(/^\d+-/, '')           // strip leading "NN-" folder prefix
        .replace(/^-+|-+$/g, '')        // trim edge hyphens
    )
    .join('/');
}
