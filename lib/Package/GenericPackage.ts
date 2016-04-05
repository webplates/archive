import {Package} from "../Package";
import Dependency from "../Dependency";

export default class GenericPackage implements Package
{
    protected _name: string;
    protected dependencies: Dependency[] = [];
    protected devDependencies: Dependency[] = [];

    constructor(name: string) {
        this._name = name;
    }

    get name(): string {
        return this._name;
    }

    getDependencies():Dependency[] {
        return this.dependencies;
    }

    addDependency(dep:Dependency):void {
        this.dependencies.push(dep);
    }

    getDevDependencies():Dependency[] {
        return this.devDependencies;
    }

    addDevDependency(dep:Dependency):void {
        this.devDependencies.push(dep);
    }
}
