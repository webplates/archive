import Dependency from "./Dependency";

export interface Package {
    getDependencies(): Dependency[];
    addDependency(dep: Dependency): void;

    getDevDependencies(): Dependency[];
    addDevDependency(dep: Dependency): void;
}
