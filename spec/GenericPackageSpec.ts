/// <reference path="../typings/main.d.ts" />

import GenericPackage from "../src/Package/GenericPackage";
import Dependency from "../src/Dependency";

describe("A dependency", function () {
    var pkg = new GenericPackage("my_package");

    it("has a name", function () {
        expect(pkg.name).toBe("my_package");
    });

    it("accepts a dependency", function () {
        var dep = new Dependency("dep", "v1.0.0");

        pkg.addDependency(dep);

        expect(pkg.getDependencies()).toContain(dep);
    });

    it("accepts a dev dependency", function () {
        var dep = new Dependency("dev_dep", "v1.0.0");

        pkg.addDevDependency(dep);

        expect(pkg.getDevDependencies()).toContain(dep);
    });
});
