import { useCallback, type HTMLAttributes } from "react";

interface NodeContextMenuProps
  extends Omit<HTMLAttributes<HTMLDivElement>, "id" | "style" | "deletenode"> {
  id: string;
  style?: React.CSSProperties;
  deleteNode: (id: string) => void;
}

export default function NodeContextMenu(props: NodeContextMenuProps) {
  const { id, style, deleteNode, ...restProps } = props;

  const _deleteNode = useCallback(() => {
    deleteNode(id);
  }, [id, deleteNode]);

  return (
    <div style={style} className="context-menu" {...restProps}>
      <p style={{ margin: "0.5em" }}>
        <small>node: {id}</small>
      </p>
      <button onClick={_deleteNode}>delete</button>
    </div>
  );
}
