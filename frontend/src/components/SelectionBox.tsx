/* eslint-disable @typescript-eslint/no-explicit-any */
import { useRef, type PointerEvent, useEffect, useState } from "react";
import { useReactFlow, useStore } from "@xyflow/react";

export function SelectionBox() {
  const { screenToFlowPosition, setNodes } = useReactFlow();
  const { width, height, nodeLookup } = useStore((state) => ({
    width: state.width,
    height: state.height,
    nodeLookup: state.nodeLookup,
  }));

  const canvas = useRef<HTMLCanvasElement>(null);
  const [shiftPressed, setShiftPressed] = useState(false);
  const isSelecting = useRef(false);
  const startPoint = useRef<{ x: number; y: number } | null>(null);
  const currentPoint = useRef<{ x: number; y: number } | null>(null);

  // Handle Shift key detection
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Shift") {
        setShiftPressed(true);
      }
    };

    const handleKeyUp = (event: KeyboardEvent) => {
      if (event.key === "Shift") {
        setShiftPressed(false);
        isSelecting.current = false;
        startPoint.current = null;
        currentPoint.current = null;
        clearCanvas();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    window.addEventListener("keyup", handleKeyUp);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("keyup", handleKeyUp);
    };
  }, []);

  function clearCanvas() {
    const ctx = canvas.current?.getContext("2d");
    if (ctx) {
      ctx.clearRect(0, 0, width, height);
    }
  }

  function handlePointerDown(e: PointerEvent) {
    if (!shiftPressed) return;

    (e.target as HTMLCanvasElement).setPointerCapture(e.pointerId);
    isSelecting.current = true;
    startPoint.current = { x: e.pageX, y: e.pageY };
    currentPoint.current = { x: e.pageX, y: e.pageY };

    drawSelectionBox();
  }

  function handlePointerMove(e: PointerEvent) {
    if (!isSelecting.current || !startPoint.current) return;

    currentPoint.current = { x: e.pageX, y: e.pageY };
    drawSelectionBox();
  }

  function handlePointerUp(e: PointerEvent) {
    if (!isSelecting.current || !startPoint.current || !currentPoint.current)
      return;

    (e.target as HTMLCanvasElement).releasePointerCapture(e.pointerId);

    // Select nodes within the rectangle
    selectNodesInRectangle();

    isSelecting.current = false;
    startPoint.current = null;
    currentPoint.current = null;
    clearCanvas();
  }

  function drawSelectionBox() {
    if (!startPoint.current || !currentPoint.current) return;

    const ctx = canvas.current?.getContext("2d");
    if (!ctx) return;

    clearCanvas();

    const x = Math.min(startPoint.current.x, currentPoint.current.x);
    const y = Math.min(startPoint.current.y, currentPoint.current.y);
    const width = Math.abs(currentPoint.current.x - startPoint.current.x);
    const height = Math.abs(currentPoint.current.y - startPoint.current.y);

    ctx.fillStyle = "rgba(0, 123, 255, 0.1)";
    ctx.strokeStyle = "rgba(0, 123, 255, 0.8)";
    ctx.lineWidth = 2;

    ctx.fillRect(x, y, width, height);
    ctx.strokeRect(x, y, width, height);
  }

  function selectNodesInRectangle() {
    if (!startPoint.current || !currentPoint.current) return;

    const startFlowPos = screenToFlowPosition(startPoint.current);
    const endFlowPos = screenToFlowPosition(currentPoint.current);

    const selectionRect = {
      x: Math.min(startFlowPos.x, endFlowPos.x),
      y: Math.min(startFlowPos.y, endFlowPos.y),
      width: Math.abs(endFlowPos.x - startFlowPos.x),
      height: Math.abs(endFlowPos.y - startFlowPos.y),
    };

    const nodesToSelect = new Set<string>();

    nodeLookup.forEach((node) => {
      const nodeRect = {
        x: node.internals.positionAbsolute.x,
        y: node.internals.positionAbsolute.y,
        width: node.measured.width || 0,
        height: node.measured.height || 0,
      };

      if (isNodeInSelection(nodeRect, selectionRect)) {
        nodesToSelect.add(node.id);
      }
    });

    setNodes((nodes) =>
      nodes.map((node) => ({
        ...node,
        selected: nodesToSelect.has(node.id),
      }))
    );
  }

  function isNodeInSelection(nodeRect: any, selectionRect: any) {
    return (
      nodeRect.x < selectionRect.x + selectionRect.width &&
      nodeRect.x + nodeRect.width > selectionRect.x &&
      nodeRect.y < selectionRect.y + selectionRect.height &&
      nodeRect.y + nodeRect.height > selectionRect.y
    );
  }

  return (
    <canvas
      ref={canvas}
      width={width}
      height={height}
      className={`selection-overlay ${shiftPressed ? "selection-active" : ""}`}
      onPointerDown={handlePointerDown}
      onPointerMove={handlePointerMove}
      onPointerUp={handlePointerUp}
    />
  );
}
