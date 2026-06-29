import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { pathToFileURL } from "node:url";

const [solidDir, regularDir, brandsDir, output] = process.argv.slice(2);

if (!solidDir || !regularDir || !brandsDir || !output) {
  throw new Error(
    "usage: node scripts/build_icon_sprite.mjs SOLID REGULAR BRANDS OUTPUT",
  );
}

const icons = [
  ["bars", solidDir, "faBars"],
  ["search", solidDir, "faMagnifyingGlass"],
  ["chevron-down", solidDir, "faChevronDown"],
  ["rss", solidDir, "faRss"],
  ["language", solidDir, "faLanguage"],
  ["sun-outline", regularDir, "faSun"],
  ["sun", solidDir, "faSun"],
  ["moon", solidDir, "faMoon"],
  ["location", solidDir, "faLocationDot"],
  ["globe", solidDir, "faGlobe"],
  ["arrow-left", solidDir, "faArrowLeft"],
  ["arrow-right", solidDir, "faArrowRight"],
  ["email", solidDir, "faEnvelope"],
  ["facebook", brandsDir, "faFacebook"],
  ["github", brandsDir, "faGithub"],
  ["linkedin", brandsDir, "faLinkedin"],
  ["x-twitter", brandsDir, "faXTwitter"],
  ["instagram", brandsDir, "faInstagram"],
  ["twitter", brandsDir, "faTwitter"],
  ["mastodon", brandsDir, "faMastodon"],
  ["creative-commons", brandsDir, "faCreativeCommons"],
  ["creative-commons-by", brandsDir, "faCreativeCommonsBy"],
  ["creative-commons-nc", brandsDir, "faCreativeCommonsNc"],
  ["creative-commons-sa", brandsDir, "faCreativeCommonsSa"],
  ["creative-commons-nd", brandsDir, "faCreativeCommonsNd"],
  ["creative-commons-zero", brandsDir, "faCreativeCommonsZero"],
  ["creative-commons-pd", brandsDir, "faCreativeCommonsPd"],
];

const symbols = [];
for (const [id, directory, exportName] of icons) {
  const modulePath = join(directory, `${exportName}.js`);
  await readFile(modulePath);
  const module = await import(pathToFileURL(modulePath));
  const { icon } = module[exportName];
  const [width, height, , , path] = icon;
  const paths = Array.isArray(path)
    ? path.map((value) => `<path d="${value}"/>`).join("")
    : `<path d="${path}"/>`;
  symbols.push(
    `<symbol id="${id}" viewBox="0 0 ${width} ${height}">${paths}</symbol>`,
  );
}

await mkdir(dirname(output), { recursive: true });
await writeFile(
  output,
  `<svg xmlns="http://www.w3.org/2000/svg"><defs>${symbols.join("")}</defs></svg>\n`,
);
