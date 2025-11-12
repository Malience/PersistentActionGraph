/* eslint-disable @typescript-eslint/no-explicit-any */
import {
  addEdge,
  applyEdgeChanges,
  applyNodeChanges,
  Background,
  BackgroundVariant,
  MiniMap,
  Panel,
  ReactFlow,
  reconnectEdge,
  type ReactFlowInstance,
} from "@xyflow/react";
import { lazy, useCallback, useEffect, useRef, useState } from "react";
import "@xyflow/react/dist/style.css";
import NodeContainer from "./nodes/NodeContainer";
import type CustomNode from "./nodes/CustomNode";
import NodeContextMenu from "./menu/NodeContextMenu";
import NodeRouter from "./nodes/NodeRouter";
import ContextMenu from "./menu/ContextMenu";
import { NodeSocketProvider } from "./sockets/NodeSocketProvider";
import { useStoreApi } from "@xyflow/react";
import { SelectionBox } from "./components/SelectionBox";

/**
 * LOAD CUSTOM NODES
 */
const CUSTOM_NODES_DIR = "../../custom_nodes/";
const frontend_nodes: { [node: string]: CustomNode } = {};
const node_router = new NodeRouter();

async function load_custom_nodes() {
  const response = await fetch("http://localhost:8000/custom_nodes", {
    method: "GET",
  });
  const response_json = await response.json();
  const frnt_nodes = response_json["frontend_nodes"];
  const routes = response_json["routes"];

  async function import_frontend_nodes() {
    for (const node in frnt_nodes) {
      const import_path = CUSTOM_NODES_DIR + frnt_nodes[node];
      frontend_nodes[node] = lazy(() => import(import_path));
    }
  }
  await import_frontend_nodes();

  for (const nodetype in routes) {
    const route = routes[nodetype];
    node_router.registerNode(nodetype, route);
  }
}
await load_custom_nodes();

function check_frontend_node(node: string) {
  return node in frontend_nodes;
}

function get_frontend_node(node: string) {
  return frontend_nodes[node];
}

console.log(frontend_nodes);

console.log("Custom Nodes finished Loading!");

/**
 * INITIALIZATION
 */
const initialEdges: { id: string; source: string; target: string }[] = []; //[{ id: "n1-n2", source: "n1", target: "n2" }];

const nodeTypes = {
  customNode: NodeContainer,
};

