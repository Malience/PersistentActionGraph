# Persistent Action Graph

A full-stack visual programming environment built with FastAPI (Python backend) and React/TypeScript (frontend) for creating, managing, and executing node-based workflows with real-time state tracking.

## Features

- **Visual Programming**: Drag-and-drop node-based interface for building complex workflows
- **Data Pulling Architecture**: Nodes actively request data rather than passively receiving messages
- **Type-Safe Connections**: Explicit data typing for input/output slots
- **Custom Signaling**: Advanced messaging system beyond simple data flow
- **Extensible Node System**: Easy to add custom nodes in both backend and frontend
- **Graph State Persistence**: Rather than compiling and running like a caluclator, this graph runs based on actions. As actions flow through the graph they trigger nodes. These nodes have persistent data that doesn't reset.

## Tech Stack

### Backend

- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI web server implementation

### Frontend

- **React** - UI library for building user interfaces
- **TypeScript** - Typed JavaScript for better development experience
- **Vite** - Fast build tool and development server
- **React Flow** - Library for building node-based editors

## Prerequisites

- **Python 3.8+**
- **Node.js 18+** and npm
- **Modern Browser** - Firefox recommended

## Running the Application

#### Create a new virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### Start the Servers

```bash
# Run the batch files
run_backend.bat
run_frontend.bat
```

The backend server will start on `http://localhost:8000`
The frontend server will start on `http://localhost:3000`

### LLM Server

Some nodes may utilize an LLM server. Theoretically, any LLM server should be able to work, however, this has only been tested with KoboldCPP. As a note, this architecture will munch tokens like no tomorrow. I do not recommend using an API. Check the Chatbot example for how to set up a simple generator to use an LLM.

### Connect

Connect to the frontend server at `http://localhost:3000` in your preferred browser.

## Usage

- **Adding Nodes**: Right-click on the canvas to open the context menu and select from available node types
- **Connecting Nodes**: Drag from output slots to input slots to create data flow connections
- **Node States**: Nodes change color based on their execution state (yellow = processing, green = done) (This is buggy!)
- **Data Flow**: Nodes pull data from connected upstream nodes when activated
- **Saving/Loading**: Use the panel controls in the top-right to save your workflow or load existing ones

## Controls

### Basic Navigation

- **Move around**: Click and drag the background to pan the canvas
- **Zoom**: Use mouse wheel to zoom in and out
- **Select nodes**: Click on any node to select it

### Creating and Connecting Nodes

- **Add nodes**: Right-click on empty canvas → "Create Node" → Choose node type
- **Connect nodes**: Drag from an output socket (right side) to an input socket (left side)
- **Disconnect**: Drag a connection away from a socket

### Working with Nodes

- **Move nodes**: Click and drag nodes to reposition them
- **Delete nodes**: Right-click a node → "delete"

### Selection and Multi-Node Operations

- **Multi-select**: Hold Shift + drag to select multiple nodes with selection box
- **Copy selected**: Ctrl/Cmd + C to copy selected nodes and connections
- **Paste**: Ctrl/Cmd + V to paste copied nodes

### File Operations

- **Save**: Click "Save" button to download your graph as JSON
- **Load**: Use file picker to load a saved graph
- **Clear**: "Clear" button removes all nodes and starts fresh

## Node Categories

- **Chat**: Conversation management
- **Display**: Output visualization
- **LLM**: AI/ML integration (Text generation, Tool calling)
- **Logic**: Control flow (ForLoop, Conditional, Boolean logic)
- **Primitives**: Basic data types (String, Int, Float, JSON)
- **Utility**: Data manipulation (Arrays, Dicts, JSON operations)
- **Widgets**: Interactible elements (eg. Buttons)

## Examples

Check the `EXAMPLES/` directory for sample workflows including:

- Basic chat systems
- Text generation pipelines
- Data processing flows
- Loop and conditional logic demonstrations

The Liars Dice example requires a slightly more powerful LLM, but it fully shows off the power of this architecture and why it had to be designed this way.

## Custom Nodes

Adding your own custom node is very easy! Check out the backend/custom_nodes folder for node examples. Simply adding your own py file into the backend/custom_nodes folder! (Nesting works too!)

Additional information concerning nodes:

- **Naming**: The file name (eg. _Name_.py) must match the class definition in the file (eg. class _Name_(CustomNode):) (It's the only way I could get python to dynamically load files!)
- **Route**: Each node is required to have a "route". (eg. "primitives/float") This determines where the node will end up on the context menu.
- **Slots**: The slots added to a node represent it's potential connections. Each slot can have a static datatype. This datatype is checked during connections and won't connect to other sockets of a different type! The notable exception is "any" which can connect to anything.
- **Frontend**: A frontend can be given to the node by placing a tsx file in the appropriate folder in frontend/custom_nodes. Make sure the nesting and naming are consistent! Check the folder for more examples. Note: A node does not require a frontend! Without a frontend, you will still have the sockets as normal.
- **Data Pathways**: There are a few ways that data can flow through the graph.
  - **Pulling**: Directly pulls data from the given input_socket.
  - **Activating**: Pushes data to the next node and activates the connected socket on that node. (Can be used with or without additional parameters!)
  - **Syncing**: Syncs the data between the nodes frontend and backend.
  - **Signaling**: Sends signals between the nodes frontend and backend.
