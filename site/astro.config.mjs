import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const vaultRoot = path.resolve(__dirname, '..');

export default defineConfig({
  site: 'https://etiennenel.com',
  vite: {
    plugins: [tailwindcss()],
    server: {
      fs: { allow: [vaultRoot] },
    },
  },
});