// APP
export default function App() {
  const ref = useRef<any>(null);
  const [rfInstance, setRfInstance] = useState<ReactFlowInstance | null>(null);
  const edgeReconnectSuccessful = useRef(true);
  const isLoadingRef = useRef(false);
  const [nodes, setNodes] = useState<any>([]);
  const [edges, setEdges] = useState(initialEdges);
  const [nodeMenu, setNodeMenu] = useState<any>(null);
  const [paneMenu, setPaneMenu] = useState<any>(null);

  const store = useStoreApi();
  const { addSelectedNodes, resetSelectedElements } = store.getState();

  const getEdgeID = (
    source: string,
    sourceHandle: string,
    target: string,
    targetHandle: string
  ) => {
    return `edge_${source}-${sourceHandle}_${target}-${targetHandle}`;
  };

  const createEdge = useCallback(
    async (
      edgeid: string,
      src_id: string,
      src_slot: string,
      dst_id: string,
      dst_slot: string
    ) => {
      const response = await fetch("http://localhost:8000/add_edge", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          edgeid: edgeid,
          src_id: src_id,
          src_slot: src_slot,
          dst_id: dst_id,
          dst_slot: dst_slot,
        }),
      });

      if (!response.ok) {
        console.log("ERROR: Could not reach the server: ", response.statusText);
        return false;
      }

      return true;
    },
    []
  );

  const removeEdge = useCallback(async (edgeid: string) => {
    const response = await fetch(
      "http://localhost:8000/remove_edge/" + edgeid,
      {
        method: "DELETE",
      }
    );

    if (!response.ok) {
      console.log("ERROR: Could not reach the server: ", response.statusText);
      return false;
    }

    return true;
  }, []);

  const onConnect = useCallback((params: any) => {
    const newParams = { ...params, reconnectable: "target" };

    const edge_id = getEdgeID(
      params.source,
      params.sourceHandle,
      params.target,
      params.targetHandle
    );

    if (
      !createEdge(
        edge_id,
        params.source,
        params.sourceHandle,
        params.target,
        params.targetHandle
      )
    )
      return;

    setEdges((edgesSnapshot) => addEdge(newParams, edgesSnapshot));
  }, []);

  const addEdge2 = useCallback(
    (
      id: string,
      source: string,
      sourceHandle: string,
      target: string,
      targetHandle: string
    ) => {
      const newParams = {
        id: id,
        source: source,
        sourceHandle: sourceHandle,
        target: target,
        targetHandle: targetHandle,
        reconnectable: "target",
      };

      setEdges((edgesSnapshot) => addEdge(newParams, edgesSnapshot));
    },
    []
  );

  const onReconnectStart = useCallback(() => {
    edgeReconnectSuccessful.current = false;
  }, []);

  const onReconnect = useCallback((oldEdge: any, newConnection: any) => {
    edgeReconnectSuccessful.current = true;

    const old_edge_id = getEdgeID(
      oldEdge.source,
      oldEdge.sourceHandle,
      oldEdge.target,
      oldEdge.targetHandle
    );

    const edge_id = getEdgeID(
      newConnection.source,
      newConnection.sourceHandle,
      newConnection.target,
      newConnection.targetHandle
    );

    // Possible bug where remove succeeds but create fails
    if (!removeEdge(old_edge_id)) return;

    if (
      !createEdge(
        edge_id,
        newConnection.source,
        newConnection.sourceHandle,
        newConnection.target,
        newConnection.targetHandle
      )
    )
      return;

    setEdges((els) => reconnectEdge(oldEdge, newConnection, els));
  }, []);

  const onReconnectEnd = useCallback((_: any, edge: any) => {
    if (!edgeReconnectSuccessful.current) {
      const edge_id = getEdgeID(
        edge.source,
        edge.sourceHandle,
        edge.target,
        edge.targetHandle
      );
      if (!removeEdge(edge_id)) return;

      setEdges((eds) => eds.filter((e) => e.id !== edge.id));
    }

    edgeReconnectSuccessful.current = true;
  }, []);

  const onSave = useCallback(async () => {
    const response = await fetch("http://localhost:8000/", {
      method: "GET",
    });

    if (!response.ok) {
      console.log("ERROR: Could not reach the server: ", response.statusText);
      return;
    }

    const data = await response.json();
    console.log(data);
    const jsonString = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonString], { type: "application/json" });
    const url = URL.createObjectURL(blob);

    // Create a temporary anchor element to trigger the download
    const a = document.createElement("a");
    a.href = url;
    a.download = "graph_state.json";
    a.click();

    // Clean up
    URL.revokeObjectURL(url);
  }, []);

  const onClear = useCallback(async () => {
    const response = await fetch("http://localhost:8000/clear_graph", {
      method: "POST",
    });

    if (!response.ok) {
      console.log("ERROR: Could not reach the server: ", response.statusText);
      return;
    }

    // Clear the frontend state
    setNodes([]);
    setEdges([]);

    console.log("Scene cleared successfully");
  }, []);

  const onLoad = useCallback(
    async (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = async (e) => {
          const jsonString = e.target?.result;
          if (typeof jsonString === "string") {
            try {
              // Send the loaded graph to the server
              const response = await fetch("http://localhost:8000/load_graph", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: jsonString,
              });

              if (!response.ok) {
                console.log(
                  "ERROR: Could not reach the server: ",
                  response.statusText
                );
                return;
              }
              // Pull data back from server and reload page
              loadPage();
            } catch (error) {
              console.error("Failed to parse JSON:", error);
            }
          }
        };
        reader.readAsText(file);
      }
    },
    []
  );

  const onNodeMove = useCallback(
    async (nodeid: string, x: number, y: number) => {
      const response = await fetch(
        "http://localhost:8000/move_node/" + nodeid,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ x: x, y: y }),
        }
      );

      if (!response.ok) {
        console.log("ERROR: Server failed to move: ", response.statusText);
        return;
      }
    },
    []
  );

  const onNodeResize = useCallback(
    async (nodeid: string, width: number, height: number) => {
      const response = await fetch(
        "http://localhost:8000/resize_node/" + nodeid,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ width: width, height: height }),
        }
      );

      if (!response.ok) {
        console.log("ERROR: Server failed to resize: ", response.statusText);
        return;
      }
    },
    []
  );

  const onNodesChange = useCallback((changes: any) => {
    for (const change of changes) {
      if (change.type == "position") {
        if (!change.dragging) {
          const nodeid = change.id;
          const pos = change.position;
          onNodeMove(nodeid, pos.x, pos.y);
        }
      }

      if (change.type == "dimensions") {
        if (!change.resizing) {
          const nodeid = change.id;
          const dim = change.dimensions;
          onNodeResize(nodeid, dim.width, dim.height);
        }
      }
    }

    setNodes((nodesSnapshot: any) => applyNodeChanges(changes, nodesSnapshot));
  }, []);

  const onEdgesChange = useCallback((changes: any) => {
    setEdges((edgesSnapshot) => applyEdgeChanges(changes, edgesSnapshot));
  }, []);

  const addNode = (data: {
    nodeid: string;
    pos?: { x: number; y: number };
    nodetype: string;
    input_slots: any;
    output_slots: any;
    label: string;
    data: any;
    size?: { width: number; height: number };
  }) => {
    let position = { x: 0, y: 0 };
    if (data.pos) position = data.pos;

    const node = {
      id: data.nodeid,
      type: "customNode",
      position: position,
      data: {
        nodetype: data.nodetype,
        input_slots: data.input_slots,
        output_slots: data.output_slots,

        label: data.label,
        data: data.data,
        functions: {
          check_frontend_node: check_frontend_node,
          get_frontend_node: get_frontend_node,
        },
      },
    };

    if (data.size) {
      node["width"] = data.size.width;
      node["height"] = data.size.height;
    }

    setNodes((prevNodes: any) => {
      // Check if node with this ID already exists
      const existingNode = prevNodes.find(
        (node: any) => node.id === data.nodeid
      );
      if (existingNode) {
        console.warn(
          `Node with ID ${data.nodeid} already exists, skipping duplicate`
        );
        return prevNodes;
      }
      return [...prevNodes, node];
    });
  };

  const createNode = useCallback(
    async (nodetype: string, x: number, y: number) => {
      const response = await fetch(
        "http://localhost:8000/add_node/" + nodetype,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ x: x, y: y }),
        }
      );

      if (!response.ok) {
        console.log("ERROR: Failed to add node: ", response.statusText);
        return;
      }

      const nodedata = await response.json();

      addNode({
        nodeid: nodedata.id,
        pos: { x: x, y: y },
        nodetype: nodedata.nodetype,
        input_slots: nodedata.input_slots,
        output_slots: nodedata.output_slots,
        label: nodedata.label,
        data: nodedata.data,
      });
    },
    []
  );

  const addSubgraph = useCallback(
    async (new_nodes: any, new_edges: any) => {
      for (const node of new_nodes) {
        addNode({
          nodeid: node.id,
          pos: node.pos,
          nodetype: node.nodetype,
          input_slots: node.input_slots,
          output_slots: node.output_slots,
          label: node.label,
          data: node.data,
          size: node.size,
        });
      }

      for (const edge of new_edges) {
        addEdge2(
          edge.edgeid,
          edge.src_id,
          edge.src_slot,
          edge.dst_id,
          edge.dst_slot
        );
      }
    },
    [addEdge2]
  );

  const loadPage = useCallback(async () => {
    if (isLoadingRef.current) return;
    isLoadingRef.current = true;

    try {
      setEdges([]);
      setNodes([]);

      const response = await fetch("http://localhost:8000/", {
        method: "get",
      });

      const data = await response.json();

      console.log(data);
      addSubgraph(data.nodes, data.edges);
    } finally {
      isLoadingRef.current = false;
    }
  }, [addSubgraph]);

  useEffect(() => {
    console.log("LOADED");

    loadPage();
  }, [loadPage]);

  // const removeNode = (id: string) => {
  //   setNodes((nodes: any) => nodes.filter((node: any) => node.id !== id));
  //   setEdges((edges: any) => edges.filter((edge: any) => edge.source !== id));
  // };

  const removeNode = useCallback((id: string) => {
    setNodes((nodes: any) => nodes.filter((node: any) => node.id !== id));
    setEdges((edges: any) => edges.filter((edge: any) => edge.source !== id));
  }, []);

  const deleteNode = useCallback(
    async (id: string) => {
      const response = await fetch("http://localhost:8000/remove_node/" + id, {
        method: "DELETE",
      });

      if (!response.ok) {
        console.log(
          "ERROR: Failed to delete node. Server did not respond: ",
          response.statusText
        );
        return;
      }

      const resp = await response.json();
      if (!resp.result) {
        console.log(
          "ERROR: Failed to delete node. Server refused: ",
          response.statusText
        );
        return;
      }

      removeNode(id);
    },
    [removeNode]
  );

  const getStyle = (event: {
    preventDefault: () => void;
    clientY: number;
    clientX: number;
  }) => {
    const pane = ref.current.getBoundingClientRect();

    const style: any = {};
    const top = event.clientY < pane.height - 200 && event.clientY;
    const left = event.clientX < pane.width - 200 && event.clientX;
    const right =
      event.clientX >= pane.width - 200 && pane.width - event.clientX;
    const bottom =
      event.clientY >= pane.height - 200 && pane.height - event.clientY;
    if (top) style["top"] = top;
    if (left) style["left"] = left;
    if (right !== false) style["right"] = right;
    if (bottom) style["bottom"] = bottom;

    return style;
  };

  const onNodeContextMenu = useCallback(
    (
      event: { preventDefault: () => void; clientY: number; clientX: number },
      node: { id: any }
    ) => {
      if (!ref.current) return;
      // Prevent native context menu from showing
      event.preventDefault();

      // Calculate position of the context menu. We want to make sure it
      // doesn't get positioned off-screen.
      const style = getStyle(event);
      setNodeMenu({
        id: node.id,
        style: style,
        deleteNode: deleteNode,
      });
    },
    [setNodeMenu, deleteNode]
  );

  const onPaneContextMenu = useCallback(
    (event: any) => {
      if (!ref.current || !rfInstance) return;
      // Prevent native context menu from showing
      event.preventDefault();

      // Calculate position of the context menu. We want to make sure it
      // doesn't get positioned off-screen.
      const style = getStyle(event);
      const pos = rfInstance.screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });
      setPaneMenu({
        style: style,
        routes: node_router.node_routes,
        pos: pos,
        contextCall: contextCall,
        label: "Create Node",
      });
    },
    [setPaneMenu, createNode, rfInstance]
  );

  const contextCall = useCallback(
    (pos: { x: number; y: number }, nodetype: string) => {
      setPaneMenu(null);
      createNode(nodetype, pos.x, pos.y);
    },
    []
  );

  // Close all context menus if it's open whenever the window is clicked.
  const onPaneClick = useCallback(() => {
    setNodeMenu(null);
    setPaneMenu(null);
  }, [setNodeMenu]);

  useEffect(() => {
    let isMounted = true;
    let ws: WebSocket | null = null;

    const connectWebSocket = () => {
      if (!isMounted) return;

      try {
        ws = new WebSocket("ws://localhost:8000/current_node");

        ws.onopen = () => {
          if (isMounted) {
            console.log("WebSocket connection opened");
          }
        };

        ws.onmessage = (event) => {
          if (isMounted) {
            // setMessages((prevMessages) => [...prevMessages, event.data]);
            console.log(event.data);
          }
        };

        ws.onclose = () => {
          if (isMounted) {
            console.log("WebSocket connection closed");
          }
        };

        ws.onerror = (error) => {
          if (isMounted) {
            console.error("WebSocket error:", error);
          }
        };
      } catch (error) {
        if (isMounted) {
          console.error("Failed to create WebSocket:", error);
        }
      }
    };

    connectWebSocket();

    return () => {
      isMounted = false;
      if (ws) {
        ws.close();
      }
    };
  }, []);

  // Copy-paste functionality
  const copySelectedNodes = useCallback(async () => {
    const selectedNodes = nodes.filter((node: any) => node.selected);
    if (selectedNodes.length === 0) {
      console.log("No nodes selected to copy");
      return;
    }

    const nodeIds = selectedNodes.map((node: any) => node.id);

    try {
      const response = await fetch("http://localhost:8000/get_subgraph", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ node_ids: nodeIds }),
      });

      if (!response.ok) {
        console.log("ERROR: Failed to get subgraph: ", response.statusText);
        return;
      }

      const subgraph = await response.json();
      const subgraphJson = JSON.stringify(subgraph, null, 2);

      // Copy to clipboard
      await navigator.clipboard.writeText(subgraphJson);
      console.log("Copied subgraph to clipboard:", subgraph);
    } catch (error) {
      console.error("Failed to copy subgraph:", error);
    }
  }, [nodes]);

  const pasteSubgraph = useCallback(async () => {
    try {
      const clipboardText = await navigator.clipboard.readText();

      // Check if clipboard contains valid JSON
      let subgraph;
      try {
        subgraph = JSON.parse(clipboardText);
      } catch {
        console.log("Clipboard does not contain valid JSON");
        return;
      }

      // Validate subgraph structure
      if (!subgraph.nodes || !subgraph.edges) {
        console.log("Clipboard JSON does not contain valid subgraph structure");
        return;
      }

      // Get cursor position (Didn't work, everything is terrible)
      const position = { x: 50, y: 50 };

      // Prepare data for backend
      const requestData = {
        subgraph: subgraph,
        position_offset: position || { x: 0, y: 0 },
      };

      // Send subgraph to backend
      const response = await fetch("http://localhost:8000/add_subgraph", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        console.log("ERROR: Failed to add subgraph: ", response.statusText);
        return;
      }

      const result = await response.json();
      console.log("Pasted subgraph:", result);

      console.log(result.new_nodes);
      console.log(result.new_node_ids);
      // Reload the page to show the new nodes
      addSubgraph(result.new_nodes, result.new_edges);

      // This doesn't seem to work properly, but it's the best I've got!
      // resetSelectedElements();
      // addSelectedNodes(result.new_node_ids);

      const selected_ids = new Set(result.new_node_ids);

      setNodes((nodes) =>
        nodes.map((node) => ({
          ...node,
          selected: selected_ids.has(node.id),
        }))
      );
    } catch (error) {
      console.error("Failed to paste subgraph:", error);
    }
  }, [addSubgraph, resetSelectedElements, addSelectedNodes, rfInstance]);

  // Keyboard event handler
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Don't handle copy/paste if an input/textarea/select is focused
      const activeElement = document.activeElement;
      if (
        activeElement &&
        (activeElement.tagName === "INPUT" ||
          activeElement.tagName === "TEXTAREA" ||
          activeElement.tagName === "SELECT")
      ) {
        return;
      }

      // Ctrl+C or Cmd+C
      if ((event.ctrlKey || event.metaKey) && event.key === "c") {
        event.preventDefault();
        copySelectedNodes();
      }

      // Ctrl+V or Cmd+V
      if ((event.ctrlKey || event.metaKey) && event.key === "v") {
        event.preventDefault();
        pasteSubgraph();
      }
    };

    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [copySelectedNodes, pasteSubgraph]);

  // I don't think this is going to work
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [signal, setSignal] = useState<WebSocket | null>(null);
  // useEffect(() => {
  //   const ws = new WebSocket("ws://localhost:8000/current_node");

  //   ws.onopen = () => {
  //     console.log("WebSocket connection opened");
  //     setSignal(ws);
  //   };

  //   ws.onmessage = (event) => {
  //     // setMessages((prevMessages) => [...prevMessages, event.data]);
  //     console.log(event.data);
  //   };

  //   ws.onclose = () => {
  //     console.log("WebSocket connection closed");
  //   };

  //   ws.onerror = (error) => {
  //     console.error("WebSocket error:", error);
  //   };

  //   return () => {
  //     ws.close(); // Clean up the WebSocket connection on component unmount
  //     setSignal(null);
  //   };
  // }, []);

  return (
    <NodeSocketProvider socketUrl="ws://localhost:8000/node_socket">
      {/* <ConnectionContext value={connectionContext}> */}
      <ReactFlow
        ref={ref}
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onReconnectStart={onReconnectStart}
        onReconnect={onReconnect}
        onReconnectEnd={onReconnectEnd}
        onInit={(instance) => setRfInstance(instance as any)}
        onPaneClick={onPaneClick}
        onNodeContextMenu={onNodeContextMenu}
        onPaneContextMenu={onPaneContextMenu}
        nodeTypes={nodeTypes}
        minZoom={0.1}
        fitView
      >
        <Background
          color="#1A1A1A"
          bgColor="#222222"
          variant={BackgroundVariant.Lines}
        />
        <Panel position="top-right">
          <button onClick={onSave}>Save</button>
          <input type="file" accept=".json" onChange={onLoad} />
          <button onClick={onClear}>Clear</button>
        </Panel>
        {nodeMenu && <NodeContextMenu onClick={onPaneClick} {...nodeMenu} />}
        {paneMenu && <ContextMenu {...paneMenu} />}
        <SelectionBox />
        <MiniMap />
      </ReactFlow>
      {/* </ConnectionContext> */}
    </NodeSocketProvider>
  );
}
