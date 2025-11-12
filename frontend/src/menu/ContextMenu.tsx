/* eslint-disable @typescript-eslint/no-explicit-any */
import { useCallback, useState } from "react";

type ContextMenuProps = {
  style?: React.CSSProperties;
  routes: object;
  pos: { x: number; y: number };
  contextCall: (pos: { x: number; y: number }, nodetype: string) => void;
  label?: string;
};

export default function ContextMenu(props: ContextMenuProps) {
  const { style, routes, pos, contextCall, label, ...rprops } = props;
  const [submenu, setSubmenu] = useState<ContextMenuProps | null>(null);

  const normal_style = {};
  const submenu_style = {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "0px",
  };

  const routeSelect = useCallback(
    (key: string, value: any) => {
      // Calculate position of the context menu. We want to make sure it
      // doesn't get positioned off-screen.

      if (typeof value === "object") {
        setSubmenu({
          routes: routes[key],
          pos: pos,
          contextCall: contextCall,
        });
      } else if (typeof value === "string") {
        contextCall(pos, value);
      }
    },
    [contextCall, pos, routes]
  );

  // Please avert your eyes, this is absolutely atrocious
  return (
    <div>
      {style ? (
        <div style={style} className="context-menu" {...rprops}>
          <div style={submenu ? submenu_style : normal_style}>
            <div>
              {label ? (
                <p style={{ margin: "0.5em" }}>
                  <small>{label}</small>
                </p>
              ) : (
                <div />
              )}
              {Object.entries(routes).map(([key, value]) => (
                <button
                  key={key}
                  onClick={() => {
                    routeSelect(key, value);
                  }}
                >
                  <div
                    style={{
                      display: "grid",
                      gridTemplateColumns: "1fr 1fr",
                      gap: "12px",
                      width: "100%",
                    }}
                  >
                    <div>{key}</div>
                    {typeof value === "object" && (
                      <div style={{ textAlign: "right" }}>{">"}</div>
                    )}
                  </div>
                </button>
              ))}
            </div>
            {submenu && <ContextMenu {...submenu} />}
          </div>
        </div>
      ) : (
        <div>
          <div style={submenu ? submenu_style : normal_style}>
            <div>
              {label ? (
                <p style={{ margin: "0.5em" }}>
                  <small>{label}</small>
                </p>
              ) : (
                <div />
              )}
              {Object.entries(routes).map(([key, value]) => (
                <button
                  key={key}
                  onClick={() => {
                    routeSelect(key, value);
                  }}
                >
                  <div
                    style={{
                      display: "grid",
                      gridTemplateColumns: "1fr 1fr",
                      gap: "12px",
                      width: "100%",
                    }}
                  >
                    <div>{key}</div>
                    {typeof value === "object" && (
                      <div style={{ textAlign: "right" }}>{">"}</div>
                    )}
                  </div>
                </button>
              ))}
            </div>
            {submenu && <ContextMenu {...submenu} />}
          </div>
        </div>
      )}
    </div>
  );
}
