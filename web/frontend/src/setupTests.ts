/*
Jest (the test runner) runs this file first before running any of the test suites.
Create mock matchMedia and localStorage for the tests to work.
*/
window.matchMedia = window.matchMedia || function () {
  return {
    matches: false,
    addListener: function () { },
    removeListener: function () { }
  };
};

class LocalStorageMock {
  store = {};
  constructor() {
    this.store = {};
  }

  clear() {
    this.store = {};
  }

  getItem(key) {
    return this.store[key];
  }

  setItem(key, value) {
    this.store[key] = value.toString();
  }

  removeItem(key) {
    delete this.store[key];
  }
};

window.localStorage = new LocalStorageMock;