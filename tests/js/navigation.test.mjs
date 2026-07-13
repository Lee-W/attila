import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import vm from "node:vm";

class EventTarget {
  constructor() {
    this.listeners = new Map();
  }

  addEventListener(type, listener) {
    const listeners = this.listeners.get(type) ?? [];
    listeners.push(listener);
    this.listeners.set(type, listeners);
  }

  dispatch(type, event = {}) {
    event.preventDefault ??= () => {};
    event.stopPropagation ??= () => {};
    for (const listener of this.listeners.get(type) ?? []) listener(event);
  }
}

class ClassList {
  constructor() {
    this.values = new Set();
  }

  add(...names) {
    names.forEach((name) => this.values.add(name));
  }

  remove(...names) {
    names.forEach((name) => this.values.delete(name));
  }

  contains(name) {
    return this.values.has(name);
  }

  toggle(name, force) {
    const enabled = force ?? !this.contains(name);
    enabled ? this.add(name) : this.remove(name);
    return enabled;
  }
}

class Element extends EventTarget {
  constructor() {
    super();
    this.attributes = new Map();
    this.classList = new ClassList();
    this.focused = false;
    this.inert = false;
    this.querySelectorAll = () => [];
  }

  setAttribute(name, value) {
    this.attributes.set(name, String(value));
  }

  getAttribute(name) {
    return this.attributes.get(name) ?? null;
  }

  focus() {
    this.focused = true;
  }
}

const script = await readFile(
  "../src/pelican/themes/attila/static/js/script.js",
  "utf8",
);

test("mobile menu and theme controls keep their accessible state in sync", () => {
  const html = new Element();
  html.style = {};
  const menu = new Element();
  const close = new Element();
  const navigation = new Element();
  const firstNavigationItem = new Element();
  const lastNavigationItem = new Element();
  const wrapper = new Element();
  const theme = new Element();
  theme.setAttribute("data-dark", "Dark theme");
  theme.setAttribute("data-light", "Light theme");

  const document = new EventTarget();
  document.documentElement = html;
  document.activeElement = null;
  document.querySelector = (selector) =>
    ({ ".nav-menu": menu, ".nav-close": close, ".js-theme": theme })[
      selector
    ] ?? null;
  document.querySelectorAll = () => [];
  document.getElementById = (id) =>
    ({ "site-navigation": navigation, wrapper })[id] ?? null;
  navigation.querySelectorAll = () => [firstNavigationItem, lastNavigationItem];
  for (const element of [menu, firstNavigationItem, lastNavigationItem]) {
    element.focus = () => {
      element.focused = true;
      document.activeElement = element;
    };
  }

  const window = new EventTarget();
  window.matchMedia = () => ({ matches: false, addEventListener: () => {} });
  window.requestAnimationFrame = (callback) => callback();

  const values = new Map();
  const localStorage = {
    getItem: (key) => values.get(key) ?? null,
    setItem: (key, value) => values.set(key, value),
    removeItem: (key) => values.delete(key),
  };

  vm.runInNewContext(script, {
    AbortController,
    URL,
    document,
    localStorage,
    window,
  });
  document.dispatch("DOMContentLoaded");

  menu.dispatch("click");
  assert.equal(html.classList.contains("menu-active"), true);
  assert.equal(menu.getAttribute("aria-expanded"), "true");
  assert.equal(wrapper.inert, true);
  assert.equal(document.activeElement, firstNavigationItem);

  document.activeElement = lastNavigationItem;
  document.dispatch("keydown", { key: "Tab" });
  assert.equal(document.activeElement, firstNavigationItem);

  document.dispatch("keydown", { key: "Tab", shiftKey: true });
  assert.equal(document.activeElement, lastNavigationItem);

  document.dispatch("keydown", { key: "Escape" });
  assert.equal(html.classList.contains("menu-active"), false);
  assert.equal(menu.getAttribute("aria-expanded"), "false");
  assert.equal(wrapper.inert, false);
  assert.equal(menu.focused, true);

  // No saved preference and OS prefers light: the toggle reflects light
  // without writing to storage.
  assert.equal(theme.getAttribute("aria-pressed"), "false");
  assert.equal(theme.getAttribute("aria-label"), "Light theme");
  assert.equal(values.has("attila_theme"), false);

  theme.dispatch("click");
  assert.equal(theme.getAttribute("aria-pressed"), "true");
  assert.equal(theme.getAttribute("aria-label"), "Dark theme");
  assert.equal(values.get("attila_theme"), "dark");

  theme.dispatch("click");
  assert.equal(theme.getAttribute("aria-pressed"), "false");
  assert.equal(theme.getAttribute("aria-label"), "Light theme");
  assert.equal(values.get("attila_theme"), "light");

  theme.dispatch("click");
  assert.equal(theme.getAttribute("aria-pressed"), "true");
  assert.equal(theme.getAttribute("aria-label"), "Dark theme");
  assert.equal(values.get("attila_theme"), "dark");
});

test("first click flips away from the OS-dark effective theme when nothing is saved", () => {
  const html = new Element();
  html.style = {};
  const theme = new Element();
  theme.setAttribute("data-dark", "Dark theme");
  theme.setAttribute("data-light", "Light theme");

  const document = new EventTarget();
  document.documentElement = html;
  document.activeElement = null;
  document.querySelector = (selector) =>
    ({ ".js-theme": theme })[selector] ?? null;
  document.querySelectorAll = () => [];
  document.getElementById = () => null;

  const window = new EventTarget();
  // OS prefers dark, and the visitor has never saved a preference.
  window.matchMedia = () => ({ matches: true, addEventListener: () => {} });
  window.requestAnimationFrame = (callback) => callback();

  const values = new Map();
  const localStorage = {
    getItem: (key) => values.get(key) ?? null,
    setItem: (key, value) => values.set(key, value),
    removeItem: (key) => values.delete(key),
  };

  vm.runInNewContext(script, {
    AbortController,
    URL,
    document,
    localStorage,
    window,
  });
  document.dispatch("DOMContentLoaded");

  // Effective theme is dark (from the OS), even though no class is set.
  assert.equal(html.classList.contains("theme-dark"), false);
  assert.equal(html.classList.contains("theme-light"), false);
  assert.equal(theme.getAttribute("aria-pressed"), "true");
  assert.equal(theme.getAttribute("aria-label"), "Dark theme");
  assert.equal(values.has("attila_theme"), false);

  // The first click must flip away from dark (the effective theme), not
  // no-op or re-affirm dark.
  theme.dispatch("click");
  assert.equal(html.classList.contains("theme-light"), true);
  assert.equal(theme.getAttribute("aria-pressed"), "false");
  assert.equal(theme.getAttribute("aria-label"), "Light theme");
  assert.equal(values.get("attila_theme"), "light");
});
