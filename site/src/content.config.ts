import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const vaultRoot = path.resolve(__dirname, '../..'); // src → site → vault root

const clefNotes = defineCollection({
  loader: glob({
    pattern: ['**/*.md', '!**/CLAUDE.md', '!**/index.md', '!**/log.md'],
    base: path.join(vaultRoot, 'Cleef Notes'),
  }),
  schema: z.object({
    type: z.string().optional(),
    module: z.string().optional(),
    lesson: z.string().optional(),
    title: z.string().optional(),
    last_updated: z.union([z.string(), z.date()]).transform(v => v instanceof Date ? v.toISOString().split('T')[0] : v).optional(),
    tags: z.array(z.string()).optional(),
  }),
});

export const collections = { 'clef-notes': clefNotes };
