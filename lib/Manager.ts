import Package from "./Package";

export interface Manager {
    getDependencies(): Package[];
    getDevDependencies(): Package[];
}
