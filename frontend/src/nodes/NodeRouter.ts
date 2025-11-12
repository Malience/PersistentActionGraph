/* eslint-disable @typescript-eslint/no-explicit-any */
export default class NodeRouter {
  node_routes: any = {};

  registerNode(nodetype: string, route: string) {
    const splits = route.split("/");

    const last = splits.length - 1;
    let root = this.node_routes;
    let full_route = "";
    for (let i = 0; i < last; i++) {
      const cur = splits[i];
      full_route += cur;

      if (!(cur in root)) {
        root[cur] = {};
        root = root[cur];
        continue;
      }

      if (!(root[cur] instanceof Object)) {
        console.log(
          `ERROR: Route collision. Nodetype '${nodetype}' tries to replace route '${full_route}'`
        );
        return;
      }

      root = root[cur];
    }

    const name = splits[last];
    if (!(name in root)) {
      root[name] = nodetype;
    } else {
      console.log(
        `ERROR: Route collision. Node '${nodetype}' tries to replace route '${full_route}'`
      );
    }
  }

  clear() {
    this.node_routes.clear();
  }
}
