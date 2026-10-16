/**
 * make-logos.mjs — copies the official brand SVGs (simple-icons, CC0)
 * into public/logos with their licence, for the Skills section.
 *   node scripts/make-logos.mjs
 */
import { mkdirSync, writeFileSync } from "node:fs";
import * as si from "simple-icons";

const WANT = {
  google: "Google Workspace",
  microsoft: "Microsoft 365",
  moodle: "Moodle",
  canvas: "Canvas LMS",
  zoom: "Zoom",
  obsstudio: "OBS Studio",
};

const dir = new URL("../public/logos/", import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1");
mkdirSync(dir, { recursive: true });

let ok = 0;
for (const [slug, label] of Object.entries(WANT)) {
  const icon = si[`si${slug.charAt(0).toUpperCase()}${slug.slice(1)}`];
  if (!icon) { console.warn(`skip ${slug} (not in simple-icons)`); continue; }
  const svg =
    `<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" width="64" height="64">` +
    `<title>${label}</title><path fill="#${icon.hex}" d="${icon.path}"/></svg>\n`;
  writeFileSync(`${dir}/${slug}.svg`, svg);
  console.log(`ok ${slug}.svg  #${icon.hex}`);
  ok++;
}

writeFileSync(
  `${dir}/LICENSE`,
  `Brand logos in this folder come from simple-icons (https://simple-icons.com),\n` +
  `licensed CC0 1.0 (https://creativecommons.org/publicdomain/zero/1.0/).\n` +
  `The logos themselves are trademarks of their respective owners and are used\n` +
  `here only to identify the referenced technologies.\n` +
  `Concept-skill line icons are original work of this repository (MIT licence\n` +
  `as declared in the repository root).\n`
);
console.log(`\n${ok}/${Object.keys(WANT).length} logos written to public/logos + LICENSE`);
