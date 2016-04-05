/// <reference path="../typings/main.d.ts" />

import Dependency from "../src/Dependency";

describe("A dependency", function () {
    var dep = new Dependency("dep", "v1.0.0");

    it("has a name", function () {
        expect(dep.name).toBe("dep");
    });

    it("has a version", function () {
        expect(dep.version).toBe("v1.0.0");
    });
});
