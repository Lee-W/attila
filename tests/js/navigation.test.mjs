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

  const window = new EventTarget();
  window.matchMedia = () => ({ matches: false });
  window.requestAnimationFrame = (callback) => callback();

  const values = new Map();
  const localStorage = {
    getItem: (key) => values.get(key) ?? null,
    setItem: (key, value) => values.set(key, value),
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

  document.dispatch("keydown", { key: "Escape" });
  assert.equal(html.classList.contains("menu-active"), false);
  assert.equal(menu.getAttribute("aria-expanded"), "false");
  assert.equal(menu.focused, true);

  assert.equal(theme.getAttribute("aria-pressed"), "false");
  assert.equal(theme.getAttribute("aria-label"), "Light theme");
  theme.dispatch("click");
  assert.equal(theme.getAttribute("aria-pressed"), "true");
  assert.equal(theme.getAttribute("aria-label"), "Dark theme");
});
